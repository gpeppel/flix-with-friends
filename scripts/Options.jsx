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
			playlist: document.getElementById('playlist').value
		}, (data) =>
		{
			console.log('playlist -->');
			console.log(data);
			console.log('------');
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
		<div class="options-wrapper">
		<div className="box">
   			<div className="column" id="box-left">
				   <br />
      			CREATE A NEW VIEWING ROOM
				  
				  <img src="/static/images/line_left.png" id="line" />
   			</div>
   				<div className="column" id="box-right">
				   <br />
      				JOIN A VIEWING ROOM NOW
					  <img src="/static/images/line_right.png" id="line-sm" />
   				</div>
			</div>
			<div className="box">
   					<div className="column" id="box-left"><img src="/static/images/ticket.png" /></div>
   					<div className="column" id="box-right"><img src="/static/images/popcorn_icon.png"/></div>
			</div>
			<div className="box">
   				<div className="column" id="box-left"><input id='playlist' onKeyUp={onKeyUp} placeholder='Video URL GOES HERE' /></div>
   				<div className="column" id="box-right"><input id='roomCode' onKeyUp={onKeyUp} placeholder='Room Code' /></div>
			</div>
			<div className="box">
   				<div className="column" id="box-left"><button className='button' onClick={onRoomJoinClick}>Join Viewing Room</button></div>
   				<div className="column" id="box-right"><button className='button' onClick={onRoomNewClick}>Host Viewing Room</button></div>
			</div>
			<div className="box">
   				<div className="column" id="box-left"><br /></div>
   				<div className="column" id="box-right"></div>
			</div>
			<div className="box" id="box-last">
   				<div className="column" id="box-left"></div>
   			<div className="column" id="box-right-last">
      			Text goes here jwebfiuibewofjfbwie
   			</div>
			   
		</div>
		</div>
	);
}
