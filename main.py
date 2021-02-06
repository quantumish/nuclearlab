import matplotlib.pyplot as plt
import pandas as pd
import scipy.optimize
import numpy as np
import os

import warnings
warnings.filterwarnings("ignore")
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "sans-serif",
    "font.sans-serif": ["Helvetica"],
})

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
    f2 = lambda n: (f(n) - (f(x)+6.63))
    if (f2(0) < 0): a = 0
    else: a = scipy.optimize.bisect(f2, 0, x)
    if (f2(10000000) < 0): b = 10000000
    else: b = scipy.optimize.bisect(f2, x, 10000000)
    return (a, b, x, f(x))


def graph_file(fig, axs, i, ii, filename, name):
    df = pd.read_csv(filename)
    ncr = df["NCR"][1:].reset_index()["NCR"]
    wid = df["Width"][1:].reset_index()["Width"]
    ncr_sig = df["NCR \sigma"][1:].reset_index()["NCR \sigma"]
    ncr_sig[0] = 0.000001
    o = optim(0.9, wid, ncr, ncr_sig)
    xnew = np.linspace(wid.min(), wid.max(), 300)
    a=gen_approx(xnew, o[2])
    a1=gen_approx(xnew, o[0])

    a2=gen_approx(xnew, o[1])

    a = gen_approx(xnew, o[2])
    a1 = gen_approx(xnew, o[0])
    a2 = gen_approx(xnew, o[1])
    print(filename[2:-4], round(o[2][0], 4), round(o[0],4), round(o[1],4), round(o[3][0], 4), len(wid)-1, sep="\t")

    axs[i, ii].plot(wid, ncr, color="#1f77b4")

    ax, bars, caps = axs[i,ii].errorbar(wid, ncr, ncr_sig, alpha=0.2)

    [bar.set_alpha(1) for bar in bars]

    axs[i, ii].fill_between(wid, ncr-ncr_sig, ncr+ncr_sig, alpha=0.1, color="#1f77b4")
    axs[i, ii].plot(xnew, a, color="#6cad50")
    axs[i, ii].fill_between(xnew, a1, a2, alpha=0.2, color="#6cad50")
    #axs[i, ii].plot(xnew, a2)

    axs[i, ii].set_title("Absorber Width vs NCR (" + name[0] + ", " + name[1]+")")
    axs[i, ii].set_xlabel("Width (in)")
    axs[i, ii].set_ylabel("NCR")


print("Name\t\tT_best\tT_min\tT_max\tS_min\tN-1")
titles = [("Plastic", "Orange"),("Plastic", "Green"), ("Tissue", "Yellow"), ("Lead", "Green"), ("Aluminum", "Green"), ("Lead", "Orange"), ("Aluminum", "Orange")]
fig, axs = plt.subplots(3,3)
c = 0
for i in os.listdir("."):
    if i.endswith(".csv"):
        graph_file(fig, axs, c//3, c%3, "./"+i,titles[c])
        c+=1

axs[2, 2].axis("off")
axs[2, 1].axis("off")
plt.subplots_adjust(left=0.07, right=0.93, top=0.95, bottom=0.05)
custom_lines = [plt.Line2D([0], [0], color="#1f77b4", lw=2),
                plt.Line2D([0], [0], color='w', markerfacecolor="#1f77b4", marker='o', markersize=15, alpha=0.1),
                plt.Line2D([0], [0], color="#6cad50", lw=2),
                plt.Line2D([0], [0], color='w', markerfacecolor="#6cad50", marker='o', markersize=15, alpha=0.1)]
plt.legend(custom_lines, ["Recorded NCR", "Recorded NCR error", "Fitted NCR", "Fitted NCR error"])
import textwrap
axs[2,1].text(0, 0.8, "\n".join(textwrap.wrap("Figure A: Graphs of absorber width vs recorded and fit NCR (given by $0.5^{t/T}$) for each combination of sources and absorbers. Uncertainty in recorded NCR (propagated with standard formulas) is depicted via the transparent blue region, whilst uncertainty in fit (given by the curves of maximum and minimum half-thickness) is transparent green.", 70)))
plt.show()
