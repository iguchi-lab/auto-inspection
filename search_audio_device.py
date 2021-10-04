import pyaudio
import wave

audio = pyaudio.PyAudio()

for x in range(0, audio.get_device_count()):
    print(audio.get_device_info_by_index(x))
    