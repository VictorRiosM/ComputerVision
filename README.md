# ComputerVision


This repository is focused on computer vision projects.

##Edge detection
The first work is an edge detector. The edgedetector.py file contains the code for such work. I have included a folder with images that have been used with the edge detector.

##Shape detection
The second work is a shapes detector. shapesdetector.py is the script that detects shapes.

The script receives two parameters: the input image and the output image. If the arguments are not given the script displays a window to select the input image.

The output:
- All the shapes and the background are randomly colored.
- Each shape has its own bounding box. The color of the box is the same of the shape.
- The white lines are the borders of a shape.
- A yellow point indicates the bounding box center.
- A black point indicates the mass center. Note: the yellow points can overwrite the black points.
- The script yields the image space percentage used by each shape and the background.

The folder 'Shapesdetection' contains some images in which the script has been used.

##Line detection
The third work detects lines in images.
The folder Linedetection contains some examples.