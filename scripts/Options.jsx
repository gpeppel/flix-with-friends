import React, { useState } from 'react';
import { Content } from './Content';
import './options.css';
import { Socket } from './Socket';
import { FacebookButton } from './FacebookButton';


export function Options()
{
	const [userFlag, setFlag] = useState(false);

	function handleSubmit(event)
	{

		setFlag(true);
		event.preventDefault();
	}


	if (userFlag)
	{
		return (<Content />);
	}

	return (
		<body>
			<div className="centered">
				<h1>Create New Viewing Room</h1>
				<FacebookButton />
				<button onClick={handleSubmit}>Create Now!</button>
			</div>
		</body>
	);
}
