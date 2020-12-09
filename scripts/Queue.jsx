import { QueuedVideo } from './QueuedVideo';
import * as React from 'react';
import { Socket } from './Socket';
import { UserContext, UserDispatchContext } from './UserProvider';
import { AwesomeButton } from "react-awesome-button";
import './css/theme-eric.css';

const EVENT_YT_LOAD = 'yt_load';
const EVENT_YT_ENQUEUE = 'yt_enqueue';
const youtubeUrl = require('youtube-url');

export function Queue()
{
	const userDetails = React.useContext(UserContext);
	const updateUserDetails = React.useContext(UserDispatchContext);
	const [queue, setQueue] = React.useState([]);

	React.useEffect(() =>
	{
		Socket.on('queue_updated', (data) =>
		{
			console.log('Queue feed updated.');

			console.log(data['videos']);
			setQueue(data['videos']);

			updateUserDetails({
				room: {
					playlist: data
				}
			});
		});
	}, []);

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
			<AwesomeButton
				id="watchNow"
				onPress={handleSubmit}
				type='secondary'
			>
					Watch Now
			</AwesomeButton>
			<AwesomeButton
				id="enqueue"
				onPress={handleSubmit}
				type='secondary'
			>
					Add to Queue
			</AwesomeButton>
			{/* <button id="watchNow" type="submit" onClick={handleSubmit}>Watch Now</button>
			<button id="enqueue" type="submit" onClick={handleSubmit}>Add to Queue</button> */}
			{/* <AwesomeButton
				id="dequeue"
				onPress={deQueue}
				type='secondary'
			>
					Add to Queue
			</AwesomeButton> */}
			{/* <button id="dequeue" type="submit" onClick={deQueue}>Remove from Queue (test button)</button> */}
			<div id='queueFeed'>
				{
					queue.map((queuedVideo) => (<QueuedVideo key={queuedVideo.video_id} queuedVideo={queuedVideo} />))
				}
			</div>
		</div>
	);
}

