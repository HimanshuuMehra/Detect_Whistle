import pyaudio
import numpy as np
import time
from scipy.fft import fft

Rate = 44100
Chunk = 1024
Whistle_threshold = 1000

p = pyaudio.PyAudio()

stream = p.open(format=pyaudio.paInt16, channels=1,
                rate=Rate,input=True,frames_per_buffer=Chunk)
Whistle_count=0

def detect_whistle(data):
    audio_data = np.frombuffer(data,dtype=np.int16)
    transformed_data = fft(audio_data)
    freqs = np.fft.fftfreq(len(transformed_data), 1/Rate)
    peak_freq = abs(freqs[np.argmax(np.abs(transformed_data))])
    if 1000 <= peak_freq <= 4000:
        return True
    return False

try:
    print("Listening  for whistles")
    while True:
        data=stream.read(Chunk,exception_on_overflow=False)
        if detect_whistle(data):
            Whistle_count += 1
            print(f"Whistle detected! count :{Whistle_count}")

        time.sleep(0.1) 
except KeyboardInterrupt:
    print("stopping")

finally:
    stream.stop_stream()
    stream.close()
    p.terminate()
