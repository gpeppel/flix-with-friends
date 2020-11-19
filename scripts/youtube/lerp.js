export default class Lerp
{
	static float(a, b, t)
	{
		return a + (b - a) * t;
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

		return a + (b - a) * t;
	}

	static rotation(aYaw, aPitch, aRoll, bYaw, bPitch, bRoll, t)
	{
		return [Lerp.floatAngle(aYaw, bYaw, t), Lerp.floatAngle(aPitch, bPitch, t), Lerp.floatAngle(aRoll, bRoll, t)];
	}
}
