from tkinter import XView

import keyboard
import mouse
import time
import os
import math
from PIL import Image
from PIL import ImageGrab
import tkinter as tk
from pathlib import Path
from stitching import Stitcher
stitcher = Stitcher()

# Values
xDef = 0
yDef = 0
xOffset = 0
yOffset = 0
continueToPartTwoG = False
setupMousePosG = 1
currentStripG = 0
mousePos1 = list()
mousePos2 = list()
mousePos3 = list()
bb1 = list()
bb2 = list()
buttonPressed = 0
coordsText = ""
estimText = ""

def windowLoop():
    global buttonPressed
    global buttonX
    global mousePos1
    global mousePos2
    global mousePos3
    global bb1
    global bb2
    global coordsText
    global estimText
    if buttonPressed == 1:
        buttonX.config(text="Click to set position, space to confirm.")
        if mouse.is_pressed(button='left'):
            mousePos1 = mouse.get_position()
        if keyboard.is_pressed('space'):
            buttonPressed = 0
            text = str(mousePos1)
            buttonX.config(text=text)
        time.sleep(0.01)
    if buttonPressed == 2:
        buttonY.config(text="Click to set position, space to confirm.")
        if mouse.is_pressed(button='left'):
            mousePos2 = mouse.get_position()
        if keyboard.is_pressed('space'):
            buttonPressed = 0
            text = str(mousePos2)
            buttonY.config(text=text)
        time.sleep(0.01)
    if buttonPressed == 3:
        buttonGo.config(text="Click to set position, space to confirm.")
        if mouse.is_pressed(button='left'):
            mousePos3 = mouse.get_position()
        if keyboard.is_pressed('space'):
            buttonPressed = 0
            text = str(mousePos3)
            buttonGo.config(text=text)
        time.sleep(0.01)
    if buttonPressed == 4:
        buttonTopL.config(text="Click to set position, space to confirm.")
        if mouse.is_pressed(button='left'):
            bb1 = mouse.get_position()
        if keyboard.is_pressed('space'):
            buttonPressed = 0
            text = str(bb1)
            buttonTopL.config(text=text)
        time.sleep(0.01)
    if buttonPressed == 5:
        buttonBotR.config(text="Click to set position, space to confirm.")
        if mouse.is_pressed(button='left'):
            bb2 = mouse.get_position()
        if keyboard.is_pressed('space'):
            buttonPressed = 0
            text = str(bb2)
            buttonBotR.config(text=text)
        time.sleep(0.01)
    coordsText = "X" + str(xDef + xOffset) + " x Y" + str(yDef + yOffset)
    estimText = str(((abs(xDef)*2)+1)*788) + "*" + str(((abs(yDef)*2)+1)*758)
    textBoxCoords.config(state='normal')
    textBoxCoords.delete('1.0',tk.END)
    textBoxCoords.insert('1.0', coordsText)
    textBoxCoords.config(state='disabled')
    textboxEstim.config(state='normal')
    textboxEstim.delete('1.0',tk.END)
    textboxEstim.insert('1.0', estimText)
    textboxEstim.config(state='disabled')
    window.after(1, windowLoop)

def main():
    x = xDef
    y = yDef
    i = True
    temp = 0
    temp2 = 0
    i = False
    step = 0
    imagesForStrip = list()
    stripsForFinal = list()
    global mousePos1
    global mousePos2
    global mousePos3
    global bb1
    global bb2
    global xOffset
    global yOffset
    currentStrip = currentStripG
    Path("C:/strips/").mkdir(parents=True, exist_ok=True)
    Path("C:/wcreenshots/").mkdir(parents=True, exist_ok=True)


    continueToPartTwo = continueToPartTwoG
    setupMousePos = setupMousePosG
    #bb1, bb2, mousePos1, mousePos2, mousePos3, step, setupMousePos = setup_positions(step, setupMousePos, mousePos1, mousePos2, mousePos3, bb1, bb2)

    while temp != (abs(xDef) * 2) + 1:
        if not os.path.exists("C:/strips/" + str(currentStrip) + ".png"):
            time.sleep(1)
            y_loop(bb1, bb2, mousePos1, mousePos2, mousePos3, temp2, x, y, imagesForStrip)
            temp, temp2, x, y, currentStrip = create_strip(temp, x, imagesForStrip, stripsForFinal, currentStrip)
        else:
            temp = temp + 1
            x = x +1
            stripsForFinal.append("C:/strips/" + str(currentStrip) + ".png")
            print("Skipping strip " + str(currentStrip))
            currentStrip = currentStrip + 1
    stitchColumns(stripsForFinal)


def setup_positions(step, setupMousePos1, mousePos1, mousePos2, mousePos3, bb1, bb2):
    mousePos1 = mousePos1
    mousePos2 = mousePos2
    mousePos3 = mousePos3
    bb1= bb1
    bb2 = bb2
    step = step
    setupMousePos = setupMousePos1
    while setupMousePos == 1:
        if step == 0:
            if mouse.is_pressed(button='left'):
                mousePos1 = mouse.get_position()
        if step == 1:
            if mouse.is_pressed(button='left'):
                mousePos2 = mouse.get_position()
        if step == 2:
            if mouse.is_pressed(button='left'):
                mousePos3 = mouse.get_position()
        if step == 3:
            if mouse.is_pressed(button='left'):
                bb1 = mouse.get_position()
        if step == 4:
            if mouse.is_pressed(button='left'):
                bb2 = mouse.get_position()
        if keyboard.is_pressed('space'):
            step = step + 1
            if step >= 5:
                setupMousePos = 0
        time.sleep(0.1)
        print("Current step is " + str(step))
    return bb1, bb2, mousePos1, mousePos2, mousePos3, step, setupMousePos


def create_strip(temp, x, imagesForStrip, stripsForFinal, currentStrip):
    # Create list of images from full path list
    print(imagesForStrip)
    images = [Image.open(v) for v in imagesForStrip]
    widths, heights = zip(*(i.size for i in images))  # Returns two lists for widths and heights using images
    max_width = max(widths)  # Sets max width to widest image (should always be the same)
    max_height = max(heights)  # Sets max height to tallest image (should always be the same)
    image_height = max_height * len(images)  # Sets image height to max_height multiplied by amount of images
    new_im = Image.new('RGB', (max_width, image_height))  # Create holding object for 'strip' image
    y_offset = 0
    for im in images:
        new_im.paste(im, (0, y_offset))
        y_offset += max_height
    new_im.save("C:/strips/" + str(currentStrip) + ".png")
    stripsForFinal.append("C:/strips/" + str(currentStrip) + ".png")
    for im in imagesForStrip:
        os.remove(im)
    imagesForStrip.clear()
    temp2 = 0
    y = yDef
    x = x + 1
    temp = temp + 1
    currentStrip = currentStrip +1
    return temp, temp2, x, y, currentStrip


def y_loop(bb1, bb2, mousePos1, mousePos2, mousePos3, temp2, x, y, imagesForStrip):
    while temp2 != (abs(yDef)*2) + 1:
        if keyboard.is_pressed('space'):
            exit()
        print(str(x) + "," + str(y))  # current cell being photographed
        mouse.move(mousePos1[0], mousePos1[1], True, 0)  # Move to first coordinate

        # Enter cell X
        mouse.click(button='left')
        keyboard.send('ctrl+a, backspace', do_press=True, do_release=True)
        keyboard.write(str(x + xOffset), delay=0, restore_state_after=True, exact=None)

        mouse.move(mousePos2[0], mousePos2[1], True, 0)  # Move to first coordinate

        # Enter cell Y
        mouse.click(button='left')
        keyboard.send('ctrl+a, backspace', do_press=True, do_release=True)
        keyboard.write(str(y + yOffset), delay=0, restore_state_after=True, exact=None)

        mouse.move(mousePos3[0], mousePos3[1], True, 0)  # Move to enter
        mouse.click(button='left')  # Click enter
        time.sleep(1)  # Wait for cell to load

        # Screenshot
        screenshot = ImageGrab.grab((bb1[0], bb1[1], bb2[0], bb2[1]), False, False)  # Screenshot cell
        screenshot = screenshot.resize((788, 758))  # Standardize size
        screenshot = screenshot.save("C:/wcreenshots/" + str(temp2) + ".jpg")  # Save Screenshot
        imagesForStrip.append("C:/wcreenshots/" + str(temp2) + ".jpg")
        temp2 = temp2 + 1  # Increment Y Counter
        y = y - 1  # Increment Y-Cell Location


def stitchColumns(stripsForFinal):
    x_offset = 0
    print(stripsForFinal)
    # Create list of images from full path list
    images2 = [Image.open(v) for v in stripsForFinal]

    widths, heights = zip(*(i.size for i in images2))  # Returns two lists for widths and heights using images

    max_width = max(widths)  # Sets max width to widest image (should always be the same)
    max_height = max(heights)  # Sets max height to tallest image (should always be the same)
    image_width = max_width * len(stripsForFinal)  # Sets image height to max_height multiplied by amount of images

    new_im = Image.new('RGB', (image_width, max_height))  # Create holding object for 'strip' image

    x_offset = 0
    #images2.reverse()
    for im in images2:
        new_im.paste(im, (x_offset, 0))
        x_offset += max_width

    new_im.save("Final.png")
    for im in stripsForFinal:
        if os.path.exists(im):
            os.remove(im)

window = tk.Tk()
window.title("Hello World")

buttonInputX = tk.Button(text = "Press to set amount of cells on X")
buttonInputY = tk.Button(text = "Press to set amount of cells on Y")
buttonInputXo = tk.Button(text = "Press to set the X offset")
buttonInputYo = tk.Button(text = "Press to set the Y offset")

buttonX = tk.Button(text="Select X Position")
def handle_button_press1(event):
    print("Sending button press")
    global buttonPressed
    buttonPressed = 1
    return
buttonY = tk.Button(text="Select Y Position")
def handle_button_press2(event):
    print("Sending button press")
    global buttonPressed
    buttonPressed = 2
    return
buttonGo = tk.Button(text="Select Go Button Position")
def handle_button_press3(event):
    print("Sending button press")
    global buttonPressed
    buttonPressed = 3
    return
buttonTopL = tk.Button(text="Select Top Left Cell Position")
def handle_button_press4(event):
    print("Sending button press")
    global buttonPressed
    buttonPressed = 4
    return
buttonBotR = tk.Button(text="Select Bottom Right Cell Position")
def handle_button_press5(event):
    print("Sending button press")
    global buttonPressed
    buttonPressed = 5
    return
textBoxX = tk.Text(height = 1, width = 5)
def handle_text_X(event):
    global xDef
    xDef = textBoxX.get("1.0",'end-1c')
    xDef = int(xDef)
    print(xDef)
    textBoxX.config(state='disabled')
    return
textBoxY = tk.Text(height = 1, width = 5)
def handle_text_Y(event):
    global yDef
    yDef = textBoxY.get("1.0",'end-1c')
    yDef = int(yDef)
    print(yDef)
    textBoxY.config(state='disabled')
    return
textBoxXo = tk.Text(height = 1, width = 5)
def handle_text_Xo(event):
    global xOffset
    xOffset = int(textBoxX.get("1.0",'end-1c'))
    print(xOffset)
    textBoxXo.config(state='disabled')
    return
textBoxYo = tk.Text(height = 1, width = 5)
def handle_text_Yo(event):
    global yOffset
    yOffset = int(textBoxYo.get("1.0",'end-1c'))
    print(yOffset)
    textBoxYo.config(state='disabled')
    return
buttonEngage = tk.Button(text="Click to start when all values are filled!")
def handle_go(event):
    window.destroy()
    main()
def char_countX(event):
    if event.keysym in {'Return'}:
        return 'break'
    count = len(textBoxX.get('1.0', 'end-1c'))
    if count >= 4 and event.keysym not in {'BackSpace', 'Delete'}:
        return 'break'  # dispose of the event, prevent typing
def char_countY(event):
    if event.keysym in {'Return'}:
        return 'break'
    count = len(textBoxY.get('1.0', 'end-1c'))
    if count >= 4 and event.keysym not in {'BackSpace', 'Delete'}:
        return 'break'  # dispose of the event, prevent typing
def char_countXo(event):
    if event.keysym in {'Return'}:
        return 'break'
    count = len(textBoxXo.get('1.0', 'end-1c'))
    if count >= 4 and event.keysym not in {'BackSpace', 'Delete'}:
        return 'break'  # dispose of the event, prevent typing
def char_countYo(event):
    if event.keysym in {'Return'}:
        return 'break'
    count = len(textBoxYo.get('1.0', 'end-1c'))
    if count >= 4 and event.keysym not in {'BackSpace', 'Delete'}:
        return 'break'  # dispose of the event, prevent typing
textBoxCoords = tk.Text(height = 1, width = 10)
textboxEstim = tk.Text(height = 1, width = 20)
buttonInputX.bind('<Button-1>', handle_text_X)
buttonInputY.bind('<Button-1>', handle_text_Y)
buttonInputXo.bind('<Button-1>', handle_text_Xo)
buttonInputYo.bind('<Button-1>', handle_text_Yo)
buttonX.bind('<Button-1>', handle_button_press1)
buttonY.bind('<Button-1>', handle_button_press2)
buttonGo.bind('<Button-1>', handle_button_press3)
buttonTopL.bind('<Button-1>', handle_button_press4)
buttonBotR.bind('<Button-1>', handle_button_press5)
buttonEngage.bind('<Button-1>', handle_go)
textBoxX.bind('<KeyPress>', char_countX)
textBoxX.bind('<KeyRelease>', char_countX)
textBoxY.bind('<KeyPress>', char_countY)
textBoxY.bind('<KeyRelease>', char_countY)
textBoxXo.bind('<KeyPress>', char_countXo)
textBoxXo.bind('<KeyRelease>', char_countXo)
textBoxYo.bind('<KeyPress>', char_countYo)
textBoxYo.bind('<KeyRelease>', char_countYo)
textBoxX.pack()
buttonInputX.pack()
textBoxY.pack()
buttonInputY.pack()
textBoxXo.pack()
buttonInputXo.pack()
textBoxYo.pack()
buttonInputYo.pack()
buttonX.pack()
buttonY.pack()
buttonGo.pack()
buttonTopL.pack()
buttonBotR.pack()
buttonEngage.pack()
textBoxCoords.pack()
textboxEstim.pack()

# Start the event loop.
window.after(1,windowLoop)
window.mainloop()