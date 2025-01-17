import curses

stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
curses.curs_set(0)
stdscr.keypad(True)
curses.start_color()

curses.init_color(1, 1000, 1000, 0)
curses.init_pair(1, 1, curses.COLOR_BLACK)

stdscr.addstr(0, 0, "Hello, World!", curses.color_pair(1))
stdscr.refresh()

stdscr.getch()

curses.init_color(1, 0, 1000, 0)
curses.init_pair(1, 1, curses.COLOR_BLACK)

stdscr.addstr(0, 0, "Hello, World!", curses.color_pair(1))
stdscr.refresh()
stdscr.getch()

curses.endwin()