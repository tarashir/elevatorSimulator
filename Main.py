# Trevor Arashiro, tarashir, sect H
# running this file creates data to run the elevator simulation with and writes
# it to the file data.txt

from tkinter import *
import math
import random
import copy
import time
import runAI

def widget(data):
    ################# functions for second window of widget if called
    # using widget here because Canvas doesn't have text box input option
    master = Tk()
    master.title("Wean Elevator Simulator 2k17")
    # sets up values to possibly be assigned by textbox input
    timeTotal = StringVar()
    people = StringVar()
    # type values for people and timeTotal
    def typeOption(timeTotal,people):
        typeButton.destroy()
        scaleButton.destroy()
        label.config(text="Time: Time elapsed in simulation" +\
                    "\nPepole: The number of people that enter the building "+\
                    "and take an elevator", justify=LEFT)
        # A function for drawing an input box with a label
        def textBox(text, width, **options):
            Label(master, text=text).pack(side="left") # label for entry box
            entry = Entry(master, width=width, **options) #create box to type in
            entry.pack(side="left")
            return entry
        timeBox = textBox("Time:", 10, textvariable=timeTotal)
        peopleBox = textBox("People:", 10, textvariable=people)
        peopleBox.pack()
        # button to continue
        continueButton = Button(master,text="Continue",width=10,\
                command = lambda: quit(timeTotal,people,err))
        continueButton.pack()
        err = Label(master, text="", justify=CENTER, fg = "red")
        err.pack()
        # skips scales screen because input already taken here
        data.slide = False
        return
    
    # used in continuation with typeOption. Quits screen if values are entered
    def quit(timeTotal,people,err):
        try:
            # does not assign values nor quit until both are ints
            int(timeTotal.get())
            int(people.get())
            timeTotal = int(timeTotal.get())
            people = int(people.get())
            master.destroy()
        # display error text
        except:
            err.config(text = "Please input two integers")
    
    # destroy scene and move to canvas
    def scaleOption():
        master.destroy()
    ################# Set up buttons on first screen
    
    # directions for selecting input type
    label=Label(master,text="To type the number of people and time interval "+\
            "(both numbers must be less than 1040), click 'type'\nTo use a "+\
            "scale to input the number of people and time, click 'scale'",\
            justify=CENTER)
    label.pack()
    # creates buttons to select for type and scale input
    typeButton = Button(master, text="type", width=10,\
                command=lambda: typeOption(timeTotal,people))
    scaleButton = Button(master, text="scale", width=10, command=scaleOption)
    typeButton.pack(side=TOP)
    scaleButton.pack(side=TOP)
    # start drawing stuff
    master.mainloop()
    # turn the string variables into ints if they're string variables
    try:
        timeTotal = int(timeTotal.get())
        people = int(people.get())
    except:
        pass
    return timeTotal,people

################# Screen for everything after widget


def init(data):
    data.boarder = 50 # data.boarder around box to draw in
    data.slider1x=2*data.boarder # people slider
    data.slider2x=2*data.boarder # time slider
    data.slider1y=1.5*data.height/4
    data.slider2y=2.35*data.height/4
    data.sliderRadius = 10
    data.movePeopleSlider = False # was the mouse pressed on slider 1 or 2
    data.moveTimeSlider = False
    data.pointx=[]# canvas coordinates of time
    data.pointy=[]# canvas coordinates of rate at which people are arriving
    data.set=set()
    data.onScreen=True
    data.timerDelay = 10 # refresh rate
    data.slide = True # turns to false once return pressed, leaves slider page
    data.moreText = False # has at least 1 point been entered before continuing
    data.integral = False # turns true when we reload the graph to show integral
    data.press = False # erases warning text after first click on graph
    data.color = "#ffffff" # color for flashing box
    data.time = 0 # used for cos(time) to calculate color hex code
    data.count = False # false till first dot drawn, start incrementing timer
    data.copypx=[]# copy of pointx incase user wants to retry drawing
    data.copypy=[]
    data.color2="#ffffff" # color of text that changed in integral
    data.exit=False # displays exit text and begins calculations
    data.loop2 = False # allows for "exit" text to display before time.sleep
    data.loop3 = False # same as loop2
    data.tooFar = False # are too many people arriving within 1 sec of eachother
    data.ccolor = "green" # red if too many ppl arrive within 1 sec of eachother
    data.brightness = 140 # turn into hex code, brightness of continue button
    data.adjust = False # true if any values changed b/c people arrive to close
    data.lines = 10 # of x and y axis bars
    data.triples = [] # array of tuples of time, floor entry, floor exiting

def mousePressed(event, data, root):
    x = event.x
    y = event.y
    # create a point on the canvas if on draw screen
    if data.slide == False:
        if not data.integral:
            # check if click was in box
            if y>=data.boarder and y<=data.height-data.boarder:
                if x>=data.boarder and x<=data.width-data.boarder:
                    # count and press are diff cuz count is reset with 'esc'
                    data.count = True # start counter 'click to continue' flashs
                    data.press = True
                if not (x - x%2) in data.set:
                    data.pointx+=[x-x%2]
                    data.pointy+=[y]
                    data.set.add(x - x%2)
            # check if continue button was pressed and at least 1 point exists
            elif x>=4*data.width/5-75 and x<=4*data.width/5+75 and \
                y<=data.height-data.boarder+45\
                    and y>data.height-data.boarder+24 and data.count and \
                        data.time>500:
                            dataAdjust(data)
                            data.integral = True # transition to integral screen
                            root.unbind('<B1-Motion>')
                            data.time=0
        # check if continue button pressed on integral page after certain time
        elif x>=4*data.width/5-75 and x<=4*data.width/5+75 and y<=data.height-\
                data.boarder+45 and y>data.height-data.boarder+24 and \
                data.count and data.time>500:
                        # exits screen and opens up options
                        data.exit = True
    else:
        x1=data.slider1x
        x2=data.slider2x
        y1=data.slider1y
        y2=data.slider2y
        # if slider 1 clicked, set move1 to true
        if (x-x1)**2+(y-y1)**2<=data.sliderRadius**2:
            data.movePeopleSlider = True
        else:
            data.movePeopleSlider = False
        # if slider 2 clicked, set move2 to true
        if (x-x2)**2+(y-y2)**2<=data.sliderRadius**2:
            data.moveTimeSlider = True
        else:
            data.moveTimeSlider = False
    
    

#create points on canvas while dragging mouse
def onDrag(event,data):
    # if point x has not already been passed over, add x to set, 
    
    if not (event.x - event.x%2) in data.set:
        # check if mouse still within y boarders
        # not checking if x is still within boarders is more efficient b\c we 
        # can just remove those points after
        if event.y>=data.boarder and event.y<=data.height-data.boarder:
            # if point in box, erase warning text, 
            # start counter for flashing button
            if not data.count and event.x>=data.boarder and\
                event.x<=data.width-data.boarder:
                    # count and press are different cuz count is reset with 
                    # 'esc' start counter so 'click to continue' flashes
                    data.count = True 
                    data.press = True
            data.pointx+=[event.x-event.x%2]
            data.pointy+=[event.y]
            data.set.add(event.x-event.x%2)
        pass
    # if point within y bounds, draw it at current x cuz x already passed over
    elif event.y>=data.boarder and event.y<=data.height-data.boarder:
        data.pointy[data.pointx.index(event.x-event.x%2)]=event.y
        pass
    

# drag the slider left and right
def onDragSlider(event,data):
    if event.x < data.width-2*data.boarder and event.x > 2*data.boarder:
        if data.movePeopleSlider: # move people slider
            data.slider1x=event.x
            # if too many people appearing in one second, move second slider
            if ((data.slider1x-2*data.boarder+1)**1.7//25+1)/((data.slider2x\
                    -2*data.boarder+1)**1.7//25+1)>10:
                # increase slider2x until time*10>people
                while ((data.slider2x-2*data.boarder+1)**1.7//25+1)*10<\
                        (data.slider1x-2*data.boarder+1)**1.7//25+1:
                            data.slider2x+=1
                            
        elif data.moveTimeSlider: # move time slider
            data.slider2x=event.x
        # if too many people appearing in one second, signal to user
        if ((data.slider1x-2*data.boarder+1)**1.7//25+1)/((data.slider2x\
            -2*data.boarder+1)**1.7//25+1)>16:
                data.tooFar = True
                data.ccolor = "red"
        else:
            data.tooFar = False
            data.ccolor = "green"

# move past screen for sliders and reset drawing screen, 
# canvas passed for binding    
def keyPressed(event, data, root):
    # reset drawing screen
    if event.keysym == "Escape" and not data.integral:
        data.count = False
        data.pointx=[]
        data.pointy=[]
        data.set=set()
        data.color = "#ffffff"
    # moves past sliders screen
    elif event.keysym == "Return" and data.slide:
        data.timeTotal = int((data.slider2x-2*data.boarder+1)**1.7//25 + 1)
        data.people = int((data.slider1x-2*data.boarder+1)**1.7//25 + 1)
        # show user their values for people and time
        print("Initially:")
        print("Total time elapsed during simulation=",data.timeTotal,"seconds")
        if data.people == 1:
            print("Total number of people that enter building = 1 person")
        else:
            print("Total number of people that enter building = %i people"%\
                (data.people))
        data.slide = False
        # sliding the mouse now drags the slider instead of drawing dots
        root.bind('<B1-Motion>', lambda event: onDrag(event,data))
    # puts data back to how it was
    elif event.keysym == "Escape" and data.integral:
        data.pointx=data.copypx # assign data.pointx to its values before adjust
        data.pointy=data.copypy


        root.bind('<B1-Motion>', lambda event: onDrag(event,data))
        data.count = True # stops flashing after draw screen
        data.integral = False
        data.adjust = False
        data.time = 0
        data.color = "white"
    pass

#changes color of "continue" text and info on integral page
def timerFired(data, root):
    # flash continue button once timer past certain point
    if data.time > 500:
        # red and blue color hex values for continue button color
        rbcolor="%02x"%int(122*math.cos((data.time-500)/130)+122)
        # green hex value
        gcolor="%02x"%int((255-data.brightness)*int(rbcolor, 16)/255+\
                data.brightness)
        data.color="#"+rbcolor+gcolor+rbcolor
    # once first dot created, start timer this is incremented after above
    # if statement so 'esc' reset function works properly
    if data.count:
        data.time+=data.timerDelay
    else:
        data.color = "#ffffff"
    # color of info on integral page.  starts white goes blue
    if data.integral:
        data.time+=data.timerDelay
        data.color2="#"+("%02x"%int(251//(1+(data.time/1100+0.5)**13.5)+5))*2+\
                        "ff"
    # close window
    if data.exit and data.integral:
        if data.loop2:
            # loop 3 is to prevent glitches.  Sometimes, tkinter won't have time
            # to update graphics on screen before re-calling timerFired
            if data.loop3:
                time.sleep(0)
                root.destroy()
            data.loop3 = True
        # ensures text displays before sleep and destroy
        data.loop2 = True

def redrawAll(canvas, data):
    # slider screen
    if data.slide:
        x1=data.slider1x
        x2=data.slider2x
        y1=data.slider1y
        y2=data.slider2y
        # draw directions for how to use sliders
        canvas.create_text(data.width/2,105, text="Adjust the top slider to"+\
                        " adjust the total number of people that\nenter the"+\
                        " building. Adjust the bottom slider to adjust the\n"+\
                        "total time that elapses during the simulation.  "+\
                        "Please ensure that \nno more than 20 people arrive "+\
                        "within 1 second of eachother.\nIn general, try to "+\
                        "keep total people <= 18*total time\n*Bottom* slider "+\
                        "adjusts to *attempt* to ensure that no more than\n"+\
                        "20 people arrive within 1 second of eachother", \
                        anchor = CENTER, font="helvetica 13", fill = "#587272",\
                        justify = "center")
        # draw population slider and text
        canvas.create_oval(x1-data.sliderRadius,y1-data.sliderRadius,\
                        x1+data.sliderRadius,y1+data.sliderRadius,fill="orange")
        canvas.create_line(2*data.boarder,y1,data.width-2*data.boarder,y1)
        
        # in the case that there is one PERSON, type person
        if (x1-2*data.boarder+1)**1.5//25==0:
            canvas.create_text(data.width/2,y1+30,text="Total number of "+\
                            "people to enter building = 1 person",anchor=\
                            CENTER,font="helvetica 15", fill = data.ccolor)
        # in the case that there is > 1 person, type PEOPLE
        else:
            canvas.create_text(data.width/2,y1+30,text="Total number of "+\
                            "people to enter building = %i people"\
                            %((x1-2*data.boarder+1)**1.7//25+1),anchor=CENTER,\
                            font="helvetica 15", fill = data.ccolor)
        # draw time duration slider and text
        canvas.create_oval(x2-data.sliderRadius,y2-data.sliderRadius,\
                    x2+data.sliderRadius,y2+data.sliderRadius,fill="#203737")
        canvas.create_line(2*data.boarder,y2,data.width-2*data.boarder,y2)
        canvas.create_text(data.width/2, y2+30, text="Total amount of time"+\
                    " till last person enters the building = "+\
                    "%is" %((x2-2*data.boarder+1)**1.7//25 + 1),\
                    anchor = CENTER, font="helvetica 15", fill = data.ccolor)
        # press enter to continue
        canvas.create_text(data.width/2, y2+120,text="Press enter to continue",\
                        anchor = CENTER, font="helvetica 15")
        if data.tooFar:
            canvas.create_text(data.width/2, y2-50,text="Time elapsed during "+\
                            "simulation will be adjust by some amount",\
                            anchor = CENTER,justify = CENTER,\
                            font = "helvetica 11 bold", fill = "red")
        pass
    # after enter has been pressed, this draws the function
    else:
        # directions for drawing on draw screen
        if not data.integral:
            canvas.create_text(data.width / 2, data.boarder / 2,
                            text="Click and drag mouse to draw a function. The"\
                            +" x axis is time and the y axis is the\nrate at"+\
                            " which people arrive at that time.  Press "+\
                            "'esc' to redraw", anchor = CENTER,justify=CENTER,\
                            font = "helvetica 11", fill = "blue")
        else:
            # desc of second graph
            canvas.create_text(data.width / 2, data.boarder / 2,
                            text="Each point now represents a person entering"+\
                            " the building at the point's\ncorresponding time"+\
                            ".  Press 'esc' to redraw the function.",\
                            anchor = CENTER, font="helvetica 11", \
                            fill = data.color2, justify = "center")
        #draw a bounding box so the person knows where to draw
        canvas.create_rectangle(data.boarder,data.boarder,data.width-\
                data.boarder,data.height-data.boarder,width= 4)
        # draw grid data.lines and time incriments and warning text if 
        # data had to be adjusted
        for i in range(data.lines):
            for j in range(data.lines):
                side=(data.width-2*data.boarder)/(data.lines)
                x=side*i+side
                y=side*j+side
                canvas.create_rectangle(x,y,x+side,y+side)
            side=(data.width-2*data.boarder)/(data.lines)
            if not data.adjust:
                canvas.create_text(data.boarder+side*(i+1),data.height-\
                        data.boarder+12,text = "%.2f"%((i+1)/data.lines*\
                        data.timeTotal),font="helvetica 10", fill = "black")
            # if timeTotal been adjusted due to pepole arriving too closely
            else:
                # make sure index isnt in list to check if any points can
                # possibly interfere
                index = -1
                # make sure text doesnt clash with warning text
                for point in data.pointx:
                    # find last point that can clash with text WRT x coordinate
                    if point > 300:
                        index = data.pointx.index(point)
                        break
                # draw adjust warning text top right
                if index != -1 and data.pointy[index] > 300:
                    # draw background box for text
                    canvas.create_rectangle(3*data.boarder/2-16,\
                                    3*data.boarder/2-13,\
                                    3*data.boarder/2+236,3*data.boarder/2+106,\
                                    fill = "red")
                    canvas.create_rectangle(3*data.boarder/2-12,\
                                    3*data.boarder/2-9,\
                                    3*data.boarder/2+232,3*data.boarder/2+102,\
                                    fill = "white")
                    canvas.create_text(3*data.boarder/2+1,3*data.boarder/2,\
                        text="DUE TO TOO MANY PEOPLE\nARRIVING AT ONE TIME, "+\
                        "THE\nLAST PERSON WILL NOW\nENTER THE BUILDING\nAT "+\
                        "%.3f SECONDS" %(data.triples[len(data.triples)-1][0]),\
                        anchor = NW, font="Times 13", fill = "black",\
                        justify = CENTER)
                # draw adjust warning text bottom right
                elif index == -1 or data.pointy[index] > 60:
                    # draw red background box for adjust warning text
                    canvas.create_rectangle(data.width-data.boarder-261,\
                                    data.width-data.boarder-128,\
                                    data.width-data.boarder-10,\
                                    data.width-data.boarder-13,\
                                    fill = "red")
                    # draw white background box for adjust warning text
                    canvas.create_rectangle(data.width-data.boarder-257,\
                                    data.width-data.boarder-124,\
                                    data.width-data.boarder-14,\
                                    data.width-data.boarder-17,\
                                    fill = "white")
                    canvas.create_text(data.width-3*data.boarder/2+1,\
                        data.height-3*data.boarder/2+3,text="DUE TO TOO MANY "+\
                        "PEOPLE\nARRIVING AT ONE TIME, THE\nLAST PERSON WILL "+\
                        "NOW\nENTER THE BUILDING\nAT %.3f SECONDS"\
                        %(data.triples[len(data.triples)-1][0]), anchor = SE,\
                        font="Times 13", fill = "black", justify = CENTER)
                canvas.create_text(data.boarder+side*(i+1),data.height-\
                        data.boarder+12,text="%.2f"%((i+1)/data.lines*\
                        data.triples[len(data.triples)-1][0]),\
                        font="helvetica 10"+" bold", fill = "red")
                
        # draw the points on the graph
        # if too many dots, only draw so many
        if len(data.pointx) > 1500:
            step = int(len(data.pointx)//750)
        else:
            step = 1
        for j in range(0,len(data.pointx),step):
            canvas.create_oval(data.pointx[j]-1,data.pointy[j]-1,\
                            data.pointx[j]+1,data.pointy[j]+1, outline="green",
                            fill = "green")
        # draw x axis title
        canvas.create_text(data.width/2,data.height-data.boarder+32,\
                        text="Time (s)",font="helvetica 14", fill = "#203737")
        # draw y axis title dp/dt if on drawing screen
        if not data.integral:
            canvas.create_text(23,data.height/2,text="Rate of building "+\
                            "population increase",font="helvetica 14",\
                            fill="#203737",angle=90, anchor="center")
        # draw y axis as time if on integral screen
        else:
            canvas.create_text(23,data.height/2,text="Number of people that "+\
                            "have entered the building",font="helvetica 14",\
                            fill="#203737", angle=90, anchor="center")
        if not data.press:
            # draw background boxes behind warning click text
            canvas.create_rectangle(data.boarder+17,210,data.width-\
                            data.boarder-22,390,fill="red")
            canvas.create_rectangle(data.boarder+23,216,data.width-\
                            data.boarder-28,384,fill="white")
            # prompt user to click in square
            canvas.create_text(data.width/2+1,data.height/2,\
                           text = "Only points drawn in bounding \nbox will "\
                           "be used!\nPlease click at least 1 point\nin the "+\
                           "box",anchor = CENTER, font="helvetica 25",\
                           fill="black",justify = CENTER)
        # continue button, draw rectangle and text
        if data.time > 1000 or not data.integral:
            canvas.create_rectangle(4*data.width/5-75,data.height-data.boarder+\
                    42,4*data.width/5+75,data.height-data.boarder+25,width=3,\
                    outline=data.color)
            canvas.create_text(4*data.width/5,data.height-data.boarder+34, 
                    text = "Click here to continue",font="helvetica 10",\
                    fill=data.color)
        pass


def main(width, height):
    ## run function for drawing
    ## adapted from https://www.cs.cmu.edu/~112/notes/hw6.html
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, data):
        mousePressed(event, data, root)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, data):
        keyPressed(event, data, root)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data, root)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width # width of canvas
    data.height = height # height of canvas
    init(data)
    # returns timeTotal and people.  Don't run widget till now because we must
    # check if the user used the scale or typing option for data input
    data.timeTotal,data.people = widget(data)
    # if used typing option, show print values for time and people
    if isinstance(data.timeTotal,int):
        print("Initially:")
        print("Total time elapsed during simulation =",data.timeTotal,"seconds")
        if data.people == 1:
            print("Total number of people that enter building = 1 person")
        else:
            print("Total number of people that enter building = %i people"%\
                (data.people))
    # create the root and the canvas
    root = Tk()
    root.title("Wean Elevator Simulator 2k17")
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, data))
    timerFiredWrapper(canvas, data)
    # if data input through widget, start at next screen w/ new bind
    if not data.slide: 
        root.bind('<B1-Motion>', lambda event: onDrag(event,data))
    else:
        root.bind('<B1-Motion>', lambda event: onDragSlider(event,data))
    # and launch the app
    root.mainloop()  # blocks until window is closed
    # write to file
    writeToFile(data.triples,data.people)

## fix point array
def dataAdjust(data):
    data.copypx = copy.deepcopy(data.pointx)
    data.copypy = copy.deepcopy(data.pointy)
    #remove points drawn outside the frame
    i = 0
    while i < len(data.pointx):
        if data.pointx[i] < data.boarder or data.pointx[i] > \
            data.width-data.boarder:
                data.pointy.pop(i)
                data.pointx.pop(i)
                i-=1
        i+=1
    def merge(a, start1, start2, end):
        index1 = start1
        index2 = start2
        length = end - start1
        aux = [None] * length
        for i in range(length):
            if ((index1 == start2) or
                ((index2 != end) and (a[index1] > a[index2]))):
                aux[i] = a[index2]
                index2 += 1
            else:
                aux[i] = a[index1]
                index1 += 1
        for i in range(start1, end):
            a[i] = aux[i - start1]
    
    #copy of data.pointx for use in sorting data.pointy
    cpy = copy.deepcopy(data.pointx)
    #sort data.pointx
    def mergeSort(a):
        n = len(a)
        step = 1
        while (step < n):
            for start1 in range(0, n, 2*step):
                start2 = min(start1 + step, n)
                end = min(start1 + 2*step, n)
                merge(a, start1, start2, end)
            step *= 2
    mergeSort(data.pointx)
    # copy of data.pointy for use in sorting data.pointy
    cpy2= copy.deepcopy(data.pointy)
    # sort data.pointy by moving each element to where its corresponding value 
    # in data.pointx moved to
    for i in range (len(cpy)):
        cpy2[i]=data.pointy[data.pointx.index(cpy[i])]
    data.pointy=cpy2
    
    # changes coordinates to our perspective (canvas coordinates are inverted)
    for i in range(len(data.pointy)):
        data.pointy[i]=data.height-data.pointy[i]
    # adds a point between points that are a large x distance apart
    def smooth():
        i = 0
        while i < len(data.pointx)-1:
            if data.pointx[i+1]-data.pointx[i] > 2:
                data.pointx.insert(i+1,(data.pointx[i]+data.pointx[i+1])/2)
                data.pointy.insert(i+1,(data.pointy[i]+data.pointy[i+1])/2)
                i = i-1
            i+=1
    smooth()
## create times and floors for arrival and departure calculate integral
    
    area = sum(data.pointy)
    time2=[] # when people arrive.  Last time is last dot on graph
    i=1 # go through the numbering of people in the order they arrive
    partialArea = data.pointy[0] # sum of dots we've checked so far
    x=0
    while i <= data.people:
        # basically taking integral from 0 until 
        # areaintegrated/totalarea=person/totalpeople
        while area*i>partialArea*data.people:
            x+=1
            partialArea+=data.pointy[x]
        # change canvas coordinates proportionally to time
        time2+=[(data.pointx[x]-data.boarder)*data.timeTotal\
            /(data.width-data.boarder*2)] 
        i+=1
    
    # probability of a person entering or exiting on a floor sum to 100 
    one = 8
    two = 4
    three = 4
    four = 20
    five = 31
    six = 10
    seven = 15
    eight = 8
        
    def floor():
        num= random.randint(1,one+two+three+four+five+six+seven+eight)
        if num <= one:
            return 1
        if num <= one + two:
            return 2
        if num <= one + two + three:
            return 3
        if num <= one + two + three + four:
            return 4
        if num <= one + two + three + four + five:
            return 5
        if num <= one + two + three + four + five + six:
            return 6
        if num <= one + two + three + four + five + six + seven:
            return 7
        if num <= one + two + three + four + five + six + seven + eight:
            return 8
    data.triples = []
    for i in range(data.people):
        # generate random floor to enter and exit on
        entry = floor()
        exit = floor()
        # ensure no person gets on and leaves on same floor
        while entry==exit:
            exit = floor()
        # add people to list
        data.triples+=[[time2[i],entry,exit]]
        
   
    # adjusts y and x so that they fit the graph and shows integral
    data.pointy=[(data.height-data.boarder-range(1,data.people+1)[i]*\
        (data.height-2*data.boarder)/data.people) for i in range(data.people)]
    data.pointx=[(data.triples[i][0]*(data.width-data.boarder*2)\
        /data.timeTotal+data.boarder) for i in range(data.people)]
    # ensures no two people arrive within 0.04 seconds of eachother 
    def tooClose(n):
        found = False
        for i in range (n,data.people-1):
            if data.triples[i+1][0]-data.triples[i][0]<=0.05:
                if not found:
                    k=i
                data.triples[i+1][0]+=0.05001+(i-k)/10000
                found = True
                data.adjust = True
        if found:
            return tooClose(k)
    tooClose(0)
    if data.adjust:
        print("\033[1m" + "*"*50 + "\033[4m" + "\nDUE TO TOO MANY "+\
            "PEOPLE ARRIVING AT ONE TIME,\nTHE LAST PERSON WILL "+\
            "NOW ENTER THE BUILDING AT %.3f SECONDS\n"\
            %(data.triples[len(data.triples)-1][0])+\
            "*" * 50 + "\033[0m")

################# Write data to file
# write data to file
def writeToFile(triples,people):
    # if no points drawn, dont write to file
    if len(triples) == 0:
        return
    f = open('data.txt','w')
    f.write('')
    f.close()
    f = open('data.txt','a')
    for i in range(people-1):
        # joins list row into string to be printed to file
        f.write(','.join([(str(triples[i][j])) for j in range(3)])+"\n")
    f.write(','.join([(str(triples[people-1][j])) for j in range(3)]))
    f.close()

#################

main(600, 600)
runAI.main()