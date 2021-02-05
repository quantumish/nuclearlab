import matplotlib.pyplot as plt
import pandas as pd
import scipy.optimize
import numpy as np
import os

# 1. NaN s stat
# 2. Gigantic s stat
# 3.


def pearsonstat(D_i, M_i, sig_i):
    sum = 0
    for i in range(len(D_i)):
        sum += ((D_i[i]-M_i[i])/(sig_i[i]))**2
    return sum


def gen_approx(d, T):
    new = []
    for i in d:
        if (T != 0): new.append(0.5 ** (i/T))
        else: new.append(0.5 ** (i/0.001))
    return new


def deriv(f, h=0.001):
    return lambda x: (f(x+h)-f(x))/h


def optim(initial, wid, ncr, ncr_sig):
    f = lambda x: pearsonstat(gen_approx(wid, x), ncr, ncr_sig)
    x = scipy.optimize.minimize(f, initial).x
    print(gen_approx(wid, x))
    f2 = lambda n: (f(n) - (f(x)+6.63))
    # vals = []
    # lin = np.linspace(0, 20*wid.max(), 300)
    # for i in lin:
    #     vals.append(f2(i))
    # plt.plot(lin, vals)
    # plt.show()
    if (f2(0) < 0): a = 0
    else: a = scipy.optimize.bisect(f2, 0, x)
    if (f2(10000000) < 0): b = 10000000
    else: b = scipy.optimize.bisect(f2, x, 10000000)
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
    o = optim(0.9, wid, ncr, ncr_sig)
    xnew = np.linspace(wid.min(), wid.max(), 300)
    a=gen_approx(xnew, o[2])
    a1=gen_approx(xnew, o[0])

    a2=gen_approx(xnew, o[1])

    a = gen_approx(xnew, o[2])
    a1 = gen_approx(xnew, o[0])
    a2 = gen_approx(xnew, o[1])

    axs[i, ii].plot(wid, ncr, color="#1f77b4")

    ax, bars, caps = axs[i,ii].errorbar(wid, ncr, ncr_sig, alpha=0.2)

    [bar.set_alpha(1) for bar in bars]

    axs[i, ii].fill_between(wid, ncr-ncr_sig, ncr+ncr_sig, alpha=0.1, color="#1f77b4")
    axs[i, ii].plot(xnew, a, color="#6cad50")
    axs[i, ii].plot(xnew, a1)
    axs[i, ii].plot(xnew, a2)
    axs[i, ii].text(.5, .9, name, horizontalalignment='center', transform=axs[i, ii].transAxes)


fig, axs = plt.subplots(3,3)
c = 0
for i in os.listdir("."):
    if i.endswith(".csv"):
        print(i)
        graph_file(fig, axs, c//3, c%3, "./"+i)
        c+=1

axs[2, 2].axis("off")
axs[2, 1].axis("off")
plt.show()
