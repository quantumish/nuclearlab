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
    x = scipy.optimize.minimize(f, initial).x
    print(wid)
    print(x, f(0.04))
    f2 = lambda n: (f(n) - (x+6.63))
    vals = []
    lin = np.linspace(0, 20*wid.max(), 300)
    for i in lin:
        vals.append(f(i))
    # plt.plot(lin, vals)
    # plt.show()
    a = scipy.optimize.bisect(f2, 0, x)
    b = scipy.optimize.bisect(f2, x, 10000000)
    # vals = []
    # lin = np.linspace(wid.min(), wid.max(), 300)
    # for i in lin:
    #     vals.append(f2(i))
    # plt.plot(lin, vals)
    # plt.scatter(a, [0])
    # plt.scatter(b, [0])
    # plt.show()
    return (a, b, x)


def graph_file(fig, axs, i, ii, name):
    df = pd.read_csv(name)
    ncr = df["NCR"][1:].reset_index()["NCR"]
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

    axs[i,ii].plot(wid, ncr, color="#1f77b4")

    ax, bars, caps = axs[i,ii].errorbar(wid, ncr, ncr_sig, alpha=0.2)

    [bar.set_alpha(1) for bar in bars]

    axs[i,ii].fill_between(wid, ncr-ncr_sig, ncr+ncr_sig, alpha=0.1, color="#1f77b4")
    axs[i,ii].plot(xnew, a_smooth, color="#6cad50")
    axs[i,ii].fill_between(xnew, a1_smooth, a2_smooth, alpha=0.1, color="#6cad50")
    axs[i,ii].text(.5,.9,name, horizontalalignment='center', transform=axs[i,ii].transAxes)


def graph_manual(fig, axs, i, ii, name, g, g1, g2):
    df = pd.read_csv(name)
    ncr = df["NCR"][1:].reset_index()["NCR"]
    wid = df["Width"][1:].reset_index()["Width"]
    ncr_sig = df["NCR \sigma"][1:].reset_index()["NCR \sigma"]
    a=gen_approx(wid, g)
    a1=gen_approx(wid, g1)
    a2=gen_approx(wid, g2)

    xnew = np.linspace(wid.min(), wid.max(), 300)
    spl = make_interp_spline(wid, a, k=3)
    a_smooth = spl(xnew)
    spl = make_interp_spline(wid, a1, k=3)
    a1_smooth = spl(xnew)
    spl = make_interp_spline(wid, a2, k=3)
    a2_smooth = spl(xnew)

    axs[i,ii].plot(wid, ncr, color="#1f77b4")

    ax, bars, caps = axs[i,ii].errorbar(wid, ncr, ncr_sig, alpha=0.2)

    [bar.set_alpha(1) for bar in bars]

    axs[i,ii].fill_between(wid, ncr-ncr_sig, ncr+ncr_sig, alpha=0.1, color="#1f77b4")
    axs[i,ii].plot(xnew, a_smooth, color="#6cad50")
    axs[i,ii].fill_between(xnew, a1_smooth, a2_smooth, alpha=0.1, color="#6cad50")
    axs[i,ii].text(.5,.9,name, horizontalalignment='center', transform=axs[i,ii].transAxes)

import os
fig, axs = plt.subplots(3,3)
c = 0
for i in os.listdir("."):
    if i.endswith(".csv"):
        print(i)
        try:
            graph_file(fig, axs, c//3, c%3, "./"+i)
        except:
            # axs[c//3, c%3].text(0.5,0.5,"ValueError Pain", horizontalalignment='center', verticalalignment='center', transform=axs[c//3,c%3].transAxes)
            # axs[c//3,c%3].text(.5,.9,"./"+i, horizontalalignment='center', transform=axs[c//3,c%3].transAxes)
            graph_manual(fig, axs, c//3, c%3, "./"+i, 0.5, 0.4, 0.6)
            pass
        c+=1
axs[2,2].axis("off")
axs[2,1].axis("off")
plt.show()
