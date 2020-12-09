/* eslint-disable react/prop-types */

import * as React from 'react';
import { UserContext, isCreator } from './UserProvider';
import { Socket } from './Socket';

import './css/user.css';

export function User(props)
{
	const userDetails = React.useContext(UserContext);

	function confirmHostChange(event)
	{
		console.log(event);
		if(confirm(`Are you sure you want to make ${props.user.username} the new host?`))
		{
			Socket.emit('room_assign_host', {
				'sid': props.user.sid
			});
		}
	}

	return (
		<div className='user'>
			<div className='header'>
				<span className='left'>
					<img className='profileImg' alt='Profile' src={props.user.profile_url} />
					<span className='username'>{props.user.username}</span>
				</span>

				{(() =>
				{
					if(!isCreator(userDetails) || userDetails.sid == props.user.sid)
						return (<div></div>);

					return (
						<button className='assign-host' onClick={confirmHostChange}>
							Assign as New Host
						</button>
					);
				})()}
			</div>
		</div>
	);
}
