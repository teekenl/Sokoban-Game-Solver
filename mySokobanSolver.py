
'''

The partially defined functions and classes of this module 
will be called by a marker script. 

You should complete the functions and classes according to their specified interfaces.
 

'''

import search

import math

import sokoban

from search import breadth_first_graph_search, depth_first_graph_search, astar_graph_search

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def my_team():
    '''
    Return the list of the team members of this assignment submission as a list
    of triplet of the form (student_number, first_name, last_name)
    
    '''
    return [ (9901990, 'Jia Sheng', 'Chong'), (9532897, 'TeeKen', 'Lau'), (9552286, 'Yew Lren', 'Chong') ]


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def taboo_cells(warehouse):
    '''  
    Identify the taboo cells of a warehouse. A cell is called 'taboo' 
    if whenever a box get pushed on such a cell then the puzzle becomes unsolvable.  
    When determining the taboo cells, you must ignore all the existing boxes, 
    simply consider the walls and the target  cells.  
    Use only the following two rules to determine the taboo cells;
     Rule 1: if a cell is a corner and not a target, then it is a taboo cell.
     Rule 2: all the cells between two corners along a wall are taboo if none of 
             these cells is a target.
    
    @param warehouse: a Warehouse object

    @return
       A string representing the puzzle with only the wall cells marked with 
       an '#' and the taboo cells marked with an 'X'.  
       The returned string should NOT have marks for the worker, the targets,
       and the boxes.  
    '''   
    
    taboo_string = ""
    # list to store cells (x,y) for rule 1
    corner_taboo_cells = []
    # list to store cells (x,y) for rule 2
    other_taboo_cells = []
    # list to store cells (x,y) of targets
    targetsXY = []
    
    cells = str(warehouse).split('\n')
    
    index = 0
    for strings in cells:
        cells[index] = list(strings)
        index += 1
    
    # Codes to get cells for rule 1 
    # Copy cells into temp by splitting everything
    temp = cells[:]
    
    for r_indx, row in enumerate(cells):
        inside_cell = False    
        for c_indx, char in enumerate(row):
            
            # Always turn the goal into a legit spot
            if char == "." or char == '$' or char == '*':
                cells[r_indx][c_indx] = " " # TODO change this later
                inside_cell = True
            
            if char == "." or char == "*":
                targetsXY.append((r_indx, c_indx))
                    
                
            # If a wall is encountered, check if it is within the playing area
            elif char == '#':
                inside_cell = True
                for index in range(c_indx):
                    if cells[r_indx][index] == '#':
                        inside_cell = False
                cells[r_indx][c_indx] = char
                
            else:
                # Check if the space is within the cell and if it's in the corner of the warehouse
                if inside_cell == False or r_indx == 0 or r_indx == len(cells) - 1 or c_indx == 0 or c_indx == len(cells[r_indx]) - 1:
                    cells[r_indx][c_indx] = char
                else:
                    
                    taboo1 = temp[r_indx][c_indx - 1] == '#' and temp[r_indx - 1][c_indx] == '#' # Checks left top
                    taboo2 = temp[r_indx][c_indx + 1] == '#' and temp[r_indx - 1][c_indx] == '#' # Checks right top
                    taboo3 = temp[r_indx][c_indx - 1] == '#' and temp[r_indx + 1][c_indx] == '#' # Checks left bottom
                    taboo4 = temp[r_indx][c_indx + 1] == '#' and temp[r_indx + 1][c_indx] == '#' # Checks right bottom
                    
                    if taboo1 or taboo2 or taboo3 or taboo4:
                        cells[r_indx][c_indx] = 'X'
                        corner_taboo_cells.append((r_indx, c_indx))
                    else:
                        cells[r_indx][c_indx] = ' '
    
    # Codes to get cells for Rule 2
    potentialTabooXY = []
    isTaboo = False
    
    for aCell in corner_taboo_cells:
        # if a corner taboo cell is in a Top Left Corner
        if cells[aCell[0]][aCell[1] - 1] == '#' and cells[aCell[0] - 1][aCell[1]] == '#':
            # Check and get the all the cells below the corner taboo cell untill a wall is encountered
            y = aCell[0] + 1
            
            while cells[y][aCell[1]] != '#':
                potentialTabooXY.append((y, aCell[1]))
                y = y + 1
            
            if len(potentialTabooXY) > 0:
                # Check all the cells are in between two corners
                if potentialTabooXY[-1] in corner_taboo_cells:
                    isTaboo = True
                    for aXY in potentialTabooXY:
                        # Check the left side of all the cells, if one of is not a wall,
                        # then all cells are not taboo cells
                        if cells[aXY[0]][aXY[1]- 1 ] != '#':
                            isTaboo = False
                        
                        # Check if any of the cells is a target, if it is a target.
                        # then all cells are not taboo cells
                        if aXY in targetsXY:
                            isTaboo = False
            
            if isTaboo:
                other_taboo_cells.extend(potentialTabooXY)
                isTaboo = False
            
            potentialTabooXY = []
                
            # Check and get the all the cells to the right the corner taboo cell untill a wall is encountered
            x = aCell[1] + 1
            while cells[aCell[0]][x] != '#':
                potentialTabooXY.append((aCell[0], x))
                x = x + 1
                
            if len(potentialTabooXY) > 0:    
                # Check all the cells are in between two corners
                if potentialTabooXY[-1] in corner_taboo_cells:
                    isTaboo = True
                    for aXY in potentialTabooXY:
                        # Check the top side of all the cells, if one of is not a wall,
                        # then all cells are not taboo cells
                        if cells[aXY[0] - 1][aXY[1]] != '#':
                            isTaboo = False
                            
                        # Check if any of the cells is a target, if it is a target,
                        # then all cells are not taboo cells    
                        if aXY in targetsXY:
                            isTaboo = False
            
            if isTaboo:
                other_taboo_cells.extend(potentialTabooXY)
                isTaboo = False
            
            potentialTabooXY = []
                
        # if a corner taboo cell is in a Top Right corner
        # This part of the code is similar to the section above, the only difference is
        # this will check the cells along the walls of the top right corner
        if cells[aCell[0]][aCell[1] + 1] == '#' and cells[aCell[0] - 1][aCell[1]] == '#':
            y = aCell[0] + 1
            while cells[y][aCell[1]] != '#':
                potentialTabooXY.append((y, aCell[1]))
                y = y + 1
            
            if len(potentialTabooXY) > 0:
                if potentialTabooXY[-1] in corner_taboo_cells:
                    isTaboo = True
                    for aXY in potentialTabooXY:
                        if cells[aXY[0]][aXY[1] + 1 ] != '#':
                            isTaboo = False
                        if aXY in targetsXY:
                            isTaboo = False
            
            if isTaboo:
                other_taboo_cells.extend(potentialTabooXY)
                isTaboo = False
            
            potentialTabooXY = []
                
            x = aCell[1] - 1
            while cells[aCell[0]][x] != '#':
                potentialTabooXY.append((aCell[0], x))
                x = x - 1
            
            if len(potentialTabooXY) > 0:
                if potentialTabooXY[-1] in corner_taboo_cells:
                    isTaboo = True
                    for aXY in potentialTabooXY:
                        # Check top
                        if cells[aXY[0] - 1][aXY[1]] != '#':
                            isTaboo = False
                        if aXY in targetsXY:
                            isTaboo = False
            
            if isTaboo:
                other_taboo_cells.extend(potentialTabooXY)
                isTaboo = False
            
            potentialTabooXY = []
            
        # if a corner taboo cell is in a Bottom Left Corner
        # This part of the code is similar to the section above, the only difference is
        # this will check the cells along the walls of the Bottom Left Corner
        if cells[aCell[0]][aCell[1] - 1] == '#' and cells[aCell[0] + 1][aCell[1]] == '#':
            y = aCell[0] - 1
            
            while cells[y][aCell[1]] != '#':
                potentialTabooXY.append((y, aCell[1]))
                y = y - 1
            
            if len(potentialTabooXY) > 0:
                if potentialTabooXY[-1] in corner_taboo_cells:
                    isTaboo = True
                    for aXY in potentialTabooXY:
                        if cells[aXY[0]][aXY[1] - 1 ] != '#':
                            isTaboo = False
                        if aXY in targetsXY:
                            isTaboo = False
            
            if isTaboo:
                other_taboo_cells.extend(potentialTabooXY)
                isTaboo = False
            
            potentialTabooXY = []
                
            x = aCell[1] + 1
            
            while cells[aCell[0]][x] != '#':
                potentialTabooXY.append((aCell[0], x))
                x = x + 1
            
            if len(potentialTabooXY) > 0:
                if potentialTabooXY[-1] in corner_taboo_cells:
                    isTaboo = True
                    for aXY in potentialTabooXY:
                        if cells[aXY[0] + 1][aXY[1]] != '#':
                            isTaboo = False
                        if aXY in targetsXY:
                            isTaboo = False
            
            if isTaboo:
                other_taboo_cells.extend(potentialTabooXY)
                isTaboo = False
            
            potentialTabooXY = []
            
        # if a corner taboo cell is in a Bottom Right Corner
        # This part of the code is similar to the section above, the only difference is
        # this will check the cells along the walls of Bottom Right Corner
        if cells[aCell[0]][aCell[1] + 1] == '#' and cells[aCell[0] + 1][aCell[1]] == '#':
            y = aCell[0] - 1
            
            while cells[y][aCell[1]] != '#':
                potentialTabooXY.append((y, aCell[1]))
                y = y - 1
            
            if len(potentialTabooXY) > 0:
                if potentialTabooXY[-1] in corner_taboo_cells:
                    isTaboo = True
                    for aXY in potentialTabooXY:
                        if cells[aXY[0]][aXY[1] + 1 ] != '#':
                            isTaboo = False
                        if aXY in targetsXY:
                            isTaboo = False
            
            if isTaboo:
                other_taboo_cells.extend(potentialTabooXY)
                isTaboo = False
            
            potentialTabooXY = []
            
            x = aCell[1] - 1
            while cells[aCell[0]][x] != '#':
                potentialTabooXY.append((aCell[0], x))
                x = x - 1
            
            if len(potentialTabooXY) > 0:
                if potentialTabooXY[-1] in corner_taboo_cells:
                    isTaboo = True
                    for aXY in potentialTabooXY:
                        if cells[aXY[0] + 1][aXY[1]] != '#':
                            isTaboo = False
                        if aXY in targetsXY:
                            isTaboo = False
            
            if isTaboo:
                other_taboo_cells.extend(potentialTabooXY)
                isTaboo = False
            
            potentialTabooXY = []
            
    
    for aCell in other_taboo_cells:
        cells[aCell[0]][aCell[1]] = 'X'                                        
                                
    cells = cells[1:]
             
    for row in cells:
        taboo_string += "\n" 
        taboo_string += ''.join(row)   

    return taboo_string

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class SokobanPuzzle(search.Problem):
    '''
    Class to represent a Sokoban puzzle.
    Your implementation should be compatible with the
    search functions of the provided module 'search.py'.
    
    	Use the sliding puzzle and the pancake puzzle for inspiration!
    
    '''
    def result(self, state, action):
        '''
        Function that applies an action to the a state (warehouse) and return
        a new state.
        
        @param state: A Warehouse object
        
        @param action: An action from list ['Left', 'Down', 'Right', 'Up'] 
            
        @return
            Return the state (a Warehouse with the updated location of worker 
            and boxes) after applying an action.
        
        '''
        cur_warehouse = state
        worker = list(cur_warehouse.worker)
        boxes = list(cur_warehouse.boxes)
        
        assert action in self.actions(state)
                
        x, y = find_move(action)
        worker[0] += x
        worker[1] += y
              
        for idx, box in enumerate(boxes):
            if box == (worker[0], worker[1]):
                box_x = box[0] + x
                box_y = box[1] + y
                boxes[idx] = (box_x, box_y)
        
        cur_warehouse = state.copy(tuple(worker), boxes)
        
        return cur_warehouse
    
    def goal_test(self, state):
        '''
        Override the function in search.py
        Check a state if it matches the goal state by checking the positions of 
        boxes is the same with the positions of targets (goals)
        
        @param state: a Warehouse object
        
        @return True: if the positions of the boxes match the positions of 
            the targets
        
        @return False: if the positions of the boxes do not match the positions
            of the targets
        '''
        return set(self.goal) == set(state.boxes) 
    
    
    def __init__(self, warehouse,initial=None,goal=None):
        '''
        Initialization Function
        @param:
                warehouse: a valid warehouse object
                initial: the initial state of warehouse
                goal: the list of targets or goals located in the warehouse
        '''
        self.x_size, self.y_size = find_size(warehouse)
        self.taboo_cells = taboo_cells(warehouse)
        if goal is None:
            self.goal = warehouse.targets
        else:
            self.goal = goal
        if initial is None:
            self.initial = warehouse
        else:
            self.initial = initial
        
    def actions(self, state):
        """
        Return the list of actions that can be executed in the given state 
        if these actions do not push a box in a taboo cell.
        The actions must belong to the list ['Left', 'Down', 'Right', 'Up']

        @param state: a changed state of valid warehouse object
        """
        move = []
        worker_x = state.worker[0]
        worker_y = state.worker[1]
        walls = state.walls
        boxes = state.boxes
        
        ## Check the action is not pushing the boxes to the taboo cells, and also the box shouldn't move if there's box or walls located behind them
        ## in the same moving direction

        #Left
        if isNot_walls_next_move(worker_x-1,worker_y,walls):
            if isNot_boxes_next_move(worker_x-1,worker_y,boxes):
                move.append("Left")
            else:
                if isNot_boxes_next_move(worker_x-2,worker_y,boxes) and isNot_walls_next_move(worker_x-2,worker_y,walls) and \
                    is_taboo_cells(worker_x-2,worker_y,self.taboo_cells) == False :
                    move.append("Left")
        #Right
        if isNot_walls_next_move(worker_x+1,worker_y,walls):
            if isNot_boxes_next_move(worker_x+1,worker_y,boxes):
                move.append("Right")
            else:
                if isNot_boxes_next_move(worker_x+2,worker_y,boxes) and isNot_walls_next_move(worker_x+2,worker_y,walls) and \
                    is_taboo_cells(worker_x+2,worker_y,self.taboo_cells) == False :
                    move.append("Right")
        #Up
        if isNot_walls_next_move(worker_x,worker_y-1,walls):
            if isNot_boxes_next_move(worker_x,worker_y-1,boxes):
                move.append("Up")
            else:
                if isNot_boxes_next_move(worker_x,worker_y-2,boxes) and isNot_walls_next_move(worker_x,worker_y-2,walls) and \
                    is_taboo_cells(worker_x,worker_y-2,self.taboo_cells) == False :
                    move.append("Up")
        #Down
        if isNot_walls_next_move(worker_x,worker_y+1,walls):
            if isNot_boxes_next_move(worker_x,worker_y+1,boxes):
                move.append("Down")
            else:
                if isNot_boxes_next_move(worker_x,worker_y+2,boxes) and isNot_walls_next_move(worker_x,worker_y+2,walls) and \
                    is_taboo_cells(worker_x,worker_y+2,self.taboo_cells) == False :
                    move.append("Down")
                    
        return move  

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def check_action_seq(warehouse, action_seq):
    '''
    
    Determine if the sequence of actions listed in 'action_seq' is legal or not.
    
    Important notes:
      - a legal sequence of actions does not necessarily solve the puzzle.
      - an action is legal even if it pushes a box onto a taboo cell.
        
    @param warehouse: a valid Warehouse object

    @param action_seq: a sequence of legal actions.
           For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
           
    @return
        The string 'Failure', if one of the action was not successul.
           For example, if the agent tries to push two boxes at the same time,
                        or push one box into a wall.
        Otherwise, if all actions were successful, return                 
               A string representing the state of the puzzle after applying
               the sequence of actions.  This must be the same string as the
               string returned by the method  Warehouse.__str__()
    '''
    
    boxes = list(warehouse.boxes)
    worker = list(warehouse.worker)
    cur_warehouse = warehouse.copy(worker, boxes)
    
    for action in action_seq:  
        # Check if the move is possible first
        # If it is not possible, return 'Failure'
        if is_move_possible(cur_warehouse, action):
            x, y = find_move(action)
            worker[0] += x
            worker[1] += y
            
            # Check all boxes if they are the same as the new worker position
            # If there is a box at the same coordinates
            # Push the box at the same direction the worker was walking
            for idx, box in enumerate(boxes):
                if box == (worker[0], worker[1]):
                    box_x = box[0] + x
                    box_y = box[1] + y
                    boxes[idx] = (box_x, box_y)

            cur_warehouse = warehouse.copy(worker, boxes)
        else:
            return "Failure"
        
    cur_warehouse = warehouse.copy(worker, boxes)    
    return cur_warehouse.__str__()

def check_macro_action_seq(warehouse,action_seq):
    '''
    Determine if the sequence of actions listed in the action seq is legal or not
    For example: some action cannot be used to move the boxes should returns Failure or else Correct if it can be used to fix the puzzle:
    
    @param warehouse: a valid warehouse object
    
    @param action_seq: a sequence of actions generated by solve_macro_move
    
    @return
            "Move is not found": for use of defensive programming if the action is not belongs to the
            ['Left','Right','Up','Down']
            
            "Failure" : if the action is not possible to move the boxes, For example the wall or box is located right
            beside the moving box in the same direction
            
    '''
    curr_warehouse = warehouse.copy()
    move_status = "Correct move"
    available_move = ['Left','Right','Up','Down']
    
    for (action_coordinate,action_move) in action_seq:
        worker = curr_warehouse.worker
        boxes = curr_warehouse.boxes
        worker = action_coordinate

        if action_move not in available_move: # defensive programming
            return "Move is not found"


        #Left        
        if action_move is "Left":
            if isNot_boxes_next_move(worker[0]-2,worker[1],boxes) and isNot_walls_next_move(worker[0]-2,worker[1],boxes):
                for index in range(len(boxes)):
                    if boxes[index] == (worker[0]-1,worker[1]):
                        boxes[index] == (worker[0]-2,worker[1])
                        worker = (worker[0]-1,worker[1])
            else:
                return "Failure"
        #Right    
        if action_move is "Right":
            if isNot_boxes_next_move(worker[0]+2,worker[1],boxes) and isNot_walls_next_move(worker[0]+2,worker[1],boxes):
                for index in range(len(boxes)):
                    if boxes[index] == (worker[0]+1,worker[1]):
                        boxes[index] == (worker[0]+2,worker[1])
                        worker = (worker[0]+1,worker[1])
            else:
                return "Failure"
        #Down    
        if action_move is "Down":
            if isNot_boxes_next_move(worker[0],worker[1]+2,boxes) and isNot_walls_next_move(worker[0],worker[1]+2,boxes):
                for index in range(len(boxes)):
                    if boxes[index] == (worker[0],worker[1]+1):
                        boxes[index] == (worker[0],worker[1]+2)
                        worker = (worker[0],worker[1]+1)
            else:
                return "Failure"
        #Up    
        if action_move is "Up":
            if isNot_boxes_next_move(worker[0],worker[1]-2,boxes) and isNot_walls_next_move(worker[0],worker[1]-2,boxes):
                for index in range(len(boxes)):
                    if boxes[index] == (worker[0],worker[1]-1):
                        boxes[index] == (worker[0],worker[1]-2)
                        worker = (worker[0],worker[1]-1)
            else:
                return "Failure"
    

        curr_warehouse = curr_warehouse.copy(worker,boxes)
        
    return move_status
    
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def solve_sokoban_elem(warehouse):
    '''    
    This function should solve using elementary actions 
    the puzzle defined in a file.
    
    @param warehouse: a valid Warehouse object

    @return
        A list of strings.
        If puzzle cannot be solved return ['Impossible']
        If a solution was found, return a list of elementary actions that solves
            the given puzzle coded with 'Left', 'Right', 'Up', 'Down'
            For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
            If the puzzle is already in a goal state, simply return []
    '''
    puzzle = SokobanPuzzle(warehouse)

    puzzleGoalState = warehouse.copy() 
    puzzleSolution = breadth_first_graph_search(puzzle)
    #puzzleSolution = depth_first_graph_search(puzzle)
    #puzzleSolution = astar_graph_search(puzzle, get_Heuristic)
    step_move_solution = []
    
    if (puzzle.goal_test(puzzleGoalState)):
        return step_move_solution
    elif (puzzleSolution is None or check_action_seq(warehouse,find_action(puzzleSolution)) is "Failure"):
        return ['Impossible']
    else:
        return find_action(puzzleSolution)
   

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def can_go_there(warehouse, dst):
    '''    
    Determine whether the worker can walk to the cell dst=(row,col) 
    without pushing any box.
    
    @param warehouse: a valid Warehouse object

    @return
      True if the worker can walk to cell dst=(row,col) without pushing any box
      False otherwise
    '''
    
    size_x, size_y = find_size(warehouse)
    
    # Set worker's x and y coordinates
    worker_x = warehouse.worker[0]
    worker_y = warehouse.worker[1]
    
    # Set destination's x and y coordinates
    dst_x = dst[0]
    dst_y = dst[1]
    
    for box in warehouse.boxes:
        # Set boxes' x and y coordinates
        box_x = box[0]
        box_y = box[1]
        
        # The worker cannot move to the destination:
        # If the box is on top of the destination
        # Or if the box is between the destination and worker in x coordinates
        # Or if the box is between the destination and worker in y coordinates
        # Or if the destination is out of bound (double elif statements)
        if box == dst:
            return False
        elif box_x in range(worker_x, dst_x) and box_y == worker_y: 
            return False      
        elif box_y in range(worker_y, dst_y) and box_x == worker_x:
            return False 
        elif dst_x <= 0 or dst_x > size_x:
            return False
        elif dst_y <= 0 or dst_y > size_y:
            return False
    
    return True

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def solve_sokoban_macro(warehouse):
    '''    
    Solve using macro actions the puzzle defined in the warehouse passed as
    a parameter. A sequence of macro actions should be 
    represented by a list M of the form
            [ ((r1,c1), a1), ((r2,c2), a2), ..., ((rn,cn), an) ]
    For example M = [ ((3,4),'Left') , ((5,2),'Up'), ((12,4),'Down') ] 
    means that the worker first goes the box at row 3 and column 4 and pushes it left,
    then goes the box at row 5 and column 2 and pushes it up, and finally
    goes the box at row 12 and column 4 and pushes it down.
    
    @param warehouse: a valid Warehouse object

    @return
        If puzzle cannot be solved return ['Impossible']
        Otherwise return M a sequence of macro actions that solves the puzzle.
        If the puzzle is already in a goal state, simply return []
    '''
    
    puzzleSolution = solve_sokoban_elem(warehouse)
    curr_warehouse = warehouse
    last_x,last_y = curr_warehouse.worker[1],curr_warehouse.worker[0]
    
    total_macro_move = []
    
    if "Impossible" in puzzleSolution or puzzleSolution is None :
        return total_macro_move.append('Impossible')
    else:
        for action in puzzleSolution:
            move_x,move_y = find_move(action)
            worker_x,worker_y = curr_warehouse.worker[0],curr_warehouse.worker[1]
            boxes = curr_warehouse.boxes
            worker_x = worker_x + move_x
            worker_y = worker_y + move_y
            worker = (worker_x,worker_y)


            #Left
            if action == "Left":
                if not isNot_boxes_next_move(worker_x,worker_y,boxes):
                    for index in range(len(boxes)):
                        if boxes[index] == (worker_x,worker_y):
                            boxes[index] = (worker_x-1,worker_y)
                                
                    total_macro_move.append(((last_x,last_y),action))
            #Right        
            if action == "Right":
                if not isNot_boxes_next_move(worker_x,worker_y,boxes):
                    for index in range(len(boxes)):
                        if boxes[index] == (worker_x,worker_y):
                            boxes[index] = (worker_x+1,worker_y)
                                
                    total_macro_move.append(((last_x,last_y),action))
            #Down        
            if action == "Down":
                if not isNot_boxes_next_move(worker_x,worker_y,boxes):
                    for index in range(len(boxes)):
                        if boxes[index] == (worker_x,worker_y):
                            boxes[index] = (worker_x,worker_y+1)
                                
                    total_macro_move.append(((last_x,last_y),action))
            #Up        
            if action == "Up":
                if not isNot_boxes_next_move(worker_x,worker_y,boxes):
                    for index in range(len(boxes)):
                        if boxes[index] == (worker_x,worker_y):
                            boxes[index] = (worker_x,worker_y-1)
                                
                    total_macro_move.append(((last_x,last_y),action))

            curr_warehouse = curr_warehouse.copy((worker_x,worker_y),boxes)
            last_x,last_y = worker_y, worker_x
            
        return total_macro_move  
    
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def find_size(warehouse):
    '''
    Helper function in order to find the size of the warehouse
    Both x and y axis

    @param: warehouse: the warehouse object
    
    @return
            x_size:  the column size of warehouse
            y_size: the row size of warehouse
    '''
    
    # Determine the y size of the warehouse by splitting all '\n'
    cells = str(warehouse).split('\n')    
    
    # Split all the strings into individual characters in order to determine 
    # the x size
    index = 0
    for strings in cells:
        cells[index] = list(strings)
        index += 1

    # Add +1 because lists starts with 0
    x_size = len(cells[0])
    y_size = len(cells)

    return (x_size, y_size)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def find_action(goal_node):
    '''
    Helper function to find the list of action from node list if the possible solution is
    found to fix the Sokoban Puzzle

    @param goal_node: the list of nodes has reached the goal test
    
    @return
            the list of actions from every node 
    '''
    path = goal_node.path()
    step_move = []
    for node in path:
        step_move.append(node.action)
    return step_move[1:]

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def is_move_possible(warehouse, action):
    '''
    Helper function to see if the next move is possible with particular action
    
    @param warehouse: the warehouse object
    @param action: the type of action. For example :['Left','Right','Up','Down']
    
    @return
        True: if the move is possible
        False: vice versa
    '''
    worker_x = warehouse.worker[0]
    worker_y = warehouse.worker[1]
    
    boxes = warehouse.boxes
    walls = warehouse.walls
    
    # Determine what kind of action it is and set the appropriate
    # number to x and y
    # xx and yy is to check if there is anything behind/infront the worker destionation
    x = 0 
    y = 0
    xx = 0
    yy = 0
    if (action == "Up"):
        y  -= 1
        yy -= 2
    elif (action == "Down"):
        y  += 1
        yy += 2
    elif (action == "Left"):
        x  -= 1
        xx -= 2
    elif (action == "Right"):
        x  += 1
        xx += 2
    else:
        return False
    
    # For every action
    # We check if the worker's new coordinates is inside the wall
    # or if the worker is moving to a box where there is another box ehind
    # or if the worker is pushing the box into a wall
    if (worker_x + x, worker_y + y) in walls:
        return False
    elif (worker_x + x, worker_y + y) in boxes and (worker_x + xx, worker_y + yy) in boxes:
        return False
    elif (worker_x + x, worker_y + y) in boxes and (worker_x + xx, worker_y + yy) in walls:
        return False
    else:
        return True
        
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def find_move(action):
    '''
    Helper function to find the position of x and y with particular action
    
    @param action: the type of action. For example :['Left','Right','Up','Down']
    
    @return
            x : x value  should be added one. For example, if the action is Right, 
            y : y value should be added one. For example, if the action is Down
    '''
    x = 0
    y = 0
    if (action == "Up"):
        y -= 1
    elif (action == "Down"):
        y += 1
    elif (action == "Left"):
        x -= 1
    elif (action == "Right"):
        x += 1
    
    return x, y

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def is_taboo(x, y, walls):
    '''
    Helper function to check if the corner walls are taboo
    @param x: the x coordinates
    @param y: the y coordinates
    @param walls: the locations of the walls
    
    @return
        True: if the coordinates is taboo
        False: vice versa
    '''
    taboo_1 = (x, y - 1) in walls and (x - 1, y) in walls # Top Left
    taboo_2 = (x, y - 1) in walls and (x + 1, y) in walls # Top Right
    taboo_3 = (x, y + 1) in walls and (x - 1, y) in walls # Bottom Left
    taboo_4 = (x, y + 1) in walls and (x + 1, y) in walls # Botoom Right
    if taboo_1 or taboo_2 or taboo_3 or taboo_4:
        return True
    else:
        return False

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def is_taboo_cells(unit_x,unit_y,taboo_cells):
    '''
    Helper function to check whether the position of moving box is located within the place market with 'X'
    @param unit_x: x coordinate of moving box
    @param unit_y: y coordinate of moving box
    @param taboo_cells: the list of string of taboo generated by taboo cells function
    @return:
            True: if the position is located in the place marked with 'X'
            False: vice versa
    '''
    taboo_rc = taboo_cells.split("\n")
    index = 0
    for strings in taboo_rc:
        taboo_rc[index] = list(strings)
        index +=1
    
    taboo_rc = taboo_rc[1:]
    
    if taboo_rc[unit_y-1][unit_x] is 'X':
        return True
    else:
        return False

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -   
   
def isNot_walls_next_move(x,y,walls):
    '''
    The function to check the location of walls

    @param x : coordinate x of unit (worker)
    @param y : cooridnate y of unit (worker)
            walls : the coordinates of walls in the updated warehouse
    @return
            True: if the walls is located at the same position as worker
            False: vice versa
    '''
    if (x,y) in walls:
        return False
    else:
        return True
        
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def isNot_boxes_next_move(x,y,boxes):
    '''
    The function to check the location of boxes

    @param x : coordinate x of unit (worker)
    @param y : cooridnate y of unit (worker)
            boxes : the coordinates of boxes in the updated warehouse
    @return
            True: if the boxes is located at the same position as worker
            False: vice versa
    '''
    if (x,y) in boxes:
        return False    
    else:
        return True
  
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  
  
def manhattan(coor_1, coor_2):
    '''
    The helper function to calculate the distance between player and boxes,
    the distance between player and targets

    @param coor_1: the x coordinate of boxes or targets
    @param coor_2: the y coordinate of boxes or targets

    @return: the distance between player and boxes or player and targets
    '''
    return abs(coor_1[0] - coor_2[0]) + abs(coor_1[1] - coor_2[1])

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def get_Distance(start, locations):
    '''
    The helper function to find the shortest distance between player
    and boxes or player and targets

    @param start: the coordinate of starting location
    @param locations: the coordinate of destination

    @return: the shortest distance 
    '''
    min_dist = 100000
    
    for coor in locations:
        dist = manhattan(start, coor)
        if (dist < min_dist):
            min_dist = dist
            
    return min_dist

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def get_Heuristic(node):
    '''
    The function used to find or get heuristic value for each node

    @param node: the changed state of warehouse object

    @return: the heuristic value for node to reach the goal
    '''
    warehouse = node.state
    worker = warehouse.worker
    boxes = warehouse.boxes
    targets = warehouse.targets
    
    sum = 0
    
    playerMin = get_Distance(worker, boxes)
    sum += playerMin
    
    for box in boxes:
        boxMin = get_Distance(box, targets)
        sum += boxMin
        
    return sum

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
