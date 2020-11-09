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

export function YoutubeContainer() {
	const [ytPlayer, setYtPlayer] = React.useState(null);
	const [playerState, setPlayerState] = React.useState([null, null]);
	const ytPlayerRef = React.useRef();

	ytPlayerRef.current = ytPlayer;

	React.useEffect(() => {
		Socket.on(EVENT_YT_STATE_CHANGE, (data) => {
			switch(data.state)
			{
				case 'play':
					ytPlayerRef.current.seekTo(data.offset);
					ytPlayerRef.current.playVideo();
					break;
				case 'pause':
					ytPlayerRef.current.seekTo(data.offset);
					ytPlayerRef.current.pauseVideo();
					break;
				case 'seek':
					ytPlayerRef.current.seekTo(data.offset);
					break;
			}
		});
	}, []);

	function onYtReady(event)
	{
		console.log('ready', event);
		setYtPlayer(event.target);

		Socket.emit(EVENT_YT_STATE_CHANGE, {
			'state': 'ready',
			'offset': 0
		});
	}

	function onYtPlay(event)
	{
		console.log('play', event, playerState);

		if(playerState[0] != PLAYER_BUFFERING)
		{
			Socket.emit(EVENT_YT_STATE_CHANGE, {
				'state': 'play',
				'offset': ytPlayerRef.current.getCurrentTime()
			});
		}
	}

	function onYtPause(event)
	{
		console.log('pause', event, playerState);

		if(playerState[0] != PLAYER_BUFFERING)
		{
			Socket.emit(EVENT_YT_STATE_CHANGE, {
				'state': 'pause',
				'offset': ytPlayerRef.current.getCurrentTime()
			});
		}
	}

	function onYtStateChange(event)
	{
		console.log('state change', event, playerState);

		setPlayerState([playerState[1], event.data]);
	}

	const videoId = 'dQw4w9WgXcQ';
	const opts = {
		playerVars: {
			autoplay: 0,
			controls: 1,
			disablekb: 0
		}
	};

	return (
		<div>
			<YouTube
				videoId={videoId}
				opts={opts}
				onReady={onYtReady}
				onPlay={onYtPlay}
				onPause={onYtPause}
				onStateChange={onYtStateChange}
			/>
		</div>
	);
}
