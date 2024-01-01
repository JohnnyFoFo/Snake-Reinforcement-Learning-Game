import pygame


FRAME_RATE = 1



class HomePage:

    def __init__(self, screen_state: list[str], current_screen_dimensions: tuple) -> None:
        '''Constructor for the home page object which stores the screen,screen_dimensions, and if the program is still running'''
        pygame.init()
        self.current_screen_dimensions = current_screen_dimensions
        self.screen = screen_state
        self.running = True

    def draw_screen(self, screen_dimensions: tuple) -> None:
        'Draws the home screen image I made as a google drawing'

        current_screen = pygame.display.set_mode(screen_dimensions, pygame.RESIZABLE)

        main_image = pygame.image.load('Images/HomeImage.jpg')
        main_image = pygame.transform.scale(main_image,(int(screen_dimensions[0]),int(screen_dimensions[1])))
        current_screen.blit(main_image,((0,0)))


    def run(self) -> None:
        '''Runs program'''

        pygame.display.set_mode(self.current_screen_dimensions[0], pygame.RESIZABLE)
        clock = pygame.time.Clock()

        frames = 0

        self.draw_screen(self.current_screen_dimensions[0])
        pygame.display.flip()

        while self.running:



            clock.tick(FRAME_RATE)

            if frames % FRAME_RATE == 0:

                key = False
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.screen[0] = 'EXIT'
                        self.running = False
                        pygame.quit()
                        break
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_0:
                            self.screen[0] = 'AI'
                            self.running = False
                        elif event.key == pygame.K_1:
                            self.screen[0] = 'Human'
                            self.running = False

                    elif event.type == pygame.VIDEORESIZE:
                        pygame.display.set_mode(event.size, pygame.RESIZABLE)
                        self.current_screen_dimensions[0] = event.size
                        self.draw_screen(self.current_screen_dimensions[0])
                        pygame.display.flip()


            frames += 1





