# Trevor Arashiro, tarashir, sect H
class Person(object):
    def __init__(self, time, floor, exit, x, y):
        self.time = time # time enters building
        self.floor = floor
        self.exit = exit # exit floor
        self.dir = int(round((exit-floor)/abs(exit-floor))) # direction headed
        self.leave = False # when true, the person walks left, out of elevator
        self.x = x # where circle first drawn on floor, given by pos in queue
        self.y = y # low on floor if going down, high if going up
        self.diameter = 8
    
    # called by elevator when it reaches floor
    def move(self,elevatorx):
        self.leave = True
        self.x -= elevatorx-100
    
    # moves dots around in elevator and into elevator
    def moveIntoElevator(self,x,y):
        self.x = x
        self.y = y
    
    def draw(self, canvas):
        x = self.x
        y = self.y
        canvas.create_oval(x,y,x+self.diameter,y+self.diameter)
    
    # equality is dictated by time since no two people arrive at the same time
    # two people are basically equal if they are on the same floor and going
    # in the same dir
    def __eq__(self,other):
        if isinstance(other,Person) and (self.time == other.time or (\
            self.floor == other.floor and self.dir == other.dir)):
            return True
        return False
    
    def __hash__(self):
        return hash((self.floor,))