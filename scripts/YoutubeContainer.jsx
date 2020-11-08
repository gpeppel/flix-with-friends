import * as React from 'react';

import { Socket } from './Socket';

import YouTube from 'react-youtube';


export function YoutubeContainer() {
	const [ytPlayer, setYtPlayer] = React.useState(null);
	const ytPlayerRef = React.useRef();

	ytPlayerRef.current = ytPlayer;

	React.useEffect(() => {
		Socket.on('yt-state-change', (data) => {
			switch(data.state)
			{
				case 'play':
					ytPlayerRef.current.playVideo();
					break;
				case 'pause':
					ytPlayerRef.current.pauseVideo();
					break;
			}
		});
	}, []);

	function onYtReady(event)
	{
		setYtPlayer(event.target);
	}

	function onYtPlay(event)
	{
		console.log('play', event);

		Socket.emit('yt-state-change', {
			'state': 'play',
			'offset': undefined
		});
	}

	function onYtPause(event)
	{
		console.log('pause', event);

		Socket.emit('yt-state-change', {
			'state': 'pause',
			'offset': undefined
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
