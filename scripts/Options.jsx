import React, { useState } from 'react';
import { Content } from './Content';
import './options.css';
import { Socket } from './Socket';
import { FacebookButton } from './FacebookButton';


export function Options() {
    const [userFlag, setFlag] = useState(false);
    
    function handleSubmit(event) {
        
        setFlag(true);
        event.preventDefault();
    }
    
  
  if (userFlag) {
    return (<Content />);
  }
  
    return (
        <body>
        <div className="header">
        <img src="static/images/logo.png" alt="logo" />
        </div>
        <div className="split left">
         <div className="centered">
         <img className="fb_button" src="static/images/fb_button.png" alt="fb_button" />
         <FacebookButton />
         </div>
        </div>
        <div className="split right">
        <div className="centered">
        <img className="popcorn_button" src="static/images/popcorn_button.png" alt="popcorn_button" />
           
        <button className="button" onClick={handleSubmit}>Create New Viewing Room!</button>
            </div>
            </div>
        </body>
        )
}
