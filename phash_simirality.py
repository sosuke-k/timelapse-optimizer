# coding=utf-8

import sys
import os
import numpy as np
import matplotlib.pyplot as plt
# import seaborn.plt as plt
import seaborn as sns
from PIL import Image
import imagehash


def get_hashs(datadir, filenames, hash_function=None):
    if hash_function is None:
        hashs = {
            "ahash": [],
            "phash": [],
            "dhash": [],
            # "whash": [],
        }
        for filename in filenames:
            print("Hashing %s" % filename)
            image = Image.open(os.path.join(datadir, filename))
            hashs["ahash"].append(imagehash.average_hash(image))
            hashs["phash"].append(imagehash.phash(image))
            hashs["dhash"].append(imagehash.dhash(image))
            # hashs["whash"].append(imagehash.whash(image))
            del image
    else:
        hashs = []
        for filename in filenames:
            print("Hashing %s" % filename)
            image = Image.open(os.path.join(datadir, filename))
            hashs.append(hash_function(image))
            del image

    return hashs


def get_similarities(hashs):

    def _get_similarities(hashs):
        n = len(hashs) - 1
        _similarities = [0]
        for i in xrange(n):
            _similarities.append(hashs[i + 1] - hashs[i])

        return np.array(_similarities)

    if isinstance(hashs, list):
        return _get_similarities(hashs)
    elif isinstance(hashs, dict):
        similarities = {}
        for key in hashs.keys():
            similarities[key] = _get_similarities(hashs[key])

        return similarities


def check_similarity(datadir="./data/images/001", filename_format="DSC%05d.JPG", start=416, n=3000):
    filenames = [(filename_format % i) for i in xrange(start, start + n)]

    hashs = get_hashs(datadir, filenames, hash_function=imagehash.phash)
    similarities = get_similarities(hashs)

    for i in xrange(len(filenames)):
        print("{0}\t{1}\t{2}".format(filenames[i], hashs[i], similarities[i]))


def output_graph_images(similarities, outputdir="./output", filename_format="sim_%05d.png"):
    hashnames = similarities.keys()

    n = len(similarities[hashnames[0]])
    x = np.arange(n)

    simmax = {}
    for hashname in hashnames:
        simmax[hashname] = np.max(similarities[hashname])

    for i in xrange(n):
        if i % 100 == 0:
            print("%5d/%d" % (i, n))

        for hashname in hashnames:
            plt.plot(x, similarities[hashname], label=hashname)
            plt.plot([i, i], [0, simmax[hashname]], color="red")
            plt.plot(i, similarities[hashname][i], "om")

            plt.legend(loc=2)
            # plt.show()
            plt.savefig(os.path.join(outputdir, hashname + "_" + (filename_format % i)))
            plt.clf()


def output_similarity_tsv(filenames, similarities, outputdir="./data/tsv", filename="sim.tsv"):
    n = len(filenames)
    hashnames = similarities.keys()

    f = open(os.path.join(outputdir, filename), "w")
    line = ",".join(["name"] + hashnames) + "\n"
    f.write(line)
    for i in xrange(n):
        line = ",".join([filenames[i]] + [("%d" % similarities[hashname][i])
                                          for hashname in hashnames]) + "\n"
        f.write(line)

    f.close()


def output_similarity_graph(datadir="./data/images/001", filename_format="DSC%05d.JPG", start=416, n=3000):
    print("Creating filenames")
    filenames = [(filename_format % i) for i in xrange(start, start + n)]

    hashs = get_hashs(datadir, filenames)
    similarities = get_similarities(hashs)
    # output_graph_images(similarities)
    output_similarity_tsv(filenames, similarities)


if __name__ == "__main__":
    # check_similarity(n=20)
    output_similarity_graph()
