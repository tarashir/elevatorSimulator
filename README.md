# elevatorSimulator

To run the program: first compile Elevator.py and Person.py, then runAI.py, then finally run main.py.  

No API's were used, the algorithm used by the elevators is completely hardcoded.

In the final window, the rectangles are the elevators and the circles are people.  Each horizontal line represents one floor. 

IF YOU JUST WANT TO WITNESS THE PROGRAM IN ACTION, USE THE FOLLOWING DIRECTIONS:
1) When main.py is run, a window will pop up, click on "type" and then enter the values 100 for time and 150 for people; click continue.
2) On the next screen, draw a straight line across the middle of the graph, then click continue in the bottom right.
3) On the next two screens, just click the "continue" button in the bottom right of the windows.  
4) In the next window, you can adjust the slider at the top of the screen depending upon the speed at which you would like to view the simulation. 

Here is a more complex description of the program:
1) When main.py is run, a window will pop up, click on "type"
2) The "time" text entry box refers to how long the simulation will take (not real world time) and the "people" text entry box is how many people appear in the simulation.  I would suggest setting time to 100 and people to anywhere between 20 and 500.
3) The graph you draw next represents the RATE at which people will arrive to the building.  ALL DOTS ON THIS GRAPH ARE RELATIVE.  i.e. a horizontal line at the middle of the graph represents the same distribution as a horizontal line at the top of the graph.  For example, if you want very little people to arrive at the start and a lot to arrive at the end, draw a line that looks like y=2*x.
4) The graph that is shown next shows the total number of people that will have arrived at each time x. 
5) Put simply, the next window controls a few aspects of the AI's behaviour.  This program runs two simulations, the AI's approach is determined by the 1's and 0's on the options panel.  A '1' in the first slot on a button means that the AI will use the corresponding method on the first simulation and a '0' means that whenever the AI has the opportunity to use the method, it will not call the method. The same goes for the second slot. Note that options 4 and 5 can not be run simultaneously (because they contradict eachother). The options panel allows you to customize the AI's approach to solving the scenario that it has been given. 
