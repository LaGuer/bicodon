#!/usr/bin/env python3

import sys
import dill
import logging
import itertools
import pandas as pd
from Bio import SeqIO
from Bio.Seq import Seq
from collections import defaultdict,Counter

logger = logging.getLogger(__name__)


class Freqs:
    def __init__(self):
        self.codon = Counter()
        self.aa = Counter()
        self.bicodon = defaultdict(lambda: Counter())
        self.biaa = defaultdict(lambda: Counter())

    def _is_typical(self, cds_seq):
        """
        Check the following:
        * length is multiple of 3
        * Only ATGC used
        * No premature stop codon included
        """

        if len(cds_seq) % 3 != 0:
            logger.debug("not multiple of 3 ({})".format(len(cds_seq)))
            return False

        if not(set(cds_seq) <= set("ATGC")):
            logger.debug("unknown characters ({}) included".format(','.join(set(cds_seq) - set("ATGC"))))
            return False

        pro = cds_seq.translate(table=11)
        if "*" in pro[:-1]:
            logger.debug("inframe stop codon found")
            return False

        return True

    def update(self, cds_seq):
        """
        Args:
            cds_seq: Bio.Seq object
        """

        if not(self._is_typical(cds_seq)):
            return False

        pro_seq = cds_seq.translate(table=11)
        codons = [str(cds_seq[3*i:3*(i+1)]) for i in range(int(len(cds_seq)/3))]
        aas = list(cds_seq.translate())

        self.codon.update(codons)
        self.aa.update(aas)
        for i in range(len(codons)-1):
            self.bicodon[codons[i]][codons[i+1]] += 1
        for i in range(len(aas) - 1):
            self.biaa[aas[i]][aas[i+1]] += 1

        return True


def dump_freqs(freqs, fp):
    dill.dump(freqs, open(fp, "wb"))


def load_freqs(fp):
    return dill.load(open(fp, "rb"))


def calculate_pressure(freqs):
    """
    calculate bicodon pressure and return as pd.DataFrame
    """


    codons = [''.join(_) for _ in itertools.product("TCAG", repeat=3)]

    probs = dict()
    for codon in codons:
        aa = str(Seq(codon).translate(table=11))
        probs[codon] = freqs.codon[codon] / freqs.aa[aa] if freqs.aa[aa] > 0 else 0

    dct_lst = []
    for c1 in codons:
        for c2 in codons:
            bicodon = c1 + c2
            biaa = str(Seq(bicodon).translate(table=11))
            a1 = biaa[0]
            a2 = biaa[1]

            dct = {
                "bicodon": bicodon,
                "freq": freqs.bicodon[c1][c2],
                "pred": freqs.biaa[a1][a2] * probs[c1] * probs[c2]
            }
            dct_lst.append(dct)

    df = pd.DataFrame(dct_lst)
    df["pres"] = df["freq"] / df["pred"]
    return df


def main(cds_fp, out_fp):
    cdss = list(SeqIO.parse(cds_fp, 'fasta'))
    freqs = Freqs()
    cnt = 0
    for cds in cdss:
        cnt += freqs.update(cds.seq)
    logger.info("updated {}/{} cdss".format(cnt, len(cdss)))
    dump_freqs(freqs, out_fp)
    logger.info("output {}".format(out_fp))


if __name__ == "__main__":
    FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    streamHandler = logging.StreamHandler()
    streamHandler.setLevel(logging.INFO)
    logging.basicConfig(level=logging.DEBUG, handlers=[streamHandler],
                        format=FORMAT, datefmt='%m/%d/%Y %I:%M:%S')

    cds_fp = sys.argv[1]
    out_fp = sys.argv[2]
    main(cds_fp, out_fp)


