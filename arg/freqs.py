#!/usr/bin/env python3

import sys
import pandas as pd

out_fp = sys.argv[1]

ref_fp = "./data/refseq.csv"
ref_df = pd.read_csv(ref_fp)
ref_df = ref_df[ref_df["genetic_code"]==11].copy() #only table 11 for now
ref_df["in"] = ref_df["acc"].map(lambda x:"/home/mitsuki/bicodon/data/cds/{}.fna".format(x))
ref_df["out"] = ref_df["acc"].map(lambda x:"/home/mitsuki/bicodon/data/freqs/{}.freqs".format(x))
ref_df[["in", "out"]].to_csv(out_fp, index=False, header=None)
print("output {}".format(out_fp))
