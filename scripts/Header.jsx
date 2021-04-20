
import * as React from 'react';
// import './css/header.css';

import { Socket } from './Socket';
import { AwesomeButton } from 'react-awesome-button';
import { UserContext, debugElement } from './UserProvider';

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
                { debugElement(userDetails) }
            </div>

			<div>
			    {(() => {
			        if(userDetails.id !== undefined)
			        {
			            return (
			                <AwesomeButton size="small" type="facebook" onPress={(event) => {signout();}}>SIGN OUT</AwesomeButton>
			            );
			        }
			    })()}
			</div>
        </div>
    );
}
