from geometry.sphere import make_sphere
from geometry.prism import make_prism


def make_spherinder(radius=1.0, n_lat=10, n_lon=12, interpolation=0, half_height=1.0):
  """Generate a spherinder (sphere × line segment) by extruding a sphere.

  A spherinder is the Cartesian product of a 2-sphere and a line segment.
  It consists of two spherical caps (at w = ±half_height) connected by
  a cylindrical lateral surface.

  Args:
    radius: radius of the sphere cross-section
    n_lat: latitude resolution of the sphere mesh
    n_lon: longitude resolution of the sphere mesh
    interpolation: [0,1], 0 for angle interpolation, 1 for axis distance interpolation
    half_height: half the extension along the W axis

  Returns a Shape4D.
  """
  sphere = make_sphere(radius=radius, n_lat=n_lat, n_lon=n_lon, interpolation=interpolation)
  return make_prism(sphere, half_height=half_height)
