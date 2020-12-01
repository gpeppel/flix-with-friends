/* eslint-disable react/prop-types */

import * as React from 'react';
import './user.css';

export function User(props)
{
	return (
		<div className='user'>
			<div className='header'>
				<span className='left'>
					<img className='profileImg' alt='Profile' src={props.user.profile_url} />
					<span className='username'>{props.user.username}</span>
				</span>
			</div>
		</div>
	);
}
