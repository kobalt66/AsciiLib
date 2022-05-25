from math import floor
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
window_manual_update = False
window_invoke_manual_update = False
fps = 0


# Init window
def init(width, height, border_char, frame_rate, manual_update=False, name='Default'):
    global window_w, window_h, window_border_char, window_name, window_initialized, window_manual_update, fps

    window_w = width
    window_h = height
    window_border_char = border_char
    window_name = name
    window_manual_update = manual_update
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
    dx = x2 - x1
    dy = y2 - y1
    
    steps = 0
    if abs(dx) > abs(dy):
        steps = abs(dx)
    else:
        steps = abs(dy)
    
    if steps == 0:
        xinc = 0
        yinc = 0
    else:
        xinc = dx / steps
        yinc = dy / steps
    
    
    for i in range(steps):
        x = floor(x1 + xinc * i) 
        y = floor(y1 + yinc * i)
        
        idx = x + y * window_w
        if idx < len(array) and idx > -1 and x < window_w and x > -1:
            array[idx] = char
    
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
    global run_AsciiLib, window_invoke_manual_update, y, x
    if is_pressed('esc'):
        print("Shutting down AsciiLib.py")
        run_AsciiLib = False
    if is_pressed('+'):
        window_invoke_manual_update = True
    
    # Player Input
    if is_pressed('up'):
        y -= 1
    if is_pressed('down'):
        y += 1
    if is_pressed('left'):
        x -= 1
    if is_pressed('right'):
        x += 1

###########################################################################################################################################################################


init(50, 25, ' ', .01)
screen_buffer_array = init_screen_buffer()
system('CLS')

x = 10
y = 10
while run_AsciiLib:
    if window_manual_update:
        check_input()
        sleep(.1)
        
        if window_invoke_manual_update:
            window_invoke_manual_update = False
        else:
            continue
    
    # Drawing stuff
    screen_buffer_array = init_screen_buffer()
    screen_buffer_array = draw_rect_on_top(x, y, 2, 2, screen_buffer_array, '@')
    screen_buffer_array = draw_line_on_top(20, 20, x, y, screen_buffer_array, 'x')
    screen_buffer_array = draw_line_on_top(0, 0, window_w, 0, screen_buffer_array, 'X')
    screen_buffer_array = draw_line_on_top(0, 0, 0, window_h - 1, screen_buffer_array, 'X')
    screen_buffer_array = draw_line_on_top(window_w - 1, 0, window_w, window_h - 1, screen_buffer_array, 'X')
    screen_buffer_array = draw_line_on_top(0, window_h - 1, window_w, window_h - 1, screen_buffer_array, 'X')
    screen_buffer = draw(screen_buffer_array)

    system('CLS')
    print(screen_buffer)

    # Other stuff
    if not window_manual_update:
        sleep(fps)
        check_input()

system('CLS')
print("Thanks for using AsciiLib :)")
