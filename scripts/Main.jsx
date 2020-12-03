
import * as React from 'react';
import * as ReactDOM from 'react-dom';

import { Login } from './Login';
import { Header } from './Header';
import { Footer } from './Footer';

ReactDOM.render(
	(
		<div>
			<Header />
			<Login  />
			<Footer />
		</div>
	)
	, document.getElementById('content')
);
