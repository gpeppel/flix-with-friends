import FrameUpdate from './frame-update.js';

export default class KeyListener
{
	constructor(onKeyDown, onKeyUp, onUpdate)
	{
		this.onKeyDown = onKeyDown;
		this.onKeyUp = onKeyUp;
		this.onUpdate = onUpdate;

		this.keysDown = {};
		this.frameUpdate = new FrameUpdate(this.onUpdateWrapper.bind(this), FrameUpdate.fps(60));

		this.enabled = false;

		window.addEventListener('keydown', (event) =>
		{
			if(!this.enabled)
				return;

			if(this.onKeyDown)
				this.onKeyDown(event);

			this.keysDown[event.key] = performance.now();
		});

		window.addEventListener('keyup', (event) =>
		{
			if(!this.enabled)
				return;

			if(this.onKeyUp)
				this.onKeyUp(event);

			this.keysDown[event.key] = 0;
		});
	}

	start()
	{
		this.frameUpdate.start();
		this.keysDown = {};
		this.enabled = true;
	}

	stop()
	{
		this.frameUpdate.stop();
		this.keysDown = {};
		this.enabled = false;
	}

	onUpdateWrapper()
	{
		if(this.onUpdate)
			this.onUpdate();
	}

	getKeysDown()
	{
		const keys = {};
		for (const key in this.keysDown)
		{
			if(this.keysDown[key])
				keys[key] = this.keysDown[key];
		}

		return keys;
	}

	getKeysDownList()
	{
		return Object.keys(this.getKeysDown());
	}

	getKeysDownOrdered()
	{
		return Object.entries(this.getKeysDown()).sort((a, b) => a[1] - b[1]).map((x) => x[0]);
	}

	isKeyDown(key)
	{
		return !!this.keysDown[key];
	}
}
