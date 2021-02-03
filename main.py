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
print(gen_approx(ncr, optim(0.9, wid, ncr, ncr_sig).x[0]))
plt.plot(wid, gen_approx(wid, optim(0.9, wid, ncr, ncr_sig).x[0]))
plt.plot(wid, ncr)
plt.show()
#print(pearsonstat(a, ncr, ncr_sig))
