from math import cos, floor, sin, pi, sqrt
from numba import njit, int32, types
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
window_default_char = ''
window_name = ''
window_manual_update = False
window_invoke_manual_update = False
mouseX = 0
mouseY = 0
fps = 0

loop_func = None
input_func = None


ascii_special_chars = "๑•ิ.•ั๑ ๑๑ ♬✿.｡.:* ★ ☆ εїз℡❣·۰•●○●ōゃ ♥ ♡๑ﺴ ☜ ☞ ☎ ☏♡ ⊙◎ ☺ ☻✖╄ஐﻬ ► ◄ ▧ ▨ ♨ ◐ ◑ ↔ ↕ ▪ ▫ ☼ ♦ ▀ ▄ █▌ ▐░ ▒ ▬♦ ◊ ◦ ☼ ♠♣ ▣ ▤ ▥ ▦ ▩ ◘ ◙ ◈ ♫ ♬ ♪ ♩ ♭ ♪ の ☆"


# Init window
def init(width, height, default_char, frame_rate, manual_update=False, name='Default'):
    global window_w, window_h, window_default_char, window_name, window_initialized, window_manual_update, fps

    window_w = width
    window_h = height
    window_default_char = default_char
    window_name = name
    window_manual_update = manual_update
    fps = frame_rate
    window_initialized = True

    print(f"Successfully initialized the Window: '{window_name}'")
    sleep(3)


def init_functions(loop, input):
    global loop_func, input_func
    loop_func = loop
    input_func = input
    

# Init "screen_buffer_array"
def init_screen_buffer():
    array = List()

    for y in range(window_h):
        for x in range(window_w):
            array.append(window_default_char)

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


@njit
def draw_screen_borders_on_top(array, char='X'):
    array = draw_line_on_top(Vec2(0, 0),            Vec2(window_w, 0),            array, char)
    array = draw_line_on_top(Vec2(0, 0),            Vec2(0, window_h - 1),        array, char)
    array = draw_line_on_top(Vec2(window_w - 1, 0), Vec2(window_w, window_h - 1), array, char)
    array = draw_line_on_top(Vec2(0, window_h - 1), Vec2(window_w, window_h - 1), array, char)
    return array


@njit
def draw_box_on_top(vec1, vec2, vec3, vec4, array, char='#'):
    array = draw_line_on_top(vec1, vec2, array, char)
    array = draw_line_on_top(vec2, vec3, array, char)
    array = draw_line_on_top(vec3, vec4, array, char)
    array = draw_line_on_top(vec4, vec1, array, char)
    return array


@njit
def draw_model_whitespace(vec, model, array):
    x = vec.x
    y = vec.y
    
    for i in range(model.h):
        for j in range(model.w):
            idx = (x + j) + ((y + i) * window_w)
            if idx < len(array) and idx > -1 and x + j < window_w and x + j > -1:
                array[idx] = model.data[j + i * model.w]

    return array

@njit
def draw_model_no_whitespace(vec, model, array):
    x = vec.x
    y = vec.y
    
    for i in range(model.h):
        for j in range(model.w):
            idx = (x + j) + ((y + i) * window_w)
            char = model.data[j + i * model.w]
            if not char == ' ':
                if idx < len(array) and idx > -1 and x + j < window_w and x + j > -1:
                    array[idx] = char

    return array


@njit
def draw_text_on_top(vec, text, array):
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
    global run_AsciiLib, window_invoke_manual_update
    if is_pressed('esc'):
        print("Shutting down AsciiLib.py")
        run_AsciiLib = False
    if is_pressed('+'):
        window_invoke_manual_update = True

    if input_func:
        input_func()
        

###########################################################################################################################################################################


_Vec2 = [ ('x', int32), ('y', int32) ]
@jitclass(_Vec2)
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


_Model = [ ('w', int32), ('h', int32), ('data', types.string) ]
@jitclass(_Model)
class Model:
    def __init__(self, data):
        array = data.split('\n')
        self.w = len(array[0])
        self.h = len(array)
        
        final_data = ''
        for i in range(len(array)):
            final_data += array[i]
        
        self.data = final_data


###########################################################################################################################################################################


def math_gen_transformation_matrix():
    pass

def math_rotation_point(vec, r):
    x0 = vec.x
    y0 = vec.y
    
    x1 = x0 * cos(r) + y0 * -sin(r)
    y1 = x0 * sin(r) + y0 *  cos(r)
    return Vec2(x1, y1)
    

###########################################################################################################################################################################


def run():
    global screen_buffer_array, mouseX, mouseY
    screen_buffer_array = init_screen_buffer()
    system('CLS')
    
    # The main loop
    while run_AsciiLib:
        if window_manual_update:
            check_input()
            sleep(.1)

            if window_invoke_manual_update:
                window_invoke_manual_update = False
            else:
                continue

        if loop_func:
            screen_buffer = loop_func()

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
