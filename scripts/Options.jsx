import React, { useState } from 'react';
import { Content } from './Content';
import './options.css';


export function Options()
{
	const [userFlag, setFlag] = useState(false);

	function handleSubmit(event)
	{
		React.useEffect(() =>
		{
			Socket.emit('get_room_id', (data) =>
			{
				// TODO may have to set message scrollbar to bottom or something later
			});
		});
		document.body.style.backgroundColor = '#00c9c8';
		setFlag(true);
		event.preventDefault();
	}


	if (userFlag)
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

				<button className="button" onClick={handleSubmit}>Enter viewing room!</button>
			</div>

		</body>
	);
}
