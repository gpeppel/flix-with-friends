import * as React from 'react';
import { Chat } from './Chat';
import { YoutubeContainer } from './YoutubeContainer';
import { Queue } from './Queue';

import { Socket } from './Socket';

import './css/content.css';

export function Content() {
  const [roomID, setRoomID] = React.useState([]);

  console.log('emitting');
  Socket.emit('new room');

  Socket.emit('chat_loaded');

  React.useEffect(() => {
    Socket.on('new room id', setRoomID);
  }, []);
  console.log(roomID);

  return (
    <div className="main-content">
      <div style={{
        display: 'flex',
        flex: 1,
      }}
      >
        <Chat />
      </div>
      <div className="media-area">
        <YoutubeContainer />
        <Queue />
      </div>
      <div style={{
        flex: 1,
      }}
      />
    </div>
  );
}
