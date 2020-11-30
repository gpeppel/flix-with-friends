// https://blog.logrocket.com/a-deep-dive-into-react-context-api/

import * as React from 'react';
import PropTypes from 'prop-types';

import { Socket } from './Socket';

export const UserContext = React.createContext(undefined);
export const UserDispatchContext = React.createContext(undefined);

export function UserProvider({children})
{
	React.useEffect(() =>
	{
		Socket.on('connect', (data) =>
		{
			console.log(data);
		});
	}, []);

	const [userDetails, setUserDetails] = React.useState({
		id: undefined,
		username: undefined,
		email: undefined,
		profileUrl: undefined,
		settings: undefined,
		oauthId: undefined,
		oauthType: undefined,
		sid: undefined,
		sessionId: undefined,
		room: undefined
	});

	function updateUserDetails(user)
	{
		setUserDetails(Object.assign({}, userDetails, user));
	}

	return (
		<UserContext.Provider value={userDetails}>
			<UserDispatchContext.Provider value={updateUserDetails}>
				{children}
			</UserDispatchContext.Provider>
		</UserContext.Provider>
	);
}

UserProvider.propTypes = {
	children: PropTypes.node,
};


export function debugElement(user)
{
	function propsToElement(obj, prefix)
	{
		if(prefix === undefined)
			prefix = '';

		return Object.keys(obj).map((x) =>
		{
			if(obj[x] instanceof Object)
				return propsToElement(obj[x], `${prefix}${x}.`);

			return (
				<div key={prefix + x}>
					<span style={{
						fontWeight: 'bold'
					}}>{`${prefix}${x}: `}</span>
					<span>{`${obj[x]}`}</span>
				</div>
			);
		});
	}

	return (
		<div>
			{propsToElement(user)}
		</div>
	);
}
