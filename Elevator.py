# Trevor Arashiro, tarashir, sect H
import Person
import copy
import math

class Elevator(object):
    # floor it is instantiated on, direction it heads, floor people enter and
    # floor people exit
    def __init__(self, floor, dir, floorExitQue, x, height, dt, ratio):
        self.floor = floor # floor instantiated on
        self.dir = dir # 1 is up, -1 is down, 0 is stationary
        self.max = 20 # no more than 20 people in elevator at once
        self.ppl = 0 # number of people in the elevator
        self.x = x
        self.height = height # height of canvas
        self.floorExitQue = floorExitQue # list of floors people in elevator leaving on
        self.people=[] # list of people in elevator
        self.delay = .3 # seconds an elevator delayed at a floor
        self.wait = 0 # seconds remaining to wait at floor
        self.convert = height/10 # convert floors to pixels
        self.target = None # heads towards target and will pass or land on it
        self.targetDir = None
        self.targetFloor = None
        self.dt = dt # animation time that passes every frame
        self.vel = 1 # vel*32/(height*.8*dt)/=speed in meters per second
        self.dy = self.dt*self.vel # of pixels elevator moves each frame
        self.previousWait = 0 # was the elevator waiting last frame
        self.loops = 0
        # time person must wait before elevator registers them on floor
        self.minWaitTime = 1
        # very rough estimate of stopping at a floor elevator is passing
        self.pOfStop = 1-math.e**(-ratio)
    
    def __eq__(self,other):
        if isinstance(other,Elevator) and other.x == self.x:
            return True
        return False
    
    # expected time to travel n floors
    def timeToTravelNFloors(self,n):
        return (1/self.vel+self.pOfStop*self.delay)*n-self.pOfStop*self.delay
    
    def pause(self):
        if self.wait <= 0:
            self.wait=self.delay
        self.loops = 0 # after two loops, set previous wait to 0.
        return
    
    def isPaused(self):
        if self.wait > 0 or self.dir == 0:
            return True
        return False
    
    # returns true if elevator has no wait time remaining
    def isLastFrame(self):
        if self.wait <= self.dt:
            return True
        return False
    
    def wasLastFrame(self):
        if self.previousWait > 0:
            return True
        return False
        
    def adjustWait(self,dt):
        self.previousWait=self.wait
        self.wait-=dt
        
    def adjustPreviousWait(self,dt):
        self.loops+=1
        if self.loops == 2:
            self.previousWait = 0
            self.loops = 0
    
    # dropping people off at floor
    def dropOff(self,floor,leaveQue,time):
        # dont even try to drop people off if floor isn't in floorque
        if floor in self.floorExitQue:
            flq = copy.copy(self.floorExitQue)
            for i in range(len(self.floorExitQue)):
                if self.floorExitQue[i] == floor:
                    # work around for removing people from people because
                    # floorQue[i] corresponds to people[i] so find first
                    # occurance of floor in flq and pop that from flq and people
                    index = flq.index(floor)
                    self.people[index].move(self.x) # move person out of elevator
                    leaveQue += [[self.people.pop(index),time]] # remove people getting off here
                    flq.pop(index)
                    self.ppl-=1
        self.floorExitQue = flq
        # for those remaining in elevator, move them to front of elevator
        for i in range(len(self.people)):
            self.people[i].moveIntoElevator(self.x+8*(i%4),\
                                    self.height-(self.floor+1)*self.convert+\
                                    8*(i//4))
        return
    
    
    def pickUp(self,totalPeople,time,longestWait,avgWait,fqueFloor,masterQueue,\
        allTargets):
            dir2 = int((self.dir+1)/2)
            # need cpy so dont .pop() values from fqueFloor to iterate through
            cpy = copy.copy(fqueFloor[dir2])
            if len(fqueFloor[dir2])==0:
                return
            # if first person waited longer than anyone else, update longestWait
            if time-fqueFloor[dir2][0].time > longestWait[0]:
                longestWait[2] = longestWait[1] # third longest wait
                longestWait[1] = longestWait[0] # second longest wait
                longestWait[0] = time-fqueFloor[dir2][0].time # longest wait
            # add people until full or no more on floor going in elev.dir
            for human in fqueFloor[dir2]:
                # if full stop trying to add people
                if self.ppl >= self.max:
                    break
                else:
                    if not self.wasLastFrame():
                        self.pause()
                    avgWait[0]+=(time-human.time)/totalPeople
                    self.floorExitQue+=[human.exit] # add exit floor to que
                    self.people+=[human]
                    # removes people from fqueFloor as they enter elevator
                    cpy.pop(0)
                    self.ppl+=1 # increase number of people in elevator
                    # move dot into elevator, pass top left corner of dot
                    human.moveIntoElevator(self.x+8*((self.ppl-1)%4),\
                                        self.height-(self.floor+1)*self.convert\
                                        +8*((self.ppl-1)//4))
                    # removes human from masterQueue
                    masterQueue.pop(masterQueue.index(human))
                    if human in allTargets:
                        allTargets.pop(allTargets.index(human))
            # number of people moved from floor to elevator
            moves = len(fqueFloor[dir2]) - len(cpy)
            fqueFloor[dir2] = cpy
            # reorder the remaining dots in the floor queue
            for i in range(len(fqueFloor[dir2])):
                fqueFloor[dir2][i].x-=8*moves
    
    
    # assign target efficiently, look where elevators aren't going, finds the
    # floors it can access quicker than both elevators given their current path
    # and assign target to longest waiting person on those floors
    def complexChooseTarget(self,elevators,fQue,allTargets,person):
        # but first, check if both other elevators are going same direction
        # and theyre near the top or bottom of the building.  If so, go to
        # to the opposite side of them. 
        # observe the two other elevators, not this one
        a = [0,1,2] # indexes of other elevators
        index = a.pop(elevators.index(self)) # index of this elevator
        if elevators[a[0]].floor < 3 and elevators[a[0]].dir == -1 and \
           elevators[a[1]].floor < 3 and elevators[a[1]].dir == -1:
                # find nearest floor with someone going up
                i = int(self.floor // 1)
                if i < 3:
                    i+=1
                while i <= 8:
                    if len(fQue[i][1]) > 0:
                        return fQue[i][1][0]
                    i+=1
        if elevators[a[0]].floor > 5 and elevators[a[0]].dir == 1 and \
           elevators[a[1]].floor > 5 and elevators[a[1]].dir == 1:
                # find nearest floor with someone going down
                i = int(math.ceil(self.floor))
                if i > 5:
                    i-=1
                while i >= 1:
                    if len(fQue[i][-1]) > 0:
                        return fQue[i][-1][0]
                    i-=1
                
        # floorvisit[elevator][nth floor[dir] reached] = [floor,dir]
        # (note: floorvisit[elevator].index[floor,dir] returns when the elevator 
        # will reach that floor[dir]
        floorVisits = [[],[],[]] # next floors elevators will reach
        # round current floor of other elevator up or down depending upon
        # which floor it will reach
        for i in [0,1,2]:
            if elevators[i].dir == 1:
                floorVisits[i] += [[int(math.ceil(elevators[i].floor-0.000001)),elevators[i].dir]]
            else:
                floorVisits[i] += [[int((elevators[i].floor+0.000001)//1),elevators[i].dir]]
        # ensure that this elevator is not on the same floor as another 
        # elevator with same dir.  If so, this method will not work properly
        for i in a:
            if floorVisits[i][0][0] == floorVisits[index][0][0] and \
                floorVisits[i][0][1] == floorVisits[index][0][1]:
                    return person
        # floorVisits[i] = the next 13 floors elevator i will visit
        for i in range (1,14):
            floorVisits[0] += [[int(round(floorVisits[0][0][0]+i*elevators[0].dir)),elevators[0].dir]]
            floorVisits[1] += [[int(round(floorVisits[1][0][0]+i*elevators[1].dir)),elevators[1].dir]]
            floorVisits[2] += [[int(round(floorVisits[2][0][0]+i*elevators[2].dir)),elevators[2].dir]]
        for i in [0,1,2]: # make values floor numbers
            for j in range(14):
                if floorVisits[i][j][0] > 14:
                    floorVisits[i][j][0] = floorVisits[i][j][0]-14
                elif floorVisits[i][j][0] > 8:
                    floorVisits[i][j][0] = 16-floorVisits[i][j][0]
                    # when elevator passes this floor it is going opposite dir
                    floorVisits[i][j][1] = -floorVisits[i][j][1]
                elif floorVisits[i][j][0] < -5:
                    floorVisits[i][j][0] = 14+floorVisits[i][j][0]
                elif floorVisits[i][j][0] < 1:
                    floorVisits[i][j][0] = 2-floorVisits[i][j][0]
                    # when elevator passes this floor it is going opposite dir
                    floorVisits[i][j][1] = -floorVisits[i][j][1]
                # 8th and 1st floors only have one direction
                elif floorVisits[i][j][0] == 8:
                    floorVisits[i][j][1] = -1
                elif floorVisits[i][j][0] == 1:
                    floorVisits[i][j][1] = 1
        # find soonest time when each floorQue[dir] will be reached by one of
        # the other two elevators
        # reachableFloorQues[[floor,dir]] = how many floors away other elevators
        # are when we get there
        reachableFloorQues = dict()
        for visit in floorVisits[0]:
            # if floorQue[dir] can be reached first, add it to list
            if (min(floorVisits[a[0]].index(visit),floorVisits[a[1]].index(visit)) - floorVisits[index].index(visit)) > 0:
                # this is the number of floors this elevator will reach the
                # target before the others
                reachableFloorQues[tuple(visit)] = min(floorVisits[a[0]].index(visit),floorVisits[a[1]].index(visit)) - floorVisits[index].index(visit)
        # make a list of the person waiting the longest in each floorQue[dir]
        # that can be reached first
        reachablePeople = []
        relTimeToPerson = []
        for visit in reachableFloorQues:
            indx = int((visit[1]+1)//2)
            if len(fQue[visit[0]][indx]) != 0:
                reachablePeople.append(fQue[visit[0]][indx][0])
                relTimeToPerson.append(self.timeToTravelNFloors(reachableFloorQues[visit])-fQue[visit[0]][indx][0].time)
        # if no assignable targets found, return None
        if len(relTimeToPerson) == 0:
            return None
        # find the person who will be waiting the longest 
        maxTime = max(relTimeToPerson)
        # this persno will be assigned as the target to this elevator
        # index of person who will wait the longest
        idx = relTimeToPerson.index(maxTime)
        relTimeToPerson.pop(idx)
        newTarget = reachablePeople.pop(idx)
        # if this person is the target of another empty elevator, 
        # cancel reassign that elevator a target
        for i in a:
            if elevators[i].target == newTarget and elevators[i].isEmpty() and newTarget != None:
                if newTarget == elevators[i].complexChooseTarget(elevators,fQue,allTargets,person):
                    # if other elevator reassigned to same target, set the 
                    # target of this elevator to the second longest waiter
                    maxTime = max(relTimeToPerson)
                    idx = relTimeToPerson.index(maxTime)
                    relTimeToPerson.pop(idx)
                    newTarget = reachablePeople.pop(idx)
                    
        return newTarget
        # # if target.dir == another elevators dir and it is opposide from this
        # # elevator, then assign that elevator no target
        # for i in a:
        #     if target.dir == elevators[i].dir:
        #         if elevators[i].target != None:
        #             allTargets.pop(allTargets.index
        #             elevators[i].target 
            
                    
        
            
        
    
    # assign person and floor elevator heads towards and passes without fail
    # if second argument is a list, assign first person in list that isnt
    # already a target.  Returns none if 
    def assignTarget(self,allTargets,person,chooseComplexTarget,elevators,fQue,override = True):
        forceTarget = False
        # ensure that all 3 elevators are moving and not all on the same floor
        for elevator in elevators:
            if elevator.dir == 0:
                override = False
        if chooseComplexTarget and override:
            person = self.complexChooseTarget(elevators,fQue,allTargets,person)
            if person == None:
                return False

        if not isinstance(person,list):
            if not person in allTargets or forceTarget:
                # remove the elevator's target from the list of targets
                if self.hasTarget(allTargets):
                    allTargets.pop(allTargets.index(self.target))
                    self.target = None
                self.targetDir=person.dir
                self.targetFloor=person.floor
                # if on target floor, dont assign as target and set self.dir
                # to target.dir
                if abs(person.floor-self.floor) <= 0.0001:
                    # if not self.wasLastFrame():
                    self.pause()
                    self.dir = person.dir
                    self.target=person
                    if person not in allTargets:
                        allTargets.append(copy.copy(person))
                    return True
                else:
                    self.dir = int(round((person.floor-self.floor)/\
                                            abs(person.floor-self.floor)))
                    self.target=person
                    if person not in allTargets:
                        allTargets.append(copy.copy(person))
                    return True
        else:
            # person here is actually masterQueue here
            for dude in person:
                # note that "dude in allTargets" checks if anyone in allTargets
                # has the same dir as dude and is on the same floor as dude.
                # If so, no point in assigning them as a target
                if not dude in allTargets:
                    if self.assignTarget(allTargets,dude,chooseComplexTarget,elevators,fQue):
                        return True
        # did not find a person whose floor hasn't been assigned yet
        return False
    
    # check if elevator is empty
    def isEmpty(self):
        if self.ppl == 0:
            return True
        return False
        
    # check if elevator has target
    def hasTarget(self, allTargets):
        if self.target != None:
            if self.target in allTargets:
                return True
            else:
                self.target = None
                return False
        return False
        
    def isTargetFloor(self, floor):
        if floor == self.targetFloor:
            return True
        return False
        
    # check if anyone on floor elevator is nearing has same dir as elevator
    # and arrived more than 3 seconds ago.  If true, stops at floor
    def dirMatch(self,fqueFloor,time):
        if len(fqueFloor[int((self.dir+1)/2)]) != 0:
            if time-fqueFloor[int((self.dir+1)//2)][0].time > self.minWaitTime:
                return True
        return False
        
    # check if floors past target have anyone that shares target.dir
    def peoplePastTarget(self,allTargets,fQue,chooseComplexTarget,elevators):
        index = int((self.targetDir+1)/2) # check up or down queue on floors
        # if elevator going up, check floors above target
        if self.dir == 1:
            # set target to farthest person with targetdir 
            for i in range(8,self.targetFloor,-1):
                if len(fQue[i][index]) != 0:
                    # return True if found someone to assign
                    # passes it False to override complexChooseTarget cuz we 
                    # don't want that here.
                    if self.assignTarget(allTargets,fQue[i][index][0],chooseComplexTarget,elevators,fQue,False):
                        return True
        # elevator going down, check floors below target
        else:
            for i in range(1,self.targetFloor):
                if len(fQue[i][index]) != 0:
                    if self.assignTarget(allTargets,fQue[i][index][0],chooseComplexTarget,elevators,fQue,False):
                        return True
        return False
        
    # check if anyone in elevator getting off on the floor elevator is on
    def anyoneLeaving(self, floor):
        if floor in self.floorExitQue:
            return True
        return False
        
    # check if anyone in elevator has destination past targetFloor
    def destPastTarget(self,allTargets):
        for floors in self.floorExitQue:
            if (floors - self.targetFloor) / (self.targetFloor - self.floor) > 0:
                allTargets.pop(allTargets.index(self.target))
                self.target = None
                self.targetFloor = None
                
                return
            
    def draw(self, canvas):
        canvas.create_rectangle(self.x,self.height-(self.floor+1)*self.convert,\
                                self.x+32,self.height-(self.floor)*self.convert)
                                
    def isFull(self):
        if self.ppl >= self.max:
            return True
        return False
    
    
            