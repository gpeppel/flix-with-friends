import * as React from 'react';
import { Socket } from './Socket';


export function Chat()
{
    const [messages, setMessages] = React.useState([]);

    function getNewMessages() {
        React.useEffect(() => {
            Socket.on('messages_received', (data) => {
                console.log('EMIT RECEIVED!');
                console.log(data);
                setMessages(data);

                // TODO may have to set message scrollbar to bottom or something later
            });
        });

    }

    function handleSubmit()
    {
        var messageInput = document.getElementById('messageInput');
        var messageText = messageInput.value;

        Socket.emit('message_send', {
            'text': messageText,
        });
        messageInput.value = '';
    }

    function checkForEnter(event)
    {
        if (event.key === 'Enter')
        {
            handleSubmit();
        }
    }

    getNewMessages();

    return (
        <>
            <div id='chatBox'>
                <ul id='messageFeed' style={{ paddingLeft: "0" }}>
                    {messages.map((message, index) => (
                        <li key={index} style={{ listStyleType: "none", padding: '0', margin: '0' }}>
                               <p>userId: {message[3]}<br></br>message: {message[1]}</p>
                        </li>
                    ))}
                </ul>
                <input type='text' id='messageInput' placeholder='Message' onKeyPress={checkForEnter}></input>
                <button type='submit' onClick={handleSubmit}>Send</button>
            </div>
        </>
    )
}
