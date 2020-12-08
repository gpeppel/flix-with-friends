import * as React from 'react';
import { Socket } from './Socket';
import { User } from './User';

export function RoomInfo()
{
	const [users, setUsers] = React.useState({});
	const [creator, setCreator] = React.useState('');

	function getRoomInfo()
	{
		React.useEffect(() =>
		{
			Socket.on('room_info_received', (data) =>
			{
				var info = data['room_info'];
				console.log('Room info updated.');
				console.log(info);

				var roomCreator = info['creator'];
				setCreator(roomCreator);

				var activeUsers = info['users'];
				setUsers(activeUsers);
			});
		});
	}

	getRoomInfo();

	return (
		<div id="roomInfoBox">
			<p>Users:</p>
			<p>Room Creator: {creator ? creator.username : 'Nobody'}</p>
			<div id="userFeed">
				{
					Object.values(users).map((user) => (<User key={user.user_id} user={user} /> ))
				}
			</div>
		</div>
	);
}
