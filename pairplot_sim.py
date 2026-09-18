# coding=utf-8

import sys
import os
import math
import numpy as np
import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn.plt as plt
import seaborn as sns
from PIL import Image
import imagehash


def ave_and_var(values, window=3):

    # if not isinstance(values, list):
    #     print values

    n = len(values)
    z = []

    w = (window - 1) / 2

    for i in xrange(n):
        start = i - w if i - w > 0 else 0
        end = i + w if i + w < n else n

        _values = np.array(values[start:end])
        # avs.append(np.average(_values))
        # vas.append(np.var(_values))
        _ave = np.average(_values)
        _var = np.var(_values) + 1
        # print i
        # print values
        _z = math.sqrt((values[i] - _ave)**2) / _var
        z.append(_z)

    return np.array(z)


def main():
    csv_file = os.path.join(os.getcwd(), "data", "tsv", "sim.tsv")
    df = pd.read_csv(csv_file)
    df["phash"] = df["phash"] / np.max(df["phash"])

    start = 33
    end = 37

    phashs = list(df["phash"][start * 30:end * 30])

    # print len(phashs)

    z3 = ave_and_var(phashs, window=3)
    z5 = ave_and_var(phashs, window=5)
    z9 = ave_and_var(phashs, window=9)
    z17 = ave_and_var(phashs, window=17)
    z33 = ave_and_var(phashs, window=33)

    # print len(ave_phashs)
    # print len(var_phashs)

    # sys.exit()

    # plot_df = pd.DataFrame({
    #     "phash": phashs,
    #     "ave": ave_phashs,
    #     "var3": var_phashs,
    # })

    # print plot_df

    # with open("./data/tsv/sim_ave_var.tsv", "w") as f:
    #     f.write("sim\tave\tvar\n")
    #     for i in xrange(3000):
    #         f.write("{0}\t{1}\t{2}\n".format(plot_df["phash"][i],
    #                                          plot_df["ave"][i],
    #                                          plot_df["var"][i]))

    # sns.set(style="ticks", color_codes=True)
    # g = sns.pairplot(plot_df)
    # g.savefig("output.png")

    sns.set_style("dark")

    # sns.jointplot(x="phash", y="ave", data=plot_df)
    x = np.arange(len(phashs))
    x = x / 30.0 + start
    sns.plt.plot(x, np.array(phashs), label="dist")
    sns.plt.plot(x, z3, label="z3")
    sns.plt.plot(x, z5, label="z5")
    sns.plt.plot(x, z9, label="z9")
    sns.plt.plot(x, z17, label="z17")
    sns.plt.plot(x, z33, label="z33")
    sns.plt.legend(loc=2)
    sns.plt.show()
    # plt.savefig(os.path.join(outputdir, hashname + "_" + (filename_format % i)))
    # plt.clf()

    # sns.pairplot(data=plot_df)
    # sns.plt.show()

    # plt.plot(plot_df["phash"])
    # plt.show()

if __name__ == "__main__":
    main()
