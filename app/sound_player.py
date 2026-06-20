import os
import io
import random
import struct
import math
from app.utils import generate_default_click

try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False

def pitch_shift_pcm(wav_bytes, pitch_factor):
    """Resamples 16-bit PCM Mono or Stereo WAV bytes to alter playback speed/pitch."""
    if len(wav_bytes) < 44:
        return wav_bytes
        
    try:
        # Find 'fmt ' chunk
        fmt_idx = wav_bytes.find(b'fmt ')
        if fmt_idx == -1:
            return wav_bytes
            
        num_channels = struct.unpack('<H', wav_bytes[fmt_idx + 8 : fmt_idx + 10])[0]
        bits_per_sample = struct.unpack('<H', wav_bytes[fmt_idx + 22 : fmt_idx + 24])[0]
        
        # Only support 16-bit PCM Mono or Stereo
        if bits_per_sample != 16 or num_channels not in (1, 2):
            return wav_bytes
            
        # Find 'data' chunk
        data_idx = wav_bytes.find(b'data')
        if data_idx == -1:
            return wav_bytes
            
        data_size = struct.unpack('<I', wav_bytes[data_idx + 4 : data_idx + 8])[0]
        header = wav_bytes[:data_idx + 8]
        raw_data = wav_bytes[data_idx + 8 : data_idx + 8 + data_size]
        
        num_samples = len(raw_data) // (2 * num_channels)
        samples = []
        
        if num_channels == 1:
            for i in range(num_samples):
                val = struct.unpack('<h', raw_data[i*2 : i*2+2])[0]
                samples.append(val)
        else:
            for i in range(num_samples):
                l_val = struct.unpack('<h', raw_data[i*4 : i*4+2])[0]
                r_val = struct.unpack('<h', raw_data[i*4+2 : i*4+4])[0]
                samples.append((l_val, r_val))
                
        # Rescale sampling pointer to shift pitch
        new_num_samples = int(num_samples / pitch_factor)
        new_samples = []
        for i in range(new_num_samples):
            pos = i * pitch_factor
            idx1 = int(pos)
            idx2 = min(idx1 + 1, num_samples - 1)
            frac = pos - idx1
            
            if idx1 >= num_samples:
                break
                
            if num_channels == 1:
                val1 = samples[idx1]
                val2 = samples[idx2]
                val = int(val1 + (val2 - val1) * frac)
                new_samples.append(val)
            else:
                val1_l, val1_r = samples[idx1]
                val2_l, val2_r = samples[idx2]
                val_l = int(val1_l + (val2_l - val1_l) * frac)
                val_r = int(val1_r + (val2_r - val1_r) * frac)
                new_samples.append((val_l, val_r))
                
        # Repack to bytes
        new_raw_data = bytearray()
        if num_channels == 1:
            for val in new_samples:
                val = max(-32768, min(32767, val))
                new_raw_data.extend(struct.pack('<h', val))
        else:
            for val_l, val_r in new_samples:
                val_l = max(-32768, min(32767, val_l))
                val_r = max(-32768, min(32767, val_r))
                new_raw_data.extend(struct.pack('<h', val_l))
                new_raw_data.extend(struct.pack('<h', val_r))
                
        new_data_size = len(new_raw_data)
        new_header = bytearray(header)
        new_header[data_idx + 4 : data_idx + 8] = struct.pack('<I', new_data_size)
        
        riff_size = 36 + new_data_size
        new_header[4:8] = struct.pack('<I', riff_size)
        
        return bytes(new_header + new_raw_data)
    except Exception as e:
        print(f"Error pitch shifting WAV bytes: {e}")
        return wav_bytes

class SoundPlayer:
    def __init__(self, config):
        self.config = config
        self.mixer_initialized = False
        self.sounds = []  # List of loaded Sound objects (preloaded pitch variations)
        self.current_file = None
        
        if not PYGAME_AVAILABLE:
            print("Pygame library not found. Sound feature is disabled.")
            return

        try:
            # Low buffer size (512 or 256) is vital for minimizing typing-to-sound latency
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
            pygame.mixer.set_num_channels(32)  # Avoid channel starvation during fast typing
            self.mixer_initialized = True
        except Exception as e:
            print(f"Failed to initialize pygame.mixer: {e}")
            
        self.reload()

    def reload(self):
        """Reloads the selected sound file and regenerates pitch variations."""
        if not self.mixer_initialized:
            return

        sound_file = self.config.get("sound_file")
        volume = self.config.get("volume")
        pitch_random = self.config.get("pitch_randomize")
        
        self.sounds = []
        
        # Robust path resolution: resolve presets and relative paths
        resolved_path = None
        if sound_file:
            from app.utils import get_resource_path
            # 1. Check if the saved path exists directly
            if os.path.exists(sound_file):
                resolved_path = sound_file
            # 2. Check if we can find it in the assets folder dynamically
            else:
                base_name = os.path.basename(sound_file)
                asset_path = get_resource_path(os.path.join("assets", base_name))
                if os.path.exists(asset_path):
                    resolved_path = asset_path
                else:
                    # 3. Check if it's a relative path in MEIPASS
                    direct_path = get_resource_path(sound_file)
                    if os.path.exists(direct_path):
                        resolved_path = direct_path
                        
        self.current_file = resolved_path

        is_custom = resolved_path and os.path.exists(resolved_path)
        
        if is_custom and resolved_path.lower().endswith('.wav'):
            # Load WAV bytes for pitch shift variations
            try:
                with open(resolved_path, 'rb') as f:
                    wav_bytes = f.read()
                self._load_wav_variations(wav_bytes, pitch_random)
            except Exception as e:
                print(f"Error loading custom WAV file, falling back to default: {e}")
                self._load_default_sound(pitch_random)
        elif is_custom:
            # MP3/OGG/other custom sounds
            try:
                sound = pygame.mixer.Sound(resolved_path)
                self.sounds = [sound] * 5
            except Exception as e:
                print(f"Error loading custom sound file, falling back to default: {e}")
                self._load_default_sound(pitch_random)
        else:
            # Default procedural click sound
            self._load_default_sound(pitch_random)
            
        self.set_volume(volume)

    def _load_wav_variations(self, wav_bytes, pitch_random):
        """Generates 5 pitch variants of WAV bytes to populate sound pool."""
        factors = [0.92, 0.96, 1.00, 1.04, 1.08] if pitch_random else [1.00] * 5
        for f in factors:
            try:
                shifted = pitch_shift_pcm(wav_bytes, f)
                snd = pygame.mixer.Sound(io.BytesIO(shifted))
                self.sounds.append(snd)
            except Exception as e:
                print(f"Error compiling WAV pitch variation for factor {f}: {e}")
                
        # Ensure we have at least one sound
        if not self.sounds:
            try:
                self.sounds = [pygame.mixer.Sound(io.BytesIO(wav_bytes))] * 5
            except Exception:
                pass

    def _load_default_sound(self, pitch_random):
        """Loads default sound from procedural generator."""
        default_bytes = generate_default_click()
        self._load_wav_variations(default_bytes, pitch_random)

    def set_volume(self, volume_percent):
        """Sets base volume of all loaded sounds."""
        if not self.mixer_initialized or not self.sounds:
            return
        vol = max(0.0, min(1.0, volume_percent / 100.0))
        for snd in self.sounds:
            if snd:
                snd.set_volume(vol)

    def play_click(self):
        """Plays one of the preloaded sound variations with tiny organic fluctuations."""
        if not self.mixer_initialized or not self.config.get("sound_enabled") or not self.sounds:
            return
            
        try:
            # Random selection from pitch pool
            snd = random.choice(self.sounds)
            if snd:
                # Add micro-variation in volume (±10%) for sound organic realism
                base_vol = self.config.get("volume") / 100.0
                rand_vol = base_vol * random.uniform(0.85, 1.0)
                snd.set_volume(max(0.0, min(1.0, rand_vol)))
                snd.play()
        except Exception as e:
            print(f"Error playing sound: {e}")

    def test_play(self, file_path, volume):
        """Plays a test click of a specific audio file with a specific volume immediately."""
        if not self.mixer_initialized:
            return
            
        try:
            test_sound = None
            if file_path and os.path.exists(file_path):
                test_sound = pygame.mixer.Sound(file_path)
            else:
                test_sound = pygame.mixer.Sound(io.BytesIO(generate_default_click()))
                
            if test_sound:
                test_sound.set_volume(volume / 100.0)
                test_sound.play()
        except Exception as e:
            print(f"Error testing sound file {file_path}: {e}")
