import * as React from 'react';
import PropTypes from 'prop-types';

import FrameUpdate from './youtube/frame-update.js';


const SPEED = 4;

export function Youtube360Controller(props)
{
	const player = props.player;

	const keysDown = {};

	//useEffect?

	const keylistener = new FrameUpdate(() =>
	{
		const sphereProp = player.player.getSphericalProperties();

		if(sphereProp === undefined || Object.keys(sphereProp).length == 0)
			return;

		if(keysDown['a'])
			sphereProp.yaw += SPEED;
		if(keysDown['d'])
			sphereProp.yaw -= SPEED;
		if(keysDown['w'])
			sphereProp.pitch += SPEED;
		if(keysDown['s'])
			sphereProp.pitch -= SPEED;
		if(keysDown['q'])
			sphereProp.roll += SPEED;
		if(keysDown['e'])
			sphereProp.roll -= SPEED;

		player.player.setSphericalProperties(sphereProp);
	}, FrameUpdate.fps(60));

	window.addEventListener('keydown', (event) =>
	{
		keysDown[event.key] = performance.now();
	});

	window.addEventListener('keyup', (event) =>
	{
		keysDown[event.key] = 0;
	});

	function onChange(event)
	{
		if(event.target.checked)
		{
			keylistener.start();
		}
		else
		{
			keylistener.stop();
		}
	}

	return (
		<div>
			<input type='checkbox' onChange={onChange} />
			<label>360 Keyboard Control</label>
		</div>
	);
}

Youtube360Controller.propTypes = {
	player: PropTypes.object
};
