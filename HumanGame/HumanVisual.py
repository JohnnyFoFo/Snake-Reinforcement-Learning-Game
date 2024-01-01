import pygame
from HumanGame import Human

FRAME_RATE = 1


class HumanVisual:

    def __init__(self, current_screen, screen_dimensions):
        self.state = Human.Human((20, 20))
        self.running = True
        self.current_screen = current_screen
        self.screen_dimensions = screen_dimensions

    def draw_board(self, screen_state: tuple) -> None:
        """Draws the board's current state"""

        current_screen = pygame.display.set_mode(screen_state, pygame.RESIZABLE)
        board = self.state.board
        snakes = self.state.snake_positions
        apples = self.state.apples

        potential_width = screen_state[0] / len(board[0]) / 2
        potential_length = screen_state[1]/len(board) / 2
        block = (potential_width,'w') if potential_length >= potential_width else (potential_length,'l')

        for row in range(len(board)):
            for position in range(len(board[0])):
                if block[1] == 'w':
                    x_increment = int(.25*screen_state[0] + (block[0]) * (position))
                    y_increment = int((.25*screen_state[1] * potential_length/potential_width) + (block[0]) * (row))
                else:
                    x_increment = int((.25 * screen_state[0] * potential_width/potential_length) + (block[0] * position))
                    y_increment = int((.25 * screen_state[1]) + (block[0] * row))

                surface = pygame.display.get_surface()
                color = pygame.Color('blue') if row %2 == 0 and position % 2 == 0 or row % 2 == 1 and position % 2 == 1 else pygame.Color((173,216,230))
                snake_rectangle = pygame.Rect(x_increment, y_increment, block[0], block[0])
                pygame.draw.rect(surface, color, snake_rectangle)

        for snake in snakes:
            if block[1] == 'w':
                x_increment = int(.25 * screen_state[0] + (block[0]) * (snake[1]))
                y_increment = int((.25 * screen_state[1] * potential_length / potential_width) + (block[0]) * (snake[0]))
            else:
                x_increment = int((.25 * screen_state[0] * potential_width / potential_length) + (block[0] * snake[1]))
                y_increment = int((.25 * screen_state[1]) + (block[0] * snake[0]))

            surface = pygame.display.get_surface()
            color = pygame.Color('green')
            snake_rectangle = pygame.Rect(x_increment, y_increment, block[0], block[0])
            pygame.draw.rect(surface,color,snake_rectangle)

        for apple in apples:
            if block[1] == 'w':
                x_increment = int(.25 * screen_state[0] + (block[0]) * (apple[1]))
                y_increment = int((.25 * screen_state[1] * potential_length / potential_width) + (block[0]) * (apple[0]))
            else:
                x_increment = int((.25 * screen_state[0] * potential_width / potential_length) + (block[0] * apple[1]))
                y_increment = int((.25 * screen_state[1]) + (block[0] * apple[0]))

            surface = pygame.display.get_surface()
            color = pygame.Color('red')
            apple_rectangle = pygame.Rect(x_increment, y_increment, block[0],block[0])
            pygame.draw.rect(surface, color, apple_rectangle)


        font = pygame.font.Font('freesansbold.ttf', int(.09 * screen_state[1]))
        end_text = font.render(f'score: {self.state.length}', True, pygame.Color(255, 255, 255), pygame.Color(0, 0, 0))
        current_screen.blit(end_text, (0,0))

        button_images = pygame.image.load('Images/SnakeHumanImage.jpg')
        button_images = pygame.transform.scale(button_images, (int(screen_state[0]), int(.2*screen_state[1])))
        current_screen.blit(button_images, ((0, .8*screen_state[1])))
        return current_screen

    def set_background(self,size: tuple) -> None:
        '''Draws initial background'''
        screen = pygame.display.set_mode(size, pygame.RESIZABLE)
        screen.fill('black')


    def draw_start_text(self, size: tuple, screen: pygame.display, final_score: int = None):

        font_size = int(.1 * size[0]) if final_score is None else int(.1 * size[0] * .5)
        font = pygame.font.Font('freesansbold.ttf',font_size )
        text_string = 'Press Space To Start' if final_score is None else f'Final Score: {final_score} Press Space to Start'
        end_text = font.render(text_string, True, pygame.Color(255, 255, 255), pygame.Color(0, 0, 0))
        screen.blit(end_text, (0, size[1] / 2))


    def run(self, final_score = None) -> None:
        '''Runs program'''
        pygame.init()
        pygame.display.set_mode(self.screen_dimensions[0], pygame.RESIZABLE)

        self.set_background(self.screen_dimensions[0])

        clock = pygame.time.Clock()

        frames = 0
        exit = False
        turning = False
        ready = False
        initial_drawn = False

        while self.running:
            if not ready:
                if not initial_drawn:
                    self.set_background(self.screen_dimensions[0])
                    screen_to_edit = self.draw_board(self.screen_dimensions[0])
                    self.draw_start_text(self.screen_dimensions[0], screen_to_edit, final_score)
                    pygame.display.flip()
                    initial_drawn = True

                if frames % FRAME_RATE == 0:

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            self.current_screen[0] = 'EXIT'
                            exit = True
                            self.running = False
                        elif event.type == pygame.VIDEORESIZE:
                            self.screen_dimensions[0] = event.size
                            pygame.display.set_mode(self.screen_dimensions[0], pygame.RESIZABLE)
                            self.set_background(self.screen_dimensions[0])
                            screen_to_edit = self.draw_board(self.screen_dimensions[0])
                            self.draw_start_text(self.screen_dimensions[0], screen_to_edit, final_score)
                            pygame.display.flip()

                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE:
                                ready = True
                            elif event.key == pygame.K_0:
                                self.current_screen[0] = 'Home'
                                exit = True
                                self.running = False
                            elif event.key == pygame.K_1:
                                self.current_screen[0] = 'AI'
                                exit = True
                                self.running = False

                frames +=1
            else:
                head_direction = self.state.snake[-1][1]
                self.set_background(self.screen_dimensions[0])
                self.draw_board(self.screen_dimensions[0])
                pygame.display.flip()

                if self.state.game_over:
                    self.running = False

                clock.tick(FRAME_RATE)


                if frames % FRAME_RATE == 0:

                    key = False
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            self.current_screen[0] = 'EXIT'
                            exit = True
                            self.running = False
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_LEFT:
                                if not head_direction == 'R':
                                    if not key:
                                        key = True
                                        self.state.shift_snake_directions('L')
                                        turning = True
                            elif event.key == pygame.K_RIGHT:
                                if not head_direction == 'L':
                                    if not key:
                                        key = True
                                        self.state.shift_snake_directions('R')
                                        turning = True
                            elif event.key == pygame.K_UP:
                                if not head_direction == 'D':
                                    if not key:
                                        key = True
                                        self.state.shift_snake_directions('U')
                                        turning = True
                            elif event.key == pygame.K_DOWN:
                                if not head_direction == 'U':
                                    if not key:
                                        key = True
                                        self.state.shift_snake_directions('D')
                                        turning = True
                            elif event.key == pygame.K_0:
                                self.current_screen[0] = 'Home'
                                exit = True
                                self.running = False
                            elif event.key == pygame.K_1:
                                self.current_screen[0] = 'AI'
                                exit = True
                                self.running = False
                        elif event.type == pygame.VIDEORESIZE:
                            self.screen_dimensions[0] = event.size
                            pygame.display.set_mode(self.screen_dimensions[0], pygame.RESIZABLE)
                            self.set_background(self.screen_dimensions[0])
                            self.draw_board(self.screen_dimensions[0])
                            pygame.display.flip()

                    if not turning:
                        self.state.shift_snake_directions(head_direction)

                    self.state.shift_snake_positions()
                    self.state.check_apple_eaten()


                    turning = False

                frames += 1

        if not exit:
            score = self.state.length
            self.state.reset()
            self.running = True
            self.run(score)

        pygame.quit()

