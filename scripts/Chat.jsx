import * as React from 'react';
import { Socket } from './Socket';

    
export function Chat()
{
    const [message, setMessage] = React.useState('');
    const [messages, setMessages] = React.useState([]);

    function handleSubmit()
    {
        var messageInput = document.getElementById('messageInput');
        var messageText = messageInput.value;

        Socket.emit('message-send', {
            'text': messageText,
        });
        
        // TODO:
        //     socket on messages received -> setMessages(data)
        //     configure the mapping below to work with the messages dict that will be returned by the server


        messageInput.value = '';
    }

    function checkForEnter(event)
    {
        if (event.key === 'Enter')
        {
            handleSubmit();
        }
    }        
    
    return (
        <>
            <div id='chatBox'>
                <ul id='messageFeed'>
                    {messages.map((message, index) => (
                        <li key={index}>
                               <p>{message}</p>
                        </li>
                    ))}
                </ul>
                <input type='text' id='messageInput' placeholder='Message' onKeyPress={checkForEnter}></input>
                <button type='submit' onClick={handleSubmit}>Send</button>
            </div>
        </>
    )
}