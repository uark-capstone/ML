from PIL import Image
from math import sqrt, ceil
import glob
from io import BytesIO


def stringToImage(stringImage):
    return( Image.open(BytesIO.base64.b64decode(stringImage)))



#Place images in stack

def concat(images, outPut):
    if images:
        increment = 0
        stepsize = ceil(sqrt(len(images)))
        size = images[0].width * ceil(sqrt(len(images)))
        x = 0
        y = 0
        output = Image.new('RGBA',(size,size))
        for each in images:
            output.paste(each, (x,y))
            x += each.width
            if x == size:
                x = 0;
                y += each.width
        return(output);


    
