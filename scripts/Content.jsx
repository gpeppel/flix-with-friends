import * as React from 'react';
import { Chat } from './Chat';
import { YoutubeContainer } from './YoutubeContainer';

import { Socket } from './Socket';

import './css/content.css';


const EVENT_YT_LOAD = 'yt_load';


export function Content()
{
	const [roomID, setRoomID] = React.useState([]);

	console.log('emitting');
	Socket.emit('new room');

	Socket.emit('chat_loaded');

	React.useEffect(() =>
	{
		Socket.on('new room id', setRoomID);
	}, []);
	console.log(roomID);

	function onKeyUp(event)
	{
		if(event.key == 'Enter')
		{
			Socket.emit(EVENT_YT_LOAD, {
				'url': event.target.value
			});
		}
	}

	return (
		<div className='main-content'>
			<div style={{
				display: 'flex',
				flex: 1
			}}>
				<Chat />
			</div>
			<div className='media-area'>
				<input onKeyUp={onKeyUp} placeholder="Enter YouTube URL"/>
				<YoutubeContainer />
			</div>
			<div style={{
				flex: 1
			}}>
			</div>
		</div>
	);
}
