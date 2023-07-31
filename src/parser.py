"""
Module that parses multi-fasta files
"""


def read_fasta(fasta_file="sequences.fasta") -> list[tuple[str, str]]:
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
            sequences.append(
                (line[1:], file_str[i+1].strip())
            )
    return sequences
