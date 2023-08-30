import sounddevice as sd
import numpy as np
import time
import keyboard
import matplotlib.pyplot as plt

def calculate_db(rms, threshold=-60):
    reference_pressure = 20e-6  # Reference sound pressure in Pascals for 0 dB
    
    if rms > 0:
        db = 20 * np.log10(rms / reference_pressure)
        return db
    elif rms <= 0 and rms >= threshold:
        return threshold 
    else:
        return float("-inf")  


def main():
    duration = 5  
    sample_rate = 44100  
    channels = 1  
    sample_size = 10
    threshold = 70


    print("Recording...")

    x_pts = list(range(1,sample_size+1))
    y_pts = []
    stopper = 0
    while stopper < sample_size:
        # Record audio data
        audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=channels)
        sd.wait()
        
        # Calculate the RMS amplitude of the audio data
        rms_amplitude = np.sqrt(np.mean(np.square(audio_data)))

        # Calculate the dB level
        sound_level_db = (calculate_db(rms_amplitude))
        y_pts.append(sound_level_db)
        
        excessNoiseCounter = 0
        if(sound_level_db > threshold):
            excessNoiseCounter += 1
            print("Noise level exceeded")
        print("Datapoint " + str(stopper+1) + " collected")
        stopper += 1
    

    np.array(y_pts)
    plt.plot(x_pts,y_pts)
    plt.axhline(y=threshold) 
    plt.show()
   
if __name__ == "__main__":
    main()
