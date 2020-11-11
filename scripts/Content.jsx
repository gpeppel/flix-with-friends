import * as React from 'react';

import { YoutubeContainer } from './YoutubeContainer';
import { Socket } from './Socket';


export function Content() {
	function onKeyUp(event)
	{
		console.log(event.key);
		if(event.key == "Enter")
		{
			Socket.emit('yt-load', {
				'url': event.target.value
			});
		}
	}
	
	return (
		<div>
			<input onKeyUp={onKeyUp} />
			<YoutubeContainer />
		</div>
	);
}
