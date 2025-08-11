#!/usr/bin/env python3
"""
Generate ogre sprites for the game.
Creates idle, walk, attack, and death animations for large ogres (64x64).
Ogres are bigger, stronger, and more intimidating than goblins.
"""

from PIL import Image
import os
import json
from pathlib import Path

# Sprite dimensions - Ogres are 2x size of goblins
SPRITE_SIZE = 64

# Ogre color palette - darker, more intimidating than goblins
OUT    = (30, 20, 15, 255)       # Very dark outline
SKIN   = (80, 100, 60, 255)      # Dark olive green skin
SKIN2  = (60, 75, 45, 255)       # Darker green for shadows
SKIN3  = (100, 120, 80, 255)     # Lighter green for highlights
CLOTH  = (60, 40, 25, 255)       # Dark brown leather/hide
CLOTH2 = (45, 30, 18, 255)       # Darker brown
EYES   = (255, 80, 80, 255)      # Bright red glowing eyes
EYES_DIM = (180, 50, 50, 255)    # Dimmed red eyes for death
TEETH  = (255, 255, 220, 255)    # Yellowish teeth/tusks
WEAPON = (120, 120, 120, 255)    # Steel weapon/club
SCARS  = (40, 60, 30, 255)       # Dark scars
TRANS  = (0, 0, 0, 0)            # transparent

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

def line(img, x1, y1, x2, y2, c=OUT):
    """Draw a simple line (for scars and details)"""
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    x, y = x1, y1
    sx = -1 if x1 > x2 else 1
    sy = -1 if y1 > y2 else 1
    
    if dx > dy:
        err = dx / 2.0
        while x != x2:
            dot(img, x, y, c)
            err -= dy
            if err < 0:
                y += sy
                err += dx
            x += sx
    else:
        err = dy / 2.0
        while y != y2:
            dot(img, x, y, c)
            err -= dx
            if err < 0:
                x += sx
                err += dy
            y += sy
    dot(img, x, y, c)

def draw_ogre_idle(img, ox, oy, direction, frame):
    """Draw ogre idle animation"""
    
    # Breathing animation - slight size variation
    breath = [0, 1, 2, 1][frame % 4]
    
    if direction == "down":
        # Large head
        head_y = oy + 6 - breath//2
        fill_rect(img, ox+18, head_y, 28, 22, SKIN)
        fill_rect(img, ox+18, head_y+16, 28, 6, SKIN2)
        stroke_rect(img, ox+18, head_y, 28, 22)
        
        # Large ears
        fill_rect(img, ox+14, head_y+6, 6, 12, SKIN)
        stroke_rect(img, ox+14, head_y+6, 6, 12)
        fill_rect(img, ox+44, head_y+6, 6, 12, SKIN)
        stroke_rect(img, ox+44, head_y+6, 6, 12)
        
        # Glowing red eyes
        fill_rect(img, ox+24, head_y+8, 4, 3, EYES)
        fill_rect(img, ox+36, head_y+8, 4, 3, EYES)
        
        # Large nose/snout
        fill_rect(img, ox+29, head_y+12, 6, 4, SKIN3)
        stroke_rect(img, ox+29, head_y+12, 6, 4)
        
        # Tusks/teeth
        fill_rect(img, ox+26, head_y+15, 3, 4, TEETH)
        fill_rect(img, ox+35, head_y+15, 3, 4, TEETH)
        
        # Battle scars on face
        line(img, ox+22, head_y+5, ox+25, head_y+10, SCARS)
        line(img, ox+40, head_y+7, ox+43, head_y+12, SCARS)
        
        # Massive body
        body_y = oy + 30
        fill_rect(img, ox+16, body_y, 32, 18 + breath, CLOTH)
        fill_rect(img, ox+16, body_y+12, 32, 6 + breath, CLOTH2)
        stroke_rect(img, ox+16, body_y, 32, 18 + breath)
        
        # Muscular arms
        fill_rect(img, ox+8, body_y+2, 8, 12, SKIN)
        stroke_rect(img, ox+8, body_y+2, 8, 12)
        fill_rect(img, ox+48, body_y+2, 8, 12, SKIN)
        stroke_rect(img, ox+48, body_y+2, 8, 12)
        
        # Large hands/claws
        fill_rect(img, ox+6, body_y+14, 6, 8, SKIN)
        stroke_rect(img, ox+6, body_y+14, 6, 8)
        fill_rect(img, ox+52, body_y+14, 6, 8, SKIN)
        stroke_rect(img, ox+52, body_y+14, 6, 8)
        
        # Claws
        dot(img, ox+5, body_y+16, OUT)
        dot(img, ox+6, body_y+15, OUT)
        dot(img, ox+58, body_y+16, OUT)
        dot(img, ox+57, body_y+15, OUT)
        
        # Thick legs
        fill_rect(img, ox+20, oy+50, 8, 12, SKIN)
        stroke_rect(img, ox+20, oy+50, 8, 12)
        fill_rect(img, ox+36, oy+50, 8, 12, SKIN)
        stroke_rect(img, ox+36, oy+50, 8, 12)
        
        # Large feet
        fill_rect(img, ox+18, oy+62, 10, 2, SKIN2)
        fill_rect(img, ox+36, oy+62, 10, 2, SKIN2)
    
    elif direction == "up":
        # Back view - similar structure but showing back of head
        head_y = oy + 6 - breath//2
        fill_rect(img, ox+18, head_y, 28, 22, SKIN)
        fill_rect(img, ox+18, head_y+16, 28, 6, SKIN2)
        stroke_rect(img, ox+18, head_y, 28, 22)
        
        # Back of ears
        fill_rect(img, ox+14, head_y+6, 6, 12, SKIN2)
        stroke_rect(img, ox+14, head_y+6, 6, 12)
        fill_rect(img, ox+44, head_y+6, 6, 12, SKIN2)
        stroke_rect(img, ox+44, head_y+6, 6, 12)
        
        # No visible eyes (back view), maybe show hair/scalp details
        fill_rect(img, ox+28, head_y+4, 8, 4, SKIN2)
        
        # Body (back view)
        body_y = oy + 30
        fill_rect(img, ox+16, body_y, 32, 18 + breath, CLOTH2)  # Darker back
        stroke_rect(img, ox+16, body_y, 32, 18 + breath)
        
        # Arms (back view)
        fill_rect(img, ox+8, body_y+2, 8, 12, SKIN)
        stroke_rect(img, ox+8, body_y+2, 8, 12)
        fill_rect(img, ox+48, body_y+2, 8, 12, SKIN)
        stroke_rect(img, ox+48, body_y+2, 8, 12)
        
        # Hands (back view)
        fill_rect(img, ox+6, body_y+14, 6, 8, SKIN)
        stroke_rect(img, ox+6, body_y+14, 6, 8)
        fill_rect(img, ox+52, body_y+14, 6, 8, SKIN)
        stroke_rect(img, ox+52, body_y+14, 6, 8)
        
        # Legs (back view)
        fill_rect(img, ox+20, oy+50, 8, 12, SKIN)
        stroke_rect(img, ox+20, oy+50, 8, 12)
        fill_rect(img, ox+36, oy+50, 8, 12, SKIN)
        stroke_rect(img, ox+36, oy+50, 8, 12)
        
        # Feet (back view)
        fill_rect(img, ox+18, oy+62, 10, 2, SKIN2)
        fill_rect(img, ox+36, oy+62, 10, 2, SKIN2)
    
    elif direction == "left":
        # Side view facing left
        head_y = oy + 6 - breath//2
        fill_rect(img, ox+20, head_y, 24, 22, SKIN)
        fill_rect(img, ox+20, head_y+16, 24, 6, SKIN2)
        stroke_rect(img, ox+20, head_y, 24, 22)
        
        # Left ear visible
        fill_rect(img, ox+16, head_y+6, 6, 12, SKIN)
        stroke_rect(img, ox+16, head_y+6, 6, 12)
        
        # Left eye visible
        fill_rect(img, ox+26, head_y+8, 4, 3, EYES)
        
        # Profile nose
        fill_rect(img, ox+18, head_y+12, 4, 6, SKIN3)
        stroke_rect(img, ox+18, head_y+12, 4, 6)
        
        # Tusk visible from side
        fill_rect(img, ox+17, head_y+15, 3, 4, TEETH)
        
        # Scar on visible side
        line(img, ox+24, head_y+5, ox+27, head_y+10, SCARS)
        
        # Body (side view)
        body_y = oy + 30
        fill_rect(img, ox+18, body_y, 28, 18 + breath, CLOTH)
        stroke_rect(img, ox+18, body_y, 28, 18 + breath)
        
        # Left arm visible
        fill_rect(img, ox+10, body_y+2, 8, 12, SKIN)
        stroke_rect(img, ox+10, body_y+2, 8, 12)
        
        # Left hand
        fill_rect(img, ox+8, body_y+14, 6, 8, SKIN)
        stroke_rect(img, ox+8, body_y+14, 6, 8)
        
        # Legs (side view)
        fill_rect(img, ox+22, oy+50, 8, 12, SKIN)
        stroke_rect(img, ox+22, oy+50, 8, 12)
        fill_rect(img, ox+34, oy+50, 8, 12, SKIN)
        stroke_rect(img, ox+34, oy+50, 8, 12)
        
        # Feet (side view)
        fill_rect(img, ox+20, oy+62, 10, 2, SKIN2)
        fill_rect(img, ox+36, oy+62, 8, 2, SKIN2)
    
    elif direction == "right":
        # Side view facing right (mirror of left)
        head_y = oy + 6 - breath//2
        fill_rect(img, ox+20, head_y, 24, 22, SKIN)
        fill_rect(img, ox+20, head_y+16, 24, 6, SKIN2)
        stroke_rect(img, ox+20, head_y, 24, 22)
        
        # Right ear visible
        fill_rect(img, ox+42, head_y+6, 6, 12, SKIN)
        stroke_rect(img, ox+42, head_y+6, 6, 12)
        
        # Right eye visible
        fill_rect(img, ox+34, head_y+8, 4, 3, EYES)
        
        # Profile nose
        fill_rect(img, ox+42, head_y+12, 4, 6, SKIN3)
        stroke_rect(img, ox+42, head_y+12, 4, 6)
        
        # Tusk visible from side
        fill_rect(img, ox+44, head_y+15, 3, 4, TEETH)
        
        # Scar on visible side
        line(img, ox+37, head_y+5, ox+40, head_y+10, SCARS)
        
        # Body (side view)
        body_y = oy + 30
        fill_rect(img, ox+18, body_y, 28, 18 + breath, CLOTH)
        stroke_rect(img, ox+18, body_y, 28, 18 + breath)
        
        # Right arm visible
        fill_rect(img, ox+46, body_y+2, 8, 12, SKIN)
        stroke_rect(img, ox+46, body_y+2, 8, 12)
        
        # Right hand
        fill_rect(img, ox+50, body_y+14, 6, 8, SKIN)
        stroke_rect(img, ox+50, body_y+14, 6, 8)
        
        # Legs (side view)
        fill_rect(img, ox+22, oy+50, 8, 12, SKIN)
        stroke_rect(img, ox+22, oy+50, 8, 12)
        fill_rect(img, ox+34, oy+50, 8, 12, SKIN)
        stroke_rect(img, ox+34, oy+50, 8, 12)
        
        # Feet (side view)
        fill_rect(img, ox+18, oy+62, 8, 2, SKIN2)
        fill_rect(img, ox+38, oy+62, 10, 2, SKIN2)

def draw_ogre_walk(img, ox, oy, direction, frame):
    """Draw ogre walk animation"""
    
    # Walking bob and sway
    bob = [0, -2, 0, 2][frame % 4]
    sway = [-1, 0, 1, 0][frame % 4]
    
    if direction == "down":
        # Head with walking motion
        head_y = oy + 6 + bob
        fill_rect(img, ox+18+sway, head_y, 28, 22, SKIN)
        fill_rect(img, ox+18+sway, head_y+16, 28, 6, SKIN2)
        stroke_rect(img, ox+18+sway, head_y, 28, 22)
        
        # Ears
        fill_rect(img, ox+14+sway, head_y+6, 6, 12, SKIN)
        stroke_rect(img, ox+14+sway, head_y+6, 6, 12)
        fill_rect(img, ox+44+sway, head_y+6, 6, 12, SKIN)
        stroke_rect(img, ox+44+sway, head_y+6, 6, 12)
        
        # Eyes
        fill_rect(img, ox+24+sway, head_y+8, 4, 3, EYES)
        fill_rect(img, ox+36+sway, head_y+8, 4, 3, EYES)
        
        # Nose
        fill_rect(img, ox+29+sway, head_y+12, 6, 4, SKIN3)
        stroke_rect(img, ox+29+sway, head_y+12, 6, 4)
        
        # Tusks
        fill_rect(img, ox+26+sway, head_y+15, 3, 4, TEETH)
        fill_rect(img, ox+35+sway, head_y+15, 3, 4, TEETH)
        
        # Scars
        line(img, ox+22+sway, head_y+5, ox+25+sway, head_y+10, SCARS)
        line(img, ox+40+sway, head_y+7, ox+43+sway, head_y+12, SCARS)
        
        # Body swaying
        body_y = oy + 30 + bob//2
        fill_rect(img, ox+16+sway, body_y, 32, 18, CLOTH)
        fill_rect(img, ox+16+sway, body_y+12, 32, 6, CLOTH2)
        stroke_rect(img, ox+16+sway, body_y, 32, 18)
        
        # Arms swinging
        arm_swing = [-2, 0, 2, 0][frame % 4]
        fill_rect(img, ox+8+arm_swing, body_y+2, 8, 12, SKIN)
        stroke_rect(img, ox+8+arm_swing, body_y+2, 8, 12)
        fill_rect(img, ox+48-arm_swing, body_y+2, 8, 12, SKIN)
        stroke_rect(img, ox+48-arm_swing, body_y+2, 8, 12)
        
        # Hands
        fill_rect(img, ox+6+arm_swing, body_y+14, 6, 8, SKIN)
        stroke_rect(img, ox+6+arm_swing, body_y+14, 6, 8)
        fill_rect(img, ox+52-arm_swing, body_y+14, 6, 8, SKIN)
        stroke_rect(img, ox+52-arm_swing, body_y+14, 6, 8)
        
        # Legs walking (alternating)
        leg_lift = [0, 2, 0, -2][frame % 4]
        fill_rect(img, ox+20, oy+50+leg_lift, 8, 12-abs(leg_lift), SKIN)
        stroke_rect(img, ox+20, oy+50+leg_lift, 8, 12-abs(leg_lift))
        fill_rect(img, ox+36, oy+50-leg_lift, 8, 12-abs(leg_lift), SKIN)
        stroke_rect(img, ox+36, oy+50-leg_lift, 8, 12-abs(leg_lift))
        
        # Feet
        if leg_lift >= 0:
            fill_rect(img, ox+18, oy+62, 10, 2, SKIN2)
        if leg_lift <= 0:
            fill_rect(img, ox+36, oy+62, 10, 2, SKIN2)
    
    else:  # up, left, right directions
        # For simplicity, use similar walking logic for all directions
        # Adjust based on direction-specific features from idle
        if direction == "up":
            # Back view walking
            head_y = oy + 6 + bob
            fill_rect(img, ox+18+sway, head_y, 28, 22, SKIN)
            stroke_rect(img, ox+18+sway, head_y, 28, 22)
            fill_rect(img, ox+28, head_y+4, 8, 4, SKIN2)  # Back of head
            
        elif direction == "left":
            # Left side view walking
            head_y = oy + 6 + bob
            fill_rect(img, ox+20+sway, head_y, 24, 22, SKIN)
            stroke_rect(img, ox+20+sway, head_y, 24, 22)
            fill_rect(img, ox+16, head_y+6, 6, 12, SKIN)  # Left ear
            stroke_rect(img, ox+16, head_y+6, 6, 12)
            fill_rect(img, ox+26, head_y+8, 4, 3, EYES)  # Left eye
            
        elif direction == "right":
            # Right side view walking
            head_y = oy + 6 + bob
            fill_rect(img, ox+20+sway, head_y, 24, 22, SKIN)
            stroke_rect(img, ox+20+sway, head_y, 24, 22)
            fill_rect(img, ox+42, head_y+6, 6, 12, SKIN)  # Right ear
            stroke_rect(img, ox+42, head_y+6, 6, 12)
            fill_rect(img, ox+34, head_y+8, 4, 3, EYES)  # Right eye
        
        # Body for all other directions
        body_y = oy + 30 + bob//2
        fill_rect(img, ox+16+sway, body_y, 32, 18, CLOTH)
        stroke_rect(img, ox+16+sway, body_y, 32, 18)
        
        # Arms swinging for all directions
        arm_swing = [-2, 0, 2, 0][frame % 4]
        fill_rect(img, ox+8+arm_swing, body_y+2, 8, 12, SKIN)
        stroke_rect(img, ox+8+arm_swing, body_y+2, 8, 12)
        fill_rect(img, ox+48-arm_swing, body_y+2, 8, 12, SKIN)
        stroke_rect(img, ox+48-arm_swing, body_y+2, 8, 12)
        
        # Legs walking
        leg_lift = [0, 2, 0, -2][frame % 4]
        fill_rect(img, ox+20, oy+50+leg_lift, 8, 12-abs(leg_lift), SKIN)
        stroke_rect(img, ox+20, oy+50+leg_lift, 8, 12-abs(leg_lift))
        fill_rect(img, ox+36, oy+50-leg_lift, 8, 12-abs(leg_lift), SKIN)
        stroke_rect(img, ox+36, oy+50-leg_lift, 8, 12-abs(leg_lift))

def draw_ogre_attack(img, ox, oy, direction, frame):
    """Draw ogre attack animation"""
    
    if direction == "down":
        # Attack windup and strike
        if frame <= 1:  # Windup
            attack_offset = frame * 2
            
            # Head leaning back for windup
            head_y = oy + 6 - attack_offset
            fill_rect(img, ox+18, head_y, 28, 22, SKIN)
            fill_rect(img, ox+18, head_y+16, 28, 6, SKIN2)
            stroke_rect(img, ox+18, head_y, 28, 22)
            
            # Ears
            fill_rect(img, ox+14, head_y+6, 6, 12, SKIN)
            stroke_rect(img, ox+14, head_y+6, 6, 12)
            fill_rect(img, ox+44, head_y+6, 6, 12, SKIN)
            stroke_rect(img, ox+44, head_y+6, 6, 12)
            
            # Angry glowing eyes
            fill_rect(img, ox+24, head_y+8, 4, 3, EYES)
            fill_rect(img, ox+36, head_y+8, 4, 3, EYES)
            # Extra glow
            dot(img, ox+23, head_y+8, EYES)
            dot(img, ox+27, head_y+8, EYES)
            dot(img, ox+35, head_y+8, EYES)
            dot(img, ox+39, head_y+8, EYES)
            
            # Nose flaring
            fill_rect(img, ox+29, head_y+12, 6, 4, SKIN3)
            stroke_rect(img, ox+29, head_y+12, 6, 4)
            
            # Tusks prominent
            fill_rect(img, ox+26, head_y+15, 3, 5, TEETH)
            fill_rect(img, ox+35, head_y+15, 3, 5, TEETH)
            
            # Body
            body_y = oy + 30
            fill_rect(img, ox+16, body_y, 32, 18, CLOTH)
            fill_rect(img, ox+16, body_y+12, 32, 6, CLOTH2)
            stroke_rect(img, ox+16, body_y, 32, 18)
            
            # Arms raised for attack
            fill_rect(img, ox+8-attack_offset*2, body_y-attack_offset*3, 8, 12+attack_offset, SKIN)
            stroke_rect(img, ox+8-attack_offset*2, body_y-attack_offset*3, 8, 12+attack_offset)
            fill_rect(img, ox+48+attack_offset*2, body_y-attack_offset*3, 8, 12+attack_offset, SKIN)
            stroke_rect(img, ox+48+attack_offset*2, body_y-attack_offset*3, 8, 12+attack_offset)
            
            # Raised fists/claws
            fill_rect(img, ox+6-attack_offset*2, body_y-attack_offset*3+12, 6, 8, SKIN)
            stroke_rect(img, ox+6-attack_offset*2, body_y-attack_offset*3+12, 6, 8)
            fill_rect(img, ox+52+attack_offset*2, body_y-attack_offset*3+12, 6, 8, SKIN)
            stroke_rect(img, ox+52+attack_offset*2, body_y-attack_offset*3+12, 6, 8)
            
        else:  # Strike (frames 2-3)
            strike_offset = (frame - 1) * 3
            
            # Head lunging forward
            head_y = oy + 6 + strike_offset
            fill_rect(img, ox+18, head_y, 28, 22, SKIN)
            fill_rect(img, ox+18, head_y+16, 28, 6, SKIN2)
            stroke_rect(img, ox+18, head_y, 28, 22)
            
            # Ears
            fill_rect(img, ox+14, head_y+6, 6, 12, SKIN)
            stroke_rect(img, ox+14, head_y+6, 6, 12)
            fill_rect(img, ox+44, head_y+6, 6, 12, SKIN)
            stroke_rect(img, ox+44, head_y+6, 6, 12)
            
            # Furious eyes
            fill_rect(img, ox+24, head_y+8, 4, 3, EYES)
            fill_rect(img, ox+36, head_y+8, 4, 3, EYES)
            
            # Body lunging
            body_y = oy + 30 + strike_offset//2
            fill_rect(img, ox+16, body_y, 32, 18, CLOTH)
            stroke_rect(img, ox+16, body_y, 32, 18)
            
            # Arms striking down
            fill_rect(img, ox+8+strike_offset, body_y+strike_offset, 8, 12, SKIN)
            stroke_rect(img, ox+8+strike_offset, body_y+strike_offset, 8, 12)
            fill_rect(img, ox+48-strike_offset, body_y+strike_offset, 8, 12, SKIN)
            stroke_rect(img, ox+48-strike_offset, body_y+strike_offset, 8, 12)
            
            # Striking fists
            fill_rect(img, ox+6+strike_offset, body_y+14+strike_offset, 6, 8, SKIN)
            stroke_rect(img, ox+6+strike_offset, body_y+14+strike_offset, 6, 8)
            fill_rect(img, ox+52-strike_offset, body_y+14+strike_offset, 6, 8, SKIN)
            stroke_rect(img, ox+52-strike_offset, body_y+14+strike_offset, 6, 8)
            
            # Impact lines for frame 3
            if frame == 3:
                line(img, ox+12, body_y+22, ox+16, body_y+26, OUT)
                line(img, ox+48, body_y+22, ox+52, body_y+26, OUT)
        
        # Legs stable during attack
        fill_rect(img, ox+20, oy+50, 8, 12, SKIN)
        stroke_rect(img, ox+20, oy+50, 8, 12)
        fill_rect(img, ox+36, oy+50, 8, 12, SKIN)
        stroke_rect(img, ox+36, oy+50, 8, 12)
    
    else:  # up, left, right directions - simplified attack
        # For other directions, use a simplified but functional attack animation
        attack_offset = 2 if frame <= 1 else (frame - 1) * 3
        
        if direction == "up":
            head_y = oy + 6 + (attack_offset if frame > 1 else -attack_offset)
            fill_rect(img, ox+18, head_y, 28, 22, SKIN)
            stroke_rect(img, ox+18, head_y, 28, 22)
            fill_rect(img, ox+28, head_y+4, 8, 4, SKIN2)
        elif direction in ["left", "right"]:
            head_y = oy + 6 + (attack_offset if frame > 1 else -attack_offset)
            fill_rect(img, ox+20, head_y, 24, 22, SKIN)
            stroke_rect(img, ox+20, head_y, 24, 22)
            if direction == "left":
                fill_rect(img, ox+26, head_y+8, 4, 3, EYES)
            else:
                fill_rect(img, ox+34, head_y+8, 4, 3, EYES)
        
        # Body
        body_y = oy + 30 + (attack_offset//2 if frame > 1 else 0)
        fill_rect(img, ox+16, body_y, 32, 18, CLOTH)
        stroke_rect(img, ox+16, body_y, 32, 18)
        
        # Arms attacking
        arm_offset = attack_offset if frame > 1 else -attack_offset*2
        fill_rect(img, ox+8+arm_offset, body_y+arm_offset, 8, 12, SKIN)
        stroke_rect(img, ox+8+arm_offset, body_y+arm_offset, 8, 12)
        fill_rect(img, ox+48-arm_offset, body_y+arm_offset, 8, 12, SKIN)
        stroke_rect(img, ox+48-arm_offset, body_y+arm_offset, 8, 12)
        
        # Legs
        fill_rect(img, ox+20, oy+50, 8, 12, SKIN)
        stroke_rect(img, ox+20, oy+50, 8, 12)
        fill_rect(img, ox+36, oy+50, 8, 12, SKIN)
        stroke_rect(img, ox+36, oy+50, 8, 12)

def draw_ogre_death(img, ox, oy, direction, frame):
    """Draw ogre forward-falling death animation"""
    
    if direction == "down":
        if frame == 0:
            # Starting to stumble
            head_y = oy + 6
            fill_rect(img, ox+20, head_y, 24, 20, SKIN)
            stroke_rect(img, ox+20, head_y, 24, 20)
            
            # Dimming eyes
            fill_rect(img, ox+26, head_y+6, 3, 2, EYES_DIM)
            fill_rect(img, ox+35, head_y+6, 3, 2, EYES_DIM)
            
            # Body
            body_y = oy + 28
            fill_rect(img, ox+18, body_y, 28, 16, CLOTH)
            stroke_rect(img, ox+18, body_y, 28, 16)
            
            # Arms spread for balance
            fill_rect(img, ox+10, body_y+2, 8, 10, SKIN)
            stroke_rect(img, ox+10, body_y+2, 8, 10)
            fill_rect(img, ox+46, body_y+2, 8, 10, SKIN)
            stroke_rect(img, ox+46, body_y+2, 8, 10)
            
        elif frame == 1:
            # Falling forward
            head_y = oy + 8
            fill_rect(img, ox+18, head_y, 28, 16, SKIN)
            stroke_rect(img, ox+18, head_y, 28, 16)
            
            # Very dim eyes
            dot(img, ox+26, head_y+4, EYES_DIM)
            dot(img, ox+37, head_y+4, EYES_DIM)
            
            # Body
            body_y = oy + 26
            fill_rect(img, ox+16, body_y, 32, 14, CLOTH)
            stroke_rect(img, ox+16, body_y, 32, 14)
            
            # Arms spreading wide
            fill_rect(img, ox+6, body_y, 10, 8, SKIN)
            stroke_rect(img, ox+6, body_y, 10, 8)
            fill_rect(img, ox+48, body_y, 10, 8, SKIN)
            stroke_rect(img, ox+48, body_y, 10, 8)
            
        elif frame == 2:
            # Almost down
            head_y = oy + 12
            fill_rect(img, ox+16, head_y, 32, 12, SKIN)
            stroke_rect(img, ox+16, head_y, 32, 12)
            
            # Body
            body_y = oy + 26
            fill_rect(img, ox+14, body_y, 36, 10, CLOTH)
            stroke_rect(img, ox+14, body_y, 36, 10)
            
            # Arms flat
            fill_rect(img, ox+4, body_y+2, 12, 4, SKIN)
            stroke_rect(img, ox+4, body_y+2, 12, 4)
            fill_rect(img, ox+48, body_y+2, 12, 4, SKIN)
            stroke_rect(img, ox+48, body_y+2, 12, 4)
            
        else:  # frame == 3 - Final corpse position
            # Completely flat, face-down
            head_y = oy + 16
            fill_rect(img, ox+12, head_y, 40, 8, SKIN)
            stroke_rect(img, ox+12, head_y, 40, 8)
            
            # No visible eyes (face down)
            fill_rect(img, ox+28, head_y+2, 8, 2, SKIN2)  # Back of head detail
            
            # Body completely flat
            body_y = oy + 26
            fill_rect(img, ox+10, body_y, 44, 6, CLOTH)
            stroke_rect(img, ox+10, body_y, 44, 6)
            
            # Arms completely spread
            fill_rect(img, ox+2, body_y+1, 16, 2, SKIN)
            stroke_rect(img, ox+2, body_y+1, 16, 2)
            fill_rect(img, ox+46, body_y+1, 16, 2, SKIN)
            stroke_rect(img, ox+46, body_y+1, 16, 2)
            
            # Legs flat
            fill_rect(img, ox+16, oy+54, 12, 4, SKIN)
            stroke_rect(img, ox+16, oy+54, 12, 4)
            fill_rect(img, ox+36, oy+54, 12, 4, SKIN)
            stroke_rect(img, ox+36, oy+54, 12, 4)
    
    else:  # up, left, right directions - simplified death
        # For other directions, use a progressive flattening animation
        if frame <= 2:
            # Progressive collapse
            flatten = frame * 4
            head_y = oy + 6 + flatten
            body_y = oy + 30 + flatten//2
            
            if direction == "up":
                fill_rect(img, ox+18, head_y, 28, 22-flatten, SKIN)
                stroke_rect(img, ox+18, head_y, 28, 22-flatten)
            elif direction in ["left", "right"]:
                fill_rect(img, ox+20, head_y, 24, 22-flatten, SKIN)
                stroke_rect(img, ox+20, head_y, 24, 22-flatten)
                if direction == "left" and frame == 0:
                    dot(img, ox+26, head_y+4, EYES_DIM)
                elif direction == "right" and frame == 0:
                    dot(img, ox+34, head_y+4, EYES_DIM)
            
            # Body collapsing
            fill_rect(img, ox+16, body_y, 32, 18-flatten//2, CLOTH)
            stroke_rect(img, ox+16, body_y, 32, 18-flatten//2)
            
            # Arms spreading
            fill_rect(img, ox+8-flatten, body_y, 8+flatten, 8, SKIN)
            stroke_rect(img, ox+8-flatten, body_y, 8+flatten, 8)
            fill_rect(img, ox+48, body_y, 8+flatten, 8, SKIN)
            stroke_rect(img, ox+48, body_y, 8+flatten, 8)
            
        else:  # Final frame - completely flat
            head_y = oy + 16
            body_y = oy + 26
            
            # Flat head
            fill_rect(img, ox+12, head_y, 40, 8, SKIN)
            stroke_rect(img, ox+12, head_y, 40, 8)
            
            # Flat body  
            fill_rect(img, ox+10, body_y, 44, 6, CLOTH)
            stroke_rect(img, ox+10, body_y, 44, 6)
            
            # Completely spread arms
            fill_rect(img, ox+2, body_y+1, 16, 2, SKIN)
            stroke_rect(img, ox+2, body_y+1, 16, 2)
            fill_rect(img, ox+46, body_y+1, 16, 2, SKIN)
            stroke_rect(img, ox+46, body_y+1, 16, 2)
            
            # Flat legs
            fill_rect(img, ox+16, oy+54, 12, 4, SKIN)
            stroke_rect(img, ox+16, oy+54, 12, 4)
            fill_rect(img, ox+36, oy+54, 12, 4, SKIN)
            stroke_rect(img, ox+36, oy+54, 12, 4)

def draw_ogre(img, ox, oy, direction, frame, anim_type):
    """Main function to draw ogre sprite"""
    
    if anim_type == "idle":
        draw_ogre_idle(img, ox, oy, direction, frame)
    elif anim_type == "walk":
        draw_ogre_walk(img, ox, oy, direction, frame)
    elif anim_type == "attack":
        draw_ogre_attack(img, ox, oy, direction, frame)
    elif anim_type == "death":
        draw_ogre_death(img, ox, oy, direction, frame)

def create_ogre_spritesheet():
    """Create complete ogre sprite sheet with all animations"""
    
    # 4 animation types x 4 frames = 16 columns
    # 4 directions = 4 rows  
    sheet_width = 16 * SPRITE_SIZE
    sheet_height = 4 * SPRITE_SIZE
    
    sheet = Image.new("RGBA", (sheet_width, sheet_height), TRANS)
    
    directions = ["down", "up", "left", "right"]
    animations = ["idle", "walk", "attack", "death"]
    
    for dir_idx, direction in enumerate(directions):
        for anim_idx, anim_type in enumerate(animations):
            for frame in range(4):
                x = (anim_idx * 4 + frame) * SPRITE_SIZE
                y = dir_idx * SPRITE_SIZE
                
                draw_ogre(sheet, x, y, direction, frame, anim_type)
    
    return sheet

def create_ogre_config():
    """Create JSON config file for ogre animations"""
    
    config = {
        "image": "ogre_spritesheet.png",
        "frame_size": [SPRITE_SIZE, SPRITE_SIZE],
        "animations": {}
    }
    
    directions = ["down", "up", "left", "right"]
    animations = ["idle", "walk", "attack", "death"]
    
    for dir_idx, direction in enumerate(directions):
        for anim_idx, anim_type in enumerate(animations):
            anim_name = f"{anim_type}_{direction}"
            
            frame_duration = 0.3 if anim_type == "idle" else \
                           0.2 if anim_type == "walk" else \
                           0.15 if anim_type == "attack" else \
                           0.4  # death
            
            mode = "once" if anim_type in ["attack", "death"] else "loop"
            
            config["animations"][anim_name] = {
                "frames": [anim_idx * 4 + i for i in range(4)],
                "row": dir_idx,
                "frame_duration": frame_duration,
                "mode": mode
            }
    
    return config

def generate_ogre_sprites():
    """Generate all ogre sprites and config"""
    
    # Create output directory
    output_dir = Path("assets/sprites/characters/ogre")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate sprite sheet
    print("Generating ogre sprite sheet...")
    sheet = create_ogre_spritesheet()
    sheet_path = output_dir / "ogre_spritesheet.png"
    sheet.save(sheet_path)
    print(f"Created: {sheet_path}")
    
    # Generate config file
    print("Generating ogre config file...")
    config = create_ogre_config()
    config_path = output_dir / "ogre_config.json"
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    print(f"Created: {config_path}")
    
    # Generate individual animation directories and files
    directions = ["down", "up", "left", "right"]
    animations = ["idle", "walk", "attack", "death"]
    
    for anim_type in animations:
        anim_dir = output_dir / anim_type
        anim_dir.mkdir(exist_ok=True)
        
        for direction in directions:
            # Create animation strip
            strip = Image.new("RGBA", (SPRITE_SIZE * 4, SPRITE_SIZE), TRANS)
            for frame in range(4):
                draw_ogre(strip, frame * SPRITE_SIZE, 0, direction, frame, anim_type)
            
            strip_path = anim_dir / f"ogre_{anim_type}_{direction}_strip.png"
            strip.save(strip_path)
            
            # Create individual frames
            for frame in range(4):
                frame_img = Image.new("RGBA", (SPRITE_SIZE, SPRITE_SIZE), TRANS)
                draw_ogre(frame_img, 0, 0, direction, frame, anim_type)
                frame_path = anim_dir / f"ogre_{anim_type}_{direction}_{frame}.png"
                frame_img.save(frame_path)
    
    print(f"\nOgre sprites generated successfully!")
    print(f"- Size: {SPRITE_SIZE}x{SPRITE_SIZE} (2x larger than goblins)")
    print(f"- Dark olive green skin with battle scars")  
    print(f"- Glowing red eyes and prominent tusks")
    print(f"- Forward-falling death animation for blood puddle effect")
    print(f"- All animations: idle, walk, attack, death")

if __name__ == "__main__":
    generate_ogre_sprites()