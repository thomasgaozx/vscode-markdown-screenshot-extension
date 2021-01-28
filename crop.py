import os
import sys
import uuid
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk, ImageGrab, ImageEnhance

# Source: https://stackoverflow.com/a/60775548
def show_image(image):
    win = tk.Toplevel()
    win.image = ImageTk.PhotoImage(image)
    tk.Label(win, image=win.image).pack()
    win.grab_set()
    win.wait_window(win)

# Source: https://stackoverflow.com/a/60775548
def area_sel():
    x1 = y1 = x2 = y2 = 0
    roi_image = None

    def on_mouse_down(event):
        nonlocal x1, y1
        x1, y1 = event.x, event.y
        canvas.create_rectangle(x1, y1, x1, y1, outline='red', tag='roi')

    def on_mouse_move(event):
        nonlocal roi_image, x2, y2
        x2, y2 = event.x, event.y
        canvas.delete('roi-image') # remove old overlay image
        roi_image = image.crop((x1, y1, x2, y2)) # get the image of selected region
        canvas.image = ImageTk.PhotoImage(roi_image)
        canvas.create_image(x1, y1, image=canvas.image, tag=('roi-image'), anchor='nw')
        canvas.coords('roi', x1, y1, x2, y2)
        # make sure the select rectangle is on top of the overlay image
        canvas.lift('roi') 

    image = ImageGrab.grab()  # grab the fullscreen as select region background
    bgimage = ImageEnhance.Brightness(image).enhance(0.3)  # darken the capture image
    # create a fullscreen window to perform the select region action
    win = tk.Toplevel()
    win.attributes('-fullscreen', 1)
    win.attributes('-topmost', 1)
    canvas = tk.Canvas(win, highlightthickness=0)
    canvas.pack(fill='both', expand=1)
    tkimage = ImageTk.PhotoImage(bgimage)
    canvas.create_image(0, 0, image=tkimage, anchor='nw', tag='images')
    # bind the mouse events for selecting region
    win.bind('<ButtonPress-1>', on_mouse_down)
    win.bind('<B1-Motion>', on_mouse_move)
    win.bind('<ButtonRelease-1>', lambda e: win.destroy())
    # use Esc key to abort the capture
    win.bind('<Escape>', lambda e: win.destroy())
    # make the capture window modal
    win.focus_force()
    win.grab_set()
    win.wait_window(win)

    # show the capture image
    return roi_image

def trim_edges(img):
    """img: PIL Image object"""
    img = np.array(img)

    # image trimming algorithm: https://stackoverflow.com/a/14211727
    # might need to deal with opaque white (255) rather than transparent (0)
    img_bw = img.max(axis=2)
    img_bw[img_bw > 253] = 0
    non_empty_columns = np.where(img_bw.max(axis=0)>0)[0]
    non_empty_rows = np.where(img_bw.max(axis=1)>0)[0]
    cropBox = (min(non_empty_rows), max(non_empty_rows), min(non_empty_columns), max(non_empty_columns))

    trimmed_img = img[cropBox[0]:cropBox[1]+1, cropBox[2]:cropBox[3]+1 , :]
    return Image.fromarray(trimmed_img)

def prompt_name():
    # source: https://www.tutorialspoint.com/python/tk_entry.htm
    top = tk.Tk()
    L1 = tk.Label(top, text="Filename (Type 'no' to cancel)")
    L1.pack( side = tk.LEFT)
    E1 = tk.Entry(top, bd =5)
    E1.pack(side = tk.RIGHT)
    E1.focus()
    
    name = ""
    def on_return(event):
        nonlocal name
        name = E1.get()
        top.destroy()

    top.bind('<Return>', on_return)
    
    top.focus_force()
    top.wait_window(top)
    return name

if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise Exception("the first arg is <path-to-doc>")

    doc = sys.argv[1]
    if doc[-3:].lower() != '.md':
        raise Exception("The document is not of markdown type")
    imgdir=os.path.join(os.path.dirname(doc), 'img')
    os.makedirs(imgdir, exist_ok=True)

    img = area_sel()
    if img is None:
        exit()

    img = trim_edges(img)
    #show_image(img) #debug
    name = prompt_name().strip().lower()
    if name == 'no':
        exit()

    # process name into appropriate image path
    if len(name) == 0:
        name = uuid.uuid4().hex

    name = name.replace(' ', '-')

    img_name = name + '.jpg'
    img_path = os.path.join(imgdir, img_name)

    # TODO: smarter auto-rename algorithm
    if os.path.isfile(img_path): # avoid overriding
        raise Exception("Image {} already exists!".format(img_path))

    img.save(img_path)
    with open(doc, 'a+', encoding='utf-8') as f:
        f.write("![{}]({})".format(name, os.path.join('.', 'img', img_name)))
        f.write('\n') #gap line?
