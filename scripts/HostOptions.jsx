import * as React from 'react';
import { Socket } from './Socket';

import './host-options.css';

export function HostOptions()
{
	React.useEffect(() =>
	{
		const votePercent = document.getElementById('vote-percent-sign');

		votePercent.style.display = 'none';

		Socket.on('room_settings_get', (data) =>
		{

		});
	}, []);

	function onUsePercentage(event)
	{
		const voteThreshold = document.getElementById('vote-threshold');
		const votePercent = document.getElementById('vote-percent-sign');

		if(event.target.checked)
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
		Socket.emit('room_settings_set', getRoomSettings());
	}

	function getRoomSettings()
	{
		const voteThresholdPercentage = document.getElementById('vote-threshold-percentage');
		const voteThreshold = document.getElementById('vote-threshold');

		const settings = {};

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

	return (
		<div id='host-options'>
			<div>
				<div>
					<label htmlFor='vote-threshold'>Vote Threshold: </label>
					<input id='vote-threshold' type='number' min='0'/>
					<span id='vote-percent-sign'>%</span>
				</div>
				<div>
					<input id='vote-threshold-percentage' onChange={onUsePercentage} type='checkbox' />
					<label id='lbl-vote-threshold-percentage' htmlFor='vote-threshold-percentage'>Use Percentage</label>
				</div>
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
