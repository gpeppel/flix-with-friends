
import * as React from 'react';
import { Socket } from './Socket';
import { UserContext } from './UserProvider';

const EVENT_YT_LOAD = 'yt_load';
const EVENT_YT_ENQUEUE = 'yt_enqueue';
const EVENT_YT_DEQUEUE = 'yt_dequeue';
const youtubeUrl = require('youtube-url');

export function Queue()
{
	const userDetails = React.useContext(UserContext);
	function getEmitChannel(event)
	{
		try
		{
			const submitId = event.target.getAttribute('id');
			if (submitId === 'watchNow')
			{
				return EVENT_YT_LOAD;
			} if (submitId === 'enqueue')
			{
				return EVENT_YT_ENQUEUE;
			}
		}
		catch (e)
		{
			if (e.name === 'TypeError')
			{
				return EVENT_YT_ENQUEUE;
			}
		}
		return EVENT_YT_ENQUEUE;
	}

	function handleSubmit(event)
	{
		const urlInput = document.getElementById('urlInput');
		const urlText = urlInput.value;

		if (urlText.length > 0)
		{
			if (youtubeUrl.valid(urlText))
			{
				const roomID = userDetails.room.id;
				console.log(roomID);
				const emitChannel = getEmitChannel(event);
				Socket.emit(emitChannel, {
					url: urlText,
					roomId: roomID
				});

				urlInput.value = '';
			}
			else
			{
				urlInput.placeholder = 'Invalid URL!';
				urlInput.value = '';
			}
		}
	}

	function deQueue()
	{
		const urlInput = document.getElementById('urlInput');
		const urlText = urlInput.value;

		if (urlText.length > 0)
		{
			if (youtubeUrl.valid(urlText))
			{
				const roomID = userDetails.room.id;
				console.log(roomID);
				const emitChannel = EVENT_YT_DEQUEUE;
				Socket.emit(emitChannel, {
					url: urlText,
					roomId: roomID
				});

				urlInput.value = '';
			}
			else
			{
				urlInput.placeholder = 'Invalid URL!';
				urlInput.value = '';
			}
		}
	}

	function onKeyUp(event)
	{
		if (event.key === 'Enter')
		{
			handleSubmit();
		}
	}

	function setPlaceholder()
	{
		const inputBox = document.getElementById('urlInput');
		inputBox.placeholder = 'Enter YouTube URL';
	}

	return (
		<div className="queue">
			<input id="urlInput" onFocus={setPlaceholder} onBlur={setPlaceholder} onKeyUp={onKeyUp} placeholder="Enter YouTube URL" />
			<button id="watchNow" type="submit" onClick={handleSubmit}>Watch Now</button>
			<button id="enqueue" type="submit" onClick={handleSubmit}>Add to Queue</button>
			<button id="dequeue" type="submit" onClick={deQueue}>Remove from Queue (test button)</button>
			<ul>
				<li>
					{' '}
					<p>Queued videos go here</p>
					{ /* TODO possibly sort videos if needed*/ }
					{' '}
				</li>
			</ul>
		</div>
	);
}
