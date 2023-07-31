from itertools import groupby


def read_fasta(fasta_file="sequences.fasta"):
    sequences = []
    with open(fasta_file, 'r', encoding='UTF-8') as ff:
        file_str = ff.readlines()
        for i, line in enumerate(file_str):
            line = line.strip()
            if not (i + 1) % 2 != 0:
                continue
            sequences.append(
                (line[1:], file_str[i+1].strip())
            )
    return sequences
