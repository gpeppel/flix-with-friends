export default class FrameUpdate
{
	constructor(fncUpdate, runDelay)
	{
		this.updateFunction = fncUpdate;
		this.runDelay = runDelay;

		this.running = false;

		if(this.runDelay === undefined)
			this.runDelay = 0;
	}

	start()
	{
		this.running = true;

		let lastTime = 0;
		let timer = 0;

		const update = (timestamp) =>
		{
			const deltaTime = timestamp - lastTime;
			lastTime = timestamp;

			timer += deltaTime;
			if(timer >= this.runDelay)
			{
				this.updateFunction(timestamp, deltaTime);
				timer = 0;
			}

			if(this.running)
				requestAnimationFrame(update);
		};
		requestAnimationFrame(update);
	}

	stop()
	{
		this.running = false;
	}
}
