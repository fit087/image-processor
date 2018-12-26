# -*- coding: utf-8 -*-
"""
Created on Thu Dec 20 23:49:13 2018

@author: adolfo
"""
from PIL import Image
from numpy import array
from numpy import int64
# import Filter
# from Filter import Filter


class Filter:
    def __init__(self,img,path):
        self.img = img
        self.img_out = []
        self.path = path
        # self.fn = fn
        # self.fext = fext

    def apply_filter(): pass
    def set_parameters(parameters_list): pass
    @staticmethod
    def parameters_needed(): pass

    def _save(self,filename,fields):
        for img,fn in zip(self.img_out,filename):
            img.save(fn.format(*fields))
        return 0

    def _filename_separator(self):
        (fn, fext) = self.path.split(sep='.')
        return (fn, fext)

class Blur(Filter):

    def apply_filter(self):
        """Get the result of apply a blur filter to a given image

        Parameters
        ----------
        img : ImageType
            It's a ImageType object


        Returns
        -------
        
        

        """

        blur = self.__blur_filter()

        self.img_out.append(blur)
        
        print('Blur filter applied')

        return blur

    def set_parameters(self,parameters_list):
        self.radius, self.weight = parameters_list

    @staticmethod
    def parameters_needed():
        return ('radius','weight')

    def save(self):
        filename = '{0}-blur-radius{1}-weight{2}.{3}' 
        fn, fext = self._filename_separator()
        fields = (fn,self.radius,self.weight,fext)
        return self._save(filename,fields)

    # Blur Function
    def __blur_filter(self):
                 
        img_blur = self.img.copy()
        
        width, height = self.img.size
        
        rgb = array((0,0,0))
        
        pix_count = int(0)
    
        for x in range(width):
          
          for y in range(height):
            
            pix_count = 0
            
            # Blur Pane
            for xiradius in range(-self.radius,self.radius+1):
              for yiradius in range(-self.radius,self.radius+1):
                if x + xiradius >= 0 and x + xiradius < width:
                  if y + yiradius >= 0 and y + yiradius < height:
                    pix_count += int(1)
                    if xiradius != 0 or yiradius !=0:
                      rgb += array(self.img.getpixel((x+xiradius, y+yiradius)))
                    else:
                      rgb += self.weight*array(self.img.getpixel((x+xiradius, y+yiradius)))
                    
            rgb = rgb/self.__denominator(pix_count,self.weight)
              
            rgb = rgb.round()
            rgb = rgb.astype(int64)
              
            blur_color = tuple(rgb)
              
            img_blur.putpixel((x, y), blur_color)
    
        # img_blur.save('{0}-blur-radius{2}-weight{3}.{1}'.format(fn,fext,radius,weight))
        
        return img_blur

    @staticmethod
    def __denominator(pix_count,weight):
      return int(pix_count - 1 + weight)

class RGB_split(Filter):


    def apply_filter(self):
        """Get a 3 image results of apply the filter RGB_split to the image img

        Parameters
        ----------
        img : ImageType
            It's a ImageType object


        Returns
        -------
        Tuple
            a tuple of (red,green,blue) images
        """
        
        self.img_out =  self.__rgb_split_filter()

       # __save(__rgb_split_filter(),fn,fext)
        
        print('RGB split filter applied')
        
        return self.img_out

    def set_parameters(self,parameters_list):
        return 0

    @staticmethod
    def parameters_needed():
        return []

    def save(self):
        filename = ['{}-split-red.{}','{}-split-green.{}',\
                '{}-split-blue.{}']
        fn, fext = self._filename_separator()
        fields = (fn,fext)
        return self._save(filename,fields)

    # RGB Function
    def __rgb_split_filter(self):
        """
        Take only one channel of the RGB color spectrum
        """
      
        img_red = self.img.copy()
        img_green = self.img.copy()
        img_blue = self.img.copy()
        width, height = self.img.size
        
        for x in range(width):
            for y in range(height):
              
                  r, g, b = self.img.getpixel((x, y))
                
                  img_red.putpixel((x, y), (r, 0, 0))
                  img_green.putpixel((x, y), (0, g, 0))
                  img_blue.putpixel((x, y), (0, 0, b))
                  
        return (img_red,img_green,img_blue)
        
    def __save(self,files,fn,fext):
        files[0].save('{}-split-red.{}'.format(fn,fext), mode = 'P')
        files[1].save('{}-split-green.{}'.format(fn,fext), mode = 'P')
        files[2].save('{}-split-blue.{}'.format(fn,fext), mode = 'P')
        return 0


# Factory Pattern

class ImageType:

    #def __init__(self, path):
    def __init__(self, img, path):
        #self.img_ref = Image.open(path)
        self.path = path
        self.img_ref = img
        #self.fn, self.fext = __filename_separator(path)
        self.width, self.height = self.img_ref.size
#        self.mode = img_ref.mode
        self.filters = []

    def __filename_separator(self):
        (fn, fext) = self.path.split(sep='.')
        return (fn, fext)

    # Create based on class name:
    @staticmethod
    def factory(type, img_ref, path):
        #return eval(type + "()")
        if type == "RGB": return RGBImage(img_ref,path)
        if type == "P": return SingleChannelImage(img_ref,path)
        assert 0, "Bad type creation: " + type

    def __repr__(self):
        return "Image_repr({self.img})"

    def __str__(self):
        return "Image_str({})".format(self.img_ref)

class RGBImage(ImageType):

    def __init__(self, img_ref,path):
        super( RGBImage, self ).__init__(img_ref,path)
        self.filters =\
                {\
                "RGB split":RGB_split(img_ref,self.path),\
                "Blur":Blur(img_ref,self.path)\
                }

    def available_filters(self):
        return self.filters.keys()

class SingleChannelImage(ImageType):
    def __init__(self, img_ref,path):
        super( SingleChannelImage,self ).__init__(img_ref,path)
        self.filters =\
                {\
                "Blur":Blur(img_ref, path)\
                }

    def available_filters(self):
        return self.filters.keys()

def main(argv):

    print('This is an Image App', end = '\n\n')

    img_file = Image.open(argv[0])
    img_mode = img_file.mode

    print('Image type: {0}'.format(img_mode), end = '\n\n')

    image = ImageType.factory(img_mode, img_file,argv[0])
    
    avail_filters = display_available_filters(image)

    chosen_filter = choose_filter(avail_filters)

    parameters_list = ask_for_parameters(image, chosen_filter)

    image.filters[chosen_filter].set_parameters(parameters_list)

    results = image.filters[chosen_filter].apply_filter()
    results = image.filters[chosen_filter].save()

    #fn,fext = __filename_separator(argv[0])

    #save(results,fn,fext)

    print('Image file processed successfully!')

    return 0
    
def display_available_filters(image):
    avail_filters = list(image.available_filters())
    
    print('Available filters:')

    for i, ifilter in zip(range(len(avail_filters)), avail_filters):
        print ('{}.  {}'.format(i+1, ifilter))
    
    print('')
    return avail_filters


def choose_filter(avail_filters):

    filter_num = int(input('Type the selected filter number: '))

    chosen_filter = avail_filters[filter_num-1]
    
    print('')
    
    print('Selected Filter: {}'.format(chosen_filter))

    return chosen_filter

def ask_for_parameters(image, chosen_filter):

    parameters_list=[]

    for param in image.filters[chosen_filter].parameters_needed():
        parameters_list.append(int(input('Type the {} {}: '.format(chosen_filter, param))))
    print('')

    return parameters_list


def save(files, fn,fext):
    files[0].save('{}-split-red.{}'.format(fn,fext), mode = 'P')
    files[1].save('{}-split-green.{}'.format(fn,fext), mode = 'P')
    files[2].save('{}-split-blue.{}'.format(fn,fext), mode = 'P')
    return 0

if __name__ == "__main__":
    import sys
    main(sys.argv[1:])
