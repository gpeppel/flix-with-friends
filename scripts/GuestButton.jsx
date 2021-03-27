/* global process */

import * as React from 'react';
import { Socket } from './Socket';
import { AwesomeButton } from "react-awesome-button";
import './css/theme-eric.css';

export function GuestButton()
{
	function response(data)
	{
		Socket.emit('login_guest', {});
	}

	return (
		<AwesomeButton type="reddit" onPress={(event) => {response({})}}>LOGIN AS GUEST</AwesomeButton>
	);
}