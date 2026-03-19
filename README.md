# 4D-Viewer

## Git Incantation Notes

(I can never remember my git incantations,
so I'm saving them here.)

Commands for future reference:
* list branches: `git branch`
* make + switch to new branch: `git checkout -b BRANCHNAME`
* switch to branch `git checkout BRANCHNAME`
* make remote branch and push: `git push -u origin BRANCHNAME`
* delete local branch: `git branch -d BRANCHNAME`

## Ultimate TODOs

Some things to do in the future.

Some things to consider in the future.

### Normalise rotation speed.

### Focused Rotation

Sometimes the rotation speed is a little fast for fine adjustments,
maybe a "hold shift to rotate slower" type of thing would work.

### More Shapes

There in no shortage of shapes to consider in the fullness of time.
Some to consider:
* Remaining platonic polychora
  * Hexadecachoron (16-cell)
  * Icositetrachoron (24-cell)
  * Hexacosichoron (600-cell)
  * Hecatonicosachoron (120-cell)
* Duo-cylinder
* Prisms for Platonic solids
* Hyper-cone

### Refactoring

Refactoring Shapes:
* Tesseract -> Cubic Prism
* `make_cone()`
* Pentachoron -> Tetrahedral Pyramid

### Projection toggling

Want to be able to set the 3D -> 2D projection to swap
between orthogonal and prospective.

### W-depth colouring?

### Ray Tracing?

In order to truly see spherinders and duo-cylinders and other curved shapes,
maybe some ray-tracing mode of the move.
