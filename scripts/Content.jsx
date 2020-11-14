import * as React from 'react';
import { YoutubeContainer } from './YoutubeContainer';

import { Socket } from './Socket';
import { Chat } from './Chat';

const EVENT_YT_LOAD = 'yt_load';
import './content.css';
export function Content()
{

	const [roomID, setRoomID] = React.useState([]);


	console.log('emitting');
	Socket.emit('new room');

	Socket.emit('chat_loaded');

	React.useEffect(() =>
	{
		Socket.on('new room id', setRoomID);
	}, []);
	console.log(roomID);

	function onKeyUp(event)
	{
		if(event.key == 'Enter')
		{
			Socket.emit(EVENT_YT_LOAD, {
				'url': event.target.value
			});
		}
	}

	return (
		<div>
			<div className="header">
				<img src="static/images/logo.png" alt="logo" />
			</div>
			<div className="Content">
				<div className="Wrapper">
					<div className="RightContent">
						<YoutubeContainer />
					</div>
					<div className="LeftContent">
						<Chat />
					</div>
				</div>

			</div>
			<input onKeyUp={onKeyUp} />
		</div>
	);
}
