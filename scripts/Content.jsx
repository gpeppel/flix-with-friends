import * as React from 'react';
import { Chat } from './Chat';
import { ActiveUsers } from './ActiveUsers';
import { YoutubeContainer } from './YoutubeContainer';

import { Socket } from './Socket';

import './content.css';

const EVENT_YT_LOAD = 'yt_load';

export function Content() {
  // const [logoutFlag, setLogoutFlag] = React.useState(false);
  const [roomID, setRoomID] = React.useState([]);

  console.log('emitting');
  Socket.emit('new room');

  Socket.emit('chat_loaded');

  React.useEffect(() => {
    Socket.on('new room id', setRoomID);
  }, []);
  console.log(roomID);

  function onKeyUp(event) {
    if (event.key === 'Enter') {
      Socket.emit(EVENT_YT_LOAD, {
        url: event.target.value,
      });
    }
  }

  function logOut() {
    window.FB.logout();
    console.log('Logout called');

    Socket.emit('logout_oauth_facebook', {
    });

    // setLogoutFlag(true);
    // TODO remove user from backend
  }

  // TODO returning <Login /> here requires a circular import, may need to refactor

  return (
    <div className="main-content">
      <div style={{
        display: 'flex',
        flex: 1,
      }}
      >
        <button type="submit" onClick={logOut}>Logout</button>
        <Chat />
        <ActiveUsers />
      </div>
      <div className="media-area">
        <input onKeyUp={onKeyUp} placeholder="Enter YouTube URL" />
        <YoutubeContainer />
      </div>
      <div style={{
        flex: 1,
      }}
      />
    </div>
  );
}
