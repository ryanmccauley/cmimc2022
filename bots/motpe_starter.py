from operator import ge
import sys
import json
import random
from tkinter import E

# INPUT FORMAT (as tower):
'''
    "role": "tower"
    "generator": "uniform" or "circles" or "path"
    "parameter": The difficulty parameter for the generator
        (see problem statement for details). Most simple solutions
        can safely ignore this value.
    "airspace": A 2D (256x256) list of integers representing the grid,
        1 for an unsafe square and 0 for safe. Can be indexed via
        airspace[i][j], where i=255 is the bottom row of the grid.
'''
# OUTPUT FORMAT (as tower):
'''
    "bits": array of 64 0s or 1s, to be passed to your drone.
'''
# Function for handling tower output
def tower_output(bits):
    print(json.dumps({"bits": bits}))



# INPUT FORMAT (as drone):
'''
    "role": "drone"
    "generator": "uniform" or "circles" or "path" (same as above)
    "parameter": difficulty parameter for the generator (same as above)
    "bits": The array of 64 0s or 1s, passed to you by the tower.
'''
# OUTPUT FORMAT (as drone):
'''
    "col": Your starting square in the grid will be airspace[255][col].
    "moves": A string of length at most 2^16 = 65536, consisting of the
        letters "ULDR", denoting moves up, left, down, right,
        to be made in the order sent.
'''
# Function for handling drone output
def drone_output(col, moves):
    print(json.dumps({"col": col, "moves": moves}))



# Fetches input from grader (no need to edit)
_data = json.loads(input())
role = _data["role"]
generator = _data["generator"]
parameter = _data["parameter"]
if role == "tower":
    airspace = _data["airspace"]
if role == "drone":
    bits = _data["bits"]
# End input

def find_highest_left_move(row, col) -> list:
    max_col = col - 1
    max_height = 0

    for i in range(1, 8):
        if airspace[row][col-i] == 1:
            break
        else:
            if max_height < highest_up_from_point(row, col-i):
                max_height = highest_up_from_point(row, col-i)
                max_col = col-i
    
    return [max_height, max_col]

def find_highest_right_move(row, col) -> list:
    max_col = col + 1
    max_height = 0

    for i in range(1, 8):
        if airspace[row][col+i] == 1:
            break
        else:
            if max_height < highest_up_from_point(row, col+i):
                max_height = highest_up_from_point(row, col+i)
                max_col = col-i
    
    return [max_height, max_col]

# def findHighestLeft(row, col) -> list:
#     #print("Starting left column", col, file = sys.stderr)
#     maximum_height = 0
#     maximum_column = col-1

#     values = []

#     for move in range(0, 7):
#         new_col = col - move - 1
#         if airspace[row][new_col] == 1:
#             continue

#         if new_col < 0 or new_col > 255:
#             return [0, col]
#         highest = highest_up_from_point(row, new_col)
#         values.append(highest)
#         if highest > maximum_height:
#             maximum_height = highest
#             maximum_column = new_col

    
#     #print("Highest values", values, file = sys.stderr)

#     #print("Ending left column", maximum_column, file = sys.stderr)
#     #print("Highest left real", highest_up_from_point(row, maximum_column), "Highest left", maximum_height, file = sys.stderr)
#     return [maximum_height, maximum_column]

# def findHighestRight(row, col) -> list:
#     #rint("Starting right column", col, file = sys.stderr)
#     maximum_height = 0
#     maximum_column = col+1

#     values = []
#     for move in range(0, 7):
#         new_col = col + move + 1
#         if airspace[row][new_col] == 1:
#             continue
#         if new_col < 0 or new_col > 255:
#             return [0, col]
#         highest = highest_up_from_point(row, new_col)
#         values.append(highest)
#         if highest > maximum_height:
#             maximum_height = highest
#             maximum_column = new_col

#     #print("Highest values", values, file = sys.stderr)

#     #print("Ending right column", maximum_column, file = sys.stderr)
#     #print("Highest right real", highest_up_from_point(row, maximum_column), "Highest right", maximum_height, file = sys.stderr)       
#     return [maximum_height, maximum_column]
# """
#     Row: row, Col: col
#     Current_Pos: [row, col]
#     Current_Height: 0
# """
# def backtrack_solve(row, col, current_pos, current_height) -> str:
#     pass

def get_binary(value: int, length = 8):
    return '%0*d' % (length, int(bin(value)[2:]))

def highest_up_from_point(row, col):
    if airspace[row][col] == 1:
        return -1

    maximum_length = 0

    current_height = 0
    safe = airspace[row][col] != 1
    while safe:
        current_height += 1

        if airspace[row - current_height][col] == 1:
            safe = False
        else:
            safe = airspace[row][col] != 1

        if current_height > maximum_length:
            maximum_length = current_height

    return maximum_length


## REPLACE STRATEGY BELOW ##

def countNumberOfUps(moves):
    count = 0
    for move in moves:
        if move == "U":
            count += 1
    return count

# NOTE: grid is row major
def checkIfMovesWork(starting_col, moves, grid):
    max_height = 0
    current_pos = [255, starting_col]

    while grid[current_pos[0]][current_pos[1]] == 0:

        consume = moves[0]
        moves = moves[1:]

        if consume == "U":
            current_pos[0] -= 1
        elif consume == "L":
            current_pos[1] -= 1
        elif consume == "D":
            current_pos[0] += 1
        elif consume == "R":
            current_pos[1] += 1

        max_height = max(max_height, 255 - current_pos[0])

    print("* Maximum Height Accomplished:", max_height, file = sys.stderr)

def conertBitsToMoves(bits):
    moves = []

    starting_col = int("".join(map(str, bits[0:8])), 2)

    #print("starting binary:", "".join(map(str, bits[0:8])), file = sys.stderr)
    #print("starting: " + str(starting_col), file = sys.stderr)

    bits = bits[8:]

    #print("new length" + str(len(bits)), file = sys.stderr)

    while len(bits) >= 1:
        if len(bits) < 8:
            break

        amount_to_move_up = int("".join(map(str, bits[0:7])), 2)
        bits = bits[7:]

        #print("new length" + str(len(bits)), file = sys.stderr)


        #print("amount to move up", amount_to_move_up, file = sys.stderr)

        for _ in range(0, amount_to_move_up):
            moves.append("U")

        if len(bits) < 1:
            break
        rotate = int("".join(map(str, bits[0:1])), 2)
        bits = bits[1:]
        #print("new length" + str(len(bits)), file = sys.stderr)


        if len(bits) < 4:
            break
        #print(bits, file = sys.stderr)
        #print("amount to rotate", bits[0:4], file = sys.stderr)
        amount = int("".join(map(str, bits[0:4])), 2)
        bits = bits[4:]

        #print("new length" + str(len(bits)), file = sys.stderr)


        for _ in range(0, amount):
            if rotate == 0:
                moves.append("L")
            else:
                moves.append("R")

    return moves

def get_highest_starting_column():
    highest_starting = [0, 0]

    for i in range(0, 256):
        highest_y = highest_up_from_point(255, i)
        if highest_y > highest_starting[1]:
            highest_starting = [i, highest_y]

    starting_col = highest_starting[0]

    return starting_col

def get_best_direction(row, col):
    # 0 for left, 1 for right (By default left)
    best_direction = 0

    left_max_height = 0
    left_max_column = col-1

    right_max_height = 0
    right_max_column = col+1

    for move in range(1, 8):
        new_col = col - move
        if airspace[row][new_col] == 1:
            break
        if new_col < 0 or new_col > 255:
            break
        highest = highest_up_from_point(row, new_col)
        if highest > left_max_height:
            left_max_height = highest
            left_max_column = new_col
    
    for move in range(1, 8):
        new_col = col + move
        if airspace[row][new_col] == 1:
            break
        if new_col < 0 or new_col > 255:
            break
        highest = highest_up_from_point(row, new_col)
        if highest > right_max_height:
            right_max_height = highest
            right_max_column = new_col

    if left_max_height > right_max_height:
        best_direction = 0
    else:
        best_direction = 1

    direction = "Right" if best_direction == 1 else "Left"

    print(" Best Direction:", direction, file = sys.stderr)

    print(" Left Max Height:", left_max_height, file = sys.stderr)
    print(" Left Max Column:", left_max_column, file = sys.stderr)

    print(" Right Max Height:", right_max_height, file = sys.stderr)
    print(" Right Max Column:", right_max_column, file = sys.stderr)

    return [best_direction, left_max_column, right_max_column]

if role == "tower":
    # Can read variable "airspace", but not "bits"
    #print("airspace", ''.join(map(str, airspace[255])), file = sys.stderr) # example print

    output = []
    
    starting_col = get_highest_starting_column()
    starting_binary = str(get_binary(starting_col))
    current_pos = [255, starting_col]

    print("Starting Position", current_pos, file = sys.stderr)

    for bit in starting_binary:
        output.append(int(bit))

    highest_possible = highest_up_from_point(255, starting_col) - 2

    for bit in str(get_binary(highest_possible, 7)):  
        output.append(int(bit))

    current_pos[0] -= highest_possible

    print("Current Position:", current_pos, file = sys.stderr)

    best_direction = get_best_direction(current_pos[0], current_pos[1])
    dir_to_move = "right" if best_direction[0] == 1 else "left"

    output.append(int(best_direction[0]))

    print("Direction to move:", dir_to_move, file = sys.stderr)

    column_wanted = best_direction[1] if dir_to_move == "left" else best_direction[2]
    delta_col = column_wanted - current_pos[1]

    print("Amount to Move:", delta_col, file = sys.stderr)
    print("Amount to move bits:" + str(get_binary(abs(delta_col), 3)), file = sys.stderr)

    delta_binary = str(get_binary(abs(delta_col), 3))

    for bit in delta_binary:
        output.append(int(bit))

    current_pos[1] += delta_col

    print("Current Position:", current_pos, file = sys.stderr)

    highest_possible = highest_up_from_point(current_pos[0], current_pos[1])
    print("Highest Possible:", highest_possible, file = sys.stderr)
    for bit in str(get_binary(highest_possible, 7)):
        output.append(int(bit))

    current_pos[0] -= highest_possible
    
    best_direction = get_best_direction(current_pos[0], current_pos[1])
    dir_to_move = "right" if best_direction[0] == 1 else "left"

    output.append(int(best_direction[0]))

    print("Direction to move:", dir_to_move, file = sys.stderr)

    column_wanted = best_direction[1] if dir_to_move == "left" else best_direction[2]
    delta_col = column_wanted - current_pos[1]

    print("Amount to Move:", delta_col, file = sys.stderr)
    print("Amount to move bits:" + str(get_binary(abs(delta_col), 3)), file = sys.stderr)

    delta_binary = str(get_binary(abs(delta_col), 3))

    for bit in delta_binary:
        output.append(int(bit))

    current_pos[1] += delta_col




    # while len(output) < 64:
    #     wall_right = airspace[current_pos[0]][current_pos[1]+1] == 1
        
    #     print("Wall Right?", not wall_right, file = sys.stderr)

    #     if wall_right:
    #         output.append(0)
    #     else:
    #         output.append(1)

    #     output.append(0)
    #     output.append(0)
    #     output.append(1)

    #     current_pos[1] = current_pos[1] - 7 if wall_right else current_pos[1] + 7

    #     highest_possible = highest_up_from_point(current_pos[0], current_pos[1])

    #     for bit in str(get_binary(highest_possible+1, 7)):
    #         if len(output) > 64:
    #             continue
    
    #     output.append(int(bit))

    # while len(output) < 64:
    #     if airspace[current_pos[0]][current_pos[1]] == 1:
    #         print("DEATH!", file = sys.stderr)
    #         break

    #     highest_possible = highest_up_from_point(current_pos[0], current_pos[1])

    #     print("\n> Moving up:", highest_possible, "\n", file = sys.stderr)
        
    #     for bit in str(get_binary(highest_possible-1, 7)):
    #         if len(output) > 64:
    #             continue

    #         output.append(int(bit))

    #     current_pos[0] -= highest_possible - 1

    #     best_direction = get_best_direction(current_pos[0], current_pos[1])
                

    #     if best_direction[0] == 0:
    #         output.append(0)
    #     else:
    #         output.append(1)
        
    #     current_col = current_pos[1]
    #     needed_moves = 0 

    #     if best_direction[0] == 0:
    #         needed_moves = current_col - best_direction[1]
    #     else:
    #         needed_moves = best_direction[2] - current_col

    #     print("Needed moves", get_binary(needed_moves, 3), needed_moves, file = sys.stderr)

    #     for bit in str(get_binary(needed_moves, 3)):
    #         if len(output) > 64:
    #             continue

    #         output.append(int(bit))

    #     current_pos[1] = best_direction[1] if best_direction[0] == 0 else best_direction[2]

    tower_output(output)

def print_bits(bits):
    print("Bits", "".join(map(str, bits)), file = sys.stderr)

def convert_bits_to_moves(bits):
    moves_to_return = []

    print(len(bits), file = sys.stderr)

    while len(bits) > 0:
        direction_to_move = bits[0]
        bits = bits[1:]

        print(len(bits), file = sys.stderr)

        amount_to_move_h = int("".join(map(str, bits[0:3])), 2)

        for _ in range(amount_to_move_h):
            moves_to_return.append("R" if direction_to_move == 1 else "L")
        
        bits = bits[3:]

        amount_to_move_h = int("".join(map(str, bits[0:7])), 2)

        for _ in range(amount_to_move_h):
            moves_to_return.append("U")
            
        bits = bits[7:]
    
    print("Moves", moves_to_return, file = sys.stderr)

    return moves_to_return




if role == "drone":
    # Can read variable "bits", but not "airspace"
    #print("bits", ''.join(map(str, bits)), file = sys.stderr) # example print

    #print("bits length", len(bits), file = sys.stderr)
    #print("bits array", bits, file = sys.stderr)

    # print_bits(bits)

    # moves = []

    # starting_col = int("".join(map(str, bits[0:8])), 2)

    # #print("starting binary:", "".join(map(str, bits[0:8])), file = sys.stderr)
    # #print("starting: " + str(starting_col), file = sys.stderr)

    # bits = bits[8:]

    # print_bits(bits)

    # #print("new length" + str(len(bits)), file = sys.stderr)

    # while len(bits) >= 1:
    #     if len(bits) < 8:
    #         break

    #     print("Amount To Move Up Bits: " + "".join(map(str, bits[0:7])), file = sys.stderr)

    #     amount_to_move_up = int("".join(map(str, bits[0:7])), 2)
    #     bits = bits[7:]

    #     print("Amount To Move Up :", amount_to_move_up, file = sys.stderr)

    #     #print("new length" + str(len(bits)), file = sys.stderr)


    #     #print("amount to move up", amount_to_move_up, file = sys.stderr)

    #     for _ in range(0, amount_to_move_up):
    #         moves.append("U")

    #     if len(bits) < 1:
    #         break

    #     print("Direction Bit: " + "".join(map(str, bits[0:1])), file = sys.stderr)

    #     rotate = int("".join(map(str, bits[0:1])), 2)
    #     bits = bits[1:]
    #     #print("new length" + str(len(bits)), file = sys.stderr)


    #     if len(bits) < 4:
    #         break
    #     #print(bits, file = sys.stderr)
    #     #print("amount to rotate", bits[0:4], file = sys.stderr)
    #     print("Rotation Bits: " + "".join(map(str, bits[0:3])), file = sys.stderr)
    #     amount = int("".join(map(str, bits[0:3])), 2)
    #     bits = bits[4:]

    #     #print("new length" + str(len(bits)), file = sys.stderr)


    #     for _ in range(0, amount):
    #         if rotate == 0:
    #             moves.append("L")
    #         else:
    #             moves.append("R")

    # print("Moves:", "".join(map(str, moves)), file = sys.stderr)
    # print("Total: " + str(len(moves)), file = sys.stderr)

    # drone_output(starting_col, moves)

    #print_bits(bits)

    moves = []
    
    # Read first 8 bits
    starting_col = int("".join(map(str, bits[0:8])), 2)

    bits = bits[8:]

    print_bits(bits)

    # Get how far to first move from 7 bits
    first_move = int("".join(map(str, bits[0:7])), 2)

    for _ in range(first_move):
        moves.append("U")

    bits = bits[7:]

    while True:
        try:
            direction_to_move = bits[0]
            bits = bits[1:]

            print_bits(bits)

            print("Amount to move H bits:" + "".join(map(str, bits[0:3])), file = sys.stderr)
                    
            amount_to_move_h = int("".join(map(str, bits[0:3])), 2)
            bits = bits[3:]

            print_bits(bits)

            print("Amount to move H:", amount_to_move_h, file = sys.stderr)
                    
            for _ in range(amount_to_move_h):
                if direction_to_move != 1:
                    moves.append("L")
                else:
                    moves.append("R")

            amount_to_move_v = int("".join(map(str, bits[0:7])), 2)

            print("Amount to move V:", amount_to_move_v, file = sys.stderr)

            for _ in range(amount_to_move_v):
                moves.append("U")

            bits = bits[7:]

            print("Length: " + str(len(bits)), file = sys.stderr)
        except:
            break
    
    print("Moves: ", "".join(map(str, moves)), file = sys.stderr)

    drone_output(starting_col, moves)
