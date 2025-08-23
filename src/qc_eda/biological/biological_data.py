"""
Value counts for String/Text
DNA/RNA: GC content, length, k-Mers, Nucleotide count
Proteins: AA composition, frequency, hydrophobicity/hydrophilicity, charge distribution, molecular weight,
isoelectric point, motifs, entropy, aliphatic index, Boman index, aromaticity, instability index,
Taxonomy: capitalization patterns, potentially invalid names,
strain info in separate field => Flag for 2 Columns?
lab measurements; units
"""
from collections import defaultdict, Counter
from dataclasses import dataclass
from itertools import chain
from typing import List, Dict, Tuple

import numpy as np
import pandas as pd
import plotly.express as px


@dataclass
class DNARNAColumns:
    sequence: List[str]
    gc_content: List[float]
    length: List[int]
    count: List[int]
    nucleotide_count: List[Dict[str, int]]
    k_mers: List[List[Tuple[str, int]]]
    plot: str | None


def count_nmer(sequence, n) -> defaultdict:
    seqs = np.frombuffer(sequence.encode('utf-8'), dtype='S1')
    nmere = np.lib.stride_tricks.sliding_window_view(seqs, n)
    unique, counts = np.unique(nmere, return_counts=True, axis=0)
    result = defaultdict(int)
    for nmer, count in zip(unique, counts):
        nmer_str = b"".join(nmer).decode('utf-8')
        result[nmer_str] += count
    return result


def top_mere(seq, n=3, top=5) -> List[Tuple[str, int]] | None:
    if not seq or len(seq) < n:
        return None
    counts = count_nmer(seq, n)
    return sorted(counts.items(), key=lambda x: x[1], reverse=True)[:top]


def dna_rna_columns(seqs: pd.Series, k: int = 3, top_n: int = 5) -> DNARNAColumns:
    arr = np.char.upper(seqs.to_numpy(dtype=str))
    uniq_tmp, counts_tmp = np.unique(arr, return_counts=True)

    top_idx = np.argsort(counts_tmp)[::-1][:20]
    uniques = uniq_tmp[top_idx]
    counts = counts_tmp[top_idx]

    min_len, max_len = min(len(s) for s in uniques), max(len(s) for s in uniques)

    gc_count = np.char.count(uniques, 'G') + np.char.count(uniques, 'C')
    lengths = np.char.str_len(uniques).astype(int)
    gc_content = np.round(np.where(lengths > 0, gc_count / lengths * 100, 0.0), 2).tolist()

    nucleotide_count = [dict(Counter(seq)) for seq in uniques]
    k_mers = [top_mere(seq, n=k, top=top_n) for seq in uniques]
    barplot = None
    if min_len == max_len:
        use_logo = True
        k = min(6, min_len)
        print("logo")
    else:
        use_logo = False
        k = 3 if max_len >= 6 else 2
        # Flache Liste mit chain erstellen
        flat_kmers = chain.from_iterable(kmers_seq for kmers_seq in k_mers if kmers_seq)
        kmers, count = zip(*((kmer, np.int64(count)) for kmer, count in flat_kmers))
        barplot = plot_overview(kmers, count)

    return DNARNAColumns(
        sequence=uniques.tolist(),
        gc_content=gc_content,
        length=lengths.tolist(),
        count=counts.tolist(),
        nucleotide_count=nucleotide_count,
        k_mers=k_mers,
        plot=barplot
    )


def plot_overview(kmer, count):
    fig = px.bar(x=kmer, y=count, height=350, color_discrete_sequence=['#0F65A0'])
    fig.update_layout(bargap=0.2, plot_bgcolor='white', xaxis_title='K-mers',
        yaxis_title='Count')
    fig.update_xaxes(
        mirror=True,
        ticks='outside',
        showline=True,
        linecolor='black',
        gridcolor='lightgrey',
        tickangle=-45

    )
    fig.update_yaxes(
        mirror=True,
        ticks='outside',
        showline=True,
        linecolor='black',
        gridcolor='lightgrey'
    )
    fig.write_image("test.png")
    return fig.to_html(full_html=False, include_plotlyjs='cdn')
