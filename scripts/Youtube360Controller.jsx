import * as React from 'react';
import PropTypes from 'prop-types';

import KeyListener from './utils/keylistener.js';


const SPEED = 3;

const RESET_TIME = 1500;

export function Youtube360Controller(props)
{
	const player = props.player;

	function wrap(val, minVal, maxVal)
	{
		if(val >= minVal && val <= maxVal)
			return val;
		if(val < minVal)
			return maxVal - (minVal - val);
		return minVal + (val - maxVal);
	}

	//useEffect?

	const keylistener = new KeyListener();
	keylistener.onUpdate = () =>
	{
		if(!player || !player.player)
			return;

		const sphereProp = player.player.getSphericalProperties();

		if(sphereProp === undefined || Object.keys(sphereProp).length == 0)
			return;

		if(keylistener.isKeyDown('a'))
			sphereProp.yaw = wrap(sphereProp.yaw + SPEED, 0, 360);
		if(keylistener.isKeyDown('d'))
			sphereProp.yaw = wrap(sphereProp.yaw - SPEED, 0, 360);
		if(keylistener.isKeyDown('w'))
			sphereProp.pitch = Math.min(90, sphereProp.pitch + SPEED);
		if(keylistener.isKeyDown('s'))
			sphereProp.pitch = Math.max(-90, sphereProp.pitch - SPEED);
		if(keylistener.isKeyDown('q'))
			sphereProp.roll = wrap(sphereProp.roll + SPEED, -180, 180);
		if(keylistener.isKeyDown('e'))
			sphereProp.roll = wrap(sphereProp.roll - SPEED, -180, 180);
		if(keylistener.isKeyDown('z'))
			sphereProp.fov = Math.max(30, sphereProp.fov - SPEED);
		if(keylistener.isKeyDown('x'))
			sphereProp.fov = Math.min(120, sphereProp.fov + SPEED);

		if(keylistener.getKeyDownTime('a') > RESET_TIME && keylistener.getKeyDownTime('d') > RESET_TIME)
			sphereProp.yaw = 0;
		if(keylistener.getKeyDownTime('w') > RESET_TIME && keylistener.getKeyDownTime('s') > RESET_TIME)
			sphereProp.pitch = 0;
		if(keylistener.getKeyDownTime('q') > RESET_TIME && keylistener.getKeyDownTime('e') > RESET_TIME)
			sphereProp.roll = 0;
		if(keylistener.getKeyDownTime('z') > RESET_TIME && keylistener.getKeyDownTime('x') > RESET_TIME)
			sphereProp.fov = 100;

		if(keylistener.getKeyDownTime('r') > RESET_TIME)
		{
			sphereProp.yaw = 0;
			sphereProp.pitch = 0;
			sphereProp.roll = 0;
			sphereProp.fov = 100;
		}

		player.player.setSphericalProperties(sphereProp);
	};

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
			<input id='control360' type='checkbox' onChange={onChange} />
			<label htmlFor='control360'>360 Keyboard Control</label>
		</div>
	);
}

Youtube360Controller.propTypes = {
	player: PropTypes.object
};
