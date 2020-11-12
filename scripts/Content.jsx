import React, { useState, useEffect } from 'react';
import { Button } from './Button';
import { Socket } from './Socket';

export function Content() {
    const [addresses, setAddresses] = useState([]);
    const [roomID, setRoomID] = useState([]);
    
    
    console.log("emitting")
    Socket.emit('new room');
    
    useEffect(() => { Socket.on('new room id', setRoomID); }, []);
    console.log(roomID)
    
    
    function getNewAddresses() {
        React.useEffect(() => {
            Socket.on('addresses received', updateAddresses);
            return () => {
                Socket.off('addresses received', updateAddresses);
            }
        });
    }
    
    
    function copyID() {
      var copyText = document.getElementById("myInput");
      copyText.select();
      document.execCommand("copy");
      console.log('copied text' + copyText.value)
      alert("Copied the text: " + copyText.value);
    }
    
    function updateAddresses(data) {
        console.log("Received addresses from server: " + data['allAddresses']);
        setAddresses(data['allAddresses']);
    }
    
    getNewAddresses();

    return (
        <div>
            <h1>USPS Addresses!</h1>
                <input type="text" value={roomID} id="myInput"/>
                <button onClick={copyID}>Copy text</button>
        </div>
    );
}
