import matplotlib.pyplot as plt
import pandas as pd

def NCRplot(df):
    plt.plot(df["Width"][:11], df["NCR"][:11])
    plt.show()

def pearsonstat(D_i, M_i, sig_i):
    sum = 0
    for stat in range(len(D_i)):
        sum += ((D_i[stat]-M_i[stat])/(sig_i[stat]))**2
    return sum

def gen_approx(data, T):
    new = []
    for i in data:
        new.append(0.5 ** (i/T))
    return new

def deriv(f, h=0.001):
    return lambda x : (f(x+h)-f(x))/h

import scipy.optimize
def optim (initial, wid, ncr, ncr_sig):
    f = lambda x : pearsonstat(gen_approx(wid, x), ncr, ncr_sig)
    x = scipy.optimize.minimize(f, initial)
    return x

df = pd.read_csv("./tissueyellow.csv")
ncr = df["NCR"][1:].reset_index()["NCR"]
wid = df["Width"][1:].reset_index()["Width"]
ncr_sig = df["NCR \sigma"][1:].reset_index()["NCR \sigma"]
a=gen_approx(wid, optim(0.9, wid, ncr, ncr_sig).x[0])
print(gen_approx(ncr, optim(0.9, wid, ncr, ncr_sig).x[0]))

import numpy as np
from scipy.interpolate import make_interp_spline, BSpline, interp1d
xnew = np.linspace(wid.min(), wid.max(), 300)
ncr_smooth = interp1d(wid, ncr)

plt.plot(xnew, ncr_smooth(xnew))
print(ncr_smooth)
#ax, caps, bars = plt.errorbar(xnew, ncr_smooth, capsize=0, color="#6cad50")

#[bar.set_alpha(0.3) for bar in bars]

#plt.fill_between(wid, ncr-ncr_sig, ncr+ncr_sig, alpha=0.2, color="#6cad50")
#plt.plot(wid, a)
plt.show()
