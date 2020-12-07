import FrameUpdate from './frame-update.js';

export default class KeyListener
{
	constructor()
	{
		this.onKeyDown = undefined;
		this.onKeyUp = undefined;
		this.onUpdate = undefined;

		this.keyLifetime = 750;

		this.frameUpdate = new FrameUpdate(this.onUpdateWrapper.bind(this), FrameUpdate.fps(60));

		this._keysDown = {};
		this.enabled = false;

		window.addEventListener('keydown', (event) =>
		{
			if(!this.enabled)
				return;

			if(this.onKeyDown)
				this.onKeyDown(event);

			if(!this._keysDown[event.key])
				this._keysDown[event.key] = performance.now();
		});

		window.addEventListener('keyup', (event) =>
		{
			if(!this.enabled)
				return;

			if(this.onKeyUp)
				this.onKeyUp(event);

			this._keysDown[event.key] = 0;
		});

		window.addEventListener('blur', () =>
		{
			this._keysDown = {};
		});
	}

	start()
	{
		this.frameUpdate.start();
		this._keysDown = {};
		this.enabled = true;
	}

	stop()
	{
		this.frameUpdate.stop();
		this._keysDown = {};
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
		for (const key in this._keysDown)
		{
			if(this._keysDown[key])
				keys[key] = this._keysDown[key];
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

	getKeyDownTime(key)
	{
		const entry = this._keysDown[key];
		if(!entry)
			return 0;

		return performance.now() - entry;
	}

	isKeyDown(key)
	{
		return !!this._keysDown[key];
	}
}
