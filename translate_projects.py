"""
Translates raw project names into correct sequences names taking into account
that multiple samples have duplicated sequences
"""
from src import parser

if __name__ == "__main__":
    sequences = parser.read_fasta(ignore_seq=True)
    unique_sequences = parser.read_fasta(
        fasta_file="unique_sequences.fa", ignore_seq=True
    )
    new_names_csv_lines = []

    with open("exported_coordinates.csv", "r", encoding="UTF-8") as coords_file:
        coords = coords_file.readlines()
    for coord in coords:
        project_id, project_title, url = coord.strip().split(",")
        project_title = project_title.replace("batch_", "")
        for seq_name in unique_sequences:
            if project_title in seq_name:
                project_title = seq_name
        new_names_csv_lines.append(f"{project_id},{project_title},{url}\n")

    with open("exported_coordinates_final.csv", "w", encoding="UTF-8") as coords_file:
        for line in new_names_csv_lines:
            coords_file.write(line)
