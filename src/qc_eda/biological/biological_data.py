"""
Value counts for String/Text
DNA/RNA: GC content, length, k-Mers, Nucleotide count
Proteins: AA composition, frequency, hydrophobicity/hydrophilicity, charge distribution, molecular weight,
isoelectric point, motifs, entropy, aliphatic index, Boman index, aromaticity, instability index,
Taxonomy: capitalization patterns, potentially invalid names,
strain info in separate field => Flag for 2 Columns?
lab measurements; units
"""
import dataclasses

import pandas as pd
from Bio.SeqUtils import GC

@dataclasses
class DNA_RNA_Columns:
    gc_content: float
    length: int
    k_mers: list[str]
    nucleotide_count: dict[str, int]

