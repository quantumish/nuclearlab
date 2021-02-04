import matplotlib.pyplot as plt
import pandas as pd
import scipy.optimize
import numpy as np
from scipy.interpolate import make_interp_spline, BSpline, interp1d


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
        if (T != 0): new.append(0.5 ** (i/T))
        else: new.append(0.5 ** (i/0.001))
    return new


def deriv(f, h=0.001):
    return lambda x: (f(x+h)-f(x))/h


def optim (initial, wid, ncr, ncr_sig):
    f = lambda x: pearsonstat(gen_approx(wid, x), ncr, ncr_sig)
    # vals = []
    # lin = np.linspace(wid.min(), wid.max(), 300)
    # for i in lin:
    #     vals.append(f(i))
    # plt.plot(lin, vals)
    x = scipy.optimize.minimize(f, initial).x
    f2 = lambda n: (f(n) - (x+6.63))
    a = scipy.optimize.bisect(f2, wid.min(), x)
    b = scipy.optimize.bisect(f2, x, wid.max())
    # vals = []
    # lin = np.linspace(wid.min(), wid.max(), 300)
    # for i in lin:
    #     vals.append(f2(i))
    # plt.plot(lin, vals)
    # plt.scatter(a, [0])
    # plt.scatter(b, [0])
    # plt.show()
    return (a, b, x)

def graph_file(name):
    df = pd.read_csv(name)
    ncr = df["NCR"][1:].reset_index()["NCR"]
    if len(ncr) < 3: return
    wid = df["Width"][1:].reset_index()["Width"]
    ncr_sig = df["NCR \sigma"][1:].reset_index()["NCR \sigma"]
    o=optim(0.9, wid, ncr, ncr_sig)
    a=gen_approx(wid, o[2])
    a1=gen_approx(wid, o[0])
    a2=gen_approx(wid, o[1])

    xnew = np.linspace(wid.min(), wid.max(), 300)
    spl = make_interp_spline(wid, a, k=3)
    a_smooth = spl(xnew)
    spl = make_interp_spline(wid, a1, k=3)
    a1_smooth = spl(xnew)
    spl = make_interp_spline(wid, a2, k=3)
    a2_smooth = spl(xnew)

    plt.plot(wid, ncr, color="#1f77b4")

    ax, bars, caps = plt.errorbar(wid, ncr, ncr_sig, alpha=0.2)

    [bar.set_alpha(1) for bar in bars]

    plt.fill_between(wid, ncr-ncr_sig, ncr+ncr_sig, alpha=0.1, color="#1f77b4")
    plt.plot(xnew, a_smooth, color="#6cad50")
    plt.fill_between(xnew, a1_smooth, a2_smooth, alpha=0.1, color="#6cad50")
    plt.show()

import os
for i in os.listdir("."):
    if i.endswith(".csv"):
        print(i)
        graph_file("./"+i)
