import * as React from 'react';
import { Chat } from './Chat';
import { YoutubeContainer } from './YoutubeContainer';
import { HostOptions } from './HostOptions';
import { UserContext } from './UserProvider';
import { Socket } from './Socket';

import './content.css';


const EVENT_YT_LOAD = 'yt_load';


export function Content()
{
	const userDetails = React.useContext(UserContext);
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

	function copyRoomId()
	{
		var input = document.createElement('input');
		input.value = userDetails.room.id;
		input.id = 'inputID';
		document.body.appendChild(input);
		input.select();
		document.execCommand('copy');
		alert('Copied Room ID ' + input.value);
		document.body.removeChild(input);
	}

	return (
		<div className='main-content'>
			<div className='main-panel'>
				<Chat />
			</div>
			<div className='media-area'>
				<input onKeyUp={onKeyUp} placeholder="Enter YouTube URL"/>
				<YoutubeContainer />
				<button onClick={copyRoomId} id='btnID'>Copy Room ID</button>
			</div>
			<div className='main-panel'>
				<div>
					<HostOptions />
				</div>
				<div>
					<p>Playlist</p>
				</div>
			</div>
		</div>
	);
}
