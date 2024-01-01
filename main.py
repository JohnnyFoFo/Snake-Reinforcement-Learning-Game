from HomePage import HomePage
from HumanGame import HumanVisual
import pygame
from AIGame import AppliedModel


class Main:

    def __init__(self) -> None:
        '''Constructor for the main class, sets the screen state and the screen dimensions, while initializing pygame'''
        pygame.init()
        self.current_screen = ['Home']
        self.screen_dimensions = [(400,400)]


    def draw_screen(self) -> bool:
        '''Draws the screen based on the current screen state'''

        if self.current_screen[0] == 'Home':
            home = HomePage.HomePage(self.current_screen, self.screen_dimensions)
            home.run()
            return False
        elif self.current_screen[0] == 'Human':
            human = HumanVisual.HumanVisual(self.current_screen, self.screen_dimensions)
            human.run()
            return False
        elif self.current_screen[0] == 'AI':
            model = AppliedModel.AppliedModel(self.current_screen, self.screen_dimensions)
            model.run()
            return False
        else:
            return True


    def run(self) -> None:
        '''Runs the program'''
        pygame.display.set_mode((400,400), pygame.RESIZABLE)

        while True:
            done = self.draw_screen()
            if done:
                break


if __name__ == '__main__':
    main_object = Main()
    main_object.run()