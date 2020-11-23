/* eslint-disable react/prop-types */

import * as React from 'react';
import './chat.css';


export function ChatMessage(props)
{
	return (
		<div className='message'>
			<div className='header'>
				<span className='left'>
					<img className='profileImg' alt='Profile' src={props.message.user.profile_url} />
					<span className='username'>{props.message.user.username}</span>
					<span>:</span>
				</span>
				<span className='right'>
					<span className='timestamp'>{props.message.timestamp}</span>
				</span>
			</div>
			<div className='content'>
				<p className='text'>{props.message.text}</p>
			</div>
		</div>
	);
}
