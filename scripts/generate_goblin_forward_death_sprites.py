#!/usr/bin/env python3
"""
Generate forward-falling death animation sprites for goblins.
Creates a 4-frame death animation where the goblin falls forward and face-down.
"""

from PIL import Image
import os
import json
from pathlib import Path

# Sprite dimensions
SPRITE_SIZE = 32

# Goblin color palette
OUT   = (43, 35, 27, 255)       # dark outline
SKIN  = (120, 150, 80, 255)     # Green goblin skin
SKIN2 = (90, 110, 60, 255)      # Darker green for shadows
CLOTH = (80, 60, 40, 255)       # Brown cloth/rags
CLOTH2= (60, 45, 30, 255)       # Darker brown
EYES  = (255, 50, 50, 255)      # Red glowing eyes (dimming)
EYES_DIM = (150, 30, 30, 255)   # Dimmed red eyes
TEETH = (255, 255, 200, 255)    # Yellow teeth
WEAPON= (150, 150, 150, 255)    # Grey weapon/claw
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

def draw_goblin_forward_death_down(img, ox, oy, frame):
    """Death animation facing down - goblin falls forward and face-down"""
    # Frame 0: Normal stance, starting to stumble forward
    # Frame 1: Leaning forward, arms out for balance
    # Frame 2: Falling down, arms spread
    # Frame 3: Face-down flat on ground (final corpse frame)
    
    if frame == 0:
        # Normal position but stumbling forward
        head_y = oy + 3
        body_y = oy + 16
        
        # Head (normal size, slightly forward)
        fill_rect(img, ox+10, head_y, 12, 12, SKIN)
        fill_rect(img, ox+10, head_y+8, 12, 4, SKIN2)
        stroke_rect(img, ox+10, head_y, 12, 12)
        
        # Ears
        fill_rect(img, ox+8, head_y+3, 3, 6, SKIN)
        stroke_rect(img, ox+8, head_y+3, 3, 6)
        fill_rect(img, ox+21, head_y+3, 3, 6, SKIN)
        stroke_rect(img, ox+21, head_y+3, 3, 6)
        
        # Eyes (still glowing, slightly worried)
        dot(img, ox+13, head_y+4, EYES)
        dot(img, ox+18, head_y+4, EYES)
        
        # Body slightly leaning forward
        fill_rect(img, ox+12, body_y, 8, 6, CLOTH)
        stroke_rect(img, ox+12, body_y, 8, 6)
        
        # Arms starting to spread for balance
        fill_rect(img, ox+8, body_y+1, 3, 4, SKIN)
        stroke_rect(img, ox+8, body_y+1, 3, 4)
        fill_rect(img, ox+21, body_y+1, 3, 4, SKIN)
        stroke_rect(img, ox+21, body_y+1, 3, 4)
        
        # Legs (normal stance)
        fill_rect(img, ox+13, oy+23, 2, 6, SKIN)
        stroke_rect(img, ox+13, oy+23, 2, 6)
        fill_rect(img, ox+17, oy+23, 2, 6, SKIN)
        stroke_rect(img, ox+17, oy+23, 2, 6)
        
    elif frame == 1:
        # Leaning forward more, arms out for balance
        head_y = oy + 4
        body_y = oy + 17
        
        # Head leaning forward
        fill_rect(img, ox+11, head_y, 11, 11, SKIN)
        fill_rect(img, ox+11, head_y+7, 11, 4, SKIN2)
        stroke_rect(img, ox+11, head_y, 11, 11)
        
        # Ears
        fill_rect(img, ox+9, head_y+2, 3, 6, SKIN)
        stroke_rect(img, ox+9, head_y+2, 3, 6)
        fill_rect(img, ox+21, head_y+2, 3, 6, SKIN)
        stroke_rect(img, ox+21, head_y+2, 3, 6)
        
        # Eyes starting to dim
        dot(img, ox+13, head_y+3, EYES_DIM)
        dot(img, ox+18, head_y+3, EYES_DIM)
        
        # Body leaning forward
        fill_rect(img, ox+12, body_y, 8, 5, CLOTH)
        stroke_rect(img, ox+12, body_y, 8, 5)
        
        # Arms spread wide for balance
        fill_rect(img, ox+6, body_y, 4, 3, SKIN)
        stroke_rect(img, ox+6, body_y, 4, 3)
        fill_rect(img, ox+22, body_y, 4, 3, SKIN)
        stroke_rect(img, ox+22, body_y, 4, 3)
        
        # Legs bent, trying to catch balance
        fill_rect(img, ox+12, oy+23, 3, 5, SKIN)
        stroke_rect(img, ox+12, oy+23, 3, 5)
        fill_rect(img, ox+17, oy+23, 3, 5, SKIN)
        stroke_rect(img, ox+17, oy+23, 3, 5)
        
    elif frame == 2:
        # Falling down, almost horizontal
        head_y = oy + 6
        body_y = oy + 18
        
        # Head closer to ground
        fill_rect(img, ox+9, head_y, 14, 8, SKIN)
        fill_rect(img, ox+9, head_y+5, 14, 3, SKIN2)
        stroke_rect(img, ox+9, head_y, 14, 8)
        
        # Ears spread
        fill_rect(img, ox+6, head_y+1, 4, 4, SKIN)
        stroke_rect(img, ox+6, head_y+1, 4, 4)
        fill_rect(img, ox+22, head_y+1, 4, 4, SKIN)
        stroke_rect(img, ox+22, head_y+1, 4, 4)
        
        # Eyes very dim
        dot(img, ox+12, head_y+2, EYES_DIM)
        dot(img, ox+19, head_y+2, EYES_DIM)
        
        # Body falling horizontal
        fill_rect(img, ox+10, body_y, 12, 4, CLOTH)
        stroke_rect(img, ox+10, body_y, 12, 4)
        
        # Arms spread out completely
        fill_rect(img, ox+4, body_y, 6, 2, SKIN)
        stroke_rect(img, ox+4, body_y, 6, 2)
        fill_rect(img, ox+22, body_y, 6, 2, SKIN)
        stroke_rect(img, ox+22, body_y, 6, 2)
        
        # Legs collapsing
        fill_rect(img, ox+11, oy+24, 3, 3, SKIN)
        stroke_rect(img, ox+11, oy+24, 3, 3)
        fill_rect(img, ox+18, oy+24, 3, 3, SKIN)
        stroke_rect(img, ox+18, oy+24, 3, 3)
        
    else:  # frame == 3
        # Face-down flat on ground (final corpse position)
        head_y = oy + 8
        body_y = oy + 20
        
        # Head completely flat on ground, face down
        fill_rect(img, ox+8, head_y, 16, 6, SKIN)
        fill_rect(img, ox+8, head_y+3, 16, 3, SKIN2)
        stroke_rect(img, ox+8, head_y, 16, 6)
        
        # Ears flat against ground
        fill_rect(img, ox+4, head_y+1, 5, 2, SKIN)
        stroke_rect(img, ox+4, head_y+1, 5, 2)
        fill_rect(img, ox+23, head_y+1, 5, 2, SKIN)
        stroke_rect(img, ox+23, head_y+1, 5, 2)
        
        # No visible eyes (face down)
        # Maybe show a bit of the back of the head
        fill_rect(img, ox+14, head_y, 4, 2, SKIN2)
        
        # Body completely flat
        fill_rect(img, ox+8, body_y, 16, 3, CLOTH)
        stroke_rect(img, ox+8, body_y, 16, 3)
        
        # Arms completely spread and flat
        fill_rect(img, ox+2, body_y, 8, 1, SKIN)
        stroke_rect(img, ox+2, body_y, 8, 1)
        fill_rect(img, ox+22, body_y, 8, 1, SKIN)
        stroke_rect(img, ox+22, body_y, 8, 1)
        
        # Legs flat and spread
        fill_rect(img, ox+9, oy+25, 4, 2, SKIN)
        stroke_rect(img, ox+9, oy+25, 4, 2)
        fill_rect(img, ox+19, oy+25, 4, 2, SKIN)
        stroke_rect(img, ox+19, oy+25, 4, 2)

def draw_goblin_forward_death(img, ox, oy, direction, frame):
    """Draw goblin forward death animation frame"""
    
    if direction == "down":
        draw_goblin_forward_death_down(img, ox, oy, frame)
    elif direction == "up":
        # Up direction: falling forward away from camera (showing back)
        draw_goblin_forward_death_down(img, ox, oy, frame)  # Same as down for now
    elif direction == "left":
        # Left direction: falling to left side (similar concept)
        draw_goblin_forward_death_down(img, ox, oy, frame)  # Same as down for now
    elif direction == "right":
        # Right direction: falling to right side (similar concept)
        draw_goblin_forward_death_down(img, ox, oy, frame)  # Same as down for now

def create_death_animation_strip(direction, num_frames=4):
    """Create a horizontal strip of death animation frames"""
    strip = Image.new("RGBA", (SPRITE_SIZE * num_frames, SPRITE_SIZE), TRANS)
    
    for frame in range(num_frames):
        draw_goblin_forward_death(strip, frame * SPRITE_SIZE, 0, direction, frame)
    
    return strip

def update_goblin_sprites_with_forward_death():
    """Replace existing death animations with forward-falling versions"""
    output_dir = Path("assets/sprites/characters/goblin")
    
    directions = ["down", "up", "left", "right"]
    
    # Ensure death directory exists
    (output_dir / "death").mkdir(exist_ok=True)
    
    # Generate forward death sprites
    for direction in directions:
        # Create forward death animation strip
        strip = create_death_animation_strip(direction, 4)
        
        # Save strip
        strip_path = output_dir / "death" / f"goblin_death_{direction}_strip.png"
        strip.save(strip_path)
        print(f"Created {strip_path}")
        
        # Save individual frames
        for frame in range(4):
            frame_img = Image.new("RGBA", (SPRITE_SIZE, SPRITE_SIZE), TRANS)
            frame_img.paste(strip.crop((frame * SPRITE_SIZE, 0, 
                                       (frame + 1) * SPRITE_SIZE, SPRITE_SIZE)), 
                           (0, 0))
            
            frame_path = output_dir / "death" / f"goblin_death_{direction}_{frame}.png"
            frame_img.save(frame_path)
    
    # Update sprite sheet to include forward death animations
    existing_sheet_path = output_dir / "goblin_spritesheet.png"
    if existing_sheet_path.exists():
        existing_sheet = Image.open(existing_sheet_path)
        
        # Create new sheet with forward death animations
        new_sheet_width = 16 * SPRITE_SIZE  # 4 animations x 4 frames
        new_sheet_height = 4 * SPRITE_SIZE  # 4 directions
        new_sheet = Image.new("RGBA", (new_sheet_width, new_sheet_height), TRANS)
        
        # Copy existing animations (idle, walk, attack) - first 12 columns
        new_sheet.paste(existing_sheet.crop((0, 0, 12 * SPRITE_SIZE, new_sheet_height)), (0, 0))
        
        # Add forward death animations at columns 12-15
        for dir_idx, direction in enumerate(directions):
            death_strip = create_death_animation_strip(direction, 4)
            new_sheet.paste(death_strip, (12 * SPRITE_SIZE, dir_idx * SPRITE_SIZE))
        
        # Save updated sprite sheet
        new_sheet.save(existing_sheet_path)
        print(f"Updated sprite sheet with forward death animations: {existing_sheet_path}")

if __name__ == "__main__":
    update_goblin_sprites_with_forward_death()
    print("\nGoblin forward death sprites created successfully!")
    print("The goblins now fall forward and face-down, perfect for the 'puking' blood effect!")