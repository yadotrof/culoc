import curses
import os
from curses import panel

from .analyze import count_lines, get_dir_data


class GUI:
    def __init__(self, stdscreen):
        self.window = stdscreen
        curses.curs_set(0)

        self.panel = panel.new_panel(self.window)
        self.panel.hide()
        panel.update_panels()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_RED)

        self.position = 0

        self.current_folder = "."
        self.data = count_lines()
        self.items = get_dir_data(self.data, self.current_folder)

        self.display()

    def navigate(self, n):
        self.position += n
        if self.position < 0:
            self.position = 0
        elif self.position >= len(self.items):
            self.position = len(self.items) - 1

    def display(self):
        self.panel.top()
        self.panel.show()
        self.window.clear()

        while True:
            self.window.refresh()
            curses.doupdate()
            height, width = self.window.getmaxyx()
            title = f"-- {os.path.abspath(self.current_folder)} -- culoc v0.1 --"
            self.window.addstr(
                0, 0, ("{:" + str(width) + "}").format(title), curses.color_pair(2)
            )
            for index, item in enumerate(self.items):
                if index == self.position:
                    mode = curses.A_REVERSE
                else:
                    mode = curses.A_NORMAL
                min_index = 0
                if self.position >= height - 3:
                    min_index = self.position - height + 4
                if index >= min_index and index - min_index < height - 2:
                    file_name = item[0][len(self.current_folder) :]
                    if not os.path.isdir(item[0]):
                        file_name = file_name[1:]
                    progress = "#" * round(
                        item[1] * 10 / self.data[self.current_folder]
                    )
                    self.window.addstr(
                        index - min_index + 1,
                        0,
                        f"{item[1]:10} [{progress:10}] {file_name:30} ",
                        mode,
                    )
                    self.window.clrtobot()

            self.window.addstr(
                height - 1,
                1,
                f"Press (q) to exit, use arrows to navigate",
                curses.color_pair(1),
            )
            key = self.window.getch()
            if key in [curses.KEY_ENTER, ord("\n"), curses.KEY_RIGHT]:
                file_name = self.items[self.position][0]
                if os.path.isdir(file_name):
                    self.current_folder += file_name[len(self.current_folder) :]
                    self.items = get_dir_data(self.data, self.current_folder)
                    self.position = 0
                else:
                    curses.beep()

            if key == curses.KEY_LEFT:
                i = self.current_folder.rfind("/")
                if i == -1:
                    curses.beep()
                else:
                    self.current_folder = self.current_folder[:i]
                    self.items = get_dir_data(self.data, self.current_folder)

            elif key == curses.KEY_UP:
                self.navigate(-1)

            elif key == curses.KEY_DOWN:
                self.navigate(1)

            elif key == ord("q"):
                break

        self.window.clear()
        self.panel.hide()
        panel.update_panels()
        curses.doupdate()


curses.wrapper(GUI)


#  TODO features:
# 1) skip empty lines
# 2) select formats / save formats on scan
# 3) recursion
# 4) hidden files
# 5) sort
# 6) use stack to save position
