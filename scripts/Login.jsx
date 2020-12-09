
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
			console.log('LOGIN_RESPONSE ---> ');
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
			<div className='top'>
				<div>
					SIMPLE & EASY TO USE
					<br />
					GET STARTED BY CLICKING BELOW
					<hr className='hr-line' />
				</div>
			</div>
			<div className='login'>
				<div className="flex-item">
					<img className='login-img' src='static/images/fb_button.png' alt='fb' />
					<FacebookButton />
				</div>
				<div className="flex-item">
					<img className='login-img' src='static/images/google.png' alt='google' />
					<GoogleButton />
				</div>
				<div className="flex-item">
					<img className='login-img' src='static/images/twitter.png' alt='twitter' />
					<TwitterButton />
				</div>
			</div>
		</div>
	);
}
