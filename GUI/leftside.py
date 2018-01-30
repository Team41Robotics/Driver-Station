from tkinter import *
import math

checkles = [
	"Is the battery charged?",
	"Is everything working?"
]

#Create window
root = Tk()
root.title("GUI")
width = 800
height = 480
#Full screen
'''root.overrideredirect(True)
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
root.focus_set()  #Move focus to this widget
root.bind("<Escape>", lambda e: root.quit())'''
root.geometry("{}x{}".format(width, height))

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

bg = PhotoImage(file="driver_bg.gif")
bg = resize(bg, 1600, 960)
ctx.create_image(0, 0, image=bg)
ctx.pack()

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
def getButtons():
    return {
    "btn": {
        "btn_1": {"x": 77, "y": 304, "title": "Btn 1", "anchor": CENTER},
        "btn_2": {"x": 136, "y": 240, "title": "Btn 2", "anchor": CENTER},
        "btn_3": {"x": 194, "y": 304, "title": "Btn 3", "anchor": CENTER},
        "btn_4": {"x": 136, "y": 365, "title": "Btn 4", "anchor": CENTER},
        "btn_5": {"x": 517, "y":  401, "title": "Btn 5", "anchor": CENTER} #, "ty": 445}
    },
    "clicker": {
        "clicker_1": {"x": 330, "y": clickery, "title": "Clicky 1", "anchor": CENTER},
        "clicker_2": {"x": 458, "y": clickery, "title": "Clicky 2", "anchor": CENTER},
        "clicker_3": {"x": 586, "y": clickery, "title": "Clicky 3", "anchor": CENTER},
        "clicker_4": {"x": 714, "y": clickery, "title": "Clicky 4", "anchor": CENTER}
    },
    "slider": {
        "slider_1": {"x": 594, "y": slidery, "title": "Slider 1", "anchor": N, "ty": 180},
        "slider_2": {"x": 688, "y": slidery, "title": "Slider 2", "anchor": N, "ty": 180}
    }
    }
buttons = getButtons()

def drawButtons():
    #Draw buttons
    for category, elements in buttons.items():
        for tag, coords in elements.items():
            ctx.create_image(coords["x"], coords["y"], image=images[category], anchor=CENTER, tag=tag)
            ty = coords["y"]
            if coords["anchor"] == N: ty = coords["ty"]
            ctx.create_text(coords["x"], ty, text=coords["title"], fill="white", anchor=coords["anchor"], tag=tag + "t")
drawButtons()
#Backup button
btnImg = PhotoImage(file="btn.gif")
btnW = 100
btnH = 50
btnImg = resize(btnImg, btnW, btnH)
backupBtn = {"img": btnImg, "x": 80, "y": 40, "width": btnW, "height": btnH, "title": "Backup", "tag": "backupBtn"}
resetBtn = {"img": btnImg, "x": 80, "y": 100, "width": btnW, "height": btnH, "title": "Reset", "tag": "resetBtn"}
checkBtn = {"img": btnImg, "x": 80, "y": 160, "width": btnW, "height": btnH, "title": "Checklist", "tag": "checkBtn"}

def drawBtn(btn):
        ctx.create_image(btn["x"], btn["y"], image=btn["img"], anchor=CENTER, tag=btn["tag"])
        ctx.create_text(btn["x"], btn["y"], text=btn["title"], anchor=CENTER, fill="white", tag=btn["tag"] + "T")
def deleteBtn(btn):
	ctx.delete(btn["tag"])
	ctx.delete(btn["tag"] + "T")
drawBtn(backupBtn)
drawBtn(resetBtn)
drawBtn(checkBtn)
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
def showChecklist():
	ctx.create_rectangle(0, 0, width, height, fill="white", tag="white")
	ctx.create_text(width/2, 5, text="Checklist", anchor=N, fill="black", tag="checklist")
	i = 1
	for check in checkles:
		ctx.create_text(5, 5 + i * 15, text=str(i) + ". " + check, anchor=NW, fill="black", tag="check")
		i = i + 1
	ctx.create_rectangle(width - 40, height - 40, width, height, fill="red", tag="red")
	ctx.create_text(width - 20, height - 20, text="Exit", fill="white", anchor=CENTER, tag="checklist")
def callback(event):
    global state, changeTag, buttons
    if rectBtn(event.x, event.y, width - 20, height - 20, 40, 40):
    	if state == 3:
    		#Destroy checklist
    		ctx.delete("white")
    		ctx.delete("checklist")
    		ctx.delete("check")
    		ctx.delete("red")
    		state = 0
    	else: root.quit()
    if rectBtn(event.x, event.y, resetBtn["x"], resetBtn["y"], resetBtn["width"], resetBtn["height"]):
        deleteBtn(backupBtn)
        for category, elements in buttons.items():
            for tag, coords in elements.items():
                ctx.delete(tag)
                ctx.delete(tag + "t")
        buttons = getButtons()
        drawButtons()
        drawBtn(backupBtn)
        state = 0
    elif rectBtn(event.x, event.y, checkBtn["x"], checkBtn["y"], checkBtn["width"], checkBtn["height"]):
        state = 0
        deleteBtn(backupBtn)
        drawBtn(backupBtn)
        showChecklist()
        state = 3
    #State 0: Normal state
    elif state == 0 and rectBtn(event.x, event.y, backupBtn["x"], backupBtn["y"], backupBtn["width"], backupBtn["height"]):
        #The user has clicked on the button
        deleteBtn(backupBtn)
        ctx.create_text(backupBtn["x"]-btnW/2, backupBtn["y"], text="Click on a button to replace",
                        anchor=W, fill="white", tag="backupBtnT")
        state = 1
    #State 1: Choosing a button to backup
    elif state == 1:
        clicked = btnClicked(event.x, event.y)
        if clicked: changeTag = clicked
        if len(changeTag) > 0:
            depress(changeTag)
            state = 2
            ctx.delete("backupBtnT")
            ctx.create_text(backupBtn["x"]-btnW/2, backupBtn["y"], text="Click on a button with which to replace it",
                            anchor=W, fill="white", tag="backupBtnT")
    elif state == 2:
        clicked = btnClicked(event.x, event.y)
        if clicked:
            category = clicked.split("_")[0]
            category2 = changeTag.split("_")[0]
            if category == category2:
                ctx.delete(changeTag)
                ctx.delete(changeTag + "t")
                ctx.delete(clicked + "t")
                #ctx.delete(clicked)
                buttons[category][changeTag]["x"] = buttons[category][clicked]["x"]
                buttons[category][changeTag]["y"] = buttons[category][clicked]["y"]
                if buttons[category][changeTag]["anchor"] == N: buttons[category][changeTag]["ty"] = buttons[category][clicked]["ty"]
                #ctx.create_image(buttons[category][changeTag]["x"], buttons[category][changeTag]["y"], image=images[category], anchor=CENTER, tag=changeTag)
                ty = buttons[category][changeTag]["y"]
                if buttons[category][changeTag]["anchor"] == N: ty = buttons[category][changeTag]["ty"]
                ctx.create_text(buttons[category][changeTag]["x"], ty, text=buttons[category][changeTag]["title"], fill="white", anchor=buttons[category][changeTag]["anchor"], tag=changeTag + "t")
                state = 0
                ctx.delete("backupBtnT")
                drawBtn(backupBtn)
            else:
                ctx.delete("backupBtnT")
                ctx.create_text(backupBtn["x"]-btnW/2, backupBtn["y"], text="Error: Incompatible types",
                                anchor=W, fill="white", tag="backupBtnT")
            

ctx.bind("<Button-1>", callback)

root.mainloop()
