from PIL import Image, ImageFilter, ImageFont, ImageDraw, ImageGrab, GifImagePlugin
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

def AddCaption(caption, img):
    h, w = img.size
    draw = ImageDraw.Draw(img)
    font_size = round(w/6)
    font = ImageFont.truetype("C:\\Run\\requirements\\impact.ttf", size=font_size)
    while True: 
        if font.getlength(caption) >= w:
            font_size -= 1
            print(font_size)
            font = ImageFont.truetype("C:\\Run\\requirements\\impact.ttf", size=font_size)
        else:
            font = ImageFont.truetype("C:\\Run\\requirements\\impact.ttf", size=font_size)
            draw.text((h/2, w/20), text=caption, fill=(255,)*3, anchor="mt", font=font, stroke_fill=(0,)*3, stroke_width=round(0.05*font_size))
            return

@imagc.command()
@click.argument('image', nargs=1)
@click.argument('caption', nargs=-1)
def cap(image, caption):
    caption = " ".join(caption)
    img = GetImage(image)

    if hasattr(img, 'is_animated'):
        print("[WARNING] Image is animated. This can cause problems!")
    
    AddCaption(caption=caption, img=img)
    
    img.show()
    send_to_clipboard(img=img)

@imagc.command()
@click.argument('image', nargs=1)
@click.argument('amount', nargs=1)
@click.argument('caption', required=False, nargs=-1)
def filter(image, amount, caption):
    """Adds a lot of Edge Enchancing to image"""
    img = GetImage(image)
    amount = int(amount)
    try:
        for x in range(amount):
            img = img.filter(ImageFilter.EDGE_ENHANCE_MORE())
    except ValueError:
        return print("Can not use filters on given file format")
    
    if caption:
        caption = " ".join(caption)
        AddCaption(caption=caption, img=img)
    
    img.show()
    send_to_clipboard(img=img)

@imagc.command()
@click.argument('image', nargs=1)
@click.argument('amount', nargs=1)
@click.argument('caption', required=False, nargs=-1)
def filter2(image, amount, caption):
    """Adds Emboss to image"""
    img = GetImage(image)
    amount = int(amount)
    try:
        for x in range (amount):
            img = img.filter(ImageFilter.EMBOSS())
    except ValueError:
        return print("Can not use filters on given file format")
    
    if caption:
        caption = " ".join(caption)
        AddCaption(caption=caption, img=img)
    
    img.show()
    send_to_clipboard(img=img)

@imagc.command()
@click.argument('image', nargs=1)
@click.argument('amount', nargs=1)
@click.argument('caption', required=False, nargs=-1)
def filter3(image, amount, caption):
    """Adds Contour to image"""
    img = GetImage(image)
    amount = int(amount)
    try:
        for x in range (amount):
            img = img.filter(ImageFilter.CONTOUR())
    except ValueError:
        return print("Can not use filters on given file format")

    if caption:
        caption = " ".join(caption)
        AddCaption(caption=caption, img=img)

    img.show()
    send_to_clipboard(img=img)

@imagc.command()
@click.argument('image', nargs=1)
@click.argument('amount', nargs=1)
@click.argument('caption', required=False, nargs=-1)
def filter4(image, amount, caption):
    """Combines all 3 previous filters together"""
    img = GetImage(image)
    amount = int(amount)
    try:
        for x in range (amount):
            img = img.filter(ImageFilter.CONTOUR())
            img = img.filter(ImageFilter.EMBOSS())
            img = img.filter(ImageFilter.EDGE_ENHANCE_MORE())
    except ValueError:
        return print("Can not use filters on given file format")
    
    if caption:
        caption = " ".join(caption)
        AddCaption(caption=caption, img=img)
    
    img.show()
    send_to_clipboard(img=img)

    
if __name__ == '__main__':
    imagc()    

