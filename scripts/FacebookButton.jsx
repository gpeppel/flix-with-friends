import * as React from 'react';
import { Socket } from './Socket';
import FacebookLogin from 'react-facebook-login';

function handleSubmit(response)
{
	console.log('reached submit');
	console.log(response);
}

const responseFacebook = (response) =>
{
	console.log(response);
	Socket.emit('new_facebook_user', {
		'response': response
	});
	document.body.style.backgroundColor = '#eea1b8';
};

export function FacebookButton()
{
	return (
		<FacebookLogin
			appId="2775898756021193"
			autoLoad={false}
			fields="name,email,picture"
			onClick={handleSubmit}
			callback={responseFacebook} />
	);
}
