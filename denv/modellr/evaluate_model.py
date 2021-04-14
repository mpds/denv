"""Evaluate model with DOPE per-residue score.

This script was adapted from `evaluate_model.py` and `plot_profiles.py`, obtained
from MODELLER's website (copyright © 1989-2021 Andrej Sali).
"""
import os
import argparse

import modeller as mod
from modeller.scripts import complete_pdb  # read PDB file for energy calculations
from matplotlib import pylab


def r_enumerate(seq):
    """Enumerate a sequence in reverse order."""
    # Note that we don't use reversed() since Python 2.3 doesn't have it
    num = len(seq) - 1
    while num >= 0:
        yield num, seq[num]
        num -= 1


def get_profile(profile_file, seq):
    """Read `profile_file` into a Python array."""
    # Read all non-comment and non-blank lines from the file
    f = open(profile_file)
    vals = []
    for line in f:
        if not line.startswith("#") and len(line) > 10:
            spl = line.split()
            vals.append(float(spl[-1]))

    # Insert gaps into the profile corresponding to those in seq
    for n, res in r_enumerate(seq.residues):
        for gap in range(res.get_leading_gaps()):
            vals.insert(n, None)

    # Add a gap at position '0', so that we effectively count from 1
    vals.insert(0, None)
    return vals


def plot(target, template, model, dir):
    """Plot model and template profiles."""
    e = mod.environ()

    seq_code = target.replace(".ali", "")
    alnfile = os.path.join(dir, seq_code + "-" + template.replace(".pdb", ".ali"))
    a = mod.alignment(e, file=alnfile)

    pdb_code = template.replace(".pdb", "")
    target_profile = os.path.join(dir, pdb_code + ".profile")
    model_profile = os.path.join(dir, model.replace(".pdb", ".profile"))
    t = get_profile(target_profile, a[pdb_code])
    m = get_profile(model_profile, a[seq_code])

    # plot the template and model profiles in the same plot for comparison
    pylab.figure(1, figsize=(10, 6))
    pylab.xlabel("Alignment position")
    pylab.ylabel("DOPE per-residue score")
    pylab.plot(m, color="red", linewidth=2, label=f"Model ({model})")
    pylab.plot(t, color="green", linewidth=2, label=f"Template ({template})")
    pylab.legend()
    pylab.title("DOPE score model vs. template")
    pylab.savefig(f"{seq_code}-{pdb_code}_dope.png", dpi=150)


def main(args):
    mod.log.verbose()
    env = mod.environ()
    env.io.atom_files_directory = [".", args.dir, "../" + args.dir]

    env.libs.topology.read(file="$(LIB)/top_heav.lib")  # read topology
    env.libs.parameters.read(file="$(LIB)/par.lib")  # read parameters

    # assess model using DOPE
    model = complete_pdb(env, args.model)  # read model file
    s = mod.selection(model)  # all atoms selection
    s.assess_dope(
        output="ENERGY_PROFILE NO_REPORT",
        file=args.model.replace(".pdb", ".profile"),
        normalize_profile=True,
        smoothing_window=15,
    )

    # assess template using DOPE
    template = complete_pdb(
        env,
        args.template,
        model_segment=(
            "FIRST:" + args.chains[0].upper(),
            "LAST:" + args.chains[1].upper(),
        ),
    )
    s = mod.selection(template)  # all atoms selection
    s.assess_dope(
        output="ENERGY_PROFILE NO_REPORT",
        file=args.template.replace(".pdb", ".profile"),
        normalize_profile=True,
        smoothing_window=15,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=" Evaluate model with DOPE per-residue score and plot results."
    )
    parser.add_argument("-t", "--template", type=str, help="PDB file of template")
    parser.add_argument(
        "-r", "--target", type=str, help="Target sequence file (in PIR format, .ali)"
    )
    parser.add_argument(
        "-m", "--model", type=str, help="PDB file of selected model to evaluate"
    )
    parser.add_argument(
        "-c",
        "--chains",
        type=str,
        help="First and last chain to include (e.g. AB). In case of using just one chain, repeat it's letter (e.g. AA)",
    )
    parser.add_argument(
        "-d", "--dir", type=str, help="Path to dir containing input files"
    )
    args = parser.parse_args()

    main(args)
    os.system(f"mv *.profile {args.dir}")
    plot(args.target, args.template, args.model, args.dir)
    os.system(f"mv *.png {args.dir}")
