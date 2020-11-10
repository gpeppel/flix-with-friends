import * as React from 'react';

import { Socket } from './Socket';

import YouTube from 'react-youtube';


const EVENT_YT_STATE_CHANGE = 'yt-state-change';

const PLAYER_UNSTARTED = -1;
const PLAYER_ENDED = 0;
const PLAYER_PLAYING = 1;
const PLAYER_PAUSED = 2;
const PLAYER_BUFFERING = 3;
const PLAYER_CUED = 5;

const PLAYER_UNSTARTED_STR = 'unstarted';
const PLAYER_ENDED_STR = 'ended';
const PLAYER_PLAYING_STR = 'playing';
const PLAYER_PAUSED_STR = 'paused';
const PLAYER_BUFFERING_STR = 'buffering';
const PLAYER_CUED_STR = 'cued';


export function YoutubeContainer() {
	const [ytPlayer, setYtPlayer] = React.useState(null);
	const [lastPlayerStates, setLastPlayerStates] = React.useState([null, null, null]);
	const ytPlayerRef = React.useRef();
	const lastPlayerStatesRef = React.useRef();

	ytPlayerRef.current = ytPlayer;
	lastPlayerStatesRef.current = lastPlayerStates;

	React.useEffect(() => {
		Socket.on(EVENT_YT_STATE_CHANGE, (data) => {
			function doState(data)
			{
				console.log(data);

				let ts = (new Date()).getTime();
				let tsdiff = Math.max(0, ts - data.timestamp);
				//let adjustedOffset = Math.max(0, data.offset + (tsdiff / 1000));
				let adjustedOffset = data.offset;

				//console.log(data.offset, adjustedOffset, ts, tsdiff);

				switch(data.state)
				{
					case PLAYER_PLAYING_STR:
						ytPlayerRef.current.play(adjustedOffset);
						break;
					case PLAYER_PAUSED_STR:
						ytPlayerRef.current.pause(adjustedOffset);
						break;
				}
			}

			doState(data);

			/*
			let secdiff = Math.max(0, data.runAt - Math.floor((new Date()).getTime() / 1000));
			if(secdiff > 0)
			{
				setTimeout(() => {
					doState(data);
				}, secdiff * 1000);
			}else
			{
				doState(data);
			}
			*/
		});
	}, []);

	function onYtReady(event)
	{
		setYtPlayer(event.target);

		console.log('ready', event);

		if(!ytPlayerRef.current.initialized)
		{
			ytPlayerRef.current.initialized = true;

			ytPlayerRef.current.play = function(t){
				console.log("play", t, lastPlayerStatesRef.current);

				if(this.getPlayerState() == PLAYER_PLAYING)
				{
					console.log("play cancel");
					return;
				}

				console.log("play0");
				this.seekTo(t);
				this.playVideo();
				console.log("play1");
			}.bind(ytPlayerRef.current);

			ytPlayerRef.current.pause = function(t){
				console.log("pause", t, lastPlayerStatesRef.current);

				if(this.getPlayerState() == PLAYER_PAUSED)
				{
					console.log("pause cancel");
					return;
				}

				console.log("pause0");
				this.seekTo(t);
				this.pauseVideo();
				console.log("pause1");
			}.bind(ytPlayerRef.current);
		}

		ytPlayerRef.current.pauseVideo();

		Socket.emit(EVENT_YT_STATE_CHANGE, {
			'state': 'ready',
			'offset': 0
		});
	}

	function onYtStateChange(event)
	{
		console.log('state change', event);

		setLastPlayerStates([lastPlayerStatesRef.current[1], lastPlayerStatesRef.current[2], event.data]);

		Socket.emit(EVENT_YT_STATE_CHANGE, {
			'state': playerStateToStr(event.data),
			'offset': ytPlayerRef.current.getCurrentTime(),
			'timestamp': (new Date()).getTime()
		});
	}

	function isStateContinuation(state)
	{
		return lastPlayerStatesRef.current[0] == state && lastPlayerStatesRef.current[2] == state && lastPlayerStatesRef.current[1] == PLAYER_BUFFERING;
	}

	function playerStateToStr(state)
	{
		return [
			'unstarted', // -1
			'ended',     // 0
			'playing',   // 1
			'paused',    // 2
			'buffering', // 3
			'',
			'cued'       // 5
		][state + 1];
	}

	const videoId = 'dQw4w9WgXcQ';
	const opts = {
		playerVars: {
			autoplay: 1,
			controls: 1,
			disablekb: 1
		}
	};

	return (
		<div>
			<YouTube
				videoId={videoId}
				opts={opts}
				onReady={onYtReady}
				onStateChange={onYtStateChange}
			/>
		</div>
	);
}
