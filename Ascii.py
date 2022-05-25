from numba import njit
from numba.typed import List
from keyboard import is_pressed
from time import sleep
from os import system
from sys import stdout

run_AsciiLib = True
window_initialized = False
window_w = 0
window_h = 0
window_border_char = ''
window_name = ''
fps = 0


# Init window
def init(width, height, border_char, frame_rate, name='Default'):
    global window_w, window_h, window_border_char, window_name, window_initialized, fps

    window_w = width
    window_h = height
    window_border_char = border_char
    window_name = name
    fps = frame_rate
    window_initialized = True

    print(f"Successfully initialized the Window: '{window_name}'")


# Init screen_buffer_array
def init_screen_buffer():
    array = List()

    for y in range(window_h):
        for x in range(window_w):
            array.append(window_border_char)

    return array


@njit
def draw_rect_on_top(x, y, w, h, array, char='#'):
    for i in range(h):
        for j in range(w):
            idx = (x + j) + ((y + i) * window_w)
            if idx < len(array) and idx > -1 and x + j < window_w and x + j > -1:
                array[idx] = char

    return array


@njit
def draw_line_on_top(x1, y1, x2, y2, array, char='#'):
    return array


@njit
def create_screen_buffer(array):
    buffer = ''
    idx = 0

    for idx in range(len(array)):
        if (idx % window_w) == 0 and idx > 0:
            buffer += '\n'
        buffer += array[idx] + ' '

    return buffer


def draw(array):
    if not window_initialized:
        raise ValueError(
            "The window first has to be initialized before you can invoke the draw function!")

    # Create the screen buffer
    screen_buffer = create_screen_buffer(array)
    return screen_buffer


def check_input():
    global run_AsciiLib
    if is_pressed('esc'):
        print("Shutting down AsciiLib.py")
        run_AsciiLib = False

###########################################################################################################################################################################


init(25, 25, '.', .1, 'Test Window')
screen_buffer_array = init_screen_buffer()
system('CLS')


def one_time():
    # Drawing stuff
    screen_buffer_array = init_screen_buffer()
    screen_buffer_array = draw_rect_on_top(10, 10, 5, 5, screen_buffer_array)
    screen_buffer_array = draw_line_on_top(20, 20, 30, 30, screen_buffer_array)
    screen_buffer = draw(screen_buffer_array)

    system('CLS')
    print(screen_buffer)
    exit(0)

x = -20
y = -20
while run_AsciiLib:
    # Drawing stuff
    screen_buffer_array = init_screen_buffer()
    screen_buffer_array = draw_rect_on_top(x, y, 15, 5, screen_buffer_array)
    screen_buffer_array = draw_rect_on_top(-x, -y, 5, 5, screen_buffer_array, '@')
    screen_buffer_array = draw_line_on_top(20, 20, 30, 30, screen_buffer_array, '@')
    screen_buffer = draw(screen_buffer_array)

    system('CLS')
    print(screen_buffer)

    x += 1
    y += 1

    # Other stuff
    sleep(fps)
    check_input()

system('CLS')
print("Thanks for using AsciiLib :)")
