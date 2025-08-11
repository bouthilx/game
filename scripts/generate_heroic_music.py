#!/usr/bin/env python3
"""
8-bit Heroic Music Generator

Generates retro-style heroic music using mathematical waveforms.
Creates both individual tracks and a complete heroic theme.
Uses only built-in Python modules for maximum compatibility.
"""

import math
import wave
import random
import struct
import os


class EightBitMusicGenerator:
    """Generates 8-bit style music using basic waveforms and harmonic progressions."""
    
    def __init__(self, sample_rate=44100, bit_depth=16):
        self.sample_rate = sample_rate
        self.bit_depth = bit_depth
        self.max_amplitude = (2 ** (bit_depth - 1)) - 1
        
        # Define note frequencies (A4 = 440Hz)
        self.note_frequencies = {
            'C3': 130.81, 'C#3': 138.59, 'D3': 146.83, 'D#3': 155.56, 'E3': 164.81,
            'F3': 174.61, 'F#3': 185.00, 'G3': 196.00, 'G#3': 207.65, 'A3': 220.00,
            'A#3': 233.08, 'B3': 246.94,
            'C4': 261.63, 'C#4': 277.18, 'D4': 293.66, 'D#4': 311.13, 'E4': 329.63,
            'F4': 349.23, 'F#4': 369.99, 'G4': 392.00, 'G#4': 415.30, 'A4': 440.00,
            'A#4': 466.16, 'B4': 493.88,
            'C5': 523.25, 'C#5': 554.37, 'D5': 587.33, 'D#5': 622.25, 'E5': 659.25,
            'F5': 698.46, 'F#5': 739.99, 'G5': 783.99, 'G#5': 830.61, 'A5': 880.00,
            'A#5': 932.33, 'B5': 987.77,
            'C6': 1046.50
        }
        
        # Heroic chord progressions
        self.heroic_progressions = [
            ['C4', 'E4', 'G4'],  # C major
            ['F4', 'A4', 'C5'],  # F major
            ['G4', 'B4', 'D5'],  # G major
            ['A4', 'C5', 'E5'],  # A minor
            ['D4', 'F#4', 'A4'], # D major
            ['E4', 'G#4', 'B4'], # E major
        ]
        
    def square_wave(self, frequency, duration, duty_cycle=0.5):
        """Generate a square wave (classic 8-bit sound)."""
        samples = int(self.sample_rate * duration)
        wave = []
        
        for i in range(samples):
            t = i / self.sample_rate
            sin_val = math.sin(2 * math.pi * frequency * t)
            wave.append(1.0 if sin_val >= 0 else -1.0)
        
        # Apply duty cycle
        period_samples = int(self.sample_rate / frequency) if frequency > 0 else samples
        for i in range(0, samples, period_samples):
            duty_end = int(i + period_samples * duty_cycle)
            for j in range(i, min(duty_end, samples)):
                if j < len(wave):
                    wave[j] = 1.0
            for j in range(duty_end, min(i + period_samples, samples)):
                if j < len(wave):
                    wave[j] = -1.0
                    
        return [w * 0.3 for w in wave]  # Lower amplitude for mixing
    
    def triangle_wave(self, frequency, duration):
        """Generate a triangle wave (smoother 8-bit sound)."""
        samples = int(self.sample_rate * duration)
        wave = []
        
        for i in range(samples):
            t = i / self.sample_rate
            # Triangle wave approximation
            sin_val = math.sin(2 * math.pi * frequency * t)
            triangle_val = 2 * math.asin(sin_val) / math.pi if abs(sin_val) <= 1 else 0
            wave.append(triangle_val * 0.3)
            
        return wave
    
    def noise_wave(self, duration, frequency=1000):
        """Generate filtered noise for percussion/rhythm."""
        samples = int(self.sample_rate * duration)
        noise = [random.uniform(-1, 1) for _ in range(samples)]
        
        # Simple low-pass filter effect
        for i in range(1, len(noise)):
            noise[i] = noise[i] * 0.1 + noise[i-1] * 0.9
            
        return [n * 0.2 for n in noise]
    
    def apply_envelope(self, wave, attack=0.1, decay=0.2, sustain=0.7, release=0.3):
        """Apply ADSR envelope to make notes sound more natural."""
        samples = len(wave)
        envelope = [1.0] * samples
        
        # Attack
        attack_samples = int(samples * attack)
        for i in range(attack_samples):
            envelope[i] = i / attack_samples if attack_samples > 0 else 1.0
        
        # Decay
        decay_samples = int(samples * decay)
        decay_end = attack_samples + decay_samples
        if decay_end < samples and decay_samples > 0:
            for i in range(attack_samples, decay_end):
                t = (i - attack_samples) / decay_samples
                envelope[i] = 1.0 - t * (1.0 - sustain)
        
        # Sustain (already set in envelope initialization)
        sustain_end = samples - int(samples * release)
        for i in range(decay_end, sustain_end):
            if i < samples:
                envelope[i] = sustain
        
        # Release
        release_samples = int(samples * release)
        release_start = max(0, samples - release_samples)
        for i in range(release_start, samples):
            if release_samples > 0:
                t = (i - release_start) / release_samples
                envelope[i] = sustain * (1.0 - t)
        
        return [wave[i] * envelope[i] for i in range(len(wave))]
    
    def create_chord(self, notes, duration, waveform='square'):
        """Create a chord by mixing multiple notes."""
        if not notes:
            samples = int(self.sample_rate * duration)
            return [0.0] * samples
            
        waves = []
        for note in notes:
            if note in self.note_frequencies:
                freq = self.note_frequencies[note]
                if waveform == 'square':
                    wave = self.square_wave(freq, duration, duty_cycle=0.25)
                elif waveform == 'triangle':
                    wave = self.triangle_wave(freq, duration)
                else:
                    wave = self.square_wave(freq, duration)
                
                wave = self.apply_envelope(wave)
                waves.append(wave)
        
        if waves:
            # Mix waves by averaging
            samples = min(len(w) for w in waves)
            chord = []
            for i in range(samples):
                mixed = sum(w[i] for w in waves) / len(waves)
                chord.append(mixed)
            return chord
        
        samples = int(self.sample_rate * duration)
        return [0.0] * samples
    
    def create_melody_line(self, notes, note_duration=0.5):
        """Create a melody from a sequence of notes."""
        melody = []
        
        for note in notes:
            if note == 'REST':
                wave = [0.0] * int(self.sample_rate * note_duration)
            else:
                freq = self.note_frequencies.get(note, 440)
                wave = self.triangle_wave(freq, note_duration)
                wave = self.apply_envelope(wave, attack=0.05, decay=0.1, sustain=0.8, release=0.2)
            
            melody.extend(wave)
        
        return melody
    
    def create_bass_line(self, chord_progression, beat_duration=1.0):
        """Create a bass line following the chord progression."""
        bass = []
        
        for chord in chord_progression:
            # Use root note of chord for bass
            root_note = chord[0]
            # Drop octave for bass
            if root_note.endswith('4'):
                bass_note = root_note.replace('4', '3')
            elif root_note.endswith('5'):
                bass_note = root_note.replace('5', '4')
            else:
                bass_note = root_note
            
            freq = self.note_frequencies.get(bass_note, 130)
            wave = self.square_wave(freq, beat_duration, duty_cycle=0.125)
            wave = self.apply_envelope(wave, attack=0.02, decay=0.3, sustain=0.6, release=0.2)
            
            bass.extend(wave)
        
        return bass
    
    def create_drum_pattern(self, beats, beat_duration=0.25):
        """Create simple 8-bit drum pattern."""
        drums = []
        
        for beat in beats:
            if beat == 'KICK':
                # Low frequency square wave for kick
                wave = self.square_wave(60, beat_duration, duty_cycle=0.1)
                wave = self.apply_envelope(wave, attack=0.01, decay=0.4, sustain=0.1, release=0.1)
            elif beat == 'SNARE':
                # Noise burst for snare
                wave = self.noise_wave(beat_duration, 2000)
                wave = self.apply_envelope(wave, attack=0.01, decay=0.2, sustain=0.1, release=0.1)
            elif beat == 'HIHAT':
                # High frequency noise for hi-hat
                wave = self.noise_wave(beat_duration, 8000)
                wave = self.apply_envelope(wave, attack=0.001, decay=0.05, sustain=0.05, release=0.05)
            else:  # REST
                wave = [0.0] * int(self.sample_rate * beat_duration)
            
            drums.extend(wave)
        
        return drums
    
    def create_attack_sound(self, attack_type="sword"):
        """Create attack sound effects for the main character."""
        if attack_type == "sword":
            # Sharp, quick metallic sound
            duration = 0.2
            # Start with high frequency, quickly drop
            attack_wave = []
            samples = int(self.sample_rate * duration)
            
            for i in range(samples):
                t = i / self.sample_rate
                # Frequency sweep from 800Hz to 200Hz
                freq = 800 - (600 * t / duration)
                # Square wave for metallic sound
                sin_val = math.sin(2 * math.pi * freq * t)
                square_val = 1.0 if sin_val >= 0 else -1.0
                
                # Add some noise for texture
                noise = random.uniform(-0.2, 0.2)
                sample = square_val * 0.6 + noise
                
                # Quick attack, fast decay
                if t < 0.05:
                    envelope = t / 0.05
                else:
                    envelope = max(0, 1.0 - (t - 0.05) / (duration - 0.05))
                
                attack_wave.append(sample * envelope)
            
            return attack_wave
        
        elif attack_type == "magic":
            # Magical sparkle sound
            duration = 0.3
            attack_wave = []
            samples = int(self.sample_rate * duration)
            
            for i in range(samples):
                t = i / self.sample_rate
                # Multiple frequencies for magical effect
                freq1 = 440 + 100 * math.sin(20 * math.pi * t)  # Vibrato
                freq2 = 660 + 80 * math.sin(30 * math.pi * t)
                
                # Triangle waves for smoother magical sound
                tri1 = 2 * math.asin(math.sin(2 * math.pi * freq1 * t)) / math.pi
                tri2 = 2 * math.asin(math.sin(2 * math.pi * freq2 * t)) / math.pi
                
                sample = (tri1 + tri2) * 0.3
                
                # Longer attack, gradual decay
                if t < 0.1:
                    envelope = t / 0.1
                else:
                    envelope = max(0, 1.0 - (t - 0.1) / (duration - 0.1))
                
                attack_wave.append(sample * envelope)
            
            return attack_wave
        
        elif attack_type == "bow":
            # Arrow release sound
            duration = 0.15
            attack_wave = []
            samples = int(self.sample_rate * duration)
            
            for i in range(samples):
                t = i / self.sample_rate
                # High frequency with quick decay
                freq = 1200 - (800 * t / duration)
                
                # Mix of square and noise
                sin_val = math.sin(2 * math.pi * freq * t)
                square_val = 1.0 if sin_val >= 0 else -1.0
                noise = random.uniform(-0.3, 0.3)
                
                sample = square_val * 0.4 + noise * 0.6
                
                # Very quick attack and decay
                if t < 0.02:
                    envelope = t / 0.02
                else:
                    envelope = max(0, 1.0 - (t - 0.02) / (duration - 0.02))
                
                attack_wave.append(sample * envelope)
            
            return attack_wave
    
    def create_hurt_sound(self, hurt_type="damage"):
        """Create hurt sound effects for the main character."""
        if hurt_type == "damage":
            # Sharp pain sound - descending tone
            duration = 0.4
            hurt_wave = []
            samples = int(self.sample_rate * duration)
            
            for i in range(samples):
                t = i / self.sample_rate
                # Frequency drops from high to low
                freq = 600 - (400 * t / duration)
                
                # Square wave with some distortion
                sin_val = math.sin(2 * math.pi * freq * t)
                square_val = 1.0 if sin_val >= 0 else -1.0
                
                # Add slight vibrato for pain effect
                vibrato = 1.0 + 0.1 * math.sin(15 * math.pi * t)
                sample = square_val * vibrato * 0.5
                
                # Quick attack, sustained decay
                if t < 0.05:
                    envelope = t / 0.05
                elif t < 0.15:
                    envelope = 1.0
                else:
                    envelope = max(0, 1.0 - (t - 0.15) / (duration - 0.15))
                
                hurt_wave.append(sample * envelope)
            
            return hurt_wave
        
        elif hurt_type == "critical":
            # More intense hurt sound for critical damage
            duration = 0.6
            hurt_wave = []
            samples = int(self.sample_rate * duration)
            
            for i in range(samples):
                t = i / self.sample_rate
                # Lower, more dramatic frequency sweep
                freq = 400 - (300 * t / duration)
                
                # Mix square wave with noise for harsh sound
                sin_val = math.sin(2 * math.pi * freq * t)
                square_val = 1.0 if sin_val >= 0 else -1.0
                noise = random.uniform(-0.3, 0.3)
                
                # Heavy vibrato
                vibrato = 1.0 + 0.2 * math.sin(10 * math.pi * t)
                sample = (square_val * 0.6 + noise * 0.4) * vibrato
                
                # Longer sustain for dramatic effect
                if t < 0.1:
                    envelope = t / 0.1
                elif t < 0.3:
                    envelope = 1.0
                else:
                    envelope = max(0, 1.0 - (t - 0.3) / (duration - 0.3))
                
                hurt_wave.append(sample * envelope * 0.7)
            
            return hurt_wave
        
        elif hurt_type == "death":
            # Dramatic death sound - long descending tone
            duration = 1.2
            hurt_wave = []
            samples = int(self.sample_rate * duration)
            
            for i in range(samples):
                t = i / self.sample_rate
                # Very low frequency sweep
                freq = 300 - (250 * t / duration)
                
                # Triangle wave for smoother, more dramatic sound
                tri_val = 2 * math.asin(math.sin(2 * math.pi * freq * t)) / math.pi
                
                # Slow vibrato
                vibrato = 1.0 + 0.15 * math.sin(3 * math.pi * t)
                sample = tri_val * vibrato
                
                # Long attack, very long decay
                if t < 0.2:
                    envelope = t / 0.2
                elif t < 0.4:
                    envelope = 1.0
                else:
                    envelope = max(0, 1.0 - (t - 0.4) / (duration - 0.4))
                
                hurt_wave.append(sample * envelope * 0.6)
            
            return hurt_wave
    
    def generate_heroic_theme(self, duration=30):
        """Generate a complete heroic theme."""
        print("🎵 Generating heroic theme...")
        
        # Define the structure
        sections = int(duration / 8)  # 8-second sections
        
        # Heroic melody patterns
        heroic_melodies = [
            ['C5', 'D5', 'E5', 'F5', 'G5', 'A5', 'G5', 'F5'],
            ['G5', 'F5', 'E5', 'D5', 'C5', 'D5', 'E5', 'C5'],
            ['E5', 'G5', 'C6', 'B5', 'A5', 'G5', 'A5', 'G5'],
            ['F5', 'A5', 'G5', 'F5', 'E5', 'D5', 'C5', 'D5'],
        ]
        
        # Drum patterns (16th notes, 4/4 time)
        drum_patterns = [
            ['KICK', 'REST', 'SNARE', 'REST', 'KICK', 'HIHAT', 'SNARE', 'HIHAT'],
            ['KICK', 'HIHAT', 'HIHAT', 'SNARE', 'HIHAT', 'KICK', 'HIHAT', 'SNARE'],
            ['KICK', 'KICK', 'SNARE', 'HIHAT', 'KICK', 'HIHAT', 'SNARE', 'HIHAT'],
        ]
        
        # Build the song
        full_melody = []
        full_chords = []
        full_bass = []
        full_drums = []
        
        for section in range(sections):
            # Rotate through different patterns
            melody_pattern = heroic_melodies[section % len(heroic_melodies)]
            chord_progression = self.heroic_progressions[section % len(self.heroic_progressions)]
            drum_pattern = drum_patterns[section % len(drum_patterns)]
            
            # Create section components
            melody = self.create_melody_line(melody_pattern, note_duration=0.5)
            
            # Extend chord progression to match melody length
            extended_chords = chord_progression * 2
            chords = []
            for chord in extended_chords:
                chord_wave = self.create_chord(chord, 2.0, waveform='square')
                chords.extend(chord_wave)
            
            bass = self.create_bass_line(extended_chords, beat_duration=2.0)
            
            # Extend drum pattern
            extended_drums = drum_pattern * 4
            drums = self.create_drum_pattern(extended_drums, beat_duration=0.25)
            
            # Ensure all sections are same length
            target_length = len(melody)
            chords = self.resize_audio(chords, target_length)
            bass = self.resize_audio(bass, target_length)
            drums = self.resize_audio(drums, target_length)
            
            # Add to full song
            full_melody.extend(melody)
            full_chords.extend(chords)
            full_bass.extend(bass)
            full_drums.extend(drums)
        
        # Mix all tracks
        final_mix = []
        for i in range(len(full_melody)):
            mixed_sample = (
                full_melody[i] * 0.4 +
                full_chords[i] * 0.3 +
                full_bass[i] * 0.2 +
                full_drums[i] * 0.1
            )
            final_mix.append(mixed_sample)
        
        # Normalize
        max_val = max(abs(s) for s in final_mix) if final_mix else 1.0
        if max_val > 0:
            final_mix = [s / max_val for s in final_mix]
        
        return final_mix
    
    def resize_audio(self, audio, target_length):
        """Resize audio to target length."""
        current_length = len(audio)
        if current_length == target_length:
            return audio
        elif current_length < target_length:
            # Repeat the audio
            repeats = target_length // current_length if current_length > 0 else 0
            remainder = target_length % current_length if current_length > 0 else target_length
            resized = audio * repeats
            if remainder > 0:
                resized.extend(audio[:remainder])
            return resized
        else:
            # Truncate
            return audio[:target_length]
    
    def save_audio(self, audio_data, filename):
        """Save audio data to WAV file."""
        # Ensure audio directory exists
        output_dir = "game/assets/sounds"
        os.makedirs(output_dir, exist_ok=True)
        
        filepath = os.path.join(output_dir, filename)
        
        # Convert to 16-bit integers
        audio_int = [int(sample * self.max_amplitude) for sample in audio_data]
        
        # Save as WAV
        with wave.open(filepath, 'w') as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(self.sample_rate)
            
            # Convert to bytes
            audio_bytes = b''.join(struct.pack('<h', sample) for sample in audio_int)
            wav_file.writeframes(audio_bytes)
        
        print(f"💾 Saved: {filepath}")
        return filepath


def main():
    """Generate various 8-bit heroic music tracks."""
    print("🎮 8-bit Heroic Music Generator")
    print("=" * 40)
    
    generator = EightBitMusicGenerator()
    
    # Generate main heroic theme
    heroic_theme = generator.generate_heroic_theme(duration=30)
    generator.save_audio(heroic_theme, "heroic_theme.wav")
    
    # Generate shorter victory jingle
    print("🏆 Generating victory jingle...")
    victory_melody = ['C5', 'E5', 'G5', 'C6', 'G5', 'C6']
    victory_chords = [['C4', 'E4', 'G4'], ['F4', 'A4', 'C5'], ['C4', 'E4', 'G4']]
    
    victory_mel = generator.create_melody_line(victory_melody, note_duration=0.3)
    victory_chord_track = []
    for chord in victory_chords:
        chord_wave = generator.create_chord(chord, 0.6, waveform='triangle')
        victory_chord_track.extend(chord_wave)
    
    victory_chord_track = generator.resize_audio(victory_chord_track, len(victory_mel))
    victory_mix = []
    for i in range(len(victory_mel)):
        mixed = victory_mel[i] * 0.6 + victory_chord_track[i] * 0.4
        victory_mix.append(mixed)
    
    max_val = max(abs(s) for s in victory_mix) if victory_mix else 1.0
    if max_val > 0:
        victory_mix = [s / max_val for s in victory_mix]
    
    generator.save_audio(victory_mix, "victory_jingle.wav")
    
    # Generate battle music
    print("⚔️ Generating battle music...")
    battle_theme = generator.generate_heroic_theme(duration=20)
    # Make battle music more intense
    battle_theme = [min(1.0, max(-1.0, s * 1.2)) for s in battle_theme]
    generator.save_audio(battle_theme, "battle_theme.wav")
    
    # Generate exploration music (calmer version)
    print("🗺️ Generating exploration music...")
    exploration_melody = ['C4', 'D4', 'E4', 'G4', 'A4', 'G4', 'F4', 'E4']
    exploration_chords = [['C4', 'E4', 'G4'], ['F4', 'A4', 'C5'], ['G4', 'B4', 'D5'], ['C4', 'E4', 'G4']]
    
    exploration_mel = generator.create_melody_line(exploration_melody * 2, note_duration=0.8)
    exploration_chord_track = []
    for chord in exploration_chords * 2:
        chord_wave = generator.create_chord(chord, 1.6, waveform='triangle')
        exploration_chord_track.extend(chord_wave)
    
    exploration_chord_track = generator.resize_audio(exploration_chord_track, len(exploration_mel))
    exploration_mix = []
    for i in range(len(exploration_mel)):
        mixed = exploration_mel[i] * 0.5 + exploration_chord_track[i] * 0.3
        exploration_mix.append(mixed)
    
    max_val = max(abs(s) for s in exploration_mix) if exploration_mix else 1.0
    if max_val > 0:
        exploration_mix = [s / max_val for s in exploration_mix]
    
    generator.save_audio(exploration_mix, "exploration_theme.wav")
    
    # Generate attack sounds
    print("⚔️ Generating attack sounds...")
    sword_attack = generator.create_attack_sound("sword")
    generator.save_audio(sword_attack, "player_attack_sword.wav")
    
    magic_attack = generator.create_attack_sound("magic")
    generator.save_audio(magic_attack, "player_attack_magic.wav")
    
    bow_attack = generator.create_attack_sound("bow")
    generator.save_audio(bow_attack, "player_attack_bow.wav")
    
    # Generate hurt sounds
    print("💔 Generating hurt sounds...")
    hurt_damage = generator.create_hurt_sound("damage")
    generator.save_audio(hurt_damage, "player_hurt.wav")
    
    hurt_critical = generator.create_hurt_sound("critical")
    generator.save_audio(hurt_critical, "player_hurt_critical.wav")
    
    hurt_death = generator.create_hurt_sound("death")
    generator.save_audio(hurt_death, "player_death.wav")
    
    print("\n✅ Music and sound generation complete!")
    print("\nGenerated files:")
    print("  • heroic_theme.wav (30s main theme)")
    print("  • victory_jingle.wav (2s victory sound)")
    print("  • battle_theme.wav (20s intense battle music)")
    print("  • exploration_theme.wav (13s calm exploration music)")
    print("\nPlayer sounds:")
    print("  • player_attack_sword.wav (0.2s sword attack)")
    print("  • player_attack_magic.wav (0.3s magic attack)")
    print("  • player_attack_bow.wav (0.15s bow/arrow attack)")
    print("  • player_hurt.wav (0.4s damage sound)")
    print("  • player_hurt_critical.wav (0.6s critical damage)")
    print("  • player_death.wav (1.2s death sound)")
    print("\nFiles saved to: game/assets/sounds/")


if __name__ == "__main__":
    main()