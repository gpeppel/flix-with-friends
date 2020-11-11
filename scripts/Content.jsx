import * as React from 'react';

import { YoutubeContainer } from './YoutubeContainer';
import { Socket } from './Socket';


const EVENT_YT_LOAD = 'yt-load';


export function Content() {
	function onKeyUp(event)
	{
		if(event.key == "Enter")
		{
			Socket.emit(EVENT_YT_LOAD, {
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
