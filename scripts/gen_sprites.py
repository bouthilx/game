# sprite_strip.py
# Generates a 128x32 PNG with 4x 32x32 idle sprites (DOWN, UP, LEFT, RIGHT).
# Requires: pip install pillow

from PIL import Image, ImageDraw

W, H = 128, 32
TILE = 32

# Palette
OUT   = (43, 35, 27, 255)   # dark outline
HAIR  = (241, 211, 106, 255)
HAIR2 = (212, 176, 82, 255)
SKIN  = (243, 215, 178, 255)
TUNI  = (46, 120, 178, 255)
TUNI2 = (33, 86, 127, 255)
BELT  = (109, 69, 35, 255)
BUCK  = (214, 172, 72, 255)
BOOT  = (90, 58, 30, 255)

def fill_rect(img, x, y, w, h, c):
    for yy in range(y, y+h):
        for xx in range(x, x+w):
            if 0 <= xx < img.width and 0 <= yy < img.height:
                img.putpixel((xx, yy), c)

def stroke_rect(img, x, y, w, h, c=OUT):
    # 1px outline
    for xx in range(x, x+w):
        if 0 <= xx < img.width:
            if 0 <= y < img.height: img.putpixel((xx, y), c)
            if 0 <= y+h-1 < img.height: img.putpixel((xx, y+h-1), c)
    for yy in range(y, y+h):
        if 0 <= yy < img.height:
            if 0 <= x < img.width: img.putpixel((x, yy), c)
            if 0 <= x+w-1 < img.width: img.putpixel((x+w-1, yy), c)

def dot(img, x, y, c=OUT):
    if 0 <= x < img.width and 0 <= y < img.height:
        img.putpixel((x, y), c)

def draw_front(img, ox):
    # Hair
    fill_rect(img, ox+10, 4, 12, 6, HAIR)
    fill_rect(img, ox+10, 9, 12, 2, HAIR2)  # shadow fringe
    stroke_rect(img, ox+9, 3, 14, 8)
    # Face
    fill_rect(img, ox+11, 10, 10, 6, SKIN)
    stroke_rect(img, ox+11, 10, 10, 6, OUT)
    # Eyes
    dot(img, ox+14, 12); dot(img, ox+18, 12)
    # Tunic
    fill_rect(img, ox+9, 17, 14, 8, TUNI)
    fill_rect(img, ox+9, 21, 14, 4, TUNI2)  # lower shadow
    stroke_rect(img, ox+9, 17, 14, 8)
    # Belt
    fill_rect(img, ox+9, 21, 14, 2, BELT)
    stroke_rect(img, ox+9, 21, 14, 2)
    fill_rect(img, ox+15, 21, 2, 2, BUCK)
    # Arms (sides)
    fill_rect(img, ox+7, 18, 2, 5, TUNI2); stroke_rect(img, ox+7, 18, 2, 5)
    fill_rect(img, ox+23, 18, 2, 5, TUNI2); stroke_rect(img, ox+23, 18, 2, 5)
    # Legs/boots
    fill_rect(img, ox+12, 25, 3, 3, BOOT); stroke_rect(img, ox+12, 25, 3, 3)
    fill_rect(img, ox+17, 25, 3, 3, BOOT); stroke_rect(img, ox+17, 25, 3, 3)

def draw_back(img, ox):
    # Back hair (larger)
    fill_rect(img, ox+9, 4, 14, 7, HAIR)
    fill_rect(img, ox+9, 10, 14, 2, HAIR2)
    stroke_rect(img, ox+8, 3, 16, 9)
    # Tunic back
    fill_rect(img, ox+9, 17, 14, 8, TUNI)
    fill_rect(img, ox+9, 21, 14, 4, TUNI2)
    stroke_rect(img, ox+9, 17, 14, 8)
    # Belt
    fill_rect(img, ox+9, 21, 14, 2, BELT)
    stroke_rect(img, ox+9, 21, 14, 2)
    # Arms (sides)
    fill_rect(img, ox+7, 18, 2, 5, TUNI2); stroke_rect(img, ox+7, 18, 2, 5)
    fill_rect(img, ox+23, 18, 2, 5, TUNI2); stroke_rect(img, ox+23, 18, 2, 5)
    # Boots
    fill_rect(img, ox+12, 25, 3, 3, BOOT); stroke_rect(img, ox+12, 25, 3, 3)
    fill_rect(img, ox+17, 25, 3, 3, BOOT); stroke_rect(img, ox+17, 25, 3, 3)

def draw_left(img, ox):
    # Hair/profile
    fill_rect(img, ox+9, 5, 11, 6, HAIR)
    fill_rect(img, ox+9, 10, 11, 2, HAIR2)
    stroke_rect(img, ox+8, 4, 13, 8)
    # Face (front edge)
    fill_rect(img, ox+9, 11, 5, 5, SKIN)
    stroke_rect(img, ox+9, 11, 5, 5)
    dot(img, ox+11, 13)  # eye
    # Tunic side
    fill_rect(img, ox+11, 17, 10, 8, TUNI)
    fill_rect(img, ox+11, 21, 10, 4, TUNI2)
    stroke_rect(img, ox+11, 17, 10, 8)
    # Belt
    fill_rect(img, ox+11, 21, 10, 2, BELT)
    stroke_rect(img, ox+11, 21, 10, 2)
    # Arms/hand
    fill_rect(img, ox+10, 18, 2, 5, TUNI2); stroke_rect(img, ox+10, 18, 2, 5)
    # Boots
    fill_rect(img, ox+14, 25, 3, 3, BOOT); stroke_rect(img, ox+14, 25, 3, 3)
    fill_rect(img, ox+18, 25, 3, 3, BOOT); stroke_rect(img, ox+18, 25, 3, 3)

def draw_right(img, ox):
    # Mirror of left
    fill_rect(img, ox+12, 5, 11, 6, HAIR)
    fill_rect(img, ox+12, 10, 11, 2, HAIR2)
    stroke_rect(img, ox+11, 4, 13, 8)
    fill_rect(img, ox+18, 11, 5, 5, SKIN)
    stroke_rect(img, ox+18, 11, 5, 5)
    dot(img, ox+21, 13)
    fill_rect(img, ox+11, 17, 10, 8, TUNI)
    fill_rect(img, ox+11, 21, 10, 4, TUNI2)
    stroke_rect(img, ox+11, 17, 10, 8)
    fill_rect(img, ox+11, 21, 10, 2, BELT)
    stroke_rect(img, ox+11, 21, 10, 2)
    fill_rect(img, ox+21, 18, 2, 5, TUNI2); stroke_rect(img, ox+21, 18, 2, 5)
    fill_rect(img, ox+14, 25, 3, 3, BOOT); stroke_rect(img, ox+14, 25, 3, 3)
    fill_rect(img, ox+18, 25, 3, 3, BOOT); stroke_rect(img, ox+18, 25, 3, 3)

def main():
    img = Image.new("RGBA", (W, H), (0,0,0,0))
    draw_front(img, 0)        # Frame 1: DOWN
    draw_back(img, TILE)      # Frame 2: UP
    draw_left(img, TILE*2)    # Frame 3: LEFT
    draw_right(img, TILE*3)   # Frame 4: RIGHT
    img.save("sprite_strip.png")

if __name__ == "__main__":
    main()

