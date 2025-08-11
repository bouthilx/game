#!/usr/bin/env python3
"""
Generate goblin sprites for the enemy system.
Creates idle, walk, and attack animations for all 4 directions.
Based on player sprite generation but with goblin characteristics.
"""

from PIL import Image
import os
import json
from pathlib import Path

# Sprite dimensions
SPRITE_SIZE = 32
TILE = 32

# Goblin color palette
OUT   = (43, 35, 27, 255)       # dark outline
SKIN  = (120, 150, 80, 255)     # Green goblin skin
SKIN2 = (90, 110, 60, 255)      # Darker green for shadows
CLOTH = (80, 60, 40, 255)       # Brown cloth/rags
CLOTH2= (60, 45, 30, 255)       # Darker brown
EYES  = (255, 50, 50, 255)      # Red glowing eyes
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

# === GOBLIN DRAWING FUNCTIONS ===

def draw_goblin_down(img, ox, oy, frame=0, anim_type="idle"):
    """Draw goblin facing down (toward viewer)"""
    # Animation offsets
    bob = 0
    arm_swing = 0
    ear_twitch = 0
    
    if anim_type == "walk":
        bob = [0, 1, 0, -1][frame % 4]
        arm_swing = [-1, 0, 1, 0][frame % 4]
    elif anim_type == "attack":
        if frame == 0:  # Wind up
            oy -= 1
            ear_twitch = 1
        elif frame == 1:  # Strike
            oy += 2
            arm_swing = 2
        elif frame == 2:  # Follow through
            oy += 1
    
    oy += bob
    
    # Large goblin head (bigger than human)
    head_size = 14
    head_y = oy + 3
    fill_rect(img, ox+9, head_y, head_size, 12, SKIN)
    fill_rect(img, ox+9, head_y+8, head_size, 4, SKIN2)  # jaw shadow
    stroke_rect(img, ox+9, head_y, head_size, 12)
    
    # Pointed ears
    ear_offset = ear_twitch
    # Left ear
    fill_rect(img, ox+7-ear_offset, head_y+3, 3, 6, SKIN)
    stroke_rect(img, ox+7-ear_offset, head_y+3, 3, 6)
    dot(img, ox+7-ear_offset, head_y+3)  # pointed tip
    # Right ear
    fill_rect(img, ox+22+ear_offset, head_y+3, 3, 6, SKIN)
    stroke_rect(img, ox+22+ear_offset, head_y+3, 3, 6)
    dot(img, ox+24+ear_offset, head_y+3)  # pointed tip
    
    # Glowing red eyes
    dot(img, ox+13, head_y+4, EYES)
    dot(img, ox+18, head_y+4, EYES)
    
    # Snarling mouth with teeth
    fill_rect(img, ox+14, head_y+7, 4, 2, OUT)  # mouth
    dot(img, ox+14, head_y+7, TEETH)  # left fang
    dot(img, ox+17, head_y+7, TEETH)  # right fang
    
    # Small goblin body (shorter than human)
    body_y = oy + 16
    fill_rect(img, ox+11, body_y, 10, 6, CLOTH)
    fill_rect(img, ox+11, body_y+3, 10, 3, CLOTH2)  # shadow
    stroke_rect(img, ox+11, body_y, 10, 6)
    
    # Arms with claws
    if anim_type == "attack":
        # Extended claws for attack
        fill_rect(img, ox+8, body_y-1+arm_swing, 3, 4, SKIN)
        stroke_rect(img, ox+8, body_y-1+arm_swing, 3, 4)
        # Claws
        dot(img, ox+7, body_y-2+arm_swing, WEAPON)
        dot(img, ox+8, body_y-2+arm_swing, WEAPON)
        
        fill_rect(img, ox+21, body_y-1+arm_swing, 3, 4, SKIN)
        stroke_rect(img, ox+21, body_y-1+arm_swing, 3, 4)
        dot(img, ox+23, body_y-2+arm_swing, WEAPON)
        dot(img, ox+24, body_y-2+arm_swing, WEAPON)
    else:
        # Normal arms
        fill_rect(img, ox+9, body_y+1+arm_swing, 2, 4, SKIN)
        stroke_rect(img, ox+9, body_y+1+arm_swing, 2, 4)
        fill_rect(img, ox+21, body_y+1-arm_swing, 2, 4, SKIN)
        stroke_rect(img, ox+21, body_y+1-arm_swing, 2, 4)
    
    # Legs/feet - goblins are barefoot
    if anim_type == "walk":
        if frame % 2 == 0:
            fill_rect(img, ox+13, oy+23, 2, 3, SKIN)
            stroke_rect(img, ox+13, oy+23, 2, 3)
            fill_rect(img, ox+17, oy+24, 2, 2, SKIN)
            stroke_rect(img, ox+17, oy+24, 2, 2)
        else:
            fill_rect(img, ox+13, oy+24, 2, 2, SKIN)
            stroke_rect(img, ox+13, oy+24, 2, 2)
            fill_rect(img, ox+17, oy+23, 2, 3, SKIN)
            stroke_rect(img, ox+17, oy+23, 2, 3)
    else:
        fill_rect(img, ox+13, oy+23, 2, 3, SKIN)
        stroke_rect(img, ox+13, oy+23, 2, 3)
        fill_rect(img, ox+17, oy+23, 2, 3, SKIN)
        stroke_rect(img, ox+17, oy+23, 2, 3)

def draw_goblin_up(img, ox, oy, frame=0, anim_type="idle"):
    """Draw goblin facing up (away from viewer)"""
    bob = 0
    arm_swing = 0
    
    if anim_type == "walk":
        bob = [0, 1, 0, -1][frame % 4]
        arm_swing = [-1, 0, 1, 0][frame % 4]
    elif anim_type == "attack":
        if frame == 0:
            oy -= 1
        elif frame == 1:
            oy += 2
        elif frame == 2:
            oy += 1
    
    oy += bob
    
    # Back of head (larger for goblin)
    head_y = oy + 3
    fill_rect(img, ox+8, head_y, 16, 12, SKIN)
    fill_rect(img, ox+8, head_y+8, 16, 4, SKIN2)
    stroke_rect(img, ox+8, head_y, 16, 12)
    
    # Ears from behind
    fill_rect(img, ox+6, head_y+3, 3, 6, SKIN)
    stroke_rect(img, ox+6, head_y+3, 3, 6)
    fill_rect(img, ox+23, head_y+3, 3, 6, SKIN)
    stroke_rect(img, ox+23, head_y+3, 3, 6)
    
    # Body
    body_y = oy + 16
    fill_rect(img, ox+11, body_y, 10, 6, CLOTH)
    fill_rect(img, ox+11, body_y+3, 10, 3, CLOTH2)
    stroke_rect(img, ox+11, body_y, 10, 6)
    
    # Arms
    if anim_type == "attack":
        # Raised for attack
        fill_rect(img, ox+8, body_y-2, 3, 4, SKIN)
        stroke_rect(img, ox+8, body_y-2, 3, 4)
        fill_rect(img, ox+21, body_y-2, 3, 4, SKIN)
        stroke_rect(img, ox+21, body_y-2, 3, 4)
    else:
        fill_rect(img, ox+9, body_y+1+arm_swing, 2, 4, SKIN)
        stroke_rect(img, ox+9, body_y+1+arm_swing, 2, 4)
        fill_rect(img, ox+21, body_y+1-arm_swing, 2, 4, SKIN)
        stroke_rect(img, ox+21, body_y+1-arm_swing, 2, 4)
    
    # Feet
    if anim_type == "walk":
        if frame % 2 == 0:
            fill_rect(img, ox+13, oy+23, 2, 3, SKIN)
            stroke_rect(img, ox+13, oy+23, 2, 3)
            fill_rect(img, ox+17, oy+24, 2, 2, SKIN)
            stroke_rect(img, ox+17, oy+24, 2, 2)
        else:
            fill_rect(img, ox+13, oy+24, 2, 2, SKIN)
            stroke_rect(img, ox+13, oy+24, 2, 2)
            fill_rect(img, ox+17, oy+23, 2, 3, SKIN)
            stroke_rect(img, ox+17, oy+23, 2, 3)
    else:
        fill_rect(img, ox+13, oy+23, 2, 3, SKIN)
        stroke_rect(img, ox+13, oy+23, 2, 3)
        fill_rect(img, ox+17, oy+23, 2, 3, SKIN)
        stroke_rect(img, ox+17, oy+23, 2, 3)

def draw_goblin_left(img, ox, oy, frame=0, anim_type="idle"):
    """Draw goblin facing left"""
    bob = 0
    
    if anim_type == "walk":
        bob = [0, 1, 0, -1][frame % 4]
        ox += [-1, 0, 1, 0][frame % 4]
    elif anim_type == "attack":
        if frame == 0:
            ox += 1
        elif frame == 1:
            ox -= 3
        elif frame == 2:
            ox -= 1
    
    oy += bob
    
    # Profile head with pointed ears
    head_y = oy + 3
    fill_rect(img, ox+8, head_y, 13, 12, SKIN)
    fill_rect(img, ox+8, head_y+8, 13, 4, SKIN2)
    stroke_rect(img, ox+8, head_y, 13, 12)
    
    # Pointed ear
    fill_rect(img, ox+6, head_y+3, 3, 6, SKIN)
    stroke_rect(img, ox+6, head_y+3, 3, 6)
    dot(img, ox+6, head_y+3)  # pointed tip
    
    # Profile face
    fill_rect(img, ox+8, head_y+4, 4, 6, SKIN)
    stroke_rect(img, ox+8, head_y+4, 4, 6)
    dot(img, ox+10, head_y+6, EYES)  # red eye
    
    # Snarling mouth
    dot(img, ox+8, head_y+8, OUT)
    dot(img, ox+8, head_y+8, TEETH)  # fang
    
    # Body
    body_y = oy + 16
    fill_rect(img, ox+12, body_y, 8, 6, CLOTH)
    fill_rect(img, ox+12, body_y+3, 8, 3, CLOTH2)
    stroke_rect(img, ox+12, body_y, 8, 6)
    
    # Arm with claw
    if anim_type == "attack":
        # Extended claw
        fill_rect(img, ox+6, body_y, 5, 3, SKIN)
        stroke_rect(img, ox+6, body_y, 5, 3)
        # Claws
        dot(img, ox+4, body_y, WEAPON)
        dot(img, ox+5, body_y, WEAPON)
        dot(img, ox+6, body_y, WEAPON)
    else:
        fill_rect(img, ox+11, body_y+1, 2, 4, SKIN)
        stroke_rect(img, ox+11, body_y+1, 2, 4)
    
    # Feet
    if anim_type == "walk":
        if frame == 0 or frame == 2:
            fill_rect(img, ox+14, oy+23, 2, 3, SKIN)
            stroke_rect(img, ox+14, oy+23, 2, 3)
            fill_rect(img, ox+17, oy+23, 2, 3, SKIN)
            stroke_rect(img, ox+17, oy+23, 2, 3)
        elif frame == 1:
            fill_rect(img, ox+13, oy+23, 2, 3, SKIN)
            stroke_rect(img, ox+13, oy+23, 2, 3)
            fill_rect(img, ox+18, oy+24, 2, 2, SKIN)
            stroke_rect(img, ox+18, oy+24, 2, 2)
        else:
            fill_rect(img, ox+15, oy+24, 2, 2, SKIN)
            stroke_rect(img, ox+15, oy+24, 2, 2)
            fill_rect(img, ox+16, oy+23, 2, 3, SKIN)
            stroke_rect(img, ox+16, oy+23, 2, 3)
    else:
        fill_rect(img, ox+14, oy+23, 2, 3, SKIN)
        stroke_rect(img, ox+14, oy+23, 2, 3)
        fill_rect(img, ox+17, oy+23, 2, 3, SKIN)
        stroke_rect(img, ox+17, oy+23, 2, 3)

def draw_goblin_right(img, ox, oy, frame=0, anim_type="idle"):
    """Draw goblin facing right"""
    bob = 0
    
    if anim_type == "walk":
        bob = [0, 1, 0, -1][frame % 4]
        ox += [1, 0, -1, 0][frame % 4]
    elif anim_type == "attack":
        if frame == 0:
            ox -= 1
        elif frame == 1:
            ox += 3
        elif frame == 2:
            ox += 1
    
    oy += bob
    
    # Profile head (mirror of left)
    head_y = oy + 3
    fill_rect(img, ox+11, head_y, 13, 12, SKIN)
    fill_rect(img, ox+11, head_y+8, 13, 4, SKIN2)
    stroke_rect(img, ox+11, head_y, 13, 12)
    
    # Pointed ear
    fill_rect(img, ox+23, head_y+3, 3, 6, SKIN)
    stroke_rect(img, ox+23, head_y+3, 3, 6)
    dot(img, ox+25, head_y+3)  # pointed tip
    
    # Profile face
    fill_rect(img, ox+20, head_y+4, 4, 6, SKIN)
    stroke_rect(img, ox+20, head_y+4, 4, 6)
    dot(img, ox+22, head_y+6, EYES)  # red eye
    
    # Snarling mouth
    dot(img, ox+23, head_y+8, OUT)
    dot(img, ox+23, head_y+8, TEETH)  # fang
    
    # Body
    body_y = oy + 16
    fill_rect(img, ox+12, body_y, 8, 6, CLOTH)
    fill_rect(img, ox+12, body_y+3, 8, 3, CLOTH2)
    stroke_rect(img, ox+12, body_y, 8, 6)
    
    # Arm with claw
    if anim_type == "attack":
        # Extended claw
        fill_rect(img, ox+21, body_y, 5, 3, SKIN)
        stroke_rect(img, ox+21, body_y, 5, 3)
        # Claws
        dot(img, ox+26, body_y, WEAPON)
        dot(img, ox+27, body_y, WEAPON)
        dot(img, ox+25, body_y, WEAPON)
    else:
        fill_rect(img, ox+19, body_y+1, 2, 4, SKIN)
        stroke_rect(img, ox+19, body_y+1, 2, 4)
    
    # Feet
    if anim_type == "walk":
        if frame == 0 or frame == 2:
            fill_rect(img, ox+14, oy+23, 2, 3, SKIN)
            stroke_rect(img, ox+14, oy+23, 2, 3)
            fill_rect(img, ox+17, oy+23, 2, 3, SKIN)
            stroke_rect(img, ox+17, oy+23, 2, 3)
        elif frame == 1:
            fill_rect(img, ox+13, oy+24, 2, 2, SKIN)
            stroke_rect(img, ox+13, oy+24, 2, 2)
            fill_rect(img, ox+18, oy+23, 2, 3, SKIN)
            stroke_rect(img, ox+18, oy+23, 2, 3)
        else:
            fill_rect(img, ox+15, oy+23, 2, 3, SKIN)
            stroke_rect(img, ox+15, oy+23, 2, 3)
            fill_rect(img, ox+16, oy+24, 2, 2, SKIN)
            stroke_rect(img, ox+16, oy+24, 2, 2)
    else:
        fill_rect(img, ox+14, oy+23, 2, 3, SKIN)
        stroke_rect(img, ox+14, oy+23, 2, 3)
        fill_rect(img, ox+17, oy+23, 2, 3, SKIN)
        stroke_rect(img, ox+17, oy+23, 2, 3)

# === SPRITE GENERATION ===

def create_animation_strip(direction, anim_type, num_frames=4):
    """Create a horizontal strip of animation frames"""
    strip = Image.new("RGBA", (SPRITE_SIZE * num_frames, SPRITE_SIZE), TRANS)
    
    draw_functions = {
        "down": draw_goblin_down,
        "up": draw_goblin_up,
        "left": draw_goblin_left,
        "right": draw_goblin_right
    }
    
    draw_func = draw_functions[direction]
    
    for frame in range(num_frames):
        draw_func(strip, frame * SPRITE_SIZE, 0, frame, anim_type)
    
    return strip

def generate_goblin_sprites():
    """Generate all goblin sprite animations and save them"""
    output_dir = Path("assets/sprites/characters/goblin")
    
    directions = ["down", "up", "left", "right"]
    animations = {
        "idle": 4,
        "walk": 4,
        "attack": 4
    }
    
    # Create directories
    for anim in animations:
        (output_dir / anim).mkdir(parents=True, exist_ok=True)
    
    # Generate sprites
    for anim_type, num_frames in animations.items():
        for direction in directions:
            # Create animation strip
            strip = create_animation_strip(direction, anim_type, num_frames)
            
            # Save strip
            strip_path = output_dir / anim_type / f"goblin_{anim_type}_{direction}_strip.png"
            strip.save(strip_path)
            print(f"Created {strip_path}")
            
            # Also save individual frames
            for frame in range(num_frames):
                frame_img = Image.new("RGBA", (SPRITE_SIZE, SPRITE_SIZE), TRANS)
                frame_img.paste(strip.crop((frame * SPRITE_SIZE, 0, 
                                           (frame + 1) * SPRITE_SIZE, SPRITE_SIZE)), 
                               (0, 0))
                
                frame_path = output_dir / anim_type / f"goblin_{anim_type}_{direction}_{frame}.png"
                frame_img.save(frame_path)
    
    # Create sprite sheet (all animations in one image)
    sheet_width = 12 * SPRITE_SIZE  # 3 animations x 4 frames
    sheet_height = 4 * SPRITE_SIZE  # 4 directions
    sheet = Image.new("RGBA", (sheet_width, sheet_height), TRANS)
    
    for dir_idx, direction in enumerate(directions):
        for anim_idx, (anim_type, num_frames) in enumerate(animations.items()):
            strip = create_animation_strip(direction, anim_type, num_frames)
            sheet.paste(strip, (anim_idx * 4 * SPRITE_SIZE, dir_idx * SPRITE_SIZE))
    
    sheet.save(output_dir / "goblin_spritesheet.png")
    print(f"Created complete sprite sheet: {output_dir}/goblin_spritesheet.png")
    
    # Create config file
    config = {
        "image": "goblin_spritesheet.png",
        "frame_size": [32, 32],
        "animations": {}
    }
    
    for dir_idx, direction in enumerate(directions):
        for anim_idx, (anim_type, num_frames) in enumerate(animations.items()):
            anim_name = f"{anim_type}_{direction}"
            start_frame = anim_idx * 4
            config["animations"][anim_name] = {
                "frames": list(range(start_frame, start_frame + num_frames)),
                "row": dir_idx,
                "frame_duration": 0.2 if anim_type == "idle" else 0.18 if anim_type == "walk" else 0.12,
                "mode": "once" if anim_type == "attack" else "loop"
            }
    
    config_path = output_dir / "goblin_config.json"
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"Created animation config: {config_path}")

if __name__ == "__main__":
    generate_goblin_sprites()
    print("\nAll goblin sprites generated successfully!")