import pygame
from AIGame import SnakeAI

FRAME_RATE = 5


class SnakeAIVisual:

    def __init__(self) -> None:
        '''constructor for the Snake GUI objects'''
        self.state = SnakeAI.SnakeAI((40, 40))
        self.running = True
        pygame.init()
        pygame.display.set_mode((400, 400), pygame.RESIZABLE)
        current_screen_dimensions = pygame.display.get_window_size()

        self.set_background(current_screen_dimensions)
        pygame.display.flip()

        self.clock = pygame.time.Clock()

    def draw_board(self, screen_state: tuple) -> None:
        """Draws the board's current state"""
        current_screen = pygame.display.set_mode(screen_state[0], pygame.RESIZABLE)
        board = self.state.board
        snakes = self.state.snake_positions
        apples = self.state.apple

        potential_width = screen_state[0][0] / len(board[0]) / 2
        potential_length = screen_state[0][1]/len(board) / 2
        block = (potential_width,'w') if potential_length >= potential_width else (potential_length,'l')

        for row in range(len(board)):
            for position in range(len(board[0])):
                if block[1] == 'w':
                    x_increment = int(.25*screen_state[0][0] + (block[0]) * (position))
                    y_increment = int((.25*screen_state[0][1] * potential_length/potential_width) + (block[0]) * (row))
                else:
                    x_increment = int((.25 * screen_state[0][0] * potential_width/potential_length) + (block[0] * position))
                    y_increment = int((.25 * screen_state[0][1]) + (block[0] * row))

                surface = pygame.display.get_surface()
                color = pygame.Color('blue') if row %2 == 0 and position % 2 == 0 or row % 2 == 1 and position % 2 == 1 else pygame.Color((173,216,230))
                snake_rectangle = pygame.Rect(x_increment, y_increment, block[0], block[0])
                pygame.draw.rect(surface, color, snake_rectangle)

        for snake in snakes:
            if block[1] == 'w':
                x_increment = int(.25 * screen_state[0][0] + (block[0]) * (snake[1]))
                y_increment = int((.25 * screen_state[0][1] * potential_length / potential_width) + (block[0]) * (snake[0]))
            else:
                x_increment = int((.25 * screen_state[0][0] * potential_width / potential_length) + (block[0] * snake[1]))
                y_increment = int((.25 * screen_state[0][1]) + (block[0] * snake[0]))

            surface = pygame.display.get_surface()
            color = pygame.Color('green')
            snake_rectangle = pygame.Rect(x_increment, y_increment, block[0], block[0])
            pygame.draw.rect(surface,color,snake_rectangle)

        for apple in apples:
            if block[1] == 'w':
                x_increment = int(.25 * screen_state[0][0] + (block[0]) * (apple[1]))
                y_increment = int((.25 * screen_state[0][1] * potential_length / potential_width) + (block[0]) * (apple[0]))
            else:
                x_increment = int((.25 * screen_state[0][0] * potential_width / potential_length) + (block[0] * apple[1]))
                y_increment = int((.25 * screen_state[0][1]) + (block[0] * apple[0]))

            surface = pygame.display.get_surface()
            color = pygame.Color('red')
            apple_rectangle = pygame.Rect(x_increment, y_increment, block[0],block[0])
            pygame.draw.rect(surface, color, apple_rectangle)


        font = pygame.font.Font('freesansbold.ttf', int(.09 * screen_state[0][1]))
        end_text = font.render(f'score: {self.state.length}', True, pygame.Color(255, 255, 255), pygame.Color(0, 0, 0))
        current_screen.blit(end_text, (0,0))

        button_images = pygame.image.load('Images/SnakeAIImage.jpg')
        button_images = pygame.transform.scale(button_images, (int(screen_state[0][0]), int(.2*screen_state[0][1])))
        current_screen.blit(button_images, ((0, .8*screen_state[0][1])))
        pygame.display.flip()


    def set_background(self,size: tuple) -> None:
        '''Draws initial background'''
        screen = pygame.display.set_mode(size, pygame.RESIZABLE)
        screen.fill('black')


    def set_end_screen(self,size: tuple) -> None:
        '''Draws end screen'''
        current_screen = pygame.display.set_mode(size,pygame.RESIZABLE)
        current_screen.fill((0,0,255))

        font = pygame.font.Font('freesansbold.ttf', int(.09 * size[0]))
        end_text = font.render('GAME OVER', True, pygame.Color(255,0,0), pygame.Color(0,0,0))
        current_screen.blit(end_text,(size[0]/2- int(.1*size[0]*3),size[1]/2))
        pygame.display.update()



    def play_step(self, action: str) -> tuple:
        '''
        Plays a step in snake game and updates UI for training
        :returns a tuple containing the reward, if the game is still playing, and the score
        '''
        self.state.shift_snake_directions(action)
        self.state.shift_snake_positions()

        game_over = False
        reward = 0

        if self.state.check_snake_out_of_bounds() or self.state.check_snake_collision():

            game_over = True
            reward = -10
            return reward, game_over, self.state.length-3

        if self.state.check_apple_eaten():
            reward = 10


        self.state.update_board()
        current_screen_dimensions = pygame.display.get_window_size()


        self.draw_board(current_screen_dimensions)
        self.clock.tick(FRAME_RATE)


        return reward,game_over,self.state.length

    def play_step_testing(self, action: str, screen_dimensions=None) -> None:
        '''
        Plays a step in snake game and updates UI for testing
        :returns None
        '''
        self.state.shift_snake_directions(action)
        self.state.shift_snake_positions()

        if self.state.check_snake_out_of_bounds() or self.state.check_snake_collision():
            return 'AI', True

        self.state.check_apple_eaten()

        self.state.update_board()

        if screen_dimensions is None:
            current_screen_dimensions = pygame.display.get_window_size()
            self.draw_board(current_screen_dimensions)
        else:
            self.draw_board(screen_dimensions)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'EXIT', True
            elif event.type == pygame.VIDEORESIZE:
                screen_dimensions[0] = event.size
                return 'AI', False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_0:
                    return 'Home', True
                elif event.key == pygame.K_1:
                    return 'Human', True

        self.clock.tick(FRAME_RATE)


        return 'AI',False
