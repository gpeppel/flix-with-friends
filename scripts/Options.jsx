import React, { useState } from 'react';
import { Content } from './Content';
import { Socket } from './Socket';
import { UserDispatchContext } from './UserProvider';
import './css/options.css';


export function Options()
{
	const updateUserDetails = React.useContext(UserDispatchContext);
	const [userFlag, setFlag] = useState(false);

	function enterRoom()
	{
		setFlag(true);
	}

	function onRoomNewClick()
	{
		Socket.emit('room_create', {
			description: 'test room',
			playlist: document.getElementById('playlist').value.split('\n')
		}, (data) =>
		{
			console.log(data);
			if(data.status != 'ok')
				return;

			updateUserDetails({
				room: {
					id: data.room_id,
					description: data.room_name,
					currentVideoCode: data.current_video_code
				}
			});
			enterRoom();
		});
	}

	function onRoomJoinClick()
	{
		Socket.emit('room_join', {
			roomId: document.getElementById('roomCode').value
		}, (data) =>
		{
			console.log(data);
			if(data.status != 'ok')
				return;

			updateUserDetails({
				room: {
					id: data.room_id,
					description: data.room_name,
					currentVideoCode: data.current_video_code
				}
			});
			enterRoom();
		});
	}

	function onKeyUp(event)
	{
		if(event.key == 'Enter')
			onRoomJoinClick();
	}

	if(userFlag)
	{
		return (<Content />);
	}

	return (
		<div className='options'>
			<img className='popcorn-img' src='static/images/popcorn_button.png' alt='popcorn_button' />

			<div className='section'>
				<div>
					<textarea id='playlist' placeholder='Youtube Videos (one per line)'></textarea>
				</div>
				<button className='button' onClick={onRoomNewClick}>Host Viewing Room</button>
			</div>

			<div className='section room' style={{
				display: 'flex',
				flexDirection: 'column'
			}}>
				<input id='roomCode' onKeyUp={onKeyUp} placeholder='Room Code'/>
				<button className='button' onClick={onRoomJoinClick}>Join Viewing Room</button>
			</div>
		</div>
	);
}
