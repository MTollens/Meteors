light_grey = (200, 200, 200)
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
dark_red= (200, 0, 0)
green = (0, 255, 0)
dark_green = (0, 200, 0)
blue = (0, 0, 255)
item_yellow = (236, 255, 145)
brown = (119, 77, 0)
light_brown = (173, 112, 0)
grey = (96, 96, 96)
light_blue = (173, 216, 230)
pink = (255, 100, 100)
orange = (234, 118, 0)
purple = (90, 7, 120)

all_colors = [purple, orange, pink, light_blue, grey, light_brown, brown, item_yellow, blue, dark_green, green, dark_red, red, white, black, light_grey]

def add(color1, color2):
    return (color1[0] + color2[0], color1[1] + color2[1], color1[2] + color2[2])

def divide(color, value):
    return(color[0]/value, color[1]/ value, color[2]/value)

def muted(color, amount=None):
    if not amount:
        amount = .75
    result = [0, 0, 0]
    result[0] = round(amount * color[0])
    result[1] = round(amount * color[1])
    result[2] = round(amount * color[2])
    return result

meteor = [brown, grey, light_brown, light_brown]

stars = [light_grey, muted(item_yellow), white, grey, light_blue, white, white]

def tohex(list_obj):
    string = ""
    for x in range(0,2):
        string = string + (str(hex(list_obj[x])))
    return string

def average(fill, val):
    return divide(fill, val)

def remove_alpha(alpha_color):
    return (alpha_color[0], alpha_color[1], alpha_color[2])

def add_alpha(color, alpha):
    al = list(color)
    al.append(alpha)
    return tuple(al)
