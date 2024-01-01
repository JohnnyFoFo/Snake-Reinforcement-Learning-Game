from HumanGame import GameHelper as gh


class SnakeAI:

    def __init__(self, board_dimensions: tuple) -> None:
        '''Constructor for Snake AI game logic objects'''

        self.length = 3
        self.head_position = gh.find_head(board_dimensions[0])
        self.snake = [((self.head_position[0],0), 'R'),((self.head_position[0],1),'R'),((self.head_position[0],2),'R')]
        self.snake_positions = [(self.head_position[0],0),(self.head_position[0],1),(self.head_position[0],2)]
        self.apple = gh.create_initial_apples(board_dimensions,self.snake_positions,1)
        self.board = gh.create_board(board_dimensions,self.snake_positions,self.apple)

    def print_board(self) -> None:
        '''Prints current board state in 0,1,2 form'''
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                print(self.board[row][col][0], ' ', end='')
            print()


    def shift_snake_directions(self, new_head_direction: str) -> list[tuple]:
        '''shifts snake directions to follow the part before it'''
        previous_direction = ''
        for s in range(len(self.snake)-1,-1,-1):
            if s == len(self.snake)-1:
                previous_direction = self.snake[-1][1]
                self.snake[-1] = (self.snake[-1][0],new_head_direction)
            else:
                current = previous_direction
                previous_direction = self.snake[s][1]
                self.snake[s] = (self.snake[s][0],current)
        return self.snake

    def shift_snake_positions(self) -> None:
        '''shifts snake positions to adjust for the snake directions'''

        for pos in range(len(self.snake)-1,-1,-1):


            if self.snake[pos][1] == 'R':
                current = ((self.snake[pos][0][0], self.snake[pos][0][1] + 1 ), 'R')
                self.snake.remove(self.snake[pos])
                self.snake.insert(pos,current)

                self.snake_positions[pos] = current[0]

            elif self.snake[pos][1] == 'L':
                current = ((self.snake[pos][0][0], self.snake[pos][0][1] - 1), 'L')
                self.snake.remove(self.snake[pos])
                self.snake.insert(pos, current)

                self.snake_positions[pos] = current[0]

            elif self.snake[pos][1] == 'U':
                current = ((self.snake[pos][0][0]-1, self.snake[pos][0][1]), 'U')
                self.snake.remove(self.snake[pos])
                self.snake.insert(pos, current)

                self.snake_positions[pos] = current[0]


            elif self.snake[pos][1] == 'D':
                current = ((self.snake[pos][0][0]+1, self.snake[pos][0][1]), 'D')
                self.snake.remove(self.snake[pos])
                self.snake.insert(pos, current)

                self.snake_positions[pos] = current[0]


    def extend_snake(self) -> None:
        '''extends the snakes tail by one'''
        snake_end = self.snake[0]
        snake_end_position = snake_end[0]
        snake_end_direction = snake_end[1]

        if snake_end_direction == 'R':
            self.snake.insert(0,((snake_end_position[0],snake_end_position[1]-1),'R'))
            self.snake_positions.insert(0,(snake_end_position[0],snake_end_position[1]-1))
        elif snake_end_direction == 'L':
            self.snake.insert(0,((snake_end_position[0],snake_end_position[1]+1),'L'))
            self.snake_positions.insert(0,(snake_end_position[0],snake_end_position[1]+1))
        elif snake_end_direction == 'U':
            self.snake.insert(0,((snake_end_position[0]+1,snake_end_position[1]),'U'))
            self.snake_positions.insert(0,(snake_end_position[0]+1,snake_end_position[1]))
        elif snake_end_direction == 'D':
            self.snake.insert(0,((snake_end_position[0]-1,snake_end_position[1]),'D'))
            self.snake_positions.insert(0,(snake_end_position[0] - 1, snake_end_position[1]))
        self.length += 1



    def check_apple_eaten(self) -> bool:
        '''Checks if apple is eaten, if yes it extends snake and creates new apple, else does nothing'''
        for apple in self.apple:
            if apple in self.snake_positions:
                self.apple.remove(apple)
                self.extend_snake()
                self.apple.append(gh.create_random_apple((len(self.board),len(self.board[0])),self.snake,self.apple))
                return True
        return False


    def check_snake_out_of_bounds(self) -> bool:
        '''Checks if snake is out of bounds, if yes it returns True, else False'''
        for pos in self.snake_positions:
            row = pos[0]
            col = pos[1]
            if row >= len(self.board) or col >= len(self.board[0]) or row < 0 or col < 0:
                return True
        return False

    def check_snake_collision(self) -> bool:
        '''Checks if snake collided with itself, if yes returns True, else False'''
        for pos in range(len(self.snake_positions)):
            for new_pos in range(pos+1,len(self.snake_positions)):
                if self.snake_positions[pos] == self.snake_positions[new_pos]:
                    return True
        return False

    def update_board(self) -> None:
        '''Updates the board to adjust to new snake and apple positions'''
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                if (row,col) in self.snake_positions:
                    index = self.snake_positions.index((row,col))
                    self.board[row][col] = (1,self.snake[index][1])
                elif (row,col) in self.apple:
                    self.board[row][col] = (2,None)
                else:
                    self.board[row][col] = (0, None)




    def reset(self) -> None:
        '''Resets all object attributes after game ends'''
        self.length = 3
        self.head_position = gh.find_head(len(self.board))
        self.snake = [((self.head_position[0],0), 'R'),((self.head_position[0],1),'R'),((self.head_position[0],2),'R')]
        self.snake_positions = [(self.head_position[0],0),(self.head_position[0],1),(self.head_position[0],2)]
        self.apple = gh.create_initial_apples((len(self.board),len(self.board[0])),self.snake_positions,1)
        self.board = gh.create_board((len(self.board),len(self.board[0])),self.snake_positions,self.apple)

