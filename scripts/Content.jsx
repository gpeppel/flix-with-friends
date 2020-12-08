
import * as React from 'react';
import { Chat } from './Chat';
import { RoomInfo } from './RoomInfo';
import { YoutubeContainer } from './YoutubeContainer';
import { HostOptions } from './HostOptions';
import { UserContext, UserDispatchContext } from './UserProvider';
import { Socket } from './Socket';
import { Queue } from './Queue';
import './css/content.css';

const EVENT_YT_LOAD = 'yt_load';


export function Content()
{
	const userDetails = React.useContext(UserContext);
	const updateUserDetails = React.useContext(UserDispatchContext);

	React.useEffect(() =>
	{
		Socket.on('room_info_received', (data) =>
		{
			updateUserDetails({
				room: {
					isCreator: (data.room_info.creator ?
						data.room_info.creator.sid == userDetails.sid
						: false
					)
				}
			});
		});

		Socket.emit('user_join', {});
	}, []);

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
		const input = document.createElement('input');
		input.value = userDetails.room.id;

		document.body.appendChild(input);
		input.select();
		document.execCommand('copy');
		document.body.removeChild(input);

		alert('Copied Room ID ' + userDetails.room.id);
	}

	return (
		<div className='main-content'>
			<div className='main-panel'>
				<Chat />
				<RoomInfo />
			</div>
			<div className='media-area'>
				<input onKeyUp={onKeyUp} placeholder="Enter YouTube URL"/>
				<YoutubeContainer />
				<button onClick={copyRoomId} id='btnID'>Copy Room ID</button>
			</div>
			<div className='main-panel'>
				<div>
					<HostOptions />
					<br></br>
					<Queue />
				</div>
			</div>
		</div>
	);
}
