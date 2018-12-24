#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  3 17:55:36 2018

Add a new functionality to the program developed in the previous task to apply
 a blur filter to a given image. The functionality should be executable via
 command line
 
 The blur algorithm

The blur filter creates a new image where the color of each pixel is the
average color value of its surrounding pixels in the original image
(including itself, i.e., pixels inside the image will take the average of 9 
values).
 
@author: adolfo.correa.lopez@gmail.com
"""

from PIL import Image
from numpy import array
from numpy import int64

def main(argv):
  try:
      img = Image.open(argv[1])
      
  except IOError:
      print ("Could not read file: {}".format(argv[1]) )
      return 1

  
  fn, fext = argv[1].split(sep='.')
#  filename = argv[1].split(sep='.')
#  print('filename = '.format(filename))
#  fext = filename[-1]
#  print('fext = '.format(fext))
#  fn = argv[1][:len(filename)-len(fext)-3]
#  '.'.join(filename[:-1])
  
  if argv[0]=='-rgb':
      splitted = rgb_split_filter(img,fn,fext)
      save_rgb(splitted[0], splitted[1], splitted[2], fn, fext)
      
  elif argv[0]=='-blur':
      radius = int(argv[2])
      weight = int(argv[3])
      blur_filter(img,radius, weight, fn,fext)
  else:
      print ('{} isn\'t an available option'.format(argv[0]))
      
      
  
# RGB Function
def rgb_split_filter(img,fn,fext):
    """
    Take only one channel of the RGB color spectrum
    """
  
#  if argv[0]=='-rgb':
    
    img_red = img.copy()
    img_green = img.copy()
    img_blue = img.copy()
    width, height = img.size
    
    for x in range(width):
        for y in range(height):
          
              r, g, b = img.getpixel((x, y))
            
              img_red.putpixel((x, y), (r, 0, 0))
              img_green.putpixel((x, y), (0, g, 0))
              img_blue.putpixel((x, y), (0, 0, b))
              
    return (img_red,img_green,img_blue)
    
#    img_red.save('{}-split-red.{}'.format(fn,fext))
#    img_green.save('{}-split-green.{}'.format(fn,fext))
#    img_blue.save('{}-split-blue.{}'.format(fn,fext))
    
#    return 0
    
def save_rgb(img_red,img_green, img_blue, fn,fext):
    img_red.save('{}-split-red.{}'.format(fn,fext), mode = 'P')
    img_green.save('{}-split-green.{}'.format(fn,fext), mode = 'P')
    img_blue.save('{}-split-blue.{}'.format(fn,fext), mode = 'P')
    return 0
    
    

# Blur Function
def blur_filter(img,radius, weight, fn,fext):
             
    img_blur = img.copy()
    
    width, height = img.size
    
    rgb = array((0,0,0))
    
    pix_count = int(0)

    for x in range(width):
      
      for y in range(height):
        
        pix_count = 0
        
        # Blur Pane
        for xiradius in range(-radius,radius+1):
          for yiradius in range(-radius,radius+1):
            if x + xiradius >= 0 and x + xiradius < width:
              if y + yiradius >= 0 and y + yiradius < height:
                pix_count += int(1)
                if xiradius != 0 or yiradius !=0:
                  rgb += array(img.getpixel((x+xiradius, y+yiradius)))
                else:
                  rgb += weight*array(img.getpixel((x+xiradius, y+yiradius)))
                
        rgb = rgb/denominator(pix_count,weight)
          
        rgb = rgb.round()
        rgb = rgb.astype(int64)
          
        blur_color = tuple(rgb)
          
        img_blur.putpixel((x, y), blur_color)

    img_blur.save('{0}-blur-radius{2}-weight{3}.{1}'.format(fn,fext,radius,weight))
    
    return 0
  
def denominator(pix_count,weight):
  return int(pix_count - 1 + weight)

if __name__ == "__main__":
    import sys
    main(sys.argv[1:])
#   main(('-blur', 'test-image.png', '2', '1'))
#   main(('-blur', 'test-image.png', '1', '8'))
#   main(('-blur', 'test-image.png', '5', '1'))
#   main(('-blur', 'test-image.png', '5', '100'))
#   main(('-rgb', 'test-image.png'))
    
