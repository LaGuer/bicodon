#!/usr/bin/env python3

import pandas as pd

species_fp = "/home/mitsuki/rsyncdir/files/species.csv"
species_df = pd.read_csv(species_fp)

for _, row in species_df.iterrows():
    infp = "{}/{}_cds_from_genomic.fna.gz".format(row["ftp_path"], row["ftp_basename"])
    outfp = "/home/mitsuki/sandbox/bicodon/data/cds/{}_cds_from_genomic.fna".format(row["taxid"])
    print("{},{}".format(infp, outfp))
