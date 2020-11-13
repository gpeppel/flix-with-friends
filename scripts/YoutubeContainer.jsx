import * as React from 'react';

import { Socket } from './Socket';

import YoutubePlayer from './youtube/youtube-player.js';


const EVENT_YT_LOAD = 'yt_load';
const EVENT_YT_STATE_CHANGE = 'yt_state_change';


export function YoutubeContainer() {
	const [ytPlayer, setYtPlayer] = React.useState(null);
	const [ytComponent, setYtComponent] = React.useState(null);

	const ytPlayerRef = React.useRef();
	ytPlayerRef.current = ytPlayer;

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
	}, []);

	function onYtReady(event)
	{
		console.log('ready', event);

		ytPlayerRef.current.player.pauseVideo();

		Socket.on(EVENT_YT_LOAD, (data) => {
			console.log('load video', data);
			ytPlayerRef.current.player.loadVideoById(data.videoId);
		});

		Socket.on(EVENT_YT_STATE_CHANGE, (data) => {
			function doState(data)
			{
				data.timestamp = parseInt(data.timestamp, 10);

				let ts = (new Date()).getTime();
				let tsdiff = Math.max(0, ts - data.timestamp);
				let adjustedOffset = data.offset + (tsdiff / 1000);

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
					case 'sync':
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

		function timeoutLoop(interval) {
			setTimeout(() => {
				switch(ytPlayerRef.current.player.getPlayerState())
				{
					case YoutubePlayer.prototype.PLAYER_PLAYING:
						emitStateChange(ytPlayerRef.current.player, YoutubePlayer.prototype.PLAYER_PLAYING_STR);
						break;
					case YoutubePlayer.prototype.PLAYER_PAUSED:
						emitStateChange(ytPlayerRef.current.player, YoutubePlayer.prototype.PLAYER_PAUSED_STR);
						break;
				}

				timeoutLoop(interval);
			}, interval - ((new Date()).getTime() % interval));
		};

		timeoutLoop(5000);

		emitStateChange(ytPlayerRef.current.player, YoutubePlayer.prototype.PLAYER_READY_STR, 0, 1);
	}

	function onYtStateChange(event)
	{
		emitStateChange(ytPlayerRef.current.player, YoutubePlayer.playerStateToStr(event.data));
	}

	function onYtPlaybackRateChange(event)
	{
		console.log('playback change', event);

		emitStateChange(ytPlayerRef.current.player, YoutubePlayer.prototype.PLAYER_PLAYBACK_STR);
	}

	function emitStateChange(player, state, offset, rate, timestamp)
	{
		offset = offset || player.getCurrentTime();
		rate = rate || player.getPlaybackRate();
		timestamp = timestamp || (new Date()).getTime();

		Socket.emit(EVENT_YT_STATE_CHANGE, {
			'state': state,
			'offset': Math.round(offset * 10000) / 10000,
			'rate': rate,
			'timestamp': timestamp.toString()
		});
	}

	return (
		<div>
			{ytComponent}
		</div>
	);
}
