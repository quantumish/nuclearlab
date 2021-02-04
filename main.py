import matplotlib.pyplot as plt
import pandas as pd
import scipy.optimize


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
    return lambda x: (f(x+h)-f(x))/h


def optim (initial, wid, ncr, ncr_sig):
    f = lambda x: pearsonstat(gen_approx(wid, x), ncr, ncr_sig)
    x = scipy.optimize.minimize(f, initial)
    f2 = lambda n: (f(n) - (x.x+6.63))
    a = scipy.optimize.root(f2, [ncr.min(), ncr.max()])
    return (a, x)

df = pd.read_csv("./tissueyellow.csv")
ncr = df["NCR"][1:].reset_index()["NCR"]
wid = df["Width"][1:].reset_index()["Width"]
ncr_sig = df["NCR \sigma"][1:].reset_index()["NCR \sigma"]
o=optim(0.9, wid, ncr, ncr_sig)
print(o[1].x[0], o[0].x[0], o[0].x[1])
a=gen_approx(wid, o[1].x[0])
a1=gen_approx(wid, o[0].x[0])
a2=gen_approx(wid, o[0].x[1])

import numpy as np
from scipy.interpolate import make_interp_spline, BSpline, interp1d
xnew = np.linspace(wid.min(), wid.max(), 300)
spl = make_interp_spline(wid, ncr, k=3)
ncr_smooth = spl(xnew)
spl = make_interp_spline(wid, ncr_sig, k=3)
ncr_sig_smooth = spl(xnew)

# plt.plot(xnew, ncr_smooth, color="#6cad50")

# ax, bars, caps = plt.errorbar(wid, ncr, ncr_sig, color="#6cad50", alpha=0.2)

# [bar.set_alpha(1) for bar in bars]

# plt.fill_between(xnew, ncr_smooth-ncr_sig_smooth, ncr_smooth+ncr_sig_smooth, alpha=0.2, color="#6cad50")
plt.plot(wid, a)
plt.plot(wid, a1)
plt.plot(wid, a2)
plt.fill_between(wid, a1, a2, alpha=0.2, color="#6cad50")
plt.show()
