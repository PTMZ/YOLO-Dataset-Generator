import os
import random
from PIL import Image, ImageDraw, ImageFilter

allitems = ['apples', 'bananas', 'oranges']

label_to_int = {name:i for i,name in enumerate(allitems)}

background_dim = (480, 640)

num_dict = {}
for x in allitems:
    num_dict[x] = len(os.listdir(f'object_classes/{x}'))

num_dict['others'] = len(os.listdir(f'object_classes/others'))

def generate_num(lower=1, upper=10):
    return random.randint(lower, upper)

def generate_items(num_items):
    noise_weight = 2
    ans = []
    for i in range(num_items):
        ans.append(random.choice(allitems + ['others'] * noise_weight))
    return ans

def generate_img(item_list):
    bg = Image.open('object_classes/background/white.png').convert("RGBA")
    num_tries = 10
    margin = 20
    existing_items = []
    output = []
    zoom_factor = random.random() * 0.7 + 0.8 # range from 0.8 to 1.5
    for item_class in item_list:
        item_zoom = random.random() * 0.2 + 0.9 # range from 0.85 to 1.15
        item_img = Image.open(f'object_classes/{item_class}/{random.randint(1, num_dict[item_class])}.png').convert("RGBA")
        item_img = item_img.resize((int(item_img.size[0]*zoom_factor*item_zoom), int(item_img.size[1]*zoom_factor*item_zoom)))
        item_img = item_img.rotate(random.randint(0, 360), expand=True)
        item_w, item_h = item_img.size
        for i in range(num_tries):
            
            x = random.randint(0, background_dim[1]-item_w)
            y = random.randint(0, background_dim[0]-item_h)
            botRight_x = x + item_w
            botRight_y = y + item_h
            cur_tuple = (x, y, botRight_x, botRight_y)
            if not check_collision(existing_items, cur_tuple):
                existing_items.append(cur_tuple)
                output.append((item_class, x, y, botRight_x, botRight_y))
                bg.paste(item_img, (x, y), item_img)
                break
    
    return bg, output


def check_collision(existing_items, cur_item):
    for x in existing_items:
        xA = max(x[0], cur_item[0])
        yA = max(x[1], cur_item[1])
        xB = min(x[2], cur_item[2])
        yB = min(x[3], cur_item[3])
        # compute the area of intersection rectangle
        interArea = max(0, xB - xA + 1) * max(0, yB - yA + 1)

        if interArea > 0:
            return True
    return False



def convert_2_yolo(class_label, coords):
    # Put x,y in Center
    # Normalise numbers with image dim
    # Return class x y width height
    label = label_to_int[class_label]
    img_w, img_h = 640, 480
    x,y,bx,by = coords
    w,h = bx-x, by-y
    x += int(w/2)
    y += int(h/2)

    x /= img_w
    y /= img_h
    w /= img_w
    h /= img_h
    return (label, x, y, w, h)


