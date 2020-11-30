import React, { useState } from 'react';
import { Content } from './Content';
import { Socket } from './Socket';
import { UserDispatchContext } from './UserProvider';
import './options.css';


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
			roomName: 'test room'
		}, (data) =>
		{
			console.log(data);
			if(data.status != 'ok')
				return;

			updateUserDetails({
				roomId: data.room_id,
				roomName: data.room_name
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
				<button className='button' onClick={onRoomNewClick}>Create New Viewing Room</button>
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
