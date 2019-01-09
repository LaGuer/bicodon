import sys
import numpy as np
from collections import defaultdict

translTable = "FFLLSSSSYY**CC*WLLLLPPPPHHQQRRRRIIIMTTTTNNKKSSRRVVVVAAAADDEEGGGG"


def is_typical(seq):
    if len(seq) < 6 or len(seq) % 3 != 0:
        return False
    if not(set(str(seq)) <= set("ATGC")):
        return False
    pro = seq.translate()
    if "*" in pro[:-1]:
        return False
    return True


class InvertedIndex:
    def __init__(self):
        self.bicodon_dct = defaultdict(list)
        self.biaa_dct = defaultdict(list)

    def update_bicodon(self, seq_id, seq):
        for i in range(1, len(seq)//3):
            bicodon = str(seq[(i-1)*3 : (i+1)*3])
            position = i / (len(seq)//3)
            self.bicodon_dct[bicodon].append((seq_id, position))

    def update_biaa(self, seq_id, seq):
        pro = seq.translate()
        for i in range(1, len(pro)):
            biaa = str(pro[i-1:i+1])
            position = i / len(pro)
            self.biaa_dct[biaa].append((seq_id, position))

    def update(self, seq_id, seq):
        if is_typical(seq):
            self.update_bicodon(seq_id, seq)
            self.update_biaa(seq_id, seq)


class BiasTracker:
    def __init__(self):
        self.codec = Codec()

        self.codon_c = np.zeros(64).astype(int)
        self.bicodon_c = np.zeros((64, 64)).astype(int)
        self.aa_c = np.zeros(21).astype(int)
        self.biaa_c = np.zeros((21, 21)).astype(int)


    def update_codon(self, seq):
        for i in range(len(seq)//3):
            codon = seq[3 * i : 3 * i + 3]
            self.codon_c[self.codec.codon_encode(codon)] += 1

    def update_bicodon(self, seq):
        prv = self.codec.codon_encode(seq[0 : 3])
        for i in range(1, len(seq)//3):
            nxt = self.codec.codon_encode(seq[3 * i : 3 * i + 3])
            self.bicodon_c[prv][nxt] += 1
            prv = nxt

    def update_aa(self, seq):
        pro = seq.translate()
        for aa in pro:
            self.aa_c[self.codec.aa_encode(aa)] += 1

    def update_biaa(self, seq):
        pro = seq.translate()
        prv = self.codec.aa_encode(pro[0])
        for aa in pro[1:]:
            nxt = self.codec.aa_encode(aa)
            self.biaa_c[prv][nxt] += 1
            prv = nxt

    def update(self, seq):
        if is_typical(seq):
            self.update_codon(seq)
            self.update_bicodon(seq)
            self.update_aa(seq)
            self.update_biaa(seq)
        else:
            #print("WARN: found atypical cds", file=sys.stderr)
            pass


    def calculate_frequency(self):
        def mask(aa):
            msk = np.zeros(64).astype(bool)
            for i in range(64):
                if translTable[i] == aa:
                    msk[i] = True
            return msk

        codon_f = np.zeros(64)
        for aa in self.codec.aa_lst:
            total = self.aa_c[self.codec.aa_encode(aa)]
            msk = mask(aa)
            assert self.codon_c[msk].sum() == total

            if total > 0:
                codon_f[msk] = self.codon_c[msk] / total
            elif total == 0:
                codon_f[msk] = np.zeros(msk.sum())
        self.codon_f = codon_f

    def calculate_hypothesis(self):
        bicodon_h = np.zeros((64, 64))
        for i in range(64):
            for j in range(64):
                prv = self.codec.aa_encode(translTable[i])
                nxt = self.codec.aa_encode(translTable[j])
                bicodon_h[i][j] = self.biaa_c[prv][nxt] * self.codon_f[i] * self.codon_f[j]
        self.bicodon_h = bicodon_h

    def calculate_pressure(self):
        self.bicodon_p = self.bicodon_c / (self.bicodon_h+1)

    def calculate(self):
        self.calculate_frequency()
        self.calculate_hypothesis()
        self.calculate_pressure()


class Codec:
    def _codon_encode(self, codon):
        assert len(codon) == 3
        codon = codon.upper()
        try:
            score = 0
            base = 1
            for c in codon[::-1]:
                score += self.dna_lst.index(c) * base
                base *= 4
        except ValueError:
            print("ERROR: unusual base found in {}".format(codon), file=sys.stderr)
            return -1
        else:
            return score

    def __init__(self):
        self.dna_lst = list("TCAG")
        self.aa_lst = list("ACDEFGHIKLMNPQRSTVWY*")

        self.codon2id = {}
        self.id2codon = {}
        for i in self.dna_lst:
            for j in self.dna_lst:
                for k in self.dna_lst:
                    codon = i + j + k
                    codonid = self._codon_encode(codon)
                    self.codon2id[codon] = codonid
                    self.id2codon[codonid] = codon

        self.aa2id = {}
        self.id2aa = {}
        for i, aa in enumerate(self.aa_lst):
            self.aa2id[aa] = i
            self.id2aa[i] = aa

    def codon_encode(self, codon):
        assert len(codon) == 3
        codon = str(codon).upper()
        return self.codon2id[codon]

    def codon_decode(self, codonid):
        assert 0 <= codonid and codonid < 64
        return self.id2codon[codonid]

    def aa_encode(self, aa):
        assert len(aa) == 1
        return self.aa2id[aa]

    def aa_decode(self, aaid):
        assert 0 <= aaid and aaid < 21
        return self.id2aa[aaid]
