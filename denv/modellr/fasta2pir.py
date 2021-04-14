"""Very basic script to convert FASTA to PIR format."""

import argparse
import os


def convert_to_pir(sequence, fasta, output=""):
    header = ">P1;{0}\nsequence:{0}:::::::0.00: 0.00\n".format(sequence["header"])
    seq = sequence["data"] + "*"  # end of sequence

    output = os.path.join(output, fasta.replace(".fasta", ".ali"))
    with open(output, "w") as f:
        f.write(header)
        f.write(seq + "\n")


def get_sequence(file):
    # reads one sequence from a fasta file
    sequence = {"header": None, "data": None}

    with open(file, "r") as f:
        data = []
        for line in f.readlines():
            if line.startswith(">"):
                sequence["header"] = line[1:].lstrip().strip("\n")
            else:
                data.append(line.strip("\n"))
        sequence["data"] = "".join(data)

    return sequence


def main(args):
    res = get_sequence(args.fasta)
    convert_to_pir(res, os.path.basename(args.fasta), args.output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Very basic script to convert FASTA to PIR format."
    )
    parser.add_argument("-f", "--fasta", type=str, help="fasta file with one sequence")
    parser.add_argument("-o", "--output", type=str, help="output path", default="")
    main(parser.parse_args())
