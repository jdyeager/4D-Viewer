# 4D Object Viewer — Development Plan

## Context
Build a desktop Python application for visualizing and interacting with 4D objects (polytopes and curved shapes) to develop geometric intuition. The user is experienced with Python and math, new to graphics programming. Development proceeds incrementally with visual verification at each step.

**Stack**: Python + NumPy + Pygame + PyOpenGL
**Test bench shapes**: Tesseract, Pentachoron (5-cell), Hypersphere, Spherinder (sphere × line)

---

## Development Sequence

### Phase 1: Math Foundation (no rendering yet)
**Goal**: Get the 4D math right with unit tests before any visuals.

1. **4D geometry data structures**
   - `Shape4D` base class: vertices (Nx4 NumPy array), edges (pairs of vertex indices), faces (triples/quads of vertex indices)
   - Tesseract generator: 16 vertices at (±1,±1,±1,±1), derive edges/faces programmatically
   - Pentachoron generator: 5 vertices of the regular 5-cell, derive edges/faces

2. **4D transformation matrices (4×4)**
   - 6 rotation planes: XY, XZ, XW, YZ, YW, ZW
   - Each is a 4×4 rotation matrix parameterized by angle θ
   - Composition of rotations

3. **4D → 3D projection**
   - Orthographic: drop the W coordinate (or project along an arbitrary axis)
   - Perspective: divide XYZ by (d - W) for camera distance d

4. **Unit tests**: verify rotation matrices are orthogonal, projections of known shapes match expected results

### Phase 2: Static Wireframe Rendering
### Phase 3: 3D Camera Controls
### Phase 4: 4D Rotation (Interactive)
### Phase 5: All Test Bench Shapes (Pentachoron, Hypersphere, Spherinder)
### Phase 6: Solid Rendering with Transparency
### Phase 7: Hyperplane Slicing
### Phase 8: Polish

See the full plan in the Claude plans directory for complete details on phases 2-8.

---

## File Structure
```
4d-viewer/
├── main.py              # Entry point, Pygame loop, input handling
├── geometry/
│   ├── __init__.py
│   ├── base.py          # Shape4D base class
│   ├── tesseract.py     # Tesseract generator
│   ├── pentachoron.py   # 5-cell generator
│   ├── hypersphere.py   # Hypersphere mesh generator
│   └── spherinder.py    # Spherinder mesh generator
├── math4d/
│   ├── __init__.py
│   ├── rotations.py     # 4D rotation matrices
│   ├── projections.py   # 4D→3D projection functions
│   └── slicing.py       # Hyperplane slicing
├── renderer/
│   ├── __init__.py
│   ├── window.py        # Pygame/OpenGL window setup
│   ├── camera.py        # 3D camera (arcball)
│   ├── wireframe.py     # Wireframe renderer
│   ├── solid.py         # Solid face renderer
│   └── hud.py           # On-screen text/HUD
└── tests/
    ├── test_rotations.py
    ├── test_projections.py
    ├── test_shapes.py
    └── test_slicing.py
```
