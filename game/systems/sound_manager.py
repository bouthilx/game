"""
Sound Manager System

Manages audio playback for the game including music and sound effects.
Uses pygame.mixer for audio playback.
"""

import pygame
import os
from pathlib import Path
from typing import Dict, Optional


class SoundManager:
    """Centralized sound management system for the game."""
    
    def __init__(self):
        # Initialize pygame mixer
        pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
        pygame.mixer.init()
        
        self.sounds: Dict[str, pygame.mixer.Sound] = {}
        self.music_volume = 0.7
        self.sfx_volume = 0.8
        self.muted = False
        
        # Base path for sounds
        self.sound_path = Path("game/assets/sounds")
        
        # Load all sound effects
        self.load_sounds()
    
    def load_sounds(self):
        """Load all sound effects from the assets directory."""
        if not self.sound_path.exists():
            print(f"Warning: Sound directory {self.sound_path} does not exist")
            return
        
        sound_files = {
            # Attack sounds
            "sword_attack": "player_attack_sword.wav",
            "magic_attack": "player_attack_magic.wav", 
            "bow_attack": "player_attack_bow.wav",
            
            # Hurt sounds
            "player_hurt": "player_hurt.wav",
            "player_hurt_critical": "player_hurt_critical.wav",
            "player_death": "player_death.wav",
            
            # Music/jingles
            "victory": "victory_jingle.wav",
        }
        
        loaded_count = 0
        for sound_name, filename in sound_files.items():
            filepath = self.sound_path / filename
            if filepath.exists():
                try:
                    sound = pygame.mixer.Sound(str(filepath))
                    sound.set_volume(self.sfx_volume)
                    self.sounds[sound_name] = sound
                    loaded_count += 1
                    print(f"✅ Loaded sound: {sound_name}")
                except pygame.error as e:
                    print(f"❌ Failed to load {filename}: {e}")
            else:
                print(f"⚠️ Sound file not found: {filepath}")
        
        print(f"🎵 Sound Manager initialized with {loaded_count} sounds")
    
    def play_sound(self, sound_name: str, volume: Optional[float] = None):
        """Play a sound effect by name."""
        if self.muted:
            return
        
        if sound_name in self.sounds:
            sound = self.sounds[sound_name]
            if volume is not None:
                # Create a copy with custom volume
                sound_copy = sound
                original_volume = sound.get_volume()
                sound_copy.set_volume(volume * self.sfx_volume)
                sound_copy.play()
                # Reset volume after a short delay (this is a limitation of pygame.mixer)
                pygame.time.set_timer(pygame.USEREVENT + 1, 100)  # Reset after 100ms
            else:
                sound.play()
        else:
            print(f"⚠️ Sound '{sound_name}' not found")
    
    def play_attack_sound(self, weapon_type: str = "sword"):
        """Play appropriate attack sound based on weapon type."""
        weapon_sounds = {
            "sword": "sword_attack",
            "magic": "magic_attack", 
            "bow": "bow_attack",
            "staff": "magic_attack",  # Fallback
            "dagger": "sword_attack",  # Fallback
        }
        
        sound_name = weapon_sounds.get(weapon_type.lower(), "sword_attack")
        self.play_sound(sound_name)
    
    def play_hurt_sound(self, damage_type: str = "normal"):
        """Play hurt sound based on damage severity."""
        hurt_sounds = {
            "normal": "player_hurt",
            "critical": "player_hurt_critical", 
            "death": "player_death",
        }
        
        sound_name = hurt_sounds.get(damage_type.lower(), "player_hurt")
        self.play_sound(sound_name)
    
    def load_background_music(self, music_file: str):
        """Load and start playing background music."""
        if self.muted:
            return
        
        filepath = self.sound_path / music_file
        if filepath.exists():
            try:
                pygame.mixer.music.load(str(filepath))
                pygame.mixer.music.set_volume(self.music_volume)
                pygame.mixer.music.play(-1)  # Loop indefinitely
                print(f"🎵 Playing background music: {music_file}")
            except pygame.error as e:
                print(f"❌ Failed to load music {music_file}: {e}")
        else:
            print(f"⚠️ Music file not found: {filepath}")
    
    def stop_music(self):
        """Stop background music."""
        pygame.mixer.music.stop()
    
    def set_music_volume(self, volume: float):
        """Set background music volume (0.0 to 1.0)."""
        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume)
    
    def set_sfx_volume(self, volume: float):
        """Set sound effects volume (0.0 to 1.0)."""
        self.sfx_volume = max(0.0, min(1.0, volume))
        # Update volume for all loaded sounds
        for sound in self.sounds.values():
            sound.set_volume(self.sfx_volume)
    
    def toggle_mute(self):
        """Toggle mute state for all audio."""
        self.muted = not self.muted
        if self.muted:
            pygame.mixer.music.set_volume(0)
            for sound in self.sounds.values():
                sound.set_volume(0)
        else:
            pygame.mixer.music.set_volume(self.music_volume)
            for sound in self.sounds.values():
                sound.set_volume(self.sfx_volume)
    
    def cleanup(self):
        """Clean up audio resources."""
        pygame.mixer.quit()


# Global sound manager instance
_sound_manager: Optional[SoundManager] = None

def get_sound_manager() -> SoundManager:
    """Get the global sound manager instance."""
    global _sound_manager
    if _sound_manager is None:
        _sound_manager = SoundManager()
    return _sound_manager

def play_attack_sound(weapon_type: str = "sword"):
    """Convenience function to play attack sound."""
    get_sound_manager().play_attack_sound(weapon_type)

def play_hurt_sound(damage_type: str = "normal"):
    """Convenience function to play hurt sound."""
    get_sound_manager().play_hurt_sound(damage_type)