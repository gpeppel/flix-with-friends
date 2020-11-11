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
		
		this.reactComponent = this.getReactComponent();
		this.player = undefined;
	}
	
	onReadyWrapper(event)
	{
		console.log(event);
		return;
		
		if(this.player === undefined)
		{
			console.log(this);
			console.log(event);
			this.player = event.target;
			/*
			this.player.play = function(t){
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
			}.bind(this.player);

			this.player.pause = function(t){
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
			}.bind(this.player);
			*/
		}
		
		this.onReady.bind(event.target);
	}
	
	getReactComponent()
	{
		return (
			<YouTube
				videoId={this.videoId}
				opts={this.opts}
				onReady={this.onReadyWrapper}
				onStateChange={this.onStateChange}
			/>	
		);
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