"""Build target models using automodel class.

This script was adapted from `model_single.py`, obtained
from MODELLER's website (copyright © 1989-2021 Andrej Sali).
"""
import os
import argparse

import modeller as mod
from modeller import automodel
from modeller import soap_protein_od


def main(args):
    mod.log.verbose()
    env = mod.environ(rand_seed=args.seed)
    env.io.atom_files_directory = [".", args.dir, "../" + args.dir]

    seq = args.target.replace(".ali", "")
    alnfile = os.path.join(args.dir, seq + "-" + args.template.replace(".pdb", ".ali"))

    # in order to use the soap assess method, refer to https://salilab.org/SOAP/ and
    # download the SOAP-Protein library file. Put this file in
    # your-installation-path/lib/modeller-9.25/modlib/
    # otherwise, just comment the respective line
    a = automodel.automodel(
        env,
        alnfile=alnfile,
        knowns=args.template.replace(".pdb", ""),
        sequence=seq,
        assess_methods=(
            automodel.assess.DOPE,
            automodel.assess.GA341,
            # soap_protein_od.Scorer(),
        ),
    )

    a.starting_model, a.ending_model = 1, args.num_models
    a.make()

    # get list of all successfully built models from a.outputs
    models = [m for m in a.outputs if m["failure"] is None]
    key = "DOPE score"
    models.sort(key=lambda a: a[key])

    # print and return top model DOPE score
    top_model = models[0]
    print("Top model: %s (DOPE score %.3f)" % (top_model["name"], top_model[key]))
    return top_model["name"]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Build target model using automodel class."
    )
    parser.add_argument("-t", "--template", type=str, help="PDB code of template")
    parser.add_argument(
        "-r", "--target", type=str, help="Target sequence file (in PIR format, .ali)"
    )
    parser.add_argument(
        "-d", "--dir", type=str, help="Path to dir containing input files"
    )
    parser.add_argument(
        "-s",
        "--seed",
        type=int,
        default=-1994,
        help="Change seed to get a different model (default: -1994)",
    )
    parser.add_argument(
        "-n",
        "--num-models",
        type=int,
        default=3,
        help="Number of models to generate (default: 5)",
    )
    args = parser.parse_args()

    res = main(args)
    print(res)  # top model file (DOPE score)
    os.system("mv {}.* {}".format(args.target.replace(".ali", ""), args.dir))
