## Author: Taylor Olson

## Synopsis: Program that can get the user the best move to make for this game.
## This implements a MinMax recursion alogrithm to make best decisions.

## Overview: The program asks the user for a 6 character string. The string
## should consist of numbers from 0-9. The numbers in each position correspond
## to how many coins are in that pile. When a player takes from a pile they
## move to the right, placing one coin in each spot to the right until they
## get rid of all of the coins they picked up. If they get to the last spot
## and still have coins, those coins are dropped out of the game.
## The goal is to be the last one to pick up coins.
## The program will tell you the best move and if you will win or lose based
## on your opponent making the best move possible every turn.


from operator import itemgetter

def main():
    board = get_input()
    while board != "X":
        nums = []
        moves = get_avail_moves(board)
        dictionary = {}
        for move1 in moves:
            new_board = make_move(board, move1)
            nums.append([move1,MiniMax(new_board, False, 1, dictionary)])
            
        nums = sorted(nums, key=itemgetter(1))
        take_from = nums[-1]
        if take_from[1] < 0:
            take_from = nums[0]
            print("Take from pile " + str(take_from[0] + 1) + " and you will lose :(.")
        else:
            print("Take from pile " + str(take_from[0] + 1) + " and you will win!")
                
                
        board = get_input()
        

def get_input():
    board = input("Enter 6 character string or X to exit: ")
    if board == "X":
        return board
    new_board = []
    for char in board:
        new_board.append(int(char))
    return new_board

def board_to_string(board):
    val = ""
    for item in board:
        val += str(item)
    return val

def MiniMax(board, Max, num_of_moves, dictionary):
    if isLeaf(board):
        return evaluate(not Max, num_of_moves)
    
    
    if Max:
        highest = float('-inf')
        moves = get_avail_moves(board)
        board_string = board_to_string(board)
        for move1 in moves:
            #look up board, move, turn in table
            #if not in table then make move and add board, move, turn, val in table
            what_to_look_up = (board_string, move1, True)
            look_up_val = look_up(dictionary, what_to_look_up)
            if look_up_val == "T":
                new_board = make_move(board, move1)
                temp = MiniMax(new_board, False, num_of_moves + 1, dictionary)
                dictionary[(board_string, move1, True)] = temp
            #if in table set temp = val from table
            else:
                temp = look_up_val
            highest = max(highest, temp)
             
        return highest

    else:
        lowest = float('inf')
        moves = get_avail_moves(board)
        board_string = board_to_string(board)
        for move1 in moves:
            what_to_look_up = (board_string, move1, False)
            look_up_val = look_up(dictionary, what_to_look_up)
            if look_up_val == "T":
                new_board = make_move(board, move1)
                temp = MiniMax(new_board, True, num_of_moves + 1, dictionary)
                dictionary[(board_string, move1, False)] = temp
            else:
                temp = look_up_val
            lowest = min(lowest, temp)
            
        return lowest  


def look_up(dictionary, lookup):
    if lookup in dictionary:
        return dictionary.get(lookup)
    else:
        return "T"
            

def get_avail_moves(board):
    ##Takes in a board state
    ##Returns index of possible moves the player can take from

    list_of_moves = []
    position = 0
    for stone in board:
        if stone != 0:
            list_of_moves.append(position)
        position += 1
    return list_of_moves
    
def make_move(board, move):
    new_board = board[:]
    amount = new_board[move]
    new_board[move] = 0
    index = move+1
    while index < len(board) and amount > 0:
        new_board[index] += 1
        index+=1
        amount-=1
        
    return new_board

def isLeaf(board):
    moves = get_avail_moves(board)
    if len(moves) == 0:
        return True
    else:
        return False


def evaluate(Max, num_of_moves):
    if Max:
        return (100-num_of_moves) * 1
    else:
        return (100-num_of_moves) * -1
    
main()


