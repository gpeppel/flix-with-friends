
import * as React from 'react';
import { Options } from './Options';
import { FacebookButton } from './FacebookButton';
import { GoogleButton } from './GoogleButton';
import { TwitterButton } from './TwitterButton';
import { Socket } from './Socket';
import { UserDispatchContext } from './UserProvider';
import './css/login.css';

export function Login()
{
	const updateUserDetails = React.useContext(UserDispatchContext);
	const [userFlag, setFlag] = React.useState(false);

	React.useEffect(() =>
	{
		Socket.on('login_response', (data) =>
		{
			console.log(data);

			if(data.status != 'ok')
				return;

			const user = data.user;

			updateUserDetails({
				id: user.id,
				username: user.username,
				email: user.email,
				profileUrl: user.profile_url,
				settings: user.settings,
				oauthId: user.oauth_id,
				oauthType: user.oauth_type,
				sid: user.sid,
				sessionId: user.session_id
			});

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
					SIMPLE & EASY TO USE <br />
					GET STARTED BY CLICKING BELOW
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
	</div>
	);
}
