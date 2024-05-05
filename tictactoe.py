# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 20:09:06 2020

@author: hcadi
"""

"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    Assumes that in the initial game state, X gets the first move, as per the spec.
    """
    numX, numO = 0, 0
    for i in board:
        for n in range(len(i)):
            if i[n] == X:
                numX += 1
            elif i[n] == O:
                numO += 1
    if numX == numO:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    moves = set()
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == EMPTY:
                moves.add((i, j))
    return moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise ValueError('Not a valid action')
    else:
        tempBoard = copy.deepcopy(board)
        turn = player(tempBoard)
        tempBoard[action[0]][action[1]] = turn
    return tempBoard


def winner(board):
    """
    Returns the winner of the game, if there is one.
    Assumes there is at most one winner as per the spec.
    """
    for i in range(len(board)): # Checks if any player won with 3 in a row
        if board[i][0] == board[i][1] and board[i][1] == board[i][2]:
            return board[i][0]

    for i in range(len(board)): # Checks if any player won with 3 in a column
        if board[0][i] == board[1][i] and board[1][i] == board[2][i]:
            return board[0][i]

    if board[0][0] == board[1][1] and board[1][1] == board[2][2]: # Checks one diagonal
        return board[1][1]

    if board[0][2] == board [1][1] and board[1][1] == board[2][0]: # Checks the remaining diagonal
        return board[1][1]

    return None # Returns None if there is no winner


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) != None:
        return True
    return EMPTY not in board[0] and EMPTY not in board[1] and EMPTY not in board[2]


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    Assumes utility will only be called on a board if terminal(board) is True, as per the spec
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    if player(board) == X:
        return maxValue(board)[1]
    else:
        return minValue(board)[1]

def maxValue(board):
    """
    Returns the optimal action for the max player on the board,
    along with its utility, and number of empty cells as a proxy
    to how fast the given actions led to the reported utility.
    Follows the format (utility, action, numEmpty).
    """
    if terminal(board):
        return  (utility(board), (), numEmpty(board))
    v = (float('-inf'), (), float('-inf'))                  # Variable that stores (utility, action, numEmpty)
    for action in actions(board):
        newV = minValue(result(board, action))
        if max(v[0], newV[0]) != v[0]:                      # If the utility of the a new action is better,
            v = (newV[0], action, newV[2])                  # then stores (utility, action, numEmpty).
        elif v[0] == newV[0] and newV[2] > v[2]:            # If the new action leads to an equally optimal utility in fewer moves,
            v = (v[0], action, newV[2])                     # then store it instead.
        if v[0] == 1 and numEmpty(board) == (v[2] + 1):     # If the optimal utility has been found with the fewest moves possible, prune the remaining branches
            return v
    return v

def minValue(board):
    """
    Returns the optimal action for the min player on the board,
    along with its utility, and number of empty cells as a proxy
    to how fast the given actions led to the reported utility.
    Follows the format (utility, action, numEmpty).
    """
    if terminal(board):
        return (utility(board), (), numEmpty(board))
    v = (float('inf'), (), float('-inf'))                   # Variable that stores (utility, action, numEmpty)
    for action in actions(board):
        newV = maxValue(result(board, action))
        if min(v[0], newV[0]) != v[0]:                      # If the utility of the a new action is better,
            v = (newV[0], action, newV[2])                  # then stores (utility, action, numEmpty)
        elif v[0] == newV[0] and newV[2] > v[2]:            # If the new action leads to an equally optimal outcome in fewer moves,
            v = (v[0], action, newV[2])                     # then store it instead.
        if v[0] == -1 and numEmpty(board) == (v[2] + 1):    # If the optimal utility has been found with the fewest moves possible, prune the remaining branches
            return v
    return v

def numEmpty(board):
    """
    Returns the number of EMPTY cells in a given board.
    Used as an heuristic to pick the shortest path to the desired utility.
    """
    numEmpty = 0
    for u in range(len(board)):
        for y in range(len(board[u])):
            if board[u][y] == EMPTY:
                numEmpty += 1
    return numEmpty