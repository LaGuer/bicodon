#!/usr/bin/env python3

import glob

fp_cds_lst = glob.glob("./data/cds/*_cds_from_genomic.fna")
for fp_cds in fp_cds_lst:
    tax_id = fp_cds.split('/')[-1].replace("_cds_from_genomic.fna", "")
    fp_bt = "./data/bt/{}_bt.pkl".format(tax_id)
    fp_ii = "./data/ii/{}_ii.pkl".format(tax_id)
    print("{},{},{}".format(fp_cds, fp_bt, fp_ii))
