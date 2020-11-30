'use strict';

const WAIT_UPDATE_DATA = 3000;

const roomtable = document.getElementById('roomtable');
const usertable = document.getElementById('usertable');

function updateRoomTable(rooms)
{
	function createRow(room)
	{
		function createUsersTd(users)
		{
			const td = document.createElement('td');
			const pre = document.createElement('pre');

			let str = '';
			for (const user of users)
			{
				str += `${user.user_id}, ${user.username}\n`;
			}
			pre.innerHTML = str;

			td.appendChild(pre);
			return td;
		}

		const row = document.createElement('tr');

		row.appendChild(createTd(room.room_id));
		row.appendChild(createUsersTd([room.creator]));
		row.appendChild(createUsersTd(Object.values(room.users)));
		return row;
	}

	while(roomtable.children.length > 1)
		roomtable.removeChild(roomtable.children[1]);

	for (const roomId in rooms)
		roomtable.appendChild(createRow(rooms[roomId]));
}

function updateUserTable(users)
{
	function createRow(user)
	{
		const row = document.createElement('tr');

		row.appendChild(createTd(user.user_id));
		row.appendChild(createTd(user.username));
		row.appendChild(createTd(user.email));
		row.appendChild(createTd(user.profile_url));
		row.appendChild(createTd(user.settings));
		row.appendChild(createTd(user.oauth_id));
		row.appendChild(createTd(user.oauth_type));

		row.appendChild(createTd(user.sid));
		row.appendChild(createTd(user.session_id));

		row.appendChild(createTd(user.socket_connected));
		row.appendChild(createTd(user.last_socket_connect));

		return row;
	}

	while(usertable.children.length > 1)
		usertable.removeChild(usertable.children[1]);

	for (const userId in users)
		usertable.appendChild(createRow(users[userId]));
}

function createTd(text)
{
	const td = document.createElement('td');
	td.innerHTML = text;
	return td;
}

function loadDebugData()
{
	const xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function()
	{
		if(this.readyState == 4 && this.status == 200)
		{
			const data = JSON.parse(this.responseText);
			updateRoomTable(data.rooms);
			updateUserTable(data.users);
		}
	};

	xhttp.open('GET', '/debug.json', true);
	xhttp.send();
}

loadDebugData();
setInterval(() =>
{
	loadDebugData();
}, WAIT_UPDATE_DATA);
