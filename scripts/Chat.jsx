import * as React from 'react';
import { Socket } from './Socket';
import './chat.css'


export function Chat()
{
	const [messages, setMessages] = React.useState([]);

	function getNewMessages()
	{
		React.useEffect(() =>
		{
			Socket.on('messages_received', (data) =>
			{
				console.log('Message feed updated.');
				setMessages(data);
                console.log(data);
                
                const messageBox = document.getElementById('chatBox');
                messageBox.scrollTop = messageBox.scrollHeight - messageBox.clientHeight;
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

	function getFbName(message)
	{
		if (message[4] != null)
		{
			return message[4][0];
		}
	}

	function getFbImageUrl(message)
	{
		if (message[4] != null)
		{
			return message[4][1];
		}

	}

	getNewMessages();

	return (
		<>
			<div id='chatBox'>
				<ul id='messageFeed' style={{ paddingLeft: '0' }}>
					{messages.map((message, index) => (
						<li key={index} style={{ listStyleType: 'none', padding: '0', margin: '0' }}>
							<img id='profilePic' alt="Profile" src={getFbImageUrl(message)}></img>
							<span>
                                <p id='timestamp'> ({message[2]}) </p>
                                <p id='name'>{getFbName(message)}: </p>
                                <p id='message'>{message[1]}</p>
								<br />
							</span>
						</li>
					))}
				</ul>
				<input type='text' id='messageInput' placeholder='Message' onKeyPress={checkForEnter}></input>
				<button type='submit' onClick={handleSubmit}>Send</button>
			</div>
		</>
	);
}
