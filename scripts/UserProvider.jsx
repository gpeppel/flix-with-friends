// https://blog.logrocket.com/a-deep-dive-into-react-context-api/

import * as React from 'react';

import { Socket } from './Socket';

export const UserContext = React.createContext(undefined);
export const UserDispatchContext = React.createContext(undefined);

export function UserProvider({children}) {
	React.useEffect(() =>
	{
		Socket.on('connect', (data) =>
		{
			console.log(data);
		});
	}, []);

	const [userDetails, setUserDetails] = React.useState({
		user_id: undefined,
		username: undefined,
		email: undefined,
		profile_url: undefined,
		settings: undefined,
		oauth_id: undefined,
		oauth_type: undefined,
		sid: undefined,
		session_id: undefined
	});

	function updateUserDetails(user)
	{
		console.log(user, userDetails);
		setUserDetails(user);
	}

	return (
		<UserContext.Provider value={userDetails}>
			<UserDispatchContext.Provider value={updateUserDetails}>
				{children}
			</UserDispatchContext.Provider>
		</UserContext.Provider>
	);
}

export function debugElement(user)
{
	return (
		<div>
			<div>
				<span>Id:</span>
				<span>{user.id}</span>
			</div>
			<div>
				<span>Username:</span>
				<span>{user.username}</span>
			</div>
			<div>
				<span>Email: </span>
				<span>{user.email}</span>
			</div>
			<div>
				<span>Profile Url:</span>
				<span>{user.profile_url}</span>
			</div>
			<div>
				<span>Settings:</span>
				<span>{user.settings}</span>
			</div>
			<div>
				<span>OAuth Id:</span>
				<span>{user.oauth_id}</span>
			</div>
			<div>
				<span>OAuth Type:</span>
				<span>{user.oauth_type}</span>
			</div>
			<div>
				<span>Sid:</span>
				<span>{user.sid}</span>
			</div>
			<div>
				<span>Session Id:</span>
				<span>{user.session_id}</span>
			</div>
		</div>
	);
}
