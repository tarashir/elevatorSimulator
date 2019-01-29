# Trevor Arashiro, tarashir, sect H
import fileinput
import re
import math
import copy
from tkinter import *
import Person
import Elevator

def main():
    # customize how the AI solves the problem
    def widget():
        parent = Tk()
        parent.title("Options For Simulation conditions")
    
    
        # use floor number buttons to call elevator instead of arrows. This
        # allows us to check if the elevator is full
        checkIfFull=[0,1]
        # if heading towards target, if passes floor with someone with
        # elevator.dir, pick them up and forget about target if passenger's exit
        # is past target
        forgetTargetAndPickUp=[0,1]
        # uses the function I wrote to pick a target 
        # that minimizes the longest wait time
        chooseComplexTarget=[0,1]
        # CAN NOT HAVE BOTH "pickTarget..." AND "scanFloorD..."
        # if elevator is paused and empty, find a target instead of just looking 
        # for longest waiting on floor
        pickTargetDontPrioritizeFloor=[0,1]
        # if empty, see who has been waiting longest on the floor
        # (if anyone on it) and then set self.dir to that person's dir
        scanFloorDontContInDir=[1,0]
        
        # the text for each option in the panel
        text=[]
        text+=["Using floor number buttons to call elevators instead of\n"+\
                "arrows allows us to check if an elevator is full at any time."]
        text+=["When NOT enabled, if the elevator is heading for its target "+\
                "and it\nis not currently moving in same direction that it "+\
                "will after picking up its\ntarget, the elevator will always "+\
                "stop on the target's\nfloor.  It then picks the target up."]
        text+=["Assign targets in an efficient manner. Decreases the longest "+\
                "waiting\ntime for 90% of mid-sized data sets and tends to "+\
                "decrease avg\nwaiting time for large data sets."]
        text+=["If the elevator is paused and empty, search all floors for a"+\
                "\ntarget rather than just finding the longest waiting\n"+\
                "person on the current floor.\n*this option and option 5 "+\
                "cannot both be 1 ON THE SAME LOOP*"]
        text+=["When enabled, if an elevator becomes empty, it searches the\n"+\
                "current floor for the longest waiting person and if it finds"+\
                " someone,\nit assigns them as the current target."]
        
        
        # options for the user to try in algorithm
        variables = [checkIfFull,forgetTargetAndPickUp,chooseComplexTarget,\
                    pickTargetDontPrioritizeFloor,scanFloorDontContInDir]
        list = [[],[],[],[],[]]
        row = 1
        # left top most general desc text
        Label(text="Click the buttons on right to toggle the loop(s) for "+\
                    "which a method\nis executed  e.g. [1,0] means the "+\
                    "corresponding method is executed\non the first loop "+\
                    "but not the second. See README for more info",\
                    relief=RIDGE,width=57,height=4,\
                    font="helvetica 14").grid(row=0,column=0,pady=10,padx=15)
        Label(text="Click the\nbuttons below!",relief=RIDGE,width=19,height=4,\
            font = "helvetica 14").grid(row=0,column=1,padx = 15)
        def toggle(button):
            # button[0] is the button and button[1] is the variable
            # update the loops the method will execute in
            if button[1] == [0,0]:
                button[1][0] += 1
            elif button[1] == [1,0]:
                button[1][0] -= 1
                button[1][1] += 1
            elif button[1] == [0,1]:
                button[1][0] += 1
            else:
                button[1][0] -= 1
                button[1][1] -= 1
            # update text shown
            button[0].configure(text = "%s"%button[1])
        for i in range(5):
            Label(text="%s"%text[i],relief=RIDGE,width=57,height=5,\
                font="helvetica 14").grid(row=row,column=0)
            # This part of the code is insane. list[i] is the ith button from 
            # the top right along with its corresponding variable in a list.
            # We cant just call lambda: toggle(list[i]) because lambda will call
            # toggle with list[4] as its argument.  Hence we must give each
            # list element its own unique default argument, a pointer to some
            # element of list[i]
            list[i]+=[Button(parent,text="%s"%variables[i],width=17,\
                    height = 4,font = "helvetica 14",\
                    command = lambda q=list[i]: toggle(q)),variables[i]]
            list[i][0].grid(row=row,column=1)
            row+=1
        
        # a[i] and b[i] cant both be 1, this won't allow a 
        # quit unless theyre different
        def quit(a,b,err):
            for i in [0,1]:
                if a[i]==b[i]==1:
                    err.config(text="OPTIONS 4 AND 5 CAN'T BOTH\nBE 1"+\
                            "ON THE SAME LOOP")
                    return
            parent.destroy()
            
        err = Label(parent, text="",justify=CENTER,font="helvetica 14",fg="red")
        err.grid(row=row)
        # exit set up screen and begin simulation
        continueButton=Button(parent,text="Continue",font="helvetica 14",
                width=17,height = 3, command = lambda:\
                quit(pickTargetDontPrioritizeFloor,scanFloorDontContInDir,err))
        continueButton.grid(row=row,column=1,pady=10)
        
        # start drawing stuff
        parent.mainloop()
        for i in [0,1]:
            # if the person manually exited the window, make sure these two
            # are not both one on either loop
            if pickTargetDontPrioritizeFloor[i]==scanFloorDontContInDir[i]==1:
                return False
        return [checkIfFull,forgetTargetAndPickUp,chooseComplexTarget,\
                pickTargetDontPrioritizeFloor,scanFloorDontContInDir]
        
    ###### import file
    people = []
    def initialize(people,elevators):
        fileinput.close()
        file=fileinput.input("data.txt") # pull file with data on it
        # assign people to the array with each entry as a line in the file
        for i in file:
            people+=[re.split(',|\n',i)] # split each line at ',' and \n
            # split at \n causes blank element
            if len(people[fileinput.lineno()-1])==4: 
                people[fileinput.lineno()-1].pop(3) # removes blank element
        fileinput.close() # closes file to allow for rerun and rethread
        for i in range(len(people)):
            people[i][0]=float(people[i][0]) # float time
            people[i][1]=int(people[i][1]) # int floors
            people[i][2]=int(people[i][2])
        # if any elevators in list, remove and replace with new elevators
        for i in range(2,-1,-1):
            if i < len(elevators):
                elevators.pop(i)
        for i in range(3):
            elevators += [Elevator.Elevator(4+i,0,[],(width/2-58+43*i),\
                        height,dt,len(people)/people[len(people)-1][0])]
    #### set up simulation conditions
    width = 400 # canvas width
    height = 400 # canvas height
    dt = 0.05 # amount of time that passes each frame
    elevators = []
    longestWait = []
    options = [] # options for running AI
    avgWait = []
    fQue = [([[],[]]) for i in range (9)]
    masterQueue=[]
    leaveQue= []
    secondGo = False # true when second loop of simulation
    # probability of a person entering or exiting on a floor, sum to 100 
    one = 8
    two = 4
    three = 4
    four = 20
    five = 31
    six = 10
    seven = 15
    eight = 8
    
    
    ####### helper functions
    
    # check if elevator is close to floor, defaults to checking if elev.floor
    # is near an int
    def nearFloor(elevator,floor=None):
        if floor == None:
            if abs(elevator.floor-round(elevator.floor))<=elevator.dy/6:
                return True
            return False
        else:
            if abs(floor-elevator.floor)+0.000000001<=elevator.dy/2:
                return True
            return False
    
    # check if anyone exists on the floor
    def floorEmpty(floor):
        if fQue[floor][0] == [] and fQue[floor][1] == []:
            return True
        return False
    
    # add new people to masterQueue
    def queueAdd(person):
        floor=person[1]
        # 0 is down 1 is up
        dir=int(((person[2]-person[1])/abs((person[2]-person[1]))+1)/2)
        index=len(fQue[floor][dir])
        x = 300 + index*8 # calculated queue position of circles on screen
        y = height-floor*data.convert-8-dir*8 # calculate height of dot
        human = Person.Person(person[0],person[1],person[2],x,y)
        # add this object to both the fQue and masterQueue's
        masterQueue.append(human)
        fQue[floor][dir].append(human)
    
    def targetFloorPickUp(elevator,floor,masterQueue,fQue,data):
        if elevator.isTargetFloor(floor):
            if not elevator.wasLastFrame():
                elevator.pause()
            # forces target into elevator..
            # Be honest, if you were waiting that long you'd
            # go into that elevator even if it had 20 people
            elevator.floorExitQue+=[elevator.target.exit] # add floor to que
            # removes target from master and floor queues
            elevator.people+=[elevator.target]
            # these two checks are incase the target was picked up this frame
            if elevator.target in masterQueue:
                masterQueue.pop(masterQueue.index(elevator.target))
            if len(fQue[floor][int(round((elevator.targetDir+1)/2))])>0:
                fQue[floor][int(round((elevator.targetDir+1)/2))].pop(0)
            # changes direction of elevator to target dir
            elevator.dir = elevator.targetDir
            elevator.ppl+=1 #increases population of elevator by 1
            # remove target from list of targets
            if elevator.target in data.targets:
                data.targets.pop(data.targets.index(elevator.target))
            # moves target visually into elevator
            elevator.target.moveIntoElevator(elevator.x+8*((elevator.ppl-1)%4),\
                        elevator.height-(elevator.floor+1)*elevator.convert+\
                        8*((elevator.ppl-1)//4))
            elevator.target = None
            for i in range(len(fQue[floor][int((elevator.dir+1)/2)])):
                fQue[floor][int((elevator.dir+1)/2)][i].x-=8
            if elevator.dirMatch(fQue[floor],data.time):
                elevator.pickUp(data.totalPeople,data.time,data.longestWait,\
                        data.avgWait,fQue[floor],masterQueue,data.targets)
            else:
                return True
        else:
            if elevator.dirMatch(fQue[floor],data.time):
                # speeds it up by knowing whether or not elevator full
                if data.checkIfFull:
                    if elevator.isFull():
                        return True
                if not elevator.wasLastFrame():
                    elevator.pause()
                elevator.pickUp(data.totalPeople,data.time,data.longestWait,\
                            data.avgWait,fQue[floor],masterQueue,data.targets)
                # checks if dest of anyone in elevator is past target.
                elevator.destPastTarget(data.targets)
            else:
                return True
        return False
        
    # the sole purpose of this helper function is to make the code more readable
    # because of the massive indents and line cuts that would normally be 
    # required
    def helperFunction(elevator,fQue,floor,data,masterQueue):
        # slows it down, if executed, 
        # finds person waiting longest on floor
        if data.scanFloorDontContInDir or elevator.dir==0:
            # find person waiting longest on floor 
            # then cont w/ elevator.dir = that dir
            if len(fQue[floor][0]) != 0:
                if len(fQue[floor][1]) != 0:
                    # if ps going down waited longer
                    if fQue[floor][0][0].time<fQue[floor][1][0].time:
                        elevator.dir = -1
                    else:
                        elevator.dir = 1
                else:
                    elevator.dir = -1
            # cuz floor isn't empty and down que is, 
            # up que must have people
            else:
                elevator.dir = 1
        # if executed, complex finds target instead of continuing in dir and 
        # then goes in that dir.  in this case, cant stop from going past target
        # if someone gets on going past target and elev.dir != target.dir
        if data.pickTargetDontPrioritizeFloor:
            elevator.assignTarget(data.targets,masterQueue,\
                    data.chooseComplexTarget,elevators,fQue)
        if elevator.dirMatch(fQue[floor],data.time):
            elevator.pickUp(data.totalPeople,data.time,data.longestWait,\
                data.avgWait,fQue[floor],masterQueue,data.targets)
            return True
        else: 
            return True
        
##

    
    class Struct(object): pass
    data=Struct()
    def init(data):
        data.height=height
        data.width=width
        data.timerDelay = 1
        # height of elevator, floors, boarder, and conversion from lvl to pixels
        data.convert = data.height/10
        data.time = 0 # time that has passed since simulation started
        data.simPause = False # is the simulation paused?
        data.targets = [] # list of target for each elevator
        data.sliderXInitial=320 # timescale slider
        data.sliderX=data.sliderXInitial
        data.sliderY=20
        data.sliderRadius = 8
        data.moveSlider = False
        data.mod = 1 # every mod frames, execute timerfired. makes slider smooth
        data.count = 0
        # these are lists to make changing their value in other functions easier
        data.longestWait = [0,0,0] # three longest waiters
        data.avgWait = [0] # avg wait time till picked up.
        data.totalPeople = len(people)
        data.firstLoop = not data.firstLoop # turns true when second loop
        data.simulationOver = False
    
    # specific algorithm user wants to test
    def initLoopConditions(data,loopNum,options):
        data.checkIfFull = options[0][loopNum]
        data.forgetTargetAndPickUp = options[1][loopNum]
        data.chooseComplexTarget = options[2][loopNum]
        data.pickTargetDontPrioritizeFloor = options[3][loopNum]
        data.scanFloorDontContInDir = options[4][loopNum]

    
    def mousePressed(event, data):
        x = event.x
        y = event.y
        x1=data.sliderX
        y1=data.sliderY
        # check if slider was clicked
        if (x-x1)**2+(y-y1)**2<=data.sliderRadius**2:
            data.moveSlider = True
        else:
            # ensures you dont move the slider if you dont click on it
            data.moveSlider = False
            # pauses simulation
            if data.simPause:
                data.simPause = False
            else:
                data.simPause = True
    
    def onDragSlider(event,data):
        # if drag is still on the slider bar, move slider
        if event.x < data.sliderXInitial and \
            event.x > data.width - data.sliderXInitial:
                if data.moveSlider: # move slider
                    data.sliderX=event.x
                    # make the simulation run fast or show
                    data.mod=int(round((data.sliderXInitial-\
                            data.sliderX)**2.82/1000))+1
            
    def keyPressed(event, data):
        pass



    ## THE MAIN AI
    
    def timerFired(data,root):
        # if everyone has been delivered and left the screen, leave simulation
        if len(people) == 0 and leaveQue == [] and elevators[0].isEmpty()\
            and elevators[1].isEmpty() and elevators[2].isEmpty() and \
            masterQueue == []:
                if data.firstLoop:
                    root.destroy()
                else:
                    data.simulationOver = True
        
        data.count += 1
        if data.count % (data.mod*5) == 0:
            data.count = 0
            # continue if simulation is not paused
            if not data.simPause:
                data.time+=dt # updates total time elapsed
                if len(people) != 0 and data.time >=people[0][0]:
                    # add a person to the queue
                    queueAdd(people.pop(0))
                for elevator in elevators:
                    # right most paper and right edge of middle
                    if elevator.isPaused():
                        # elevator guaranteed near floor if paused
                        floor = int(round(elevator.floor))
                        if elevator.isLastFrame():
                            # has target, drop off phase
                            if elevator.hasTarget(data.targets):
                                if not floorEmpty(floor):
                                    if targetFloorPickUp(elevator,floor,\
                                        masterQueue,fQue,data):
                                            continue
                                else:
                                    continue
                            else:
                                # empty paused elevator without target
                                if elevator.isEmpty():
                                    if not floorEmpty(floor):
                                        helperFunction(elevator,fQue,floor,\
                                                    data,masterQueue)
                                        continue
                                    else:
                                        elevator.assignTarget(data.targets,\
                                                masterQueue,\
                                                data.chooseComplexTarget,\
                                                elevators,fQue)
                                        continue
                                else:
                                    elevator.pickUp(data.totalPeople,data.time,\
                                        data.longestWait,data.avgWait,\
                                        fQue[floor],masterQueue,data.targets)
                                    continue
                        else:
                            continue
                    else:
                        # this begins the top left paper
                        if elevator.hasTarget(data.targets):
                            # check if assigned target is still on targetFloor
                            if elevator.target in fQue[elevator.targetFloor]\
                                [int(round((elevator.targetDir+1)/2))]:
                                    # when turned off, the elevator will not go 
                                    # past the target
                                    if data.forgetTargetAndPickUp:
                                        # if elevator.targetDir != elevator.dir:
                                        # if someone past target has same dir 
                                        # as target and isn't already a target, 
                                        # this function assigns them
                                        # as the target for the elevator
                                        elevator.peoplePastTarget(data.targets,\
                                                fQue,data.chooseComplexTarget,\
                                                elevators)
                                    if nearFloor(elevator):
                                        floor = int(round(elevator.floor))
                                        if not elevator.isEmpty():
                                            if elevator.anyoneLeaving(floor):
                                                elevator.dropOff(floor,\
                                                        leaveQue,data.time)
                                                elevator.pause()
                                                continue
                                        # has target, drop off phase
                                        if targetFloorPickUp(elevator,floor,\
                                                masterQueue,fQue,data):
                                                    continue
                                        else: 
                                            # this is just to show that this
                                            # terminal node is reached
                                            continue
                                    else:
                                        continue
                            else: # another elevator picked up target
                                # remove elevator's target from target list
                                if elevator.target in data.targets:
                                    data.targets.pop(data.targets.index\
                                        (elevator.target))
                                elevator.target = None
                                continue
                        else: # if elevator doesnt have a target, middle page
                            if not elevator.isEmpty():
                                if nearFloor(elevator):
                                    floor = int(round(elevator.floor))
                                    if elevator.anyoneLeaving(floor):
                                        elevator.pause()
                                        elevator.dropOff(floor,\
                                            leaveQue,data.time)
                                    # continues and skips picking up people from 
                                    # the floor to see if new target to be 
                                    # assigned
                                    if elevator.isEmpty():
                                        if data.scanFloorDontContInDir or \
                                            data.pickTargetDontPrioritizeFloor:
                                                continue
                                    # continues in dir if possible
                                    if elevator.dirMatch(fQue[floor],data.time):
                                        # slight improvement
                                        if data.checkIfFull:
                                            if elevator.isFull():
                                                continue
                                        elevator.pickUp(data.totalPeople,\
                                            data.time,data.longestWait,\
                                            data.avgWait,fQue[floor],\
                                            masterQueue,data.targets)
                                        continue
                                    else: 
                                        continue
                                else:
                                    continue
                            else: # if elevator empty and moving without target
                                elevator.assignTarget(data.targets,masterQueue,\
                                        data.chooseComplexTarget,elevators,fQue)
                                continue
                for elevator in elevators:
                    if elevator.wait<=0:
                        elevator.adjustPreviousWait(dt)
                        if ((elevator.dir==-1 and not nearFloor(elevator,1)) or\
                            (elevator.dir == 1 and not nearFloor(elevator, 8))):
                                elevator.floor+=elevator.dir*elevator.dy
                                for human in elevator.people:
                                    human.y-=elevator.dir*elevator.dy*\
                                        elevator.convert
                    else:
                        # if the elevator was just paused, dont repause it
                        elevator.adjustWait(dt)
                for leaver in leaveQue:
                    # if leaving for more than a few seconds, delete him
                    if data.time - leaver[1] > 5:
                        leaveQue.pop(leaveQue.index(leaver))
                        continue
                    leaver[0].x-=1.2
                
    # longestWait and avgWait are values from the first loop here
    def redrawAll(canvas,data,options,longestWait=longestWait,avgWait=avgWait):
        if not data.simulationOver:
            # draw lines for floors
            for i in range (1,10):
                canvas.create_line(0,height*i/10,width,height*i/10)
            # draw elevators and people inside them
            for elevator in elevators:
                for human in elevator.people:
                    human.draw(canvas)
                elevator.draw(canvas)
            # draw people waiting on floors
            for floor in fQue:
                for human in floor[0]:
                    human.draw(canvas)
                for human in floor[1]:
                    human.draw(canvas)
            # draw people leaving elevator
            for leaver in leaveQue:
                leaver[0].draw(canvas)
            # draw time scale slider
            canvas.create_oval(data.sliderX-data.sliderRadius,
                            data.sliderY-data.sliderRadius,\
                            data.sliderX+data.sliderRadius,\
                            data.sliderY+data.sliderRadius, fill="orange")
            canvas.create_line(data.sliderXInitial,data.sliderY,\
                            data.width-data.sliderXInitial,data.sliderY)
            # create time slider text
            canvas.create_text(data.width-data.sliderXInitial,data.sliderY,\
                            text="Slow    ",anchor=E, font="helvetica 12",\
                            fill = "red")
            canvas.create_text(data.sliderXInitial,data.sliderY, \
                            text="    Fast", anchor=W, font="helvetica 12",\
                            fill = "green")
            canvas.create_text(data.width/2,data.height-data.sliderY, \
                            text="Click anywhere to pause", anchor=CENTER,\
                            font="helvetica 12", fill = "dark blue")
        else:
            # color the smaller number green cuz that part of that
            # simulation ran faster
            firstLoopCols = []
            secondLoopCols = []
            if abs(avgWait[0] - data.avgWait[0])<0.05:
                firstLoopCols += ["black"]
                secondLoopCols += ["black"]
            elif avgWait[0] > data.avgWait[0]:
                firstLoopCols += ["red"]
                secondLoopCols += ["green"]
            else:
                firstLoopCols += ["green"]
                secondLoopCols += ["red"]
            for i in range(len(longestWait)):
                if abs(longestWait[i] - data.longestWait[i])<0.0005:
                    firstLoopCols += ["black"]
                    secondLoopCols += ["black"]
                elif longestWait[i] > data.longestWait[i]:
                    firstLoopCols += ["red"]
                    secondLoopCols += ["green"]
                else:
                    firstLoopCols += ["green"]
                    secondLoopCols += ["red"]
                    
            
            # text for loop conditions
            canvas.create_text(data.width/2,17, text="CONDITIONS FOR "+\
                    "SIMULATIONS\ncheckIfFull %s\n"%options[0]+\
                    "forgetTargetAndPickUp %s\nchooseComplexTarget %s\n"\
                    %(options[1],options[2])+"pickTargetDontPrioritizeFloor "+\
                    "%s\nscanFloorDontContInDir %s"%(options[3],options[4]),\
                    anchor=N,font="arial 14", fill = "dark blue",\
                    justify = RIGHT)
            
            #dividing line between two loop's results
            canvas.create_line(200,200,200,400)
            canvas.create_line(0,200,400,200)
            # create titles for loops
            canvas.create_text(100,180,text = "Loop 1", font="arial 17",\
                    anchor = CENTER)
            canvas.create_text(300,180,text = "Loop 2", font="arial 17",\
                    anchor = CENTER)
            
            # avgWait times
            canvas.create_text(190,230,text = "avgWait = %.3f"%avgWait[0],\
                    font="arial 14",anchor=E,fill=firstLoopCols[0])
            canvas.create_text(210,230,text = "%.3f"%data.avgWait[0],\
                    font="arial 14",anchor=W,fill=secondLoopCols[0])
            # draw longest wait title
            canvas.create_text(119,320,text = "Three\nlongest:\nwaits",\
                    font="arial 15",anchor=E,justify = CENTER)
            # three longest waiting times
            for i in range(3):
                canvas.create_text(190,280+40*i,text="%.3f"%longestWait[i],\
                    font="arial 14",anchor=E,fill=firstLoopCols[i+1])
                canvas.create_text(210,280+40*i,\
                    text="%.3f"%data.longestWait[i],font="arial 14",\
                    anchor=W,fill=secondLoopCols[i+1])
            

    ## run function for drawing
    ## adapted from https://www.cs.cmu.edu/~112/notes/hw6.html
    def run(options,longestWait,avgWait,width=400, height=400):
        def redrawAllWrapper(canvas, data,options = options,\
            longestWait = longestWait, avgWait = avgWait):
                canvas.delete(ALL)
                canvas.create_rectangle(0, 0, data.width, data.height,
                                        fill='white', width=0)
                redrawAll(canvas, data,options,longestWait,avgWait)
                canvas.update()
    
        def mousePressedWrapper(event, data):
            mousePressed(event, data)
            redrawAllWrapper(canvas, data)
    
        def keyPressedWrapper(event, data):
            keyPressed(event, data)
            redrawAllWrapper(canvas, data)
    
        def timerFiredWrapper(canvas, data):
            timerFired(data, root)
            redrawAllWrapper(canvas, data)
            # pause, then call timerFired again
            canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
        
        root = Tk()
        root.title("Wean Elevator Simulator 2k17")
        init(data)
        canvas = Canvas(root, width=data.width, height=data.height)
        canvas.pack()
        # set up events
        root.bind("<Button-1>", lambda event:
                                mousePressedWrapper(event, data))
        root.bind("<Key>", lambda event:
                                keyPressedWrapper(event, data))
        root.bind('<B1-Motion>', lambda event: onDragSlider(event,data))
        timerFiredWrapper(canvas, data)
        # and launch the app
        root.mainloop()  # blocks until window is closed
    # get options the user wants to try
    options = widget()
    if options == False:
        return
    # first go
    data.firstLoop = False # becomes true in init
    initialize(people,elevators) # import file and set up scene
    initLoopConditions(data,0,options)
    run(options,longestWait,avgWait,width,height) # run animation and AI
    longestWait= data.longestWait
    avgWait+=[data.avgWait[0]]
    # second go
    initialize(people,elevators)
    initLoopConditions(data,1,options)
    run(options,longestWait,avgWait,width,height)
    longestWait+= [data.longestWait[0]]
    avgWait+=[data.avgWait[0]]
    print(options)
    print("longest waits and avg wait for first run  ",longestWait[0:3],avgWait[0])
    print("longest waits and avg wait for second run ",longestWait[3:6],avgWait[0])
    
