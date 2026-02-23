import numpy as np


def orthographic(vertices):
  """Project 4D vertices to 3D by dropping the W coordinate.

  This is the simplest projection: just ignore the 4th dimension.
  Equivalent to viewing the 4D object from infinitely far along the W axis.

  Args:
    vertices: (N, 4) array of 4D positions

  Returns:
    (N, 3) array of 3D positions (the XYZ components)
  """
  return vertices[:, :3]


def perspective(vertices, camera_distance=3.0):
  """Project 4D vertices to 3D with perspective foreshortening along W.

  Points with smaller W appear smaller (further away in 4D), just like
  how 3D perspective projection makes distant objects appear smaller.

  The formula divides each XYZ coordinate by (camera_distance - w),
  so objects at w=0 are at their natural size, objects with positive w
  are closer to the 4D "camera" and appear larger, and objects with
  negative w appear smaller.

  Args:
    vertices: (N, 4) array of 4D positions
    camera_distance: distance of the 4D camera along the W axis.
                     Must be greater than the largest W value in the
                     vertices to avoid division by zero or negative.

  Returns:
    (N, 3) array of 3D positions
  """
  w = vertices[:, 3]
  scale = camera_distance - w  # (N,) array, one scale factor per vertex
  xyz = vertices[:, :3] / scale[:, np.newaxis]
  return xyz
