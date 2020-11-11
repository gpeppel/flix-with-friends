import * as React from 'react';

import { Socket } from './Socket';

import YoutubePlayer from './youtube/youtube-player.js';


const EVENT_YT_STATE_CHANGE = 'yt-state-change';


export function YoutubeContainer() {
	const [ytPlayer, setYtPlayer] = React.useState(null);
	const [ytComponent, setYtComponent] = React.useState(null);
	const [lastPlayerStates, setLastPlayerStates] = React.useState([null, null, null]);

	const ytPlayerRef = React.useRef();
	const lastPlayerStatesRef = React.useRef();

	ytPlayerRef.current = ytPlayer;
	lastPlayerStatesRef.current = lastPlayerStates;

	React.useEffect(() => {
		let [player, component] = YoutubePlayer.createYoutubePlayer('dQw4w9WgXcQ', {
			playerVars: {
				autoplay: 1,
				controls: 1,
				disablekb: 1
			}
		}, onYtReady, onYtStateChange, onYtPlaybackRateChange);

		setYtPlayer(player);
		setYtComponent(component);

		ytPlayerRef.current = ytPlayer;

		Socket.on('yt-load', (data) => {
			ytPlayerRef.current.player.loadVideoById(data.videoId);
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
					case YoutubePlayer.prototype.PLAYER_PLAYBACK_STR:
						ytPlayerRef.current.player.setPlayback(adjustedOffset, data.rate);
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
			'state': YoutubePlayer.playerStateToStr(event.data),
			'offset': ytPlayerRef.current.player.getCurrentTime(),
			'rate': ytPlayerRef.current.player.getPlaybackRate(),
			'timestamp': (new Date()).getTime()
		});
	}

	function onYtPlaybackRateChange(event)
	{
		console.log('playback change', event);

		Socket.emit(EVENT_YT_STATE_CHANGE, {
			'state': 'playback',
			'offset': ytPlayerRef.current.player.getCurrentTime(),
			'rate': ytPlayerRef.current.player.getPlaybackRate(),
			'timestamp': (new Date()).getTime()
		});
	}

	return (
		<div>
			{ytComponent}
		</div>
	);
}
