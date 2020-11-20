def getval(d, key, default=None):
	d, s = getdict(d, key)
	return d.get(s, default)

def getdict(d, key):
	spl = key.split('.')
	for i in range(0, len(spl) - 1):
		d = d[spl[i]]
	return d, spl[-1]
