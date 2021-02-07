import csv
import tkinter as tk
from tkinter import filedialog


#inputFile = input("Input file: ")
root = tk.Tk()
root.withdraw()

inputFile = filedialog.askopenfilename()
csvarray = []

with open(inputFile, newline = "") as File:
    reader = csv.reader(File, delimiter=',', quotechar='|')
    count = 0
    for row in reader:
        if count == 0:
            count += 1
            continue
        moddedrow = []
        for value in row:
            try:
                moddedrow.append(round(float(value), 4))
            except:
                moddedrow.append(value)
        csvarray.append(moddedrow)

for row in csvarray:
    strrow = [str(x) for x in row]
    print("\t".join(strrow))
