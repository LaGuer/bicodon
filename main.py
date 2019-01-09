#!/usr/bin/env python3

import sys
import pickle
from Bio import SeqIO

from helper import BiasTracker, InvertedIndex


def solve_bt(fp_cds):
    bt = BiasTracker()
    for rec in SeqIO.parse(fp_cds, "fasta"):
        bt.update(rec.seq)
    bt.calculate()
    return bt

def solve_ii(fp_cds):
    ii = InvertedIndex()
    for seq_id, rec in enumerate(SeqIO.parse(fp_cds, "fasta")):
        ii.update(seq_id, rec.seq)
    return ii


def main(fp_cds, fp_bt, fp_ii):
    print("START: {}".format(fp_cds))

    bt = solve_bt(fp_cds)
    pickle.dump(bt, open(fp_bt, "wb"))
    print("DONE: {}".format(fp_bt))

    ii = solve_ii(fp_cds)
    pickle.dump(ii, open(fp_ii, "wb"))
    print("DONE: {}".format(fp_ii))


if __name__=="__main__":
    fp_cds = sys.argv[1]
    fp_bt = sys.argv[2]
    fp_ii = sys.argv[3]
    main(fp_cds, fp_bt, fp_ii)
