import React, { useState } from 'react';
import { Content } from './Content';
import { Socket } from './Socket';
import { UserDispatchContext } from './UserProvider';
import { AwesomeButtonProgress } from 'react-awesome-button';
import './css/Options.css';
import './css/theme-eric.css';


export function Options()
{
	window.addEventListener('unload', () =>
	{
		Socket.emit('disconnect', {
			// 'userId': userId,
		});
	});

	// window.onbeforeunload = function (event) { Socket.emit('disconnect');};

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
					currentVideoCode: data.current_video_code,
					isCreator: true
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
					currentVideoCode: data.current_video_code,
					isCreator: false
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
		<div className="options-wrapper">
			<div className="box">
				<div className="column" id="box-left">CREATE A NEW VIEWING ROOM<img src="/static/images/line_left.png" id="line" /></div>
				<div className="column" id="box-right">JOIN A VIEWING ROOM NOW<img src="/static/images/line_right.png" id="line-sm" /></div>
			</div>
			<div className="box">
				<div className="column" id="box-left"><img src="/static/images/ticket.png" /></div>
				<div className="column" id="box-right"><img src="/static/images/popcorn_icon.png" /></div>
			</div>
			<div className="box">
				<div className="column" id="text-box-left">
					<div>
						<div className="row">
							<span><input className="slide-up-left" id='playlist' type="text" placeholder="GOES HERE" />
								<label htmlFor="card">URL</label></span>
						</div>
					</div>
				</div>
				<div className="column" id="text-box-right">
					<div className="row">
						<span><input className="slide-up-right" id='roomCode' type="text" placeholder="GOES HERE" />
							<label htmlFor="card">CODE</label></span>
					</div>
				</div>
			</div>
			<div className="box">
				<div className="column" id="box-left-btn">
					<AwesomeButtonProgress
						type='twitter2'
						loadingLabel='I HOPE NOTHING BREAKS..'
						releaseDelay={5000}
						resultLabel='FOR A SECOND TIME'
						onPress={() =>
						{
							onRoomNewClick();
						}}
					>
					CREATE NEW VIEWING ROOM!
					</AwesomeButtonProgress>
				</div>
				<div className="column" id="box-right-btn">
					<AwesomeButtonProgress
						type='whatsapp'
						loadingLabel='JOINING...'
						releaseDelay={6000} resultLabel='FOUND FRIENDS!'
						onPress={() =>
						{
							onRoomJoinClick();
						}}
					>
					JOIN VIEWING ROOM
					</AwesomeButtonProgress>
				</div>
			</div>
			<div className="box" id="box-last">
				<div className="column" id="box-left"></div>
				<div className="column" id="box-right-last">
					COPY &amp; PASTE YOUR INVITATION CODE IN THE ABOVE BOX
					<hr className='hr-line2'/>
				</div>
			</div>
			<div className="box" id="box-last">
			</div>
		</div>
	);
}
