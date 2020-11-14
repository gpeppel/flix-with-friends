import * as React from 'react';
import { Socket } from './Socket';
import FacebookLogin from 'react-facebook-login';

function handleSubmit(response)
{
	console.log('reached submit');
	// let name = response.profileObj.name;
	// let email = response.profileObj.email;
	// let imgURL = response.profileObj.imageUrl;

	// Socket.emit('new_facebook_user', {
	//   'name': name,
	//   'email': email,
	//   'imgURL': imgURL,
	// });

	// console.log('Sent the name ' + name + ' to server!');
	// console.log('Sent the email ' + email + ' to server!');
	// console.log('Sent the imgage url ' + imgURL + ' to server!');

	console.log(response);

}

const responseFacebook = (response) =>
{
	console.log(response);
	Socket.emit('new_facebook_user', {
		'response': response
	});
	document.body.style.backgroundColor = "#eea1b8";
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
