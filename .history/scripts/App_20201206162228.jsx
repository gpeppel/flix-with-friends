import * as React from 'react';

import { Login } from './Login';
import { Header } from './Header';
import { Footer } from './Footer';
import { Options } from './Options';


export function App()
{
	return (
		<div>
			<Header />
			<Login />
			<Footer />
		</div>
	);
}
