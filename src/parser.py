"""
Module that parses multi-fasta files
"""


def read_fasta(fasta_file="sequences.fasta", ignore_seq=False) -> list[tuple[str, str]]:
    """
    Opens multi-FASTA file and returns list of pairs of sequences' name and sequence
    :param fasta_file: path to fasta file
    :return: list of sequences
    """
    sequences = []
    with open(fasta_file, 'r', encoding='UTF-8') as ffile:
        file_str = ffile.readlines()
        for i, line in enumerate(file_str):
            line = line.strip()
            if not (i + 1) % 2 != 0:
                continue
            if ignore_seq:
                sequences.append(line[1:])
            else:
                sequences.append(
                    (line[1:], file_str[i+1].strip())
                )
    return sequences

def unique_sequences_stats(sequences: list[tuple[str, str]]) -> dict:
    """
    Creates a dict with all names with same target sequence
    """
    unique_sequences = {}
    for name, seq in sequences:
        if seq in unique_sequences.keys():
            unique_sequences[seq].append(name)
            continue
        unique_sequences[seq] = [name]
    return unique_sequences

def export_unique_sequences_fasta(unique_sequences):
    """
    Creates a multi-Fasta file with all names corresponding to unique sequences
    """
    with open('unique_sequences.fa', 'w', encoding='UTF-8') as csvfile:
        for target_seq, names in unique_sequences.items():
            csvfile.write(f'>{"|".join(names)}\n{target_seq}\n')