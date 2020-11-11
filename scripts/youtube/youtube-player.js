import * as React from 'react';

import YouTube from 'react-youtube';

export default class YoutubePlayer
{
	constructor(videoId, opts, onReady, onStateChange)
	{
		this.videoId = videoId;
		this.opts = opts;
		this.onReady = onReady;
		this.onStateChange = onStateChange;

		this.player = undefined;
	}

	static onReadyWrapper(player, event, onReady)
	{
		player.player = event.target;

		player.player.play = function(t){
			console.log("play", t);

			if(this.getPlayerState() == YoutubePlayer.prototype.PLAYER_PLAYING)
			{
				console.log("play cancel");
				return;
			}

			console.log("play0");
			this.seekTo(t);
			this.playVideo();
			console.log("play1");
		}.bind(player.player);

		player.player.pause = function(t){
			console.log("pause", t);

			if(this.getPlayerState() == YoutubePlayer.prototype.PLAYER_PAUSED)
			{
				console.log("pause cancel");
				return;
			}

			console.log("pause0");
			this.seekTo(t);
			this.pauseVideo();
			console.log("pause1");
		}.bind(player.player);

		onReady(event);
	}

	static createYoutubePlayer(videoId, opts, onReady, onStateChange)
	{
		let player = new YoutubePlayer(videoId, opts, onReady, onStateChange);

		return [
			player,
			(
				<YouTube
					videoId={videoId}
					opts={opts}
					onReady={(event) => {
						YoutubePlayer.onReadyWrapper(player, event, onReady);
					}}
					onStateChange={onStateChange}
				/>
			)
		];
	}

	static playerStateToStr(state)
	{
		return [
			'unstarted', // -1
			'ended',     // 0
			'playing',   // 1
			'paused',    // 2
			'buffering', // 3
			'',
			'cued'       // 5
		][state + 1];
	}

	static isStateContinuation(lastStates, state)
	{
		let len = lastStates.length;
		return lastStates[len - 3] == state && lastStates[len - 1] == state && lastStates[len - 2] == YoutubePlayer.prototype.PLAYER_BUFFERING;
	}
}

YoutubePlayer.prototype.PLAYER_UNSTARTED = -1;
YoutubePlayer.prototype.PLAYER_ENDED = 0;
YoutubePlayer.prototype.PLAYER_PLAYING = 1;
YoutubePlayer.prototype.PLAYER_PAUSED = 2;
YoutubePlayer.prototype.PLAYER_BUFFERING = 3;
YoutubePlayer.prototype.PLAYER_CUED = 5;

YoutubePlayer.prototype.PLAYER_UNSTARTED_STR = 'unstarted';
YoutubePlayer.prototype.PLAYER_ENDED_STR = 'ended';
YoutubePlayer.prototype.PLAYER_PLAYING_STR = 'playing';
YoutubePlayer.prototype.PLAYER_PAUSED_STR = 'paused';
YoutubePlayer.prototype.PLAYER_BUFFERING_STR = 'buffering';
YoutubePlayer.prototype.PLAYER_CUED_STR = 'cued';
