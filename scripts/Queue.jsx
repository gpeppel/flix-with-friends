import * as React from 'react';
import { Socket } from './Socket';

const EVENT_YT_LOAD = 'yt_load';
const EVENT_YT_ENQUEUE = 'yt_enqueue';
const youtubeUrl = require('youtube-url');

export function Queue() {
  function getEmitChannel(event) {
    try {
      const submitId = event.target.getAttribute('id');
      if (submitId === 'watchNow') {
        return EVENT_YT_LOAD;
      } if (submitId === 'enqueue') {
        return EVENT_YT_ENQUEUE;
      }
    } catch (e) {
      if (e.name === 'TypeError') {
        return EVENT_YT_ENQUEUE;
      }
    }
    return EVENT_YT_ENQUEUE;
  }

  function handleSubmit(event) {
    const urlInput = document.getElementById('urlInput');
    const urlText = urlInput.value;

    if (urlText.length > 0) {
      if (youtubeUrl.valid(urlText)) {
        const emitChannel = getEmitChannel(event);
        Socket.emit(emitChannel, {
          url: urlText,
        });

        urlInput.value = '';
      } else {
        urlInput.placeholder = 'Invalid URL!';
        urlInput.value = '';
      }
    }
  }

  function onKeyUp(event) {
    if (event.key === 'Enter') {
      handleSubmit();
    }
  }

  function setPlaceholder() {
    const inputBox = document.getElementById('urlInput');
    inputBox.placeholder = 'Enter YouTube URL';
  }

  return (
    <div className="queue">
      <input id="urlInput" onFocus={setPlaceholder} onBlur={setPlaceholder} onKeyUp={onKeyUp} placeholder="Enter YouTube URL" />
      <button id="watchNow" type="submit" onClick={handleSubmit}>Watch Now</button>
      <button id="enqueue" type="submit" onClick={handleSubmit}>Add to Queue</button>
      <ul>
        <li>
          {' '}
          <p>Queued videos go here</p>
          {' '}
        </li>
      </ul>
    </div>
  );
}
