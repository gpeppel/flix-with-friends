import * as React from 'react';
import { Socket } from './Socket';
import FacebookLogin from 'react-facebook-login';


export function FacebookButton()
{
	function responseFacebook(response)
	{
		console.log(response);
		Socket.emit('login_oauth_facebook', {
			'response': response
		});
		document.body.style.backgroundColor = '#eea1b8';
	}

	return (
		<FacebookLogin
			appId="2775898756021193"
			autoLoad={false}
			fields="name,email,picture"
			callback={responseFacebook}
		/>
	);
}
