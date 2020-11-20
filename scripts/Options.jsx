import React, { useState } from 'react';
import { Content } from './Content';
import { Socket } from './Socket';
import './options.css';


export function Options()
{
	const [userFlag, setFlag] = useState(false);

	function onRoomNewClick()
	{
		Socket.emit('room_create', {
			roomName: 'test room'
		}, (data) =>
		{
			console.log(data);
			if(data.status == 'ok')
			{
				document.body.style.backgroundColor = '#00c9c8';
				setFlag(true);
			}
		});
	}

	function onRoomJoinClick()
	{
		console.log('acb');

		Socket.emit('room_join', {
			roomId: document.getElementById('roomCode').value
		}, (data) =>
		{
			console.log(data);
			if(data.status == 'ok')
			{
				document.body.style.backgroundColor = '#00c9c8';
				setFlag(true);
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

				<div>
					<input id='roomCode' onKeyUp={onKeyUp} placeholder='Room Code'/>
					<button className="button" onClick={onRoomJoinClick}>Join Viewing Room</button>
				</div>
			</div>

		</body>
	);
}
