import * as React from 'react';
import { Options } from './Options';
import { FacebookButton } from './FacebookButton';
import { GoogleButton } from './GoogleButton';
import { TwitterButton } from './TwitterButton';
import { Socket } from './Socket';
import './login.css';

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
		<div className='login'>
			<div className='section'>
				<img className='fb-img' src='static/images/fb_button.png' alt='fb_button' />
				<FacebookButton />
			</div>
			<div className='section'>
				<GoogleButton />
			</div>
			<div className='section'>
				<TwitterButton />
			</div>
		</div>
	);
}
