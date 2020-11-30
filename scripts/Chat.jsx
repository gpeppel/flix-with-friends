import * as React from 'react';
import { ChatMessage } from './ChatMessage';
import { Socket } from './Socket';
import './chat.css';


export function Chat()
{
	const [messages, setMessages] = React.useState([]);

	React.useEffect(() =>
	{
		Socket.on('messages_received', (data) =>
		{
			console.log('Message feed updated.');
			setMessages(data);
			console.log(data);

			const messageBox = document.getElementById('chatArea');
			messageBox.scrollTop = messageBox.scrollHeight - messageBox.clientHeight;
			// TODO may have to set message scrollbar to bottom or something later
		});
	}, []);

	function handleSubmit()
	{
		var messageInput = document.getElementById('messageInput');
		var messageText = messageInput.value;

		if(messageText.length > 0)
		{
			Socket.emit('message_send', {
				'text': messageText,
			});
		}
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
		<div id='chatArea'>
			<div id='messageFeed'>
				{
					messages.map((message) => (<ChatMessage key={message.message_id} message={message} />))
				}
			</div>

			<input type='text' id='messageInput' placeholder='Message' onKeyPress={checkForEnter}></input>
			<button type='submit' onClick={handleSubmit}>Send</button>
		</div>
	);
}
