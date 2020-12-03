import * as React from 'react';
import { Socket } from './Socket';

import './host-options.css';

export function HostOptions()
{
	React.useEffect(() =>
	{
		const voteThreshold = document.getElementById('vote-threshold');
		const votePercent = document.getElementById('vote-percent-sign');
		const voteDisabled = document.getElementById('vote-disabled');

		votePercent.style.display = 'none';
		voteDisabled.style.display = voteThreshold.value === '0' ? '' : 'none';

		Socket.on('room_settings_get', (data) =>
		{
			setRoomSettings(data);
		});
	}, []);

	function onVoteThresholdChange(event)
	{
		updateVoteThresholdChange(event.target.value);
	}

	function updateVoteThresholdChange(value)
	{
		const voteThreshold = document.getElementById('vote-threshold');
		const voteThresholdPercentage = document.getElementById('vote-threshold-percentage');

		voteThreshold.value = value;
		if(voteThresholdPercentage)
			voteThreshold.value = Math.min(100, voteThreshold.value);

		const voteDisabled = document.getElementById('vote-disabled');
		voteDisabled.style.display = value === '0' ? '' : 'none';
	}

	function onUsePercentage(event)
	{
		updateUsePercentage(event.target.checked);
	}

	function updateUsePercentage(enabled)
	{
		const voteThreshold = document.getElementById('vote-threshold');
		const voteThresholdPercentage = document.getElementById('vote-threshold-percentage');
		const votePercent = document.getElementById('vote-percent-sign');

		voteThresholdPercentage.checked = enabled;

		if(enabled)
		{
			voteThreshold.max = 100;
			voteThreshold.value = Math.min(100, voteThreshold.value);
			votePercent.style.display = '';
		}
		else
		{
			voteThreshold.max = undefined;
			votePercent.style.display = 'none';
		}
	}

	function onSaveChanges()
	{
		Socket.emit('room_settings_set', getRoomSettings(), (data) =>
		{
			if(data.status != 'ok')
				alert('Error: failed to save room changes. ' + data.error);
		});
	}

	function getRoomSettings()
	{
		const voteThresholdPercentage = document.getElementById('vote-threshold-percentage');
		const voteThreshold = document.getElementById('vote-threshold');

		const usersAddVideo = document.getElementById('users-add-video');

		const settings = {
			usersAddVideoEnabled: usersAddVideo.checked
		};

		try
		{
			settings.voteThreshold = parseFloat(
				voteThresholdPercentage.checked ? voteThreshold.value / 100 : voteThreshold.value,
			);
		}
		catch(e)
		{
			/* eslint-disable no-empty */
		}

		console.log(settings);
		return settings;
	}

	function setRoomSettings(settings)
	{
		console.log(settings);

		if(settings.vote_threshold !== undefined)
		{
			if(settings.vote_threshold >= 1)
			{
				updateVoteThresholdChange(settings.vote_threshold);
			}
			else
			{
				updateVoteThresholdChange(Math.floor(settings.vote_threshold * 100));
			}

			updateUsePercentage(!(settings.vote_threshold >= 1));
		}

		if(settings.users_add_video_enabled)
		{
			const usersAddVideo = document.getElementById('users-add-video');
			usersAddVideo.checked = settings.users_add_video_enabled;
		}
	}

	return (
		<div id='host-options'>
			<p className='host-title'>Host Options</p>
			<div>
				<div className='option'>
					<label htmlFor='vote-threshold'>Vote Threshold: </label>
					<input id='vote-threshold' type='number' min='0' onChange={onVoteThresholdChange}/>
					<span id='vote-percent-sign'>%</span>
					<span id='vote-disabled'>(disabled)</span>
				</div>
				<div className='option'>
					<input id='vote-threshold-percentage' onChange={onUsePercentage} type='checkbox' />
					<label id='lbl-vote-threshold-percentage' htmlFor='vote-threshold-percentage'>Use Percentage</label>
				</div>
			</div>

			<div className='option'>
				<input id='users-add-video' type='checkbox' />
				<label htmlFor='users-add-video'>Can Other Users Add Videos?</label>
			</div>

			<div style={{
				display: 'flex'
			}}>
				<button style={{
					margin: 'auto'
				}} onClick={onSaveChanges}>Save Changes</button>
			</div>
		</div>
	);
}
