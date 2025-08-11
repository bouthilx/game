#!/usr/bin/env python3
"""
Generate complete sprite sets for player character.
Creates idle, walk, and attack animations for all 4 directions.
Based on the pixel art style from scripts/gen_sprites.py
"""

from PIL import Image
import os
import json
from pathlib import Path

# Sprite dimensions
SPRITE_SIZE = 32
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
TRANS = (0, 0, 0, 0)        # transparent

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

# === CHARACTER DRAWING FUNCTIONS ===

def draw_char_down(img, ox, oy, frame=0, anim_type="idle"):
    """Draw character facing down (toward viewer)"""
    # Animation offsets
    bob = 0
    arm_swing = 0
    
    if anim_type == "walk":
        # Bobbing motion
        bob = [0, 1, 0, -1][frame % 4]
        # Arm swing
        arm_swing = [-1, 0, 1, 0][frame % 4]
    elif anim_type == "attack":
        # Attack pose progression
        if frame == 0:  # Wind up
            oy -= 2
        elif frame == 1:  # Strike
            oy += 1
        elif frame == 2:  # Follow through
            oy += 2
    
    # Apply bobbing
    oy += bob
    
    # Hair
    fill_rect(img, ox+10, oy+4, 12, 6, HAIR)
    fill_rect(img, ox+10, oy+9, 12, 2, HAIR2)
    stroke_rect(img, ox+9, oy+3, 14, 8)
    
    # Face
    fill_rect(img, ox+11, oy+10, 10, 6, SKIN)
    stroke_rect(img, ox+11, oy+10, 10, 6)
    
    # Eyes
    dot(img, ox+14, oy+12)
    dot(img, ox+18, oy+12)
    
    # Tunic
    fill_rect(img, ox+9, oy+17, 14, 8, TUNI)
    fill_rect(img, ox+9, oy+21, 14, 4, TUNI2)
    stroke_rect(img, ox+9, oy+17, 14, 8)
    
    # Belt
    fill_rect(img, ox+9, oy+21, 14, 2, BELT)
    stroke_rect(img, ox+9, oy+21, 14, 2)
    fill_rect(img, ox+15, oy+21, 2, 2, BUCK)
    
    # Arms with animation
    if anim_type == "attack":
        # Both arms forward for attack
        fill_rect(img, ox+8, oy+16, 3, 6, SKIN)
        stroke_rect(img, ox+8, oy+16, 3, 6)
        fill_rect(img, ox+21, oy+16, 3, 6, SKIN)
        stroke_rect(img, ox+21, oy+16, 3, 6)
    else:
        # Normal arms with swing
        fill_rect(img, ox+7, oy+18+arm_swing, 2, 5, TUNI2)
        stroke_rect(img, ox+7, oy+18+arm_swing, 2, 5)
        fill_rect(img, ox+23, oy+18-arm_swing, 2, 5, TUNI2)
        stroke_rect(img, ox+23, oy+18-arm_swing, 2, 5)
    
    # Legs/boots with walking animation
    if anim_type == "walk":
        # Alternate leg positions
        if frame % 2 == 0:
            fill_rect(img, ox+12, oy+25, 3, 3, BOOT)
            stroke_rect(img, ox+12, oy+25, 3, 3)
            fill_rect(img, ox+17, oy+26, 3, 2, BOOT)
            stroke_rect(img, ox+17, oy+26, 3, 2)
        else:
            fill_rect(img, ox+12, oy+26, 3, 2, BOOT)
            stroke_rect(img, ox+12, oy+26, 3, 2)
            fill_rect(img, ox+17, oy+25, 3, 3, BOOT)
            stroke_rect(img, ox+17, oy+25, 3, 3)
    else:
        # Static boots
        fill_rect(img, ox+12, oy+25, 3, 3, BOOT)
        stroke_rect(img, ox+12, oy+25, 3, 3)
        fill_rect(img, ox+17, oy+25, 3, 3, BOOT)
        stroke_rect(img, ox+17, oy+25, 3, 3)

def draw_char_up(img, ox, oy, frame=0, anim_type="idle"):
    """Draw character facing up (away from viewer)"""
    bob = 0
    arm_swing = 0
    
    if anim_type == "walk":
        bob = [0, 1, 0, -1][frame % 4]
        arm_swing = [-1, 0, 1, 0][frame % 4]
    elif anim_type == "attack":
        if frame == 0:
            oy -= 2
        elif frame == 1:
            oy += 1
        elif frame == 2:
            oy += 2
    
    oy += bob
    
    # Back hair (larger)
    fill_rect(img, ox+9, oy+4, 14, 7, HAIR)
    fill_rect(img, ox+9, oy+10, 14, 2, HAIR2)
    stroke_rect(img, ox+8, oy+3, 16, 9)
    
    # Tunic back
    fill_rect(img, ox+9, oy+17, 14, 8, TUNI)
    fill_rect(img, ox+9, oy+21, 14, 4, TUNI2)
    stroke_rect(img, ox+9, oy+17, 14, 8)
    
    # Belt
    fill_rect(img, ox+9, oy+21, 14, 2, BELT)
    stroke_rect(img, ox+9, oy+21, 14, 2)
    
    # Arms
    if anim_type == "attack":
        # Arms raised for attack
        fill_rect(img, ox+6, oy+15, 3, 6, SKIN)
        stroke_rect(img, ox+6, oy+15, 3, 6)
        fill_rect(img, ox+23, oy+15, 3, 6, SKIN)
        stroke_rect(img, ox+23, oy+15, 3, 6)
    else:
        fill_rect(img, ox+7, oy+18+arm_swing, 2, 5, TUNI2)
        stroke_rect(img, ox+7, oy+18+arm_swing, 2, 5)
        fill_rect(img, ox+23, oy+18-arm_swing, 2, 5, TUNI2)
        stroke_rect(img, ox+23, oy+18-arm_swing, 2, 5)
    
    # Boots
    if anim_type == "walk":
        if frame % 2 == 0:
            fill_rect(img, ox+12, oy+25, 3, 3, BOOT)
            stroke_rect(img, ox+12, oy+25, 3, 3)
            fill_rect(img, ox+17, oy+26, 3, 2, BOOT)
            stroke_rect(img, ox+17, oy+26, 3, 2)
        else:
            fill_rect(img, ox+12, oy+26, 3, 2, BOOT)
            stroke_rect(img, ox+12, oy+26, 3, 2)
            fill_rect(img, ox+17, oy+25, 3, 3, BOOT)
            stroke_rect(img, ox+17, oy+25, 3, 3)
    else:
        fill_rect(img, ox+12, oy+25, 3, 3, BOOT)
        stroke_rect(img, ox+12, oy+25, 3, 3)
        fill_rect(img, ox+17, oy+25, 3, 3, BOOT)
        stroke_rect(img, ox+17, oy+25, 3, 3)

def draw_char_left(img, ox, oy, frame=0, anim_type="idle"):
    """Draw character facing left"""
    bob = 0
    
    if anim_type == "walk":
        bob = [0, 1, 0, -1][frame % 4]
        # Shift character left/right for walking
        ox += [-1, 0, 1, 0][frame % 4]
    elif anim_type == "attack":
        if frame == 0:
            ox += 2  # Pull back
        elif frame == 1:
            ox -= 3  # Lunge forward
        elif frame == 2:
            ox -= 1  # Settle
    
    oy += bob
    
    # Hair/profile
    fill_rect(img, ox+9, oy+5, 11, 6, HAIR)
    fill_rect(img, ox+9, oy+10, 11, 2, HAIR2)
    stroke_rect(img, ox+8, oy+4, 13, 8)
    
    # Face (front edge)
    fill_rect(img, ox+9, oy+11, 5, 5, SKIN)
    stroke_rect(img, ox+9, oy+11, 5, 5)
    dot(img, ox+11, oy+13)  # eye
    
    # Tunic side
    fill_rect(img, ox+11, oy+17, 10, 8, TUNI)
    fill_rect(img, ox+11, oy+21, 10, 4, TUNI2)
    stroke_rect(img, ox+11, oy+17, 10, 8)
    
    # Belt
    fill_rect(img, ox+11, oy+21, 10, 2, BELT)
    stroke_rect(img, ox+11, oy+21, 10, 2)
    
    # Arm
    if anim_type == "attack":
        # Arm extended left
        fill_rect(img, ox+5, oy+18, 6, 2, SKIN)
        stroke_rect(img, ox+5, oy+18, 6, 2)
    else:
        fill_rect(img, ox+10, oy+18, 2, 5, TUNI2)
        stroke_rect(img, ox+10, oy+18, 2, 5)
    
    # Boots
    if anim_type == "walk":
        # Animate legs
        if frame == 0 or frame == 2:
            fill_rect(img, ox+14, oy+25, 3, 3, BOOT)
            stroke_rect(img, ox+14, oy+25, 3, 3)
            fill_rect(img, ox+18, oy+25, 3, 3, BOOT)
            stroke_rect(img, ox+18, oy+25, 3, 3)
        elif frame == 1:
            fill_rect(img, ox+13, oy+25, 3, 3, BOOT)
            stroke_rect(img, ox+13, oy+25, 3, 3)
            fill_rect(img, ox+19, oy+26, 3, 2, BOOT)
            stroke_rect(img, ox+19, oy+26, 3, 2)
        else:  # frame == 3
            fill_rect(img, ox+15, oy+26, 3, 2, BOOT)
            stroke_rect(img, ox+15, oy+26, 3, 2)
            fill_rect(img, ox+17, oy+25, 3, 3, BOOT)
            stroke_rect(img, ox+17, oy+25, 3, 3)
    else:
        fill_rect(img, ox+14, oy+25, 3, 3, BOOT)
        stroke_rect(img, ox+14, oy+25, 3, 3)
        fill_rect(img, ox+18, oy+25, 3, 3, BOOT)
        stroke_rect(img, ox+18, oy+25, 3, 3)

def draw_char_right(img, ox, oy, frame=0, anim_type="idle"):
    """Draw character facing right"""
    bob = 0
    
    if anim_type == "walk":
        bob = [0, 1, 0, -1][frame % 4]
        ox += [1, 0, -1, 0][frame % 4]
    elif anim_type == "attack":
        if frame == 0:
            ox -= 2
        elif frame == 1:
            ox += 3
        elif frame == 2:
            ox += 1
    
    oy += bob
    
    # Hair/profile (mirror of left)
    fill_rect(img, ox+12, oy+5, 11, 6, HAIR)
    fill_rect(img, ox+12, oy+10, 11, 2, HAIR2)
    stroke_rect(img, ox+11, oy+4, 13, 8)
    
    # Face
    fill_rect(img, ox+18, oy+11, 5, 5, SKIN)
    stroke_rect(img, ox+18, oy+11, 5, 5)
    dot(img, ox+21, oy+13)
    
    # Tunic
    fill_rect(img, ox+11, oy+17, 10, 8, TUNI)
    fill_rect(img, ox+11, oy+21, 10, 4, TUNI2)
    stroke_rect(img, ox+11, oy+17, 10, 8)
    
    # Belt
    fill_rect(img, ox+11, oy+21, 10, 2, BELT)
    stroke_rect(img, ox+11, oy+21, 10, 2)
    
    # Arm
    if anim_type == "attack":
        fill_rect(img, ox+21, oy+18, 6, 2, SKIN)
        stroke_rect(img, ox+21, oy+18, 6, 2)
    else:
        fill_rect(img, ox+21, oy+18, 2, 5, TUNI2)
        stroke_rect(img, ox+21, oy+18, 2, 5)
    
    # Boots
    if anim_type == "walk":
        if frame == 0 or frame == 2:
            fill_rect(img, ox+14, oy+25, 3, 3, BOOT)
            stroke_rect(img, ox+14, oy+25, 3, 3)
            fill_rect(img, ox+18, oy+25, 3, 3, BOOT)
            stroke_rect(img, ox+18, oy+25, 3, 3)
        elif frame == 1:
            fill_rect(img, ox+13, oy+26, 3, 2, BOOT)
            stroke_rect(img, ox+13, oy+26, 3, 2)
            fill_rect(img, ox+19, oy+25, 3, 3, BOOT)
            stroke_rect(img, ox+19, oy+25, 3, 3)
        else:
            fill_rect(img, ox+15, oy+25, 3, 3, BOOT)
            stroke_rect(img, ox+15, oy+25, 3, 3)
            fill_rect(img, ox+17, oy+26, 3, 2, BOOT)
            stroke_rect(img, ox+17, oy+26, 3, 2)
    else:
        fill_rect(img, ox+14, oy+25, 3, 3, BOOT)
        stroke_rect(img, ox+14, oy+25, 3, 3)
        fill_rect(img, ox+18, oy+25, 3, 3, BOOT)
        stroke_rect(img, ox+18, oy+25, 3, 3)

# === SPRITE GENERATION ===

def create_animation_strip(direction, anim_type, num_frames=4):
    """Create a horizontal strip of animation frames"""
    strip = Image.new("RGBA", (SPRITE_SIZE * num_frames, SPRITE_SIZE), TRANS)
    
    draw_functions = {
        "down": draw_char_down,
        "up": draw_char_up,
        "left": draw_char_left,
        "right": draw_char_right
    }
    
    draw_func = draw_functions[direction]
    
    for frame in range(num_frames):
        draw_func(strip, frame * SPRITE_SIZE, 0, frame, anim_type)
    
    return strip

def generate_all_sprites():
    """Generate all sprite animations and save them"""
    output_dir = Path("assets/sprites/characters/player")
    
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
            strip_path = output_dir / anim_type / f"player_{anim_type}_{direction}_strip.png"
            strip.save(strip_path)
            print(f"Created {strip_path}")
            
            # Also save individual frames
            for frame in range(num_frames):
                frame_img = Image.new("RGBA", (SPRITE_SIZE, SPRITE_SIZE), TRANS)
                frame_img.paste(strip.crop((frame * SPRITE_SIZE, 0, 
                                           (frame + 1) * SPRITE_SIZE, SPRITE_SIZE)), 
                               (0, 0))
                
                frame_path = output_dir / anim_type / f"player_{anim_type}_{direction}_{frame}.png"
                frame_img.save(frame_path)
    
    # Create sprite sheet (all animations in one image)
    sheet_width = 12 * SPRITE_SIZE  # 3 animations x 4 frames
    sheet_height = 4 * SPRITE_SIZE  # 4 directions
    sheet = Image.new("RGBA", (sheet_width, sheet_height), TRANS)
    
    for dir_idx, direction in enumerate(directions):
        for anim_idx, (anim_type, num_frames) in enumerate(animations.items()):
            strip = create_animation_strip(direction, anim_type, num_frames)
            sheet.paste(strip, (anim_idx * 4 * SPRITE_SIZE, dir_idx * SPRITE_SIZE))
    
    sheet.save(output_dir / "player_spritesheet.png")
    print(f"Created complete sprite sheet: {output_dir}/player_spritesheet.png")
    
    # Create config file
    config = {
        "image": "player_spritesheet.png",
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
                "frame_duration": 0.15 if anim_type == "walk" else 0.1 if anim_type == "attack" else 0.2,
                "mode": "once" if anim_type == "attack" else "loop"
            }
    
    config_path = output_dir / "player_config.json"
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"Created animation config: {config_path}")

if __name__ == "__main__":
    generate_all_sprites()
    print("\nAll sprites generated successfully!")