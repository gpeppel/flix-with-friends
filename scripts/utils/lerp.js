export default class Lerp
{
	static float(a, b, t)
	{
		//return a + (b - a) * t;
		return (1 - t) * a + t * b;
	}

	static floatAngle(a, b, t)
	{
		const theta = b - a;
		if(theta > 180)
		{
			a += 360;
		}
		else if(theta < -180)
		{
			a -= 360;
		}

		return Lerp.float(a, b, t);
	}

	static rotation(aYaw, aPitch, aRoll, bYaw, bPitch, bRoll, t)
	{
		return [Lerp.floatAngle(aYaw, bYaw, t), Lerp.floatAngle(aPitch, bPitch, t), Lerp.floatAngle(aRoll, bRoll, t)];
	}
}
