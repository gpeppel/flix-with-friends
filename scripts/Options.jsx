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
        <div className="split left">
        <div className="centered">
            <h1>Hello</h1>
            <FacebookButton />
             <button onClick={handleSubmit}>Create New Viewing Room</button>
            </div>
        </div>
        
        <div className="split right">
           <div className="centered">
            <h1>World</h1>
            <input type="text" placeholder="Enter the room URL"></input>
            <button onClick={handleSubmit}>Enter</button>
            </div>
        </div>
        
        </body>
        )
}