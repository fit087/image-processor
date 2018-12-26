# Image Processing Project

Image Processing currently presents 2 filters (RGB split and Blur) to apply over RGB images. 

Image Processing was entirely writen in Python 3.5, using an a object-oriented aprouch making use of the imaging library Pillow, and numpy library.




## Key Features

* The list of available filters take into account the image type (e.g.: if the input image is a single channel 8-bit pixel image, RGB split should not be listed in filter options).
* The code was developed for other developers to make new filters available.

Available features:

1. Blur

2. RGB Split

## How To Use

```bash
$ python main.py image.jpg

This is an Image App

Selected Filter: Blur
Type the Blur radius: 4 # User Input
Type the Blur weight: 1 # User Input
```

## Contribute


Contribution can be made implementing new filters, in order to do that a new class has to be created, it must inherites the Filter class.

 The Filter class has a apply_filter() method which must be overwritten within of the new filter class with the filter implementation itself. The filter class also has a protected method called _save() to help to save the images modificated. If needed can be created private methods pre add two undescore (__) at the beginning of the method's name. 

In addition, it is required to add a instance of the new filter within the dictionary filters in the constructor method of any image type class that that filter can be applied.


