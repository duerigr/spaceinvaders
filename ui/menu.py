import pygameMenu
from ui.config import Config


class Menu(pygameMenu.Menu):

    def __init__(self, surface, handle_start, handle_continue):
        pygameMenu.Menu.__init__(self,
                                 surface=surface,
                                 window_width=Config.DISPLAY_WIDTH,
                                 window_height=Config.DISPLAY_HEIGHT,
                                 font=Config.FONT,
                                 font_size=Config.FONT_SIZE,
                                 bgfun=self.__menubackground,
                                 fps=60,
                                 menu_alpha=60,
                                 title=Config.MAIN_MENU_TITLE)
        self.add_option("start", handle_start)
        self.add_option("continue", handle_continue)
        self.add_option("quit", pygameMenu.events.EXIT)

    def __menubackground(self):
        pass
