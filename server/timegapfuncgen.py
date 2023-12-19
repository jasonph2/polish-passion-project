import numpy as np
from scipy.interpolate import CubicSpline
import pickle

polish_recording = np.array([.5, 1, 2, 3, 5])
very_slow_y = np.array([4.5, 5.25, 6, 7, 8.5])
slow_y = np.array([3.5, 4.25, 4.75, 5.25, 6])
normal_y = np.array([1.75, 2.25, 3, 3.5, 4.5])
fast_y = np.array([1.3, 1.6, 2, 2.5, 3])
very_fast_y = np.array([1, 1.25, 1.7, 2, 2.5])

very_slow = CubicSpline(polish_recording, very_slow_y)
slow = CubicSpline(polish_recording, slow_y)
normal = CubicSpline(polish_recording, normal_y)
fast = CubicSpline(polish_recording, fast_y)
very_fast = CubicSpline(polish_recording, very_fast_y)

time_funcs = {'very_slow': very_slow, 'slow': slow, 'normal': normal, 'fast': fast, 'very_fast': very_fast}

with open('time_funcs.pkl', 'wb') as file:
    pickle.dump(time_funcs, file)

# with open('time_funcs.pkl', 'rb') as file:
#     loaded_cs_dict = pickle.load(file)