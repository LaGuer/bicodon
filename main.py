#!/usr/bin/env python3

import sys
import pickle
import numpy as np
from Bio import SeqIO

from helper import BiasTracker

def solve(fp):
    rec_lst = []
    for rec in SeqIO.parse(fp, "fasta"):
        rec_lst.append(rec)
#    print("found {} cds".format(len(rec_lst)))

    bt = BiasTracker()
    for rec in rec_lst:
        bt.update(rec.seq)
    bt.calculate()
    return bt

def main(fp_cds, fp_pkl):
    print("START: {}".format(fp_cds))
    bt = solve(fp_cds)
    pickle.dump(bt, open(fp_pkl, "wb"))
    print("DONE: {}".format(fp_pkl))

if __name__=="__main__":
    fp_cds = sys.argv[1]
    fp_pkl = sys.argv[2]
    main(fp_cds, fp_pkl)
