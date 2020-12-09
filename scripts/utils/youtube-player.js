import * as React from 'react';

import YouTube from 'react-youtube';

export default class YoutubePlayer
{
	constructor(videoId, opts, onReady, onStateChange, onPlaybackRateChange)
	{
		this.videoId = videoId;
		this.opts = opts;
		this.onReady = onReady;
		this.onStateChange = onStateChange;
		this.onPlaybackRateChange = onPlaybackRateChange;

		this.onFirstPlay = undefined;
		this.hasPlayed = false;

		this.player = undefined;

		this._loadCallback = undefined;
	}

	loadVideoById(videoId, callback)
	{
		this.player.loadVideoById(videoId);
		this._loadCallback = callback;
	}

	isVideoFinished()
	{
		return this.player.getCurrentTime() == this.player.getDuration();
	}

	isPlayerInState(state)
	{
		return this.player.getPlayerState() == state;
	}

	static checkSyncIgnore(player, t)
	{
		return Math.abs(t - player.getCurrentTime()) < YoutubePlayer.prototype.SYNC_IGNORE_SEC;
	}

	static onReadyWrapper(player, event)
	{
		player.player = event.target;

		player.player.play = function(t)
		{
			if(
				this.isPlayerInState(YoutubePlayer.prototype.PLAYER_PLAYING)
				&& YoutubePlayer.checkSyncIgnore(this.player, t)
			)
			{
				return;
			}

			this.player.seekTo(t);
			this.player.playVideo();
		}.bind(player);

		player.player.pause = function(t)
		{
			if(
				this.isPlayerInState(YoutubePlayer.prototype.PLAYER_PAUSED)
				&& YoutubePlayer.checkSyncIgnore(this.player, t)
			)
			{
				return;
			}

			this.player.seekTo(t);
			this.player.pauseVideo();
		}.bind(player);

		player.player.setPlayback = function(t, s)
		{
			if(this.player.getPlaybackRate() == s && YoutubePlayer.checkSyncIgnore(this.player, t))
			{
				return;
			}

			this.player.seekTo(t);
			this.player.setPlaybackRate(s);
		}.bind(player);

		player.onReady(event);
	}

	static onStateChangeWrapper(player, event)
	{
		if(player._loadCallback && event.data != YoutubePlayer.prototype.PLAYER_UNSTARTED)
		{
			player.hasPlayed = false;
			player._loadCallback(event);
			player._loadCallback = undefined;
		}

		if(!player.hasPlayed && event.data == YoutubePlayer.prototype.PLAYER_PLAYING)
		{
			if(player.onFirstPlay)
				player.onFirstPlay(event);
			player.hasPlayed = true;
		}

		player.onStateChange(event);
	}

	static createYoutubePlayer(videoId, opts, onReady, onStateChange, onPlaybackRateChange)
	{
		const player = new YoutubePlayer(videoId, opts, onReady, onStateChange, onPlaybackRateChange);

		return [
			player,
			(
				<YouTube
					key='yt-player'
					videoId={player.videoId}
					opts={player.opts}
					onReady={(event) =>
					{
						YoutubePlayer.onReadyWrapper(player, event);
					}}
					onStateChange={(event) =>
					{
						YoutubePlayer.onStateChangeWrapper(player, event);
					}}
					onPlaybackRateChange={player.onPlaybackRateChange}
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
}

YoutubePlayer.prototype.SYNC_IGNORE_SEC = 1;

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

YoutubePlayer.prototype.PLAYER_READY_STR = 'ready';
YoutubePlayer.prototype.PLAYER_PLAYBACK_STR = 'playback';
