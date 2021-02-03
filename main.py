import matplotlib.pyplot as plt
import pandas as pd

def NCRplot():
  df = pd.read_csv("./aluminumgreen.csv")
  print(df)
  print(df["Width (in)"][:11])
  plt.plot(df["Width (in)"][:11], df["NCR"][:11])
  plt.show()

def pearsonstat(D_i, M_i, O_i):
  sum = 0
  for stat in range(len(D_i)):
    sum += ((D_i[stat]-M_i[stat])/(O_i[stat]))**2
  return sum

NCRplot()
