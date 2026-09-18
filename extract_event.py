# coding=utf-8

import sys
import os
import math
import numpy as np
import pandas as pd
from scipy import stats
# import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
import imagehash
import cv2


def load_df():
    csv_file = os.path.join(os.getcwd(), "data", "tsv", "sim.tsv")
    df = pd.read_csv(csv_file)
    return df


def z(distances, t, w):

    # if isinstance(distances, pd.core.series.Series):
    #     distances = np.array(list(distances))
    # elif isinstance(distances, list):
    #     distances = np.array(distances)
    # elif not isinstance(distances, np.ndarray):
    #     sys.exit("distances is invalid type : {}".format(type(distances)))

    n = len(distances)
    start = t - w if t - w > 0 else 0
    end = t + w if t + w < n else n
    values = distances[start:end + 1]
    score = -stats.zscore(values)[t - start] if np.var(values) != 0 else 0.0
    return score


def half_window(n):
    return n


def main():
    df = load_df()

    distances = np.array(list(df["phash"])).astype(np.float64)
    distances = distances / np.max(distances)
    print distances.dtype
    gw = 31
    bl_distances = cv2.GaussianBlur(distances, (3, 3), 0)
    # sns.plt.plot(bl)
    # sns.plt.show()
    # sys.exit()

    # distances = cv2.GaussianBlur(np.array(list(df["phash"])), (3, 3), 0)

    global_scores = stats.zscore(df["phash"])
    # global_scores = stats.zscore(bl_distances)
    # print global_scores
    z2 = np.sqrt(np.power(global_scores, 2))
    msz = np.average(z2)
    print "mean square globla z score : %f" % msz
    print len(z2[z2 > msz])

    # z2z = stats.zscore(z2)
    # print global_scores
    # z2z2 = np.sqrt(np.power(z2z, 2))

    z2_std = np.std(z2)
    k = 0.15
    k = 1.0
    print z2_std
    print(z2.dtype)
    # sys.exit()

    th = msz * (1 + k * z2_std)
    aw = 1
    th_n = 0.05 * len(z2)

    # while True:
    #     print "aw : %d" % aw
    #     bl = cv2.GaussianBlur(global_scores, (aw, aw), 0)
    #     n = len(bl[bl > th])
    #     # n = len(bl[bl > msz])
    #     print "n : %d" % n
    #     if n < th_n:
    #         break
    #     aw = aw + 2

    # global_scores = cv2.GaussianBlur(global_scores, (gw, gw), 0)

    # z2 = cv2.GaussianBlur(z2, (61, 61), 0)
    # Adaptive Gaussian Thresholding
    # th1 = cv2.adaptiveThreshold(blured, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    #                             cv2.THRESH_BINARY, 11, 2)

    bl = cv2.GaussianBlur(global_scores, (61, 61), 0)

    # sns.plt.plot(distances * (np.max(bl) - np.min(bl)) + np.min(bl))
    sns.plt.plot(distances * 4.0)
    # sns.plt.plot(global_scores)
    sns.plt.plot(bl)
    sns.plt.plot([0, len(global_scores)], [-msz, -msz])
    sns.plt.plot([0, len(global_scores)], [-th, -th])
    sns.plt.show()
    sys.exit()

    T = df[df["phash"] < 2].index

    half_window_func = half_window

    max_n = 30

    half_window_lut = np.array([half_window_func(n) for n in xrange(max_n)])

    for t in T:
        scores = np.array([z(df["phash"], t, hf) for hf in half_window_lut])
        argmax = half_window(np.argmax(scores))
        # print t
        # print hw
        # print scores

        # sns.plt.plot(half_window_lut, scores)
        # sns.plt.plot(half_window_lut[argmax], scores[argmax], "or")
        # sns.plt.savefig("./figures/z-hf/%04d" % t)
        # sns.plt.clf()


if __name__ == "__main__":
    main()
