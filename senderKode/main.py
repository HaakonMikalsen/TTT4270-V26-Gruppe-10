import numpy as np
import scipy.io.wavfile

password = [3,0,0,1,0,1,0,1,1,1,0,0,0,1,1,1,0,3] #password in bits
print(len(password))
# password = [0,1] #password in bits
freq_map = {0: 5500, 1: 6500,2: 8000} #freq
# freq_map = {0: 5000, 1: 6000,2: 8000} #freq
duration = 1 #time in seconds
silence_duration = 0.5 #time in seconds   
sample_rate = 352_800 # sample rate type pc not cd
resolution = 2** 32 -1#bit rate per seoncds


t = np.linspace(0, duration, int(sample_rate * duration))
t_s = np.linspace(0, silence_duration, int(sample_rate * silence_duration))
k =100
modulation = (1/(1+np.exp(k*(-t+0.05))))*(1/(1+np.exp(-k*(-t+duration-0.05))))
modulation = 1
# print(modulation)
tone_0 = np.sin(2 * np.pi * freq_map[0] * t)*modulation
tone_1 = np.sin(2 * np.pi * freq_map[1] * t)*modulation
tone_2 = np.sin(2 * np.pi * freq_map[2] * t_s)*modulation
# silence = np.zeros(int(sample_rate * duration))
silence = np.sin(2 * np.pi * 6000 * t_s)

signal = []
for bit in password:
    if bit == 1: 
        signal.append(tone_1)
        signal.append(silence)
    elif bit == 2: 
        signal.append(tone_2)
    elif bit == 3: 
        signal.append(silence)
    else:
        signal.append(tone_0)
        signal.append(silence)
final_signal = np.concatenate(signal)
final_signal = final_signal * resolution / 2 
final_signal = final_signal.astype(np.int32)
scipy.io.wavfile.write(f"password{duration}x{silence_duration}.wav", sample_rate, final_signal)