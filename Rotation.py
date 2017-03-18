from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2


def RotatePoint((x,y,z), (cx,cy,cz), theta, phi): # rotate around an arbitrary origin
	# Plot the new point
	dx = x - cx
	dy = y - cy
	d = sqrt(dy**2 + dx**2)
	t = atan2(dy, dx) # tilt around the z axis
	(px,py,pz) = ( cos(t+phi)*d, sin(t+phi)*d, z ) # tilt offset around the z axis
	dz = pz - cz
	dx = px - cx
	d = sqrt(dz**2 + dx**2)
	t = atan2(dz, dx) # tilt around the y axis
	return ( cos(t+theta)*d, py, sin(t+theta)*d ) # tilt offset around the z axis

def UnRotatePoint((x,y,z), (cx,cy,cz), theta, phi): # rotate around an arbitrary origin. Order of operations reversed
	# Plot the new point
	dz = z - cz
	dx = x - cx
	d = sqrt(dz**2 + dx**2)
	t = atan2(dz, dx) # tilt around the y axis
	(px,py,pz) =( cos(t-theta)*d, y, sin(t-theta)*d ) # tilt offset around the z axis

	dx = px - cx
	dy = py - cy
	d = sqrt(dy**2 + dx**2)
	t = atan2(dy, dx) # tilt around the z axis
	return ( cos(t-phi)*d, sin(t-phi)*d, pz ) # tilt offset around the z axis
