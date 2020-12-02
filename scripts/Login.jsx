
import * as React from 'react';
import { Options } from './Options';
import { FacebookButton } from './FacebookButton';
import { GoogleButton } from './GoogleButton';
import { TwitterButton } from './TwitterButton';
import { Socket } from './Socket';

import './css/login.css';
import { Footer } from './Footer';

export function Login()
{
	const [userFlag, setFlag] = React.useState(false);

	React.useEffect(() =>
	{
		Socket.on('login_response', (data) =>
		{
			console.log(data);

			if(data.status != 'ok')
				return;

			setFlag(true);
		});

	}, []);

	if (userFlag)
	{
		return (<Options />);
	}

	return (
		<div>
			<ul className="flex-container center">
				<li className="top">
					START WATCHING WITH FRIENDS NOW!
					<hr className='line' />
				</li>
			</ul>
		<div className='login'>
			<ul className="flex-container space-evenly">
				<li className="flex-item">
					<img className='fb-img' src='static/images/fb_button.png' alt='fb' />
					<FacebookButton />
				</li>
				<li className="flex-item">		
					<img className='google-img' src='static/images/google.png' alt='google' />
					<GoogleButton />
				</li>
				<li className="flex-item">	
					<img className='twitter-img' src='static/images/twitter.png' alt='twitter' />
					<TwitterButton />
				</li>
			</ul>
		</div>
		<Footer />
		</div>
	);
}