import * as React from 'react';

import { Login } from './Login';
import { UserContext, UserProvider, debugElement } from './UserProvider';


export function App()
{
	const userDetails = React.useContext(UserContext);

	return (
		<div style={{
			height: '100%'
		}}>
			<div>
				{debugElement(userDetails)}
			</div>

			<div style={{
				display: 'flex',
				flexDirection: 'column',
				height: '100%'
			}}>
				<div className='main-header'>
					<img className='logo' src='/static/images/logo.png' alt='logo' />
				</div>

				<Login />
			</div>
		</div>
	);
}
