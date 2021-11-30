from PIL import Image, ImageDraw, ImageFilter
from utils import generate_num, generate_items, generate_img, convert_2_yolo
from utils import allitems
from tqdm import trange
import random
# Background size
# Item sizes
# Others... maybe need to resize in the beginning specifically...
# 1) load background
# 2) Generate Number of items
# 3) Generate list of items with Number
# 4) Place items in background with random rotate
#    Check if overlap, if so find another place and repeat X times
#    If cannot find place after X tries, dont place object
# 5) Label new image... hmmm
# 6) Covert to YOLO format
# 7) Save image

num_gen = 5

for i in trange(num_gen):
    rand_item = random.choice(allitems)
    item_list = generate_items(generate_num(lower=1, upper=8))
    img, item_info = generate_img([rand_item] + item_list)

    label_file = open(f"generated_labels/{i:03d}.txt","w")
    
    for item_class, x, y, bx, by in item_info:
        if item_class != 'others':
            bb = (x,y,bx,by)
            # print(item_class, bb)
            # print(' '.join(str(x) for x in convert_2_yolo(item_class, bb)))
            label_file.write(' '.join(str(x) for x in convert_2_yolo(item_class, bb)) + '\n')
    
    label_file.close()

    img.save(f'generated_imgs/{i:03d}.png', format="png")