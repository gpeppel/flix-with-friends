import React, { useState } from 'react';
import { Content } from './Content';
import { Socket } from './Socket';
import { UserDispatchContext } from './UserProvider';
import { AwesomeButtonProgress } from 'react-awesome-button';
import './css/options.css';
import './css/theme-eric.css';


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
			if(data.status != 'ok') {
				alert("Failed: " + data.error);
				return;
			}

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
			<div className="column column-left">
				<div>CREATE A NEW VIEWING ROOM<hr className='hr-line3' /></div>
				<div><img src="/static/images/ticket.png" /></div>
				<div id="text-box-left">
					<div>
						<div className="row">
							<span><input className="slide-up-left" onKeyUp={onKeyUp} id='playlist' type="text" placeholder="GOES HERE" />
								<label htmlFor="card">URL</label></span>
						</div>
					</div>
				</div>
				<div>
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
			</div>
			<div className="column column-right">
				<div>JOIN A VIEWING ROOM NOW<hr className='hr-line4' /></div>
				<div><img src="/static/images/popcorn_icon.png" /></div>
				<div id="text-box-right">
					<div className="row">
						<span><input className="slide-up-right" id='roomCode' onKeyUp={onKeyUp} type="text" placeholder="GOES HERE" />
							<label htmlFor="card">CODE</label></span>
					</div>
				</div>
				<div id="box-right-btn">
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
		</div>
	);
}
