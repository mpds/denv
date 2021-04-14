"""Align target and tamplate sequences.

This script was adapted from `align2d.py`, obtained
from MODELLER's website (copyright © 1989-2021 Andrej Sali).
"""
import argparse
import os

import modeller as mod


def main(args):
    mod.log.verbose()
    env = mod.environ()
    env.io.atom_files_directory = [".", args.dir, "../" + args.dir]
    aln = mod.alignment(env)

    mdl = mod.model(
        env,
        file=args.template,
        model_segment=(
            "FIRST:" + args.chains[0].upper(),
            "LAST:" + args.chains[1].upper(),
        ),
    )
    aln.append_model(
        mdl, align_codes=args.template.replace(".pdb", ""), atom_files=args.template
    )

    sequence_file = os.path.join(args.dir, args.target)
    sequence_code = args.target.replace(".ali", "")
    aln.append(file=sequence_file, align_codes=sequence_code)

    aln.align2d()  # perform alignment
    align_file = os.path.join(
        args.dir, sequence_code + "-" + args.template.replace(".pdb", "")
    )
    aln.write(file=align_file + ".ali", alignment_format="PIR")  # para o modeller
    aln.write(file=align_file + ".pap", alignment_format="PAP")  # +fácil de ler

    # check files
    aln.check()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Script to align target and tamplate sequences."
    )
    parser.add_argument("-t", "--template", type=str, help="PDB code of template")
    parser.add_argument(
        "-r", "--target", type=str, help="Target sequence file (in PIR format, .ali)"
    )
    parser.add_argument(
        "-c",
        "--chains",
        type=str,
        help="First and last chain to be used (e.g. AB). In case of using just one chain, repeat it's letter (e.g. AA)",
    )
    parser.add_argument(
        "-d", "--dir", type=str, help="Path to dir containing input files"
    )
    args = parser.parse_args()

    assert len(args.chains) == 2, "two letters format (e.g. AB)"
    assert args.chains.isalpha(), "only letters"

    main(args)
