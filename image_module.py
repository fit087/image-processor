# -*- coding: utf-8 -*-
"""
Created on Thu Dec 20 23:49:13 2018

@author: adolfo
"""
from PIL import Image

class Filter:
    def apply_filter(): pass
    def set_parameters(parameters_list):pass
    @staticmethod
    def parameters_needed():pass

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
        
        print('Blur filter applied')

    def set_parameters(self,parameters_list):
        self.radius, self.weight = parameters_list

    @staticmethod
    def parameters_needed():
        return ('radius','weight')


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
        
        print('RGB split filter applied')


    def set_parameters(self,parameters_list):
        return 0

    @staticmethod
    def parameters_needed():
        return []
    

# Factory Pattern

class ImageType:

    def __init__(self, img_ref):
        self.img_ref = img_ref
        self.width, self.height = self.img_ref.size
        self.mode = img_ref.mode
        self.filters = []

    # Create based on class name:
    @staticmethod
    def factory(type, img_ref):
        #return eval(type + "()")
        if type == "RGB": return RGBImage(img_ref)
        if type == "P": return SingleChannelImage(img_ref)
        assert 0, "Bad type creation: " + type

    def __repr__(self):
        return "Image_repr({self.img})"

    def __str__(self):
        return "Image_str({})".format(self.img_ref)


class RGBImage(ImageType):

    def __init__(self, img_ref):
        super( RGBImage, self ).__init__(img_ref)
        self.filters = {"RGB split":RGB_split(),"Blur":Blur()}

    def available_filters(self):
        return self.filters.keys()

    

class SingleChannelImage(ImageType):
    def __init__(self, img_ref):
        super( SingleChannelImage,self ).__init__(img_ref)
        self.filters = {"Blur":Blur()}

    def available_filters(self):
        return self.filters.keys()

def main(argv):

    print('This is an Image App', end = '\n\n')

    img_file = Image.open(argv[0])
    img_mode = img_file.mode

    print('Image type: {0}'.format(img_mode), end = '\n\n')

    image = ImageType.factory(img_mode, img_file)
    
    avail_filters = display_available_filters(image)

    chosen_filter = choose_filter(avail_filters)

    parameters_list = ask_for_parameters(image, chosen_filter)

    image.filters[chosen_filter].set_parameters(parameters_list)

    image.filters[chosen_filter].apply_filter()
    
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
