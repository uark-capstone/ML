import io
import glob
import base64
from PIL import Image
from math import sqrt, ceil

def stringToImage(input_string):
    # see base64.txt for working encoding
    img_only = input_string[input_string.find(b'/9'):] # gets image part of encoding
    b = io.BytesIO(base64.b64decode(img_only))
    img = Image.open(b)

    in_mem_file = io.BytesIO()
    img.save(in_mem_file, format=img.format)
    in_mem_file.seek(0)

    return in_mem_file


#Place images in stack
def concat(images):
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
