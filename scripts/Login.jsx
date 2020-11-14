import * as React from 'react';
import { Options } from './Options';
import { FacebookButton } from './FacebookButton';
import { Socket } from './Socket';
import './login.css';

export function Login(){
const [userFlag, setFlag] = React.useState(false);
	
	 React.useEffect(() => {
      Socket.on('unverified_user', (data) => {
        setFlag(false);
      });
    });
    
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
        <div className="login">
        <div className="centered">
        
         <img className="fb_button" src="static/images/fb_button.png" alt="fb_button" />
         <FacebookButton />
         
        </div>
        </div>
        
        </body>
	);
}
