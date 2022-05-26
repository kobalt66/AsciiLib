from math import cos, floor, sin, pi, sqrt
from numba import njit, int32
from numba.experimental import jitclass
from numba.typed import List
from keyboard import is_pressed
from time import sleep
from os import system
import pyautogui

run_AsciiLib = True
window_initialized = False
window_w = 0
window_h = 0
window_border_char = ''
window_name = ''
window_manual_update = False
window_invoke_manual_update = False
mouseX = 0
mouseY = 0
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
    sleep(3)


# Init "screen_buffer_array"
def init_screen_buffer():
    array = List()

    for y in range(window_h):
        for x in range(window_w):
            array.append(window_border_char)

    return array

###########################################################################################################################################################################

@njit
def draw_rect_on_top(vec, w, h, array, char='#'):
    x = vec.x
    y = vec.y
    
    for i in range(h):
        for j in range(w):
            idx = (x + j) + ((y + i) * window_w)
            if idx < len(array) and idx > -1 and x + j < window_w and x + j > -1:
                array[idx] = char

    return array


@njit
def draw_line_on_top(vec1, vec2, array, char='#'):
    x1 = vec1.x
    y1 = vec1.y
    x2 = vec2.x
    y2 = vec2.y
    
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


def draw_circle_on_top(vec, r, steps, array, char='#'):
    angle = pi * 2 / steps

    x = vec.x
    y = vec.y

    prevX = x
    prevY = y - r
    for i in range(steps + 1):
        I = 1 if i < 1 else I
        newX = x + floor(r * sin(angle * i))
        newY = y + floor(-r * cos(angle * i))

        array = draw_line_on_top(Vec2(prevX, prevY), Vec2(newX, newY), array, char)

        prevX = newX
        prevY = newY

    return array

@njit
def draw_triangle_on_top(vec1, vec2, vec3, array, char='#'):
    array = draw_line_on_top(vec1, vec2, array, char)
    array = draw_line_on_top(vec2, vec3, array, char)
    array = draw_line_on_top(vec3, vec1, array, char)
    
    return array


###########################################################################################################################################################################

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

spec = [ ('x', int32), ('y', int32) ]
@jitclass(spec)
class Vec2:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        
    def add(self, vec2):
        newVec = self
        newVec.x += vec2.x
        newVec.y += vec2.y
        return newVec
        
    def sub(self, vec2):
        newVec = self
        newVec.x -= vec2.x
        newVec.y -= vec2.y
        return newVec
    
    def mul(self, vec2):
        return self.x * vec2.x + self.y * vec2.y
    
    def mul(self, n):
        newVec = self
        newVec.x *= n
        newVec.y *= n
        return newVec
    
    def div(self, n):
        newVec = self
        newVec.x /= n
        newVec.y /= n
        return newVec
    
    def mag(self):
        return sqrt(pow(self.x, 2) + pow(self.y, 2))
    
    def norm(self):
        newVec = self
        newVec.x /= self.mag()
        newVec.y /= self.mag()
        return newVec


def math_gen_transformation_matrix():
    pass

def math_rotation_point(x0, y0, r):
    x1 = x0 * cos(r) + y0 * -sin(r)
    y1 = x0 * sin(r) + y0 *  cos(r)
    return Vec2(x1, y1)
    

###########################################################################################################################################################################

init(100, 50, ' ', .01)
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
    #screen_buffer_array = draw_rect_on_top(x, y, 2, 2, screen_buffer_array, '@')
    #screen_buffer_array = draw_line_on_top(20, 20, x, y, screen_buffer_array, 'x')
    screen_buffer_array = draw_circle_on_top(Vec2(10 + x, 10 + y), 50, 50, screen_buffer_array)
    #screen_buffer_array = draw_triangle_on_top(Vec2(0 + x, 10 + y), Vec2(10 + x, 0 + y), Vec2(0 + x, 0 + y), screen_buffer_array, '@')
    #screen_buffer_array = draw_line_on_top(Vec2(floor(window_w / 2), floor(window_h / 2)), Vec2(floor(mouseX / window_w), floor(mouseY / window_h)), screen_buffer_array, 'e')
    screen_buffer_array = draw_line_on_top(Vec2(0, 0),            Vec2(window_w, 0), screen_buffer_array, 'X')
    screen_buffer_array = draw_line_on_top(Vec2(0, 0),            Vec2(0, window_h - 1), screen_buffer_array, 'X')
    screen_buffer_array = draw_line_on_top(Vec2(window_w - 1, 0), Vec2(window_w, window_h - 1), screen_buffer_array, 'X')
    screen_buffer_array = draw_line_on_top(Vec2(0, window_h - 1), Vec2(window_w, window_h - 1), screen_buffer_array, 'X')
    screen_buffer = draw(screen_buffer_array)

    system('CLS')
    print(screen_buffer)

    # Other stuff
    mouseX = pyautogui.position().x
    mouseY = pyautogui.position().y
    
    if not window_manual_update:
        sleep(fps)
        check_input()

system('CLS')
print("Thanks for using AsciiLib :)")
