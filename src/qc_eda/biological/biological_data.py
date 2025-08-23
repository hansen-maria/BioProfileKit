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

import numpy as np
import pandas as pd

@dataclasses.dataclass
class DNA_RNA_Columns:
    gc_content: list[float] | None
    length: list[int] | None
    k_mers: list[str] | None
    nucleotide_count: dict[str, int] | None

def calculate_gc_content(sequence: str) -> float:
    if not sequence:
        return 0.00
    sequence = sequence.upper()
    gc_count = np.strings.count(sequence, 'G') + np.strings.count(sequence, 'C')
    total = len(sequence)
    return round((gc_count / total) * 100 if total > 0 else 0.00, 2)

def dna_rna_columns(df: pd.DataFrame, col) -> DNA_RNA_Columns:
    return DNA_RNA_Columns(
        gc_content= [calculate_gc_content(seq) for seq in df[col]],
        length=None,
        k_mers=[],
        nucleotide_count={}
        #length=df[col].str.len().tolist(),
        #k_mers=df[col].str.slice(0, 3).tolist(),
        #nucleotide_count=df[col].value_counts().to_dict()
    )