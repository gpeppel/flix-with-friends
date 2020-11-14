import React, { useState } from 'react';
import { Content } from './Content';
import './options.css';
import { Socket } from './Socket';
import { FacebookButton } from './FacebookButton';


export function Options() {
    const [userFlag, setFlag] = useState(false);
    
    function handleSubmit(event) {
        document.body.style.backgroundColor = "#00c9c8";
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
        <div className="centered">
        <img className="popcorn_button" src="static/images/popcorn_button.png" alt="popcorn_button" />
           
        <button className="button" onClick={handleSubmit}>Enter viewing room!</button>
        </div>
        
        </body>
        )
}
