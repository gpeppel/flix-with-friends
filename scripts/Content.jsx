import * as React from 'react';
import { Chat } from './Chat';
import { RoomInfo } from './RoomInfo';
import { YoutubeContainer } from './YoutubeContainer';

import { Socket } from './Socket';

import './content.css';


const EVENT_YT_LOAD = 'yt_load';


export function Content()
{
	Socket.emit('chat_loaded');

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
				<RoomInfo />
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
