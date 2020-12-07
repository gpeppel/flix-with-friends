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

	let getYoutubeTitle = require('get-youtube-title');
	getYoutubeTitle('oMpiZrgxHSU', function (err, title) {
		console.log(title);
	})
	

		

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
					  <span><input className="slide-up-left" on type="text" placeholder="URL HERE" />
					  <label htmlFor="card">ENTER</label></span>
					  </div>
				</div>
			  </div>
			  <div className="column" id="text-box-right">
				  <div className="row">
					  <span><input className="slide-up-right" type="text" placeholder="URL HERE" />
					  <label htmlFor="card">ENTER</label></span>
			  </div>
			  </div>
			  </div>
			<div className="box">
				<div className="column" id="box-left">

					<AwesomeButtonProgress type='twitter2' loadingLabel='I HOPE NOTHING BREAKS..' releaseDelay='600' resultLabel='FOR A SECOND TIME'
						onPress={(element, next) => { console.log('-------'); setTimeout(() => { next(); }, 600)}} >
					CREATE NEW VIEWING ROOM!
					</AwesomeButtonProgress>
				</div>
				<div className="column" id="box-right">	
					<AwesomeButtonProgress type='whatsapp' loadingLabel='JOINING...' releaseDelay='600' resultLabel='FOUND FRIENDS!'
						onPress={(element, next) => { console.log("What's up bro..."); setTimeout(() => { next(); }, 600)}}>
					JOIN VIEWING ROOM
					</AwesomeButtonProgress>
				</div>
			</div>
			<div className="box" id="box-last">
			  <div className="column" id="box-left"></div>
			  <div className="column" id="box-right-last">
				<p>COPY &amp; PASTE YOUR INVITATION CODE IN THE ABOVE BOX TO JOIN YOUR FRIENDS!</p>
			  </div>
			  </div>
			<div className="box" id="box-last">
			  <div className="column" id="box-left"></div>
			  <div className="column" id="box-right-last"></div>
			</div>
		  </div>
		  
	);
}
