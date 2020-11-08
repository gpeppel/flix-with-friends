import * as React from 'react';

import { Socket } from './Socket';

import YouTube from 'react-youtube';

const EVENT_YT_STATE_CHANGE = 'yt-state-change';

export function YoutubeContainer() {
	const [ytPlayer, setYtPlayer] = React.useState(null);
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
		console.log('play', event);

		Socket.emit(EVENT_YT_STATE_CHANGE, {
			'state': 'play',
			'offset': ytPlayerRef.current.getCurrentTime()
		});
	}

	function onYtPause(event)
	{
		console.log('pause', event);

		Socket.emit(EVENT_YT_STATE_CHANGE, {
			'state': 'pause',
			'offset': ytPlayerRef.current.getCurrentTime()
		});
	}

	function onYtStateChange(event)
	{
		console.log('state change', event);
	}

	return (
		<div>
			<YouTube
				videoId='dQw4w9WgXcQ'
				onReady={onYtReady}
				onPlay={onYtPlay}
				onPause={onYtPause}
				onStateChange={onYtStateChange}
			/>
		</div>
	);
}
