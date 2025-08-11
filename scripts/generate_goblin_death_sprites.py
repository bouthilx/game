#!/usr/bin/env python3
"""
Generate death animation sprites for goblins.
Creates a 4-frame death animation where the goblin falls backwards.
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

def draw_goblin_death(img, ox, oy, direction, frame):
    """Draw goblin death animation frame"""
    
    if direction == "down":
        draw_goblin_death_down(img, ox, oy, frame)
    elif direction == "up":
        draw_goblin_death_up(img, ox, oy, frame)
    elif direction == "left":
        draw_goblin_death_left(img, ox, oy, frame)
    elif direction == "right":
        draw_goblin_death_right(img, ox, oy, frame)

def draw_goblin_death_down(img, ox, oy, frame):
    """Death animation facing down - goblin falls backward"""
    # Frame 0: Normal stance, starting to fall
    # Frame 1: Tilting back
    # Frame 2: Halfway down
    # Frame 3: Flat on back (final corpse frame)
    
    if frame == 0:
        # Normal position but stumbling
        head_y = oy + 3
        body_y = oy + 16
        
        # Head (normal size)
        fill_rect(img, ox+9, head_y, 14, 12, SKIN)
        fill_rect(img, ox+9, head_y+8, 14, 4, SKIN2)
        stroke_rect(img, ox+9, head_y, 14, 12)
        
        # Ears
        fill_rect(img, ox+7, head_y+3, 3, 6, SKIN)
        stroke_rect(img, ox+7, head_y+3, 3, 6)
        fill_rect(img, ox+22, head_y+3, 3, 6, SKIN)
        stroke_rect(img, ox+22, head_y+3, 3, 6)
        
        # Eyes (still glowing)
        dot(img, ox+13, head_y+4, EYES)
        dot(img, ox+18, head_y+4, EYES)
        
        # Body
        fill_rect(img, ox+11, body_y, 10, 6, CLOTH)
        stroke_rect(img, ox+11, body_y, 10, 6)
        
        # Arms spread out (starting to fall)
        fill_rect(img, ox+7, body_y, 3, 4, SKIN)
        stroke_rect(img, ox+7, body_y, 3, 4)
        fill_rect(img, ox+22, body_y, 3, 4, SKIN)
        stroke_rect(img, ox+22, body_y, 3, 4)
        
        # Legs
        fill_rect(img, ox+13, oy+23, 2, 3, SKIN)
        stroke_rect(img, ox+13, oy+23, 2, 3)
        fill_rect(img, ox+17, oy+23, 2, 3, SKIN)
        stroke_rect(img, ox+17, oy+23, 2, 3)
        
    elif frame == 1:
        # Tilting back, head moving down
        head_y = oy + 5
        body_y = oy + 17
        
        # Head tilted
        fill_rect(img, ox+8, head_y, 16, 11, SKIN)
        fill_rect(img, ox+8, head_y+7, 16, 4, SKIN2)
        stroke_rect(img, ox+8, head_y, 16, 11)
        
        # Ears spread
        fill_rect(img, ox+5, head_y+2, 4, 5, SKIN)
        stroke_rect(img, ox+5, head_y+2, 4, 5)
        fill_rect(img, ox+23, head_y+2, 4, 5, SKIN)
        stroke_rect(img, ox+23, head_y+2, 4, 5)
        
        # Eyes dimming
        dot(img, ox+12, head_y+3, EYES_DIM)
        dot(img, ox+19, head_y+3, EYES_DIM)
        
        # Body
        fill_rect(img, ox+10, body_y, 12, 5, CLOTH)
        stroke_rect(img, ox+10, body_y, 12, 5)
        
        # Arms spread wider
        fill_rect(img, ox+5, body_y-1, 4, 3, SKIN)
        stroke_rect(img, ox+5, body_y-1, 4, 3)
        fill_rect(img, ox+23, body_y-1, 4, 3, SKIN)
        stroke_rect(img, ox+23, body_y-1, 4, 3)
        
        # Legs
        fill_rect(img, ox+14, oy+23, 2, 3, SKIN)
        stroke_rect(img, ox+14, oy+23, 2, 3)
        fill_rect(img, ox+16, oy+23, 2, 3, SKIN)
        stroke_rect(img, ox+16, oy+23, 2, 3)
        
    elif frame == 2:
        # Halfway down
        head_y = oy + 8
        body_y = oy + 18
        
        # Head more horizontal
        fill_rect(img, ox+6, head_y, 20, 9, SKIN)
        fill_rect(img, ox+6, head_y+6, 20, 3, SKIN2)
        stroke_rect(img, ox+6, head_y, 20, 9)
        
        # Ears flat
        fill_rect(img, ox+3, head_y+1, 5, 3, SKIN)
        stroke_rect(img, ox+3, head_y+1, 5, 3)
        fill_rect(img, ox+24, head_y+1, 5, 3, SKIN)
        stroke_rect(img, ox+24, head_y+1, 5, 3)
        
        # Eyes very dim
        dot(img, ox+11, head_y+2, EYES_DIM)
        dot(img, ox+20, head_y+2, EYES_DIM)
        
        # Body horizontal
        fill_rect(img, ox+8, body_y, 16, 4, CLOTH)
        stroke_rect(img, ox+8, body_y, 16, 4)
        
        # Arms spread out flat
        fill_rect(img, ox+3, body_y, 5, 2, SKIN)
        stroke_rect(img, ox+3, body_y, 5, 2)
        fill_rect(img, ox+24, body_y, 5, 2, SKIN)
        stroke_rect(img, ox+24, body_y, 5, 2)
        
        # Legs spread
        fill_rect(img, ox+12, oy+24, 2, 2, SKIN)
        stroke_rect(img, ox+12, oy+24, 2, 2)
        fill_rect(img, ox+18, oy+24, 2, 2, SKIN)
        stroke_rect(img, ox+18, oy+24, 2, 2)
        
    else:  # frame == 3
        # Flat on back (final corpse)
        head_y = oy + 12
        body_y = oy + 20
        
        # Head completely flat
        fill_rect(img, ox+4, head_y, 24, 6, SKIN)
        fill_rect(img, ox+4, head_y+4, 24, 2, SKIN2)
        stroke_rect(img, ox+4, head_y, 24, 6)
        
        # Ears completely flat
        fill_rect(img, ox+1, head_y, 6, 2, SKIN)
        stroke_rect(img, ox+1, head_y, 6, 2)
        fill_rect(img, ox+25, head_y, 6, 2, SKIN)
        stroke_rect(img, ox+25, head_y, 6, 2)
        
        # Eyes closed/dead
        dot(img, ox+10, head_y+1, OUT)
        dot(img, ox+21, head_y+1, OUT)
        
        # Body completely flat
        fill_rect(img, ox+6, body_y, 20, 3, CLOTH)
        stroke_rect(img, ox+6, body_y, 20, 3)
        
        # Arms completely spread
        fill_rect(img, ox+1, body_y, 6, 1, SKIN)
        stroke_rect(img, ox+1, body_y, 6, 1)
        fill_rect(img, ox+25, body_y, 6, 1, SKIN)
        stroke_rect(img, ox+25, body_y, 6, 1)
        
        # Legs flat
        fill_rect(img, ox+10, oy+25, 3, 1, SKIN)
        stroke_rect(img, ox+10, oy+25, 3, 1)
        fill_rect(img, ox+19, oy+25, 3, 1, SKIN)
        stroke_rect(img, ox+19, oy+25, 3, 1)

def draw_goblin_death_up(img, ox, oy, frame):
    """Death animation facing up - similar but back view"""
    # Similar logic but showing back of goblin falling forward
    if frame <= 2:
        # Show back of goblin falling forward (similar to falling back but front-facing)
        head_y = oy + 3 + frame * 2
        body_y = oy + 16 + frame
        
        # Back of head
        fill_rect(img, ox+8 - frame, head_y, 16 + frame*2, 12 - frame*2, SKIN)
        stroke_rect(img, ox+8 - frame, head_y, 16 + frame*2, 12 - frame*2)
        
        # Body
        fill_rect(img, ox+11 - frame, body_y, 10 + frame*2, 6 - frame, CLOTH)
        stroke_rect(img, ox+11 - frame, body_y, 10 + frame*2, 6 - frame)
        
    else:  # Final frame - flat on ground
        draw_goblin_death_down(img, ox, oy, frame)  # Same final position

def draw_goblin_death_left(img, ox, oy, frame):
    """Death animation facing left - falls to the side"""
    if frame <= 2:
        # Falling to left side
        head_y = oy + 3 + frame
        body_y = oy + 16 + frame
        tilt = frame * 2
        
        # Head tilting
        fill_rect(img, ox+8 - tilt, head_y, 13 + tilt, 12 - frame, SKIN)
        stroke_rect(img, ox+8 - tilt, head_y, 13 + tilt, 12 - frame)
        
        # Body
        fill_rect(img, ox+12 - tilt, body_y, 8 + tilt, 6 - frame, CLOTH)
        stroke_rect(img, ox+12 - tilt, body_y, 8 + tilt, 6 - frame)
        
    else:  # Final frame
        draw_goblin_death_down(img, ox, oy, frame)  # Same final position

def draw_goblin_death_right(img, ox, oy, frame):
    """Death animation facing right - falls to the side"""
    if frame <= 2:
        # Falling to right side (mirror of left)
        head_y = oy + 3 + frame
        body_y = oy + 16 + frame
        tilt = frame * 2
        
        # Head tilting
        fill_rect(img, ox+11, head_y, 13 + tilt, 12 - frame, SKIN)
        stroke_rect(img, ox+11, head_y, 13 + tilt, 12 - frame)
        
        # Body
        fill_rect(img, ox+12, body_y, 8 + tilt, 6 - frame, CLOTH)
        stroke_rect(img, ox+12, body_y, 8 + tilt, 6 - frame)
        
    else:  # Final frame
        draw_goblin_death_down(img, ox, oy, frame)  # Same final position

def create_death_animation_strip(direction, num_frames=4):
    """Create a horizontal strip of death animation frames"""
    strip = Image.new("RGBA", (SPRITE_SIZE * num_frames, SPRITE_SIZE), TRANS)
    
    for frame in range(num_frames):
        draw_goblin_death(strip, frame * SPRITE_SIZE, 0, direction, frame)
    
    return strip

def update_goblin_sprites_with_death():
    """Add death animations to existing goblin sprites"""
    output_dir = Path("assets/sprites/characters/goblin")
    
    directions = ["down", "up", "left", "right"]
    
    # Create death directory
    (output_dir / "death").mkdir(exist_ok=True)
    
    # Generate death sprites
    for direction in directions:
        # Create death animation strip
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
    
    # Update sprite sheet to include death animations
    # Load existing sprite sheet and expand it
    existing_sheet_path = output_dir / "goblin_spritesheet.png"
    if existing_sheet_path.exists():
        existing_sheet = Image.open(existing_sheet_path)
        
        # Create new larger sheet: 4 directions x 4 animation types (idle, walk, attack, death)
        new_sheet_width = 16 * SPRITE_SIZE  # 4 animations x 4 frames
        new_sheet_height = 4 * SPRITE_SIZE  # 4 directions
        new_sheet = Image.new("RGBA", (new_sheet_width, new_sheet_height), TRANS)
        
        # Copy existing animations (idle, walk, attack)
        new_sheet.paste(existing_sheet, (0, 0))
        
        # Add death animations at the end
        for dir_idx, direction in enumerate(directions):
            death_strip = create_death_animation_strip(direction, 4)
            new_sheet.paste(death_strip, (12 * SPRITE_SIZE, dir_idx * SPRITE_SIZE))  # 3 existing animations * 4 frames = 12
        
        # Save updated sprite sheet
        new_sheet.save(existing_sheet_path)
        print(f"Updated sprite sheet with death animations: {existing_sheet_path}")
    
    # Update config file
    config_path = output_dir / "goblin_config.json"
    if config_path.exists():
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        # Add death animations to config
        directions = ["down", "up", "left", "right"]
        for dir_idx, direction in enumerate(directions):
            anim_name = f"death_{direction}"
            config["animations"][anim_name] = {
                "frames": [12, 13, 14, 15],  # Frames 12-15 in the sheet
                "row": dir_idx,
                "frame_duration": 0.3,  # Slower death animation
                "mode": "once"  # Play once and stop
            }
        
        # Save updated config
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"Updated animation config with death animations: {config_path}")

if __name__ == "__main__":
    update_goblin_sprites_with_death()
    print("\nGoblin death sprites added successfully!")