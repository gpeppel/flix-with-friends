
import * as React from 'react';
// import './css/header.css';

import { Socket } from './Socket';
import { AwesomeButton } from 'react-awesome-button';
import { UserContext } from './UserProvider';

export function Header()
{
    const userDetails = React.useContext(UserContext);

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
			    {(() => {
			        if(userDetails.id !== undefined)
			        {
			            return (
			                <AwesomeButton type="twitter" onPress={(event) => {signout();}}>SIGN OUT</AwesomeButton>
			            );
			        }
			    })()}
			</div>
        </div>
    );
}
