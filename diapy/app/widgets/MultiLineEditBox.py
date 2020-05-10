import npyscreen
import curses


class MultiLineEditBox(npyscreen.MultiLineEdit):
    def __init__(self, *args, **kwargs):
        if 'height' in kwargs:
            kwargs['height'] -= 4
        if 'width' in kwargs:
            kwargs['width'] -= 4
        if 'max_width' in kwargs:
            kwargs['max_width'] -= 4
        if 'max_height' in kwargs:
            kwargs['max_height'] -= 4
        if 'rely' in kwargs:
            kwargs['rely'] += 2
        if 'relx' in kwargs:
            kwargs['relx'] += 2
        super().__init__(*args, **kwargs)

    def update(self, clear=True):
        if clear:
            self.clear()
        if self.hidden:
            self.clear()
            return False
        HEIGHT = self.height + 3
        WIDTH = self.width + 3
        RELY = self.rely - 2
        RELX = self.relx - 2
        # draw box.
        self.parent.curses_pad.hline(
            RELY, RELX, curses.ACS_HLINE, WIDTH)
        self.parent.curses_pad.hline(
            RELY + HEIGHT, RELX, curses.ACS_HLINE, WIDTH)
        self.parent.curses_pad.vline(
            RELY, RELX, curses.ACS_VLINE, HEIGHT)
        self.parent.curses_pad.vline(
            RELY, RELX+WIDTH, curses.ACS_VLINE, HEIGHT)

        # draw corners
        self.parent.curses_pad.addch(
            RELY, RELX, curses.ACS_ULCORNER, )
        self.parent.curses_pad.addch(
            RELY, RELX+WIDTH, curses.ACS_URCORNER, )
        self.parent.curses_pad.addch(
            RELY+HEIGHT, RELX, curses.ACS_LLCORNER, )
        self.parent.curses_pad.addch(
            RELY+HEIGHT, RELX+WIDTH, curses.ACS_LRCORNER, )

        # draw title
        if self.name:
            if isinstance(self.name, bytes):
                name = self.name.decode(self.encoding, 'replace')
            else:
                name = self.name
            name = self.safe_string(name)
            name = " " + name + " "
            if isinstance(name, bytes):
                name = name.decode(self.encoding, 'replace')
            name_attributes = curses.A_NORMAL
            if self.do_colors() and not self.editing:
                name_attributes = name_attributes | self.parent.theme_manager.findPair(
                    self, self.color)  # | curses.A_BOLD
            elif self.editing:
                name_attributes = name_attributes | self.parent.theme_manager.findPair(
                    self, 'HILIGHT')
            else:
                name_attributes = name_attributes  # | curses.A_BOLD

            if self.editing:
                name_attributes = name_attributes | curses.A_BOLD

            self.add_line(RELY, RELX+4, name,
                          self.make_attributes_list(name, name_attributes),
                          self.width-4)
            # end draw title
            super().update(clear=False)
