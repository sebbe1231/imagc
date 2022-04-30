from PIL import Image, ImageFilter, ImageFont, ImageDraw, ImageOps, ImageSequence, ImageGrab
import requests
import click
import win32clipboard, win32con, win32gui
import time
from io import BytesIO

@click.group()
def imagc():
    pass    

def get_image(file):
    if file == "clpbrd":
        if ImageGrab.grabclipboard() is None:
            print("No image file was found in your clipboard data!")
            exit(1)
        return ImageGrab.grabclipboard()
    if file == "screen":
        win32gui.ShowWindow(win32gui.GetForegroundWindow(), win32con.SW_MINIMIZE)
        time.sleep(1)
        return ImageGrab.grab(all_screens=False)
    if file == "allscreen":
        win32gui.ShowWindow(win32gui.GetForegroundWindow(), win32con.SW_MINIMIZE)
        time.sleep(1)
        return ImageGrab.grab(all_screens=True)
    try:
        r = requests.get(file, stream=True)
        if r.status_code != 200:
            raise
        return Image.open(r.raw)
    except:
        try:
            return Image.open(file)
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

def add_caption(captiontop, captionbottom, img):
    #captiontop = ""    #captionbottom = ""
    frames = []
    FONT = "C:\\Run\\requirements\\impact.ttf"
    h, w = img.size
    font_size = round(w/6)
    font = ImageFont.truetype(FONT, size=font_size)
    while True: 
        if font.getlength(captiontop) >=w or font.getlength(captionbottom) >= w:
            font_size -= 1
            print(font_size)
            font = ImageFont.truetype(FONT, size=font_size)
        else:
            if hasattr(img, 'is_animated') and img.is_animated:
                for frame in ImageSequence.Iterator(img):
                    frame.seek(0)
                    img = frame.copy()
                    img = img.convert("RGBA")
                    img.save("out.png", "PNG")
                    break

            draw = ImageDraw.Draw(img)
            draw.text((h/2, w/20), text=captiontop, fill=(255,)*3, anchor="mt", font=font, stroke_fill=(0, 0, 0), stroke_width=round(0.05*font_size))
            draw.text((h/2, w-(w/20)), text=captionbottom, fill=(255,)*3, anchor="ms", font=font, stroke_fill=(0, 0, 0), stroke_width=round(0.05*font_size))

            img.save("final.png")

            return img
   

@imagc.command()
@click.argument('image')
@click.argument('toptext', required=False, default="")
@click.argument('bottomtext', required=False, default="")
def cap(image, toptext, bottomtext):
    """Adds top text and bottom text to and image
    
    \b
    Set image as "clpbrd" to get the image from your clipboard
    Set image as "screen" to get a screenshot of your primary screen
    Set image as "allscreen" to get a screenshot of all your screens in one
    """
    img = get_image(image)

    if hasattr(img, 'is_animated') and img.is_animated:
        print("[WARNING] Image is animated. This can cause problems!")

    img = add_caption(captiontop=toptext, captionbottom=bottomtext, img=img)
    
    img.show()
    send_to_clipboard(img=img)

@imagc.command()
@click.argument('image', nargs=1)
@click.argument('width', nargs=1)
def asciify(image, width: int):
    """Make and image into ascii"""
    image = get_image(image)
    width = round(int(width))
    image = image.resize((width, round(width/2)))
    print(image.size)

    image = image.convert("L")
    pixels = image.getdata()
    imgchars = ["$", "@", "B", "%", "8", "&", "W", "M", "#", "*", "o", "a", "h", "k", "b", "d", "p", "q", "w", "m", "Z", "O", "0", "Q", "L", "C", "J", "U", "Y", "X", "z", "c", "v", "u", "n", "x", "r", "j", "f", "t", "/", "\\", "|", "(", ")", "1", "{", "}", "[", "]", "?", "-", "_", "+", "~", "<", ">", "i", "!", "l", "I", ";", ":", "\"", "^", "`", "'", ".", " "][::-1]
    ascii_img = ""

    for i, pixel in enumerate(pixels):
        if i%width == 0:
            ascii_img += "\n"
        ascii_img += imgchars[int(pixel/256*len(imgchars))]

    print(ascii_img)
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText(ascii_img)
    win32clipboard.CloseClipboard()

@imagc.command()
@click.argument('image', nargs=1)
@click.argument('amount', nargs=1)
@click.argument('toptext', required=False, default="")
@click.argument('bottomtext', required=False, default="")
def filter(image, amount, toptext, bottomtext):
    """Adds a lot of Edge Enchancing to image"""
    
    img = get_image(image)
    amount = round(int(amount))
    try:
        for x in range(amount):
            img = img.filter(ImageFilter.EDGE_ENHANCE_MORE())
    except ValueError:
        return print("Can not use filters on given file format")
    
    img = add_caption(captiontop=toptext, captionbottom=bottomtext, img=img)
    
    img.show()
    send_to_clipboard(img=img)

@imagc.command()
@click.argument('image', nargs=1)
@click.argument('amount', nargs=1)
@click.argument('toptext', required=False, default="")
@click.argument('bottomtext', required=False, default="")
def filter2(image, amount, toptext, bottomtext):
    """Adds Emboss to image"""
    img = get_image(image)
    amount = round(int(amount))
    try:
        for x in range (amount):
            img = img.filter(ImageFilter.EMBOSS())
    except ValueError:
        return print("Can not use filters on given file format")
    
    img = add_caption(captiontop=toptext, captionbottom=bottomtext, img=img)
    
    img.show()
    send_to_clipboard(img=img)

@imagc.command()
@click.argument('image', nargs=1)
@click.argument('amount', nargs=1)
@click.argument('toptext', required=False, default="")
@click.argument('bottomtext', required=False, default="")
def filter3(image, amount, toptext, bottomtext):
    """Adds Contour to image"""
    img = get_image(image)
    amount = round(int(amount))
    try:
        for x in range (amount):
            img = img.filter(ImageFilter.CONTOUR())
    except ValueError:
        return print("Can not use filters on given file format")

    img = add_caption(captiontop=toptext, captionbottom=bottomtext, img=img)

    img.show()
    send_to_clipboard(img=img)

@imagc.command()
@click.argument('image', nargs=1)
@click.argument('amount', nargs=1)
@click.argument('toptext', required=False, default="")
@click.argument('bottomtext', required=False, default="")
def filter4(image, amount, toptext, bottomtext):
    """Combines all 3 previous filters together"""
    img = get_image(image)
    amount = round(int(amount))
    try:
        for x in range(amount):
            img = img.filter(ImageFilter.CONTOUR())
            img = img.filter(ImageFilter.EMBOSS())
            img = img.filter(ImageFilter.EDGE_ENHANCE_MORE())
    except ValueError:
        return print("Can not use filters on given file format")
    
    img = add_caption(captiontop=toptext, captionbottom=bottomtext, img=img)
    
    img.show()
    send_to_clipboard(img=img)

@imagc.command()
@click.argument('image', nargs=1)
@click.argument('toptext', required=False, default="")
@click.argument('bottomtext', required=False, default="")
def grayscale(image, toptext, bottomtext):
    """Grayscale an image"""
    img = get_image(image)
    
    try:

        img = ImageOps.grayscale(img)
        img = img.convert("RGB")
    except ValueError:
        return print("Can not use filters on given file format")

    img = add_caption(captiontop=toptext, captionbottom=bottomtext, img=img)
    
    img.show()
    send_to_clipboard(img=img)

@imagc.command()
@click.argument('image', nargs=1)
@click.argument('height', nargs=1)
@click.argument('width', nargs=1)
@click.argument('toptext', required=False, default="")
@click.argument('bottomtext', required=False, default="")
def resize(image, height, width, toptext, bottomtext):
    """Resize an image"""
    img = get_image(image)
    height = round(int(height))
    width = round(int(width))
  
    img = img.resize(size=(width, height))

    img = add_caption(captiontop=toptext, captionbottom=bottomtext, img=img)
    
    img.show()
    send_to_clipboard(img=img)

@imagc.command()
def empty():
    """Empty your clipboard if needed for some reason"""
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.CloseClipboard()
    print("Emptied clipboard")

if __name__ == '__main__':
    imagc()    

