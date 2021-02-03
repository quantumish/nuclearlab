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

df = pd.read_csv("./tissueyellow.csv")
ncr = df["NCR"][1:].reset_index()["NCR"]
ncr_sig = df["NCR \sigma"][1:].reset_index()["NCR \sigma"]
a = gen_approx(ncr, 0.946)

print(pearsonstat(a, ncr, ncr_sig))
