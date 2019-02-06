#!/usr/bin/env python3

import sys
import pandas as pd

out_fp = sys.argv[1]

ref_fp = "./data/refseq.csv"
ref_df = pd.read_csv(ref_fp)
ref_df["in"] = ref_df["ftp"].map(lambda x:"{}/{}_cds_from_genomic.fna.gz".format(x, x.split('/')[-1]))
ref_df["out"] = ref_df["acc"].map(lambda x:"/home/mitsuki/bicodon/data/cds/{}.fna".format(x))
ref_df[["in", "out"]].to_csv("./arg/wget.lst", index=False, header=None)
print("output {}".format(out_fp))

