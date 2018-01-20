from tkinter import *
import math

#Create window
root = Tk()
root.title("GUI")
width = 800
height = 480
#Full screen
root.overrideredirect(True)
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
root.focus_set()  #Move focus to this widget
root.bind("<Escape>", lambda e: root.quit())

#Create canvas
ctx = Canvas(root, width=width,
             height=height, background="#808080")
ctx.pack()

def resize(photo, w, h):
    scale = (min(w / photo.width(), h / photo.height()))
    if scale > 1:
        scale = math.floor(scale)
        #print("Zoom in " + str(scale) + "x")
        photo = photo.zoom(scale)
    elif scale < 1:
        scale = math.ceil(1 / scale)
        #print("Zoom out " + str(scale) + "x")
        photo = photo.subsample(scale)
    return photo
    
#Load buttons
btn = PhotoImage(file="button.gif")
btnDep = PhotoImage(file="button_depressed.gif")
clicker = PhotoImage(file="click.gif")
clickerDep = PhotoImage(file="click_depressed.gif")
slider = PhotoImage(file="slider.gif")
sliderEmp = PhotoImage(file="slider_fill.gif")
logo = PhotoImage(file="whrhs_logo.gif")
logo = resize(logo, 40, 40)
ctx.create_image(width - 5, height - 5, image=logo, anchor=SE, tag="logo")

#Resize buttons
btnW = 72
clickerW = 75
clickerH = 10000
sliderW = 43
sliderH = 144
btn = resize(btn, btnW, btnW)
btnDep = resize(btnDep, btnW, btnW)
clicker = resize(clicker, clickerW, clickerH)
clickerDep = resize(clickerDep, clickerW, clickerH)
slider = resize(slider, sliderW, sliderH)
sliderEmp = resize(sliderEmp, sliderW, sliderH)
clickery = 287
slidery = 99
images = {"btn": btn, "clicker": clicker, "slider": slider}
depressed = {"btn": btnDep, "clicker": clickerDep, "slider": sliderEmp}
buttons = {
    "btn": {
        "btn_1": {"x": 77, "y": 304, "title": "Btn 1", "color": "white", "anchor": CENTER},
        "btn_2": {"x": 136, "y": 240, "title": "Btn 2", "color": "white", "anchor": CENTER},
        "btn_3": {"x": 194, "y": 304, "title": "Btn 3", "color": "white", "anchor": CENTER},
        "btn_4": {"x": 136, "y": 365, "title": "Btn 4", "color": "white", "anchor": CENTER},
        "btn_5": {"x": 517, "y":  401, "title": "Btn 5", "color": "white", "anchor": CENTER} #, "ty": 445}
    },
    "clicker": {
        "clicker_1": {"x": 330, "y": clickery, "title": "Clicky 1", "color": "white", "anchor": CENTER},
        "clicker_2": {"x": 458, "y": clickery, "title": "Clicky 2", "color": "white", "anchor": CENTER},
        "clicker_3": {"x": 586, "y": clickery, "title": "Clicky 3", "color": "white", "anchor": CENTER},
        "clicker_4": {"x": 714, "y": clickery, "title": "Clicky 4", "color": "white", "anchor": CENTER}
    },
    "slider": {
        "slider_1": {"x": 594, "y": slidery, "title": "Slider 1", "color": "black", "anchor": N, "ty": 180},
        "slider_2": {"x": 688, "y": slidery, "title": "Slider 2", "color": "black", "anchor": N, "ty": 180}
    }
}

#Draw buttons
for category, elements in buttons.items():
    for tag, coords in elements.items():
        ctx.create_image(coords["x"], coords["y"], image=images[category], anchor=CENTER, tag=tag)
        ty = coords["y"]
        if coords["anchor"] == N: ty = coords["ty"]
        ctx.create_text(coords["x"], ty, text=coords["title"], fill=coords["color"], anchor=coords["anchor"], tag=tag + "t")

#Backup button
buttonX = 134
buttonY = 63
buttonW = 100
buttonH = 50

def drawBackup():
	ctx.create_rectangle(buttonX - buttonW/2, buttonY - buttonH/2,
                buttonX + buttonW/2, buttonY + buttonH/2, fill="gray",
                tag="backupBtn")
	ctx.create_text(buttonX, buttonY, text="Backup", anchor=CENTER, fill="white",
                tag="backupTxt")

drawBackup()

#Establish backup functionality
state = 0
changeTag = ""
def circleBtn(mouseX, mouseY, circleX, circleY, circleR):
    dx = circleX - mouseX
    dy = circleY - mouseY
    return math.sqrt(dx*dx + dy*dy) < circleR
def rectBtn(mouseX, mouseY, rectX, rectY, rectW, rectH):
    return mouseX < rectX + rectW/2 and mouseX > rectX - rectW/2 and mouseY < rectY + rectH/2 and mouseY > rectY - rectH/2
def btnClicked(x, y):
    btnR = btn.width()/2
    clkW = clicker.width()
    clkH = clicker.height()
    sldW = slider.width()
    sldH = slider.height()
    for tag, coords in buttons["btn"].items():
        if circleBtn(x, y, coords["x"], coords["y"], btnR): return tag
    for tag, coords in buttons["clicker"].items():
        if rectBtn(x, y, coords["x"], coords["y"], clkW, clkH): return tag
    for tag, coords in buttons["slider"].items():
        if rectBtn(x, y, coords["x"], coords["y"], sldW, sldH): return tag
    return False
def depress(tag):
    category = tag.split("_")[0]
    ctx.delete(tag)
    ctx.create_image(buttons[category][tag]["x"], buttons[category][tag]["y"], image=depressed[category], anchor=CENTER, tag=tag)
def callback(event):
    global state, changeTag
    #State 0: Normal state
    if state == 0 and rectBtn(event.x, event.y, buttonX, buttonY, buttonW, buttonH):
        #The user has clicked on the button
        ctx.delete("backupBtn")
        ctx.delete("backupTxt")
        ctx.create_text(buttonX, buttonY, text="Click on a button to replace",
                        anchor=CENTER, fill="black", tag="backupTxt")
        state = 1
    #State 1: Choosing a button to backup
    elif state == 1:
        clicked = btnClicked(event.x, event.y)
        if clicked: changeTag = clicked
        if len(changeTag) > 0:
            depress(changeTag)
            state = 2
            ctx.delete("backupTxt")
            ctx.create_text(buttonX, buttonY, text="Click on a button with which to replace it",
                            anchor=CENTER, fill="black", tag="backupTxt")
    elif state == 2:
        clicked = btnClicked(event.x, event.y)
        if clicked:
            ctx.delete(changeTag)
            ctx.delete(changeTag + "t")
            ctx.delete(clicked + "t")
            ctx.delete(clicked)
            category = clicked.split("_")[0]
            buttons[category][changeTag]["x"] = buttons[category][clicked]["x"]
            buttons[category][changeTag]["y"] = buttons[category][clicked]["y"]
            if buttons[category][changeTag]["anchor"] == N: buttons[category][changeTag]["ty"] = buttons[category][clicked]["ty"]
            ctx.create_image(buttons[category][changeTag]["x"], buttons[category][changeTag]["y"], image=images[category], anchor=CENTER, tag=changeTag)
            ty = buttons[category][changeTag]["y"]
            if buttons[category][changeTag]["anchor"] == N: ty = buttons[category][changeTag]["ty"]
            ctx.create_text(buttons[category][changeTag]["x"], ty, text=buttons[category][changeTag]["title"], fill=buttons[category][changeTag]["color"], anchor=buttons[category][changeTag]["anchor"], tag=changeTag + "t")
            state = 0
            ctx.delete("backupTxt")
            drawBackup()
            

ctx.bind("<Button-1>", callback)

root.mainloop()
