#!/usr/bin/env python3
"""
Generate chest sprites for the game.
Creates closed, open, and opening animation states.
Based on goblin sprite generation pattern.
"""

from PIL import Image
import os
import json
from pathlib import Path

# Sprite dimensions
SPRITE_SIZE = 32
TILE = 32

# Chest color palette
OUT   = (43, 35, 27, 255)       # dark outline
WOOD  = (139, 101, 61, 255)     # Main wood color
WOOD2 = (101, 73, 44, 255)      # Dark wood shadow
METAL = (120, 120, 120, 255)    # Metal bands/hinges
METAL2= (80, 80, 80, 255)       # Darker metal
LOCK  = (180, 160, 40, 255)     # Golden lock
LOCK2 = (140, 120, 30, 255)     # Darker gold
INNER = (20, 15, 10, 255)       # Dark interior
TRANS = (0, 0, 0, 0)            # transparent

def fill_rect(img, x, y, w, h, c):
    for yy in range(int(y), int(y+h)):
        for xx in range(int(x), int(x+w)):
            if 0 <= xx < img.width and 0 <= yy < img.height:
                img.putpixel((xx, yy), c)

def stroke_rect(img, x, y, w, h, c=OUT):
    for xx in range(int(x), int(x+w)):
        if 0 <= xx < img.width:
            if 0 <= y < img.height: img.putpixel((xx, int(y)), c)
            if 0 <= y+h-1 < img.height: img.putpixel((xx, int(y+h-1)), c)
    for yy in range(int(y), int(y+h)):
        if 0 <= yy < img.height:
            if 0 <= x < img.width: img.putpixel((int(x), yy), c)
            if 0 <= x+w-1 < img.width: img.putpixel((int(x+w-1), yy), c)

def dot(img, x, y, c=OUT):
    if 0 <= x < img.width and 0 <= y < img.height:
        img.putpixel((int(x), int(y)), c)

# === CHEST DRAWING FUNCTIONS ===

def draw_chest_closed(img, ox, oy):
    """Draw closed chest"""
    # Main chest body
    chest_x = ox + 6
    chest_y = oy + 12
    chest_w = 20
    chest_h = 16
    
    # Bottom part (base)
    fill_rect(img, chest_x, chest_y + 8, chest_w, 8, WOOD)
    fill_rect(img, chest_x, chest_y + 12, chest_w, 4, WOOD2)  # shadow
    stroke_rect(img, chest_x, chest_y + 8, chest_w, 8)
    
    # Top part (lid)
    fill_rect(img, chest_x, chest_y, chest_w, 8, WOOD)
    fill_rect(img, chest_x, chest_y + 4, chest_w, 4, WOOD2)  # shadow
    stroke_rect(img, chest_x, chest_y, chest_w, 8)
    
    # Metal bands on base
    fill_rect(img, chest_x - 1, chest_y + 10, chest_w + 2, 2, METAL)
    fill_rect(img, chest_x - 1, chest_y + 13, chest_w + 2, 1, METAL2)
    
    fill_rect(img, chest_x - 1, chest_y + 18, chest_w + 2, 2, METAL)
    fill_rect(img, chest_x - 1, chest_y + 19, chest_w + 2, 1, METAL2)
    
    # Metal bands on lid
    fill_rect(img, chest_x - 1, chest_y + 2, chest_w + 2, 2, METAL)
    fill_rect(img, chest_x - 1, chest_y + 3, chest_w + 2, 1, METAL2)
    
    fill_rect(img, chest_x - 1, chest_y + 6, chest_w + 2, 2, METAL)
    fill_rect(img, chest_x - 1, chest_y + 7, chest_w + 2, 1, METAL2)
    
    # Lock in center
    lock_x = chest_x + chest_w // 2 - 2
    lock_y = chest_y + 6
    fill_rect(img, lock_x, lock_y, 4, 4, LOCK)
    fill_rect(img, lock_x, lock_y + 2, 4, 2, LOCK2)
    stroke_rect(img, lock_x, lock_y, 4, 4)
    
    # Lock keyhole
    dot(img, lock_x + 2, lock_y + 2, OUT)

def draw_chest_opening(img, ox, oy, frame):
    """Draw chest opening animation"""
    # Base chest body (always same)
    chest_x = ox + 6
    chest_y = oy + 12
    chest_w = 20
    chest_h = 16
    
    # Bottom part (base) - stays same
    fill_rect(img, chest_x, chest_y + 8, chest_w, 8, WOOD)
    fill_rect(img, chest_x, chest_y + 12, chest_w, 4, WOOD2)
    stroke_rect(img, chest_x, chest_y + 8, chest_w, 8)
    
    # Metal bands on base
    fill_rect(img, chest_x - 1, chest_y + 10, chest_w + 2, 2, METAL)
    fill_rect(img, chest_x - 1, chest_y + 13, chest_w + 2, 1, METAL2)
    
    fill_rect(img, chest_x - 1, chest_y + 18, chest_w + 2, 2, METAL)
    fill_rect(img, chest_x - 1, chest_y + 19, chest_w + 2, 1, METAL2)
    
    # Lid opens progressively
    if frame == 0:  # Slightly open
        lid_tilt = 1
        lid_x = chest_x
        lid_y = chest_y - 1
        lid_w = chest_w
        lid_h = 7
    elif frame == 1:  # More open
        lid_tilt = 3
        lid_x = chest_x - 1
        lid_y = chest_y - 3
        lid_w = chest_w + 1
        lid_h = 6
    elif frame == 2:  # Almost fully open
        lid_tilt = 5
        lid_x = chest_x - 2
        lid_y = chest_y - 5
        lid_w = chest_w + 2
        lid_h = 5
    else:  # Frame 3 - fully open (same as open state)
        draw_chest_open(img, ox, oy)
        return
    
    # Draw tilted lid
    fill_rect(img, lid_x, lid_y, lid_w, lid_h, WOOD)
    fill_rect(img, lid_x, lid_y + lid_h - 2, lid_w, 2, WOOD2)
    stroke_rect(img, lid_x, lid_y, lid_w, lid_h)
    
    # Metal bands on lid
    fill_rect(img, lid_x - 1, lid_y + 1, lid_w + 2, 1, METAL)
    fill_rect(img, lid_x - 1, lid_y + 3, lid_w + 2, 1, METAL)
    
    # Show dark interior as chest opens
    if frame >= 1:
        interior_h = min(6, frame * 2)
        fill_rect(img, chest_x + 1, chest_y + 8, chest_w - 2, interior_h, INNER)

def draw_chest_open(img, ox, oy):
    """Draw fully open chest"""
    chest_x = ox + 6
    chest_y = oy + 12
    chest_w = 20
    chest_h = 16
    
    # Bottom part (base)
    fill_rect(img, chest_x, chest_y + 8, chest_w, 8, WOOD)
    fill_rect(img, chest_x, chest_y + 12, chest_w, 4, WOOD2)
    stroke_rect(img, chest_x, chest_y + 8, chest_w, 8)
    
    # Metal bands on base
    fill_rect(img, chest_x - 1, chest_y + 10, chest_w + 2, 2, METAL)
    fill_rect(img, chest_x - 1, chest_y + 13, chest_w + 2, 1, METAL2)
    
    fill_rect(img, chest_x - 1, chest_y + 18, chest_w + 2, 2, METAL)
    fill_rect(img, chest_x - 1, chest_y + 19, chest_w + 2, 1, METAL2)
    
    # Dark interior
    fill_rect(img, chest_x + 1, chest_y + 8, chest_w - 2, 7, INNER)
    
    # Lid fully opened (vertical behind chest)
    lid_x = chest_x - 3
    lid_y = chest_y - 8
    lid_w = chest_w + 6
    lid_h = 8
    
    fill_rect(img, lid_x, lid_y, lid_w, lid_h, WOOD)
    fill_rect(img, lid_x, lid_y + 4, lid_w, 4, WOOD2)
    stroke_rect(img, lid_x, lid_y, lid_w, lid_h)
    
    # Metal bands on open lid
    fill_rect(img, lid_x - 1, lid_y + 2, lid_w + 2, 1, METAL)
    fill_rect(img, lid_x - 1, lid_y + 5, lid_w + 2, 1, METAL)
    
    # Hinge connection
    fill_rect(img, chest_x + chest_w // 2 - 1, chest_y + 7, 2, 3, METAL2)

# === SPRITE GENERATION ===

def create_chest_sprite(state, frame=0):
    """Create a single chest sprite"""
    sprite = Image.new("RGBA", (SPRITE_SIZE, SPRITE_SIZE), TRANS)
    
    if state == "closed":
        draw_chest_closed(sprite, 0, 0)
    elif state == "opening":
        draw_chest_opening(sprite, 0, 0, frame)
    elif state == "open":
        draw_chest_open(sprite, 0, 0)
    
    return sprite

def generate_chest_sprites():
    """Generate all chest sprites and save them"""
    output_dir = Path("assets/sprites/objects/chest")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate closed chest
    closed_sprite = create_chest_sprite("closed")
    closed_sprite.save(output_dir / "chest_closed.png")
    print(f"Created {output_dir}/chest_closed.png")
    
    # Generate open chest
    open_sprite = create_chest_sprite("open")
    open_sprite.save(output_dir / "chest_open.png")
    print(f"Created {output_dir}/chest_open.png")
    
    # Generate opening animation frames
    opening_frames = 4
    opening_strip = Image.new("RGBA", (SPRITE_SIZE * opening_frames, SPRITE_SIZE), TRANS)
    
    for frame in range(opening_frames):
        sprite = create_chest_sprite("opening", frame)
        opening_strip.paste(sprite, (frame * SPRITE_SIZE, 0))
        
        # Also save individual frames
        sprite.save(output_dir / f"chest_opening_{frame}.png")
    
    opening_strip.save(output_dir / "chest_opening_strip.png")
    print(f"Created {output_dir}/chest_opening_strip.png")
    
    # Create complete sprite sheet
    sheet_width = 6 * SPRITE_SIZE  # closed, open, + 4 opening frames
    sheet_height = SPRITE_SIZE
    sheet = Image.new("RGBA", (sheet_width, sheet_height), TRANS)
    
    # Add closed
    sheet.paste(closed_sprite, (0, 0))
    
    # Add open
    sheet.paste(open_sprite, (SPRITE_SIZE, 0))
    
    # Add opening frames
    sheet.paste(opening_strip, (2 * SPRITE_SIZE, 0))
    
    sheet.save(output_dir / "chest_spritesheet.png")
    print(f"Created complete sprite sheet: {output_dir}/chest_spritesheet.png")
    
    # Create config file
    config = {
        "image": "chest_spritesheet.png",
        "frame_size": [32, 32],
        "animations": {
            "closed": {
                "frames": [0],
                "row": 0,
                "frame_duration": 1.0,
                "mode": "loop"
            },
            "open": {
                "frames": [1],
                "row": 0,
                "frame_duration": 1.0,
                "mode": "loop"
            },
            "opening": {
                "frames": [2, 3, 4, 5],
                "row": 0,
                "frame_duration": 0.15,
                "mode": "once"
            }
        }
    }
    
    config_path = output_dir / "chest_config.json"
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"Created animation config: {config_path}")

if __name__ == "__main__":
    generate_chest_sprites()
    print("\nAll chest sprites generated successfully!")