import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib import pyplot as plt
import pickle
import numpy as np


MA_WINDOW = 100

with open(r'ep_reward_hist.pkl', 'rb') as f:
    ep_reward_hist = pickle.load(f)

moving_avg = np.convolve(ep_reward_hist, np.ones((MA_WINDOW,))/MA_WINDOW, mode='valid')

plt.plot([i for i in range(len(moving_avg))], moving_avg)
plt.show()