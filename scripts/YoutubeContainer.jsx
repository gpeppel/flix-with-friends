import * as React from 'react';

import { Socket } from './Socket';

import YoutubePlayer from './youtube/youtube-player.js';


const EVENT_YT_STATE_CHANGE = 'yt-state-change';


export function YoutubeContainer() {
	const [ytPlayer, setYtPlayer] = React.useState(new YoutubePlayer(
		'', {}, onYtReady, onYtStateChange
	));
	const [lastPlayerStates, setLastPlayerStates] = React.useState([null, null, null]);
	const ytPlayerRef = React.useRef();
	const lastPlayerStatesRef = React.useRef();

	ytPlayerRef.current = ytPlayer;
	lastPlayerStatesRef.current = lastPlayerStates;

	React.useEffect(() => {
		setYtPlayer(new YoutubePlayer('dQw4w9WgXcQ', {
			playerVars: {
				autoplay: 1,
				controls: 1,
				disablekb: 1
			}
		}, onYtReady, onYtStateChange));
		
		Socket.on('yt-load', (data) => {
			ytPlayerRef.current.player.loadVideoByUrl(data.url);	
		});
		
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
					case YoutubePlayer.prototype.PLAYER_PLAYING_STR:
						ytPlayerRef.current.player.play(adjustedOffset);
						break;
					case YoutubePlayer.prototype.PLAYER_PAUSED_STR:
						ytPlayerRef.current.player.pause(adjustedOffset);
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
		console.log('ready', event);

		ytPlayerRef.current.player.pauseVideo();

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
			'offset': ytPlayerRef.current.player.getCurrentTime(),
			'timestamp': (new Date()).getTime()
		});
	}

	function isStateContinuation(state)
	{
		return lastPlayerStatesRef.current[0] == state && lastPlayerStatesRef.current[2] == state && lastPlayerStatesRef.current[1] == YoutubePlayer.prototype.PLAYER_BUFFERING;
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

	return (
		<div>
			{ytPlayer.reactComponent}
		</div>
	);
}
