import * as React from 'react';
import { Options } from './Options';
import { FacebookButton } from './FacebookButton';
import { GoogleButton } from './GoogleButton';
import { Socket } from './Socket';
import { UserDispatchContext } from './UserProvider';
import './login.css';

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
		<div className='login'>
			<div className='section'>
				<img className='fb-img' src='static/images/fb_button.png' alt='fb_button' />
				<FacebookButton />
			</div>
			<div className='section'>
				<GoogleButton />
			</div>
		</div>
	);
}
