import * as React from 'react';

import { Socket } from './Socket';

import YouTube from 'react-youtube';


export function YoutubeContainer() {
	React.useEffect(() => {
		Socket.on('yt-state-change', (data) => {
			console.log(data);
		});
	}, []);

	return (
		<div>
			<YouTube />
		</div>
	);
}
