import * as React from 'react';
import PropTypes from 'prop-types';
import './css/youtube360.css';

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
		<div id='control360-container'>
			<div className='option'>
				<input id='control360' type='checkbox' onChange={onChange} />
				<label htmlFor='control360'>Enable 360 Keyboard Control</label>
			</div>

			<p>360 Video Keyboard Controls:</p>

			<div className='desc-container'>
				<div className='col'>
					<div className='control-description'>
						<span className='key'>A</span><span className='desc'>Yaw Left</span>
					</div>
					<div className='control-description'>
						<span className='key'>D</span><span className='desc'>Yaw Right</span>
					</div>
					<div className='control-description'>
						<span className='key'>W</span><span className='desc'>Pitch Up</span>
					</div>
					<div className='control-description'>
						<span className='key'>S</span><span className='desc'>Pitch Down</span>
					</div>
					<div className='control-description'>
						<span className='key'>Q</span><span className='desc'>Roll Left</span>
					</div>
					<div className='control-description'>
						<span className='key'>E</span><span className='desc'>Roll Right</span>
					</div>
				</div>

				<div className='col'>
					<div className='control-description'>
						<span className='key'>Z</span><span className='desc'>Zoom In</span>
					</div>
					<div className='control-description'>
						<span className='key'>X</span><span className='desc'>Zoom Out</span>
					</div>

					<div className='control-description'>
						<span className='key'>R</span><span className='desc'><span className='hold'>(hold)</span> Reset Rotation</span>
					</div>
				</div>
			</div>
		</div>
	);
}

Youtube360Controller.propTypes = {
	player: PropTypes.object
};
