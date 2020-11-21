export default class FrameUpdate
{
	constructor(fncUpdate, delayMs)
	{
		this.updateFunction = fncUpdate;
		this.delayMs = delayMs;

		this.running = false;

		if(this.delayMs === undefined)
			this.delayMs = 0;
	}

	start()
	{
		this.running = true;

		let lastTime = 0;
		let timerMs = 0;

		const update = (timestamp) =>
		{
			const deltaTime = timestamp - lastTime;
			lastTime = timestamp;

			timerMs += deltaTime;

			if(timerMs >= this.delayMs)
			{
				this.updateFunction(timestamp, deltaTime);
				timerMs = 0;
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

	static fps(frames)
	{
		return 1000 / frames;
	}
}

FrameUpdate.prototype.FRAMES_PER_SECOND = 60;
FrameUpdate.prototype.MILLISECONDS_PER_FRAME = 1000 / FrameUpdate.prototype.FRAMES_PER_SECOND;
