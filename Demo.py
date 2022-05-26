from Ascii import *

x = 10
y = 10

p1 = Vec2(10, 20)
p2 = Vec2(20, 10)
p3 = Vec2(10, 10)

model_data = '''############  ###
#               #
#               #
#____           #
#    a          #
#################'''

model = Model(model_data)

def loop():
    # Drawing stuff
    screen_buffer_array = init_screen_buffer()
    screen_buffer_array = draw_rect_on_top(Vec2(x, y), 1, 1, screen_buffer_array, '☻')
    screen_buffer_array = draw_line_on_top(Vec2(20, 20), Vec2(x, y), screen_buffer_array, '●')
    #screen_buffer_array = draw_circle_on_top(Vec2(10 + x, 10 + y), 50, 50, screen_buffer_array)
    #screen_buffer_array = draw_triangle_on_top(Vec2(0 + x, 10 + y), Vec2(10 + x, 0 + y), Vec2(0 + x, 0 + y), screen_buffer_array, '@')
    #screen_buffer_array = draw_line_on_top(Vec2(floor(window_w / 2), floor(window_h / 2)), Vec2(floor(mouseX / window_w), floor(mouseY / window_h)), screen_buffer_array, 'e')
    
    
    # Not working yet...
    # p1 = math_rotation_point(p1, 0.1)
    # p2 = math_rotation_point(p2, 0.1)
    # p3 = math_rotation_point(p3, 0.1)
    # p1 = p1.add(Vec2(x, y))
    # p2 = p2.add(Vec2(x, y))
    # p2 = p2.add(Vec2(x, y))
    # screen_buffer_array = draw_triangle_on_top(p1, p2, p3, screen_buffer_array, '@')
    screen_buffer_array = draw_model_no_whitespace(Vec2(30, 10), model, screen_buffer_array)
    screen_buffer_array = draw_box_on_top(Vec2(10, 10), Vec2(20, 10), Vec2(20, 20), Vec2(10, 20), screen_buffer_array)
    screen_buffer_array = draw_screen_borders_on_top(screen_buffer_array, '▧')
    screen_buffer = draw(screen_buffer_array)
    
    return screen_buffer


def input():
    global x, y
    
    # Player Input
    if is_pressed('up'):
        y -= 1
    if is_pressed('down'):
        y += 1
    if is_pressed('left'):
        x -= 1
    if is_pressed('right'):
        x += 1

init(100, 50, ' ', .01)
init_functions(loop, input)
run()