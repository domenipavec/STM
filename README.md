# STM
Smart thumbnail maker.

Program is primarily meant for making thumbnails, but works well for smart resize to bigger size as well.

## Installation

### Ubuntu

Prerequisites:
- python
- python-setuptools
- python-opencv
- python-numpy

Install prerequisites:
```
sudo apt-get install python python-setuptools python-opencv python-numpy
```

Clone the repository:
```
git clone https://github.com/matematik7/STM.git
```

Install:
```
sudo ./setup.py install
```

### Windows

Install prerequisites:
- [Python](https://www.python.org/downloads/)
- [Numpy](http://sourceforge.net/projects/numpy/files/NumPy/)
- [OpenCV 2](https://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_setup/py_setup_in_windows/py_setup_in_windows.html#install-opencv-python-in-windows)

Download [STM source from github](https://github.com/matematik7/STM).

Install:
```
./setup.py install
```

The stm.exe script is installed in:
```
C:\Python27\Scripts\stm.exe
```

## Usage

To run the program type:
```
stm -i input file(s) or folder(s)
```

### Additional options

```
--help
```
Display full argument options help.

```
--recursive
```
Parse input folders recurively.

```
--verbose
```
Print output thumbnail names.

```
--debug
```
Output debug image for smart resize algorithm.

### Output file options
```
--output FILE
```
Set output file (only when only one input file).

```
--prefix PREFIX
```
Set thumbnail file name prefix.

```
--postfix POSTFIX
```
Set thumbnail file name postfix.

```
--folder FOLDER
```
Set thumbnail target folder (default is "thumb"), can be relative to image location or absolute.

```
--fileFormat FILEFORMAT
```
Thumbnail file format (default is "png"), set to "source" to keep source image format.

### Scaling options

```
--size WIDTHxHEIGHT
```
Thumbnail size (default is 100x100).

```
--scale
```
Use scale algorithm, output image is scaled only to fit into *size*.

```
--crop
```
Use scale and crop to make image exact *size*. Cropping is around image center.

```
--padd
```
Scale image only, but padd to exact *size*.

```
--paddColor B,G,R,A
```
Set padding color.

```
--featured X1xY1,X2xY2
```
Set featured area of image to crop around.

```
--zoominess ZOOMINESS
```
How much to zoom in featured area. 0 means no zoom, 100 means fully zoom to featured area.
Default is 0.

```
--allowPadd
```
Whether padding is allowed if featured area does not fit in thumbnail. Default is padding not allowed.

```
--smart
```
Use edge and face detection to automatically detect featured image area. This is the default mode.

## Running unit tests

```
./setup.py test
```
Note: some tests fail on windows.
