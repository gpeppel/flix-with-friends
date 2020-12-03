import * as React from 'react';

import { Login } from './Login';


export function App()
{
	return (
		<div style={{
			height: '100%'
		}}>
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
