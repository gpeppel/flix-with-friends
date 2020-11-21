import React, { useState } from 'react';
import { Content } from './Content';
import { Socket } from './Socket';
import './options.css';


export function Options()
{
	const [userFlag, setFlag] = useState(false);

	function enterRoom()
	{
		document.body.style.backgroundColor = '#00c9c8';
		setFlag(true);
	}

	function onRoomNewClick()
	{
		Socket.emit('room_create', {
			roomName: 'test room'
		}, (data) =>
		{
			console.log(data);
			if(data.status == 'ok')
			{
				enterRoom();
			}
		});
	}

	function onRoomJoinClick()
	{
		Socket.emit('room_join', {
			roomId: document.getElementById('roomCode').value
		}, (data) =>
		{
			console.log(data);
			if(data.status == 'ok')
			{
				enterRoom();
			}
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
		<body>
			<div className="header">
				<img src="static/images/logo.png" alt="logo" />
			</div>
			<div className="centered">
				<img className="popcorn_button" src="static/images/popcorn_button.png" alt="popcorn_button" />

				<div>
					<button className="button" onClick={onRoomNewClick}>Create New Viewing Room</button>
				</div>

				<div style={{
					borderTop: '3px solid #ffc341',
					marginTop: '20px'
				}}>
					<input id='roomCode' style={{
						display: 'block',
						fontSize: '24px',
						margin: '15px 0px',
						padding: '12px 5px'
					}} onKeyUp={onKeyUp} placeholder='Room Code'/>
					<button className="button" onClick={onRoomJoinClick}>Join Viewing Room</button>
				</div>
			</div>

		</body>
	);
}
