import random


def create_board(dimensions: tuple[int], positions: list[tuple],apples: list[tuple]) -> list[list[tuple]]:
    '''Creates snake board given information about the snake and the apple positions'''
    rows = dimensions[0]
    cols = dimensions[1]
    board = []
    for row in range(rows):
        curr_row = []
        for col in range(cols):
            if (row,col) in positions:
                curr_row.append((1, None))
            elif (row,col) in apples:
                curr_row.append((2,None))
            else:
                curr_row.append((0,None))
        board.append(curr_row)
    return board



def find_head(rows: int) -> tuple[int]:
    '''find the position of the head of the snake'''
    return ((rows//2),3)


def create_random_apple(dimensions: tuple[int], snake: list[tuple], apples: list[tuple]) -> tuple:
    '''creates apple position given a snake and a list of n apple positions'''
    rows = dimensions[0]
    cols = dimensions[1]
    apple = (random.randint(0,rows-1),random.randint(0,cols-1))
    if apple in snake:
        while True:
            apple = (random.randint(0, rows-1), random.randint(0, cols-1))
            if not apple in snake and not apple in apples:
                break
    return apple

def create_initial_apples(dimensions: tuple[int],snake_positions: list[tuple],apples: int) -> list[tuple]:
    '''Creates a list of n apples stored as a list of tuples'''
    apple_list = []
    for apple in range(apples):
        apple_list.append(create_random_apple(dimensions,snake_positions,apple_list))
    return apple_list