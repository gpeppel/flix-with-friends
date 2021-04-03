
import * as React from 'react';
// import './css/header.css';

import { Socket } from './Socket';
import { AwesomeButton } from 'react-awesome-button';

export function Header()
{
    function signout()
    {
        Socket.emit('login_signout', {});
        location.reload();
    }

    return (
        <div className='main-header'>
            <div>
                <img className='logo' src="static/images/logo.png" alt="logo" />
            </div>

			<div>
                <AwesomeButton type="twitter" onPress={(event) => {signout();}}>SIGN OUT</AwesomeButton>
			</div>
        </div>
    );
}
