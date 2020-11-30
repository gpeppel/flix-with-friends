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
		roomId: undefined,
		roomName: undefined
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
	return (
		<div>
			{
				Object.keys(user).map((x) =>
					(
						<div key={x}>
							<span>{`${x}: `}</span>
							<span>{`${user[x]}`}</span>
						</div>
					)
				)
			}
		</div>
	);
}
