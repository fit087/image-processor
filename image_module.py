# -*- coding: utf-8 -*-
"""
Created on Thu Dec 20 23:49:13 2018

@author: adolfo
"""
from PIL import Image
from numpy import array
from numpy import int64
from sys import exit


class Filter:
    def __init__(self,img,path):
        """

        Parameters
        ----------
        img : Image.open() reference
            It's a Image object from pillow library

        path : String
            It`s the path to the file


        Set up
        -------
            self.img = img
            self.img_out = []
            self.path = path
        """
        self.img = img
        self.img_out = []
        self.path = path

    def apply_filter(): pass
    def set_parameters(parameters_list): pass
    @staticmethod
    def parameters_needed(): pass

    def _save(self,filename,fields):
        """Save the changed images

        Parameters
        ----------
        filename : list of strings
            It contains the strings with differents filenames

        fields : list of variables
            It contains the variables that will be used to make the filenames

        """
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
        img : Image object from Pillow library
            It's a ImageType object


        Returns
        -------
        blur : Image object from Pillow library
            It contains the changed image
        """

        blur = self.__blur_filter()

        self.img_out.append(blur)
        
        print('Blur filter applied')

        return blur

    def set_parameters(self,parameters_list):
        """Establish the input parameters of the filter
        """
        self.radius, self.weight = parameters_list

    @staticmethod
    def parameters_needed():
        """Let the user know the required parameters in orther
        to apply the filter
        """
        return ('radius','weight')

    def save(self):
        """Save the file after to apply the filter
        """
        filename = ['{0}-blur-radius{1}-weight{2}.{3}']
        fn, fext = self._filename_separator()
        fields = (fn,self.radius,self.weight,fext)
        return self._save(filename,fields)

    def __blur_filter(self):
        """
            Blur Filter
        """
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
            
            #blur_color = self.__blur_pane(x,y,rgb,pix_count, width, height)
            img_blur.putpixel((x, y), blur_color)
    
        return img_blur

    
    def __blur_pane(self,x,y,rgb,pix_count, width, height):
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
        
            return blur_color


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

        print('RGB split filter applied')
        
        return self.img_out

    def set_parameters(self,parameters_list):
        """Establish the input parameters of the filter
        """
        return 0

    @staticmethod
    def parameters_needed():
        """Let the user know the required parameters in orther
        to apply the filter
        """
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
        
# Factory Pattern

class ImageType:

    def __init__(self, img, path):
        self.path = path
        self.img_ref = img
        self.width, self.height = self.img_ref.size
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
        """Store the available filters filters for the specific Image type
        """
        super( RGBImage, self ).__init__(img_ref,path)
        self.filters =\
                {\
                "RGB split":RGB_split(img_ref,self.path),\
                "Blur":Blur(img_ref,self.path)\
                }

    def available_filters(self):
        """Return the list of the filter available for the specific Image type
        """
        return self.filters.keys()

class SingleChannelImage(ImageType):
    def __init__(self, img_ref,path):
        """Store the available filters filters for the specific Image type
        """
        super( SingleChannelImage,self ).__init__(img_ref,path)
        self.filters =\
                {\
                "Blur":Blur(img_ref, path)\
                }

    def available_filters(self):
        """Return the list of the filter available for the specific Image type
        """
        return self.filters.keys()

class cli_verify():

    aval_flags = ('-rgb','-blur')
    flags_filters= {'-rgb':'RGB split','-blur':'Blur'}
    chosen_flag = ''

    def __init__(self, argv):
        self.argv = argv
        self.flag = self.exist_a_flag()
        self.filename = self.get_filename()
        self.exist_file()
        if self.exist_a_flag():
            self.existing_flag()
                

    def chosen_command(self):
        return self.flags_filters[self.chosen_flag]

        
    def exist_a_flag(self):
        if self.argv[0][0] == '-':
            self.chosen_flag=self.argv[0][0]
            self.parameters = map(lambda x : int(x) ,self.argv[2:])
            return True
        else:
            return False

    def exist_file(self):
       try:
           fn = open(self.filename, 'r')
       except FileNotFoundError:
            print('File not found')
            exit(1)
            return False

       return True

    def get_filename(self):
        if self.exist_a_flag() == True:
            return self.argv[1]
        else:
            return self.argv[0]

    def existing_flag(self):
        for fgs in self.aval_flags:
            if self.argv[0] == fgs:
                self.chosen_flag = self.argv[0]
                finded = True
                break
            else:
                finded = False
        if finded:
            return True
        else:
                print('Wrong flag')
                exit(1)
                return False



def main(argv):

    print('This is an Image App', end = '\n\n')

    arguments = cli_verify(argv)

    img_file = Image.open(arguments.filename)
    print('362 {}'.format(arguments.filename))
    img_mode = img_file.mode

    print('Image type: {0}'.format(img_mode), end = '\n\n')

    image = ImageType.factory(img_mode, img_file,arguments.filename)

    
    if not arguments.flag:
        avail_filters = display_available_filters(image)

        chosen_filter = choose_filter(avail_filters)

        parameters_list = ask_for_parameters(image, chosen_filter)

    else:
        chosen_filter = arguments.chosen_command()
        parameters_list = arguments.parameters

    image.filters[chosen_filter].set_parameters(parameters_list)

    results = image.filters[chosen_filter].apply_filter()
    results = image.filters[chosen_filter].save()

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

if __name__ == "__main__":
    import sys
    main(sys.argv[1:])
