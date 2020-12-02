import * as React from 'react';
import * as ReactDOM from 'react-dom';

import { Login } from './Login';

ReactDOM.render(
	(
		<div style={{
			display: 'flex',
			flexDirection: 'column',
			height: '100%'
		}}>
			<div className='main-header'>
				<img className='logo' src="static/images/logo.png" alt="logo" />
			</div>

			<Login />
		</div>
	)
	, document.getElementById('content')
);
