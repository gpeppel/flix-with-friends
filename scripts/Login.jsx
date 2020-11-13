import * as React from 'react';

import { FacebookButton } from './FacebookButton';
import { Socket } from './Socket';

export function Content()
{
	// function getNewUser() {
	//     React.useEffect(() => {
	//         Socket.on('user_received', updateAddresses);
	//         return () => {
	//             Socket.off('addresses received', updateAddresses);
	//         }
	//     });
	// }

	// function updateAddresses(data) {
	//     console.log("Received addresses from server: " + data['allAddresses']);
	//     setAddresses(data['allAddresses']);
	// }

	// getNewAddresses();

	return (
		<div>
			<h1>Facebook Button Test!</h1>
			<FacebookButton />
		</div>
	);
}
