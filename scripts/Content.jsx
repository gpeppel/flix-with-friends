import * as React from 'react';
import { YoutubeContainer } from './YoutubeContainer';

import { Socket } from './Socket';
import { Chat } from './Chat';

const EVENT_YT_LOAD = 'yt-load';

export function Content() {

    const [roomID, setRoomID] = React.useState([]);


    console.log("emitting")
    Socket.emit('new room');

    React.useEffect(() => { Socket.on('new room id', setRoomID); }, []);
    console.log(roomID)


    function copyID() {
      var copyText = document.getElementById("myInput");
      copyText.select();
      document.execCommand("copy");
      console.log('copied text' + copyText.value)
      alert("Copied the text: " + copyText.value);
    }

	function onKeyUp(event)
	{
		if(event.key == "Enter")
		{
			Socket.emit(EVENT_YT_LOAD, {
				'url': event.target.value
			});
		}
	}

	return (
		<div>
			<input onKeyUp={onKeyUp} />
			<YoutubeContainer />
      <Chat />
		</div>
	);
}
