#!/usr/bin/env python3

import glob

fp_lst = glob.glob("./data/cds/*_cds_from_genomic.fna")
for fp in fp_lst:
    id_ = fp.split('/')[-1].replace("_cds_from_genomic.fna", "")
    fp_pkl = "./data/pkl/{}_bt.pkl".format(id_)
    print("{},{}".format(fp, fp_pkl))
