import * as React from 'react';
import { Options } from './Options';
import { FacebookButton } from './FacebookButton';
import { Socket } from './Socket';
import './options.css';

export function Login(){
const [userFlag, setFlag] = React.useState(false);

	function authUser() {
    React.useEffect(() => {
      Socket.on('verified_user', (data) => {
        setFlag(true);
      });
    });
  }

	authUser();
    
	
	if (userFlag) {
    return (<Options />);
  }
  
	return (
		<body>
        <div className="header">
        <img src="static/images/logo.png" alt="logo" />
        </div>
        <div>
        
         <img className="fb_button" src="static/images/fb_button.png" alt="fb_button" />
         <FacebookButton />
         
        
        </div>
        
        </body>
	);
}
