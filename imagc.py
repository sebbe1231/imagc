from PIL import Image, ImageFilter, ImageFont, ImageDraw, ImageGrab, GifImagePlugin, ImageOps
import requests
import click
import win32clipboard
import win32con
from io import BytesIO

@click.group()
def imagc():
    pass

def GetImage(file):
    try:
        r = requests.get(file, stream=True)
        if r.status_code != 200:
            raise
        return Image.open(r.raw)
    except:
        print("Image could not be loaded")
        exit(1)

def send_to_clipboard(img):
    output = BytesIO()
    img.convert("RGB").save(output, "BMP")
    data = output.getvalue()[14:]
    output.close()
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32con.CF_DIB, data)
    win32clipboard.CloseClipboard()

def AddCaption(captiontop, captionbottom, img):
    #captiontop = ""
    #captionbottom = ""
    h, w = img.size
    draw = ImageDraw.Draw(img)
    font_size = round(w/6)
    font = ImageFont.truetype("C:\\Run\\requirements\\impact.ttf", size=font_size)
    while True: 
        if font.getlength(captiontop) >=w or font.getlength(captionbottom) >= w:
            font_size -= 1
            print(font_size)
            font = ImageFont.truetype("C:\\Run\\requirements\\impact.ttf", size=font_size)
        else:
            font = ImageFont.truetype("C:\\Run\\requirements\\impact.ttf", size=font_size)
            draw.text((h/2, w/20), text=captiontop, fill=(255,)*3, anchor="mt", font=font, stroke_fill=(0, 0, 0), stroke_width=round(0.05*font_size))
            draw.text((h/2, w-(w/20)), text=captionbottom, fill=(255,)*3, anchor="ms", font=font, stroke_fill=(0, 0, 0), stroke_width=round(0.05*font_size))
            return
   

@imagc.command()
@click.argument('image')
@click.argument('toptext', required=False, default="")
@click.argument('bottomtext', required=False, default="")
def cap(image, toptext, bottomtext):
    #toptext = " ".join(toptext)
    img = GetImage(image)

    if hasattr(img, 'is_animated'):
        print("[WARNING] Image is animated. This can cause problems!")
    
    AddCaption(captiontop=toptext, captionbottom=bottomtext, img=img)
    
    img.show()
    send_to_clipboard(img=img)

@imagc.command()
@click.argument('image', nargs=1)
@click.argument('amount', nargs=1)
@click.argument('toptext', required=False, default="")
@click.argument('bottomtext', required=False, default="")
def filter(image, amount, toptext, bottomtext):
    """Adds a lot of Edge Enchancing to image"""
    img = GetImage(image)
    amount = round(int(amount))
    try:
        for x in range(amount):
            img = img.filter(ImageFilter.EDGE_ENHANCE_MORE())
    except ValueError:
        return print("Can not use filters on given file format")
    
    AddCaption(captiontop=toptext, captionbottom=bottomtext, img=img)
    
    img.show()
    send_to_clipboard(img=img)

@imagc.command()
@click.argument('image', nargs=1)
@click.argument('amount', nargs=1)
@click.argument('toptext', required=False, default="")
@click.argument('bottomtext', required=False, default="")
def filter2(image, amount, toptext, bottomtext):
    """Adds Emboss to image"""
    img = GetImage(image)
    amount = round(int(amount))
    try:
        for x in range (amount):
            img = img.filter(ImageFilter.EMBOSS())
    except ValueError:
        return print("Can not use filters on given file format")
    
    AddCaption(captiontop=toptext, captionbottom=bottomtext, img=img)
    
    img.show()
    send_to_clipboard(img=img)

@imagc.command()
@click.argument('image', nargs=1)
@click.argument('amount', nargs=1)
@click.argument('toptext', required=False, default="")
@click.argument('bottomtext', required=False, default="")
def filter3(image, amount, toptext, bottomtext):
    """Adds Contour to image"""
    img = GetImage(image)
    amount = round(int(amount))
    try:
        for x in range (amount):
            img = img.filter(ImageFilter.CONTOUR())
    except ValueError:
        return print("Can not use filters on given file format")

    AddCaption(captiontop=toptext, captionbottom=bottomtext, img=img)

    img.show()
    send_to_clipboard(img=img)

@imagc.command()
@click.argument('image', nargs=1)
@click.argument('amount', nargs=1)
@click.argument('toptext', required=False, default="")
@click.argument('bottomtext', required=False, default="")
def filter4(image, amount, toptext, bottomtext):
    """Combines all 3 previous filters together"""
    img = GetImage(image)
    amount = round(int(amount))
    try:
        for x in range(amount):
            img = img.filter(ImageFilter.CONTOUR())
            img = img.filter(ImageFilter.EMBOSS())
            img = img.filter(ImageFilter.EDGE_ENHANCE_MORE())
    except ValueError:
        return print("Can not use filters on given file format")
    
    AddCaption(captiontop=toptext, captionbottom=bottomtext, img=img)
    
    img.show()
    send_to_clipboard(img=img)

@imagc.command()
@click.argument('image', nargs=1)
@click.argument('toptext', required=False, default="")
@click.argument('bottomtext', required=False, default="")
def grayscale(image, toptext, bottomtext):
    """Grayscale an image"""
    img = GetImage(image)
    
    try:

        img = ImageOps.grayscale(img)
        img = img.convert("RGB")
    except ValueError:
        return print("Can not use filters on given file format")

    AddCaption(captiontop=toptext, captionbottom=bottomtext, img=img)
    
    img.show()
    send_to_clipboard(img=img)

@imagc.command()
@click.argument('image', nargs=1)
@click.argument('height', nargs=1)
@click.argument('width', nargs=1)
@click.argument('toptext', required=False, default="")
@click.argument('bottomtext', required=False, default="")
def resize(image, height, width, toptext, bottomtext):
    img = GetImage(image)
    height = round(int(height))
    width = round(int(width))
  
    img = img.resize(size=(width, height))

    AddCaption(captiontop=toptext, captionbottom=bottomtext, img=img)
    
    img.show()
    send_to_clipboard(img=img)


if __name__ == '__main__':
    imagc()    

