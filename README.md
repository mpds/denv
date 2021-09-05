Publication: https://journals.asm.org/doi/10.1128/Spectrum.00256-21

# Scripts usage

Install dependencies using [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-from-an-environment-yml-file):
```
conda env create -f environment.yml
```

## MODELLER
First, `cd modellr`. 

To generate models, you will need at least two inputs: 
* target sequence in FASTA format;
* template structure in PDB format.

Target sequences must be converted to PIR format before proceeding. A script `fasta2pir.py` for simple cases is available.

Usage:
```
fasta2pir.py [-h] [-f FASTA] [-o OUTPUT]

Very basic script to convert FASTA to PIR format.

arguments:
  -h, --help            show this help message and exit
  -f FASTA, --fasta FASTA
                        fasta file with one sequence
  -o OUTPUT, --output OUTPUT
                        output path
```

Example:
```
python fasta2pir.py --fasta files/basic-example/ns3#123.fasta --output files/basic-example/
```

All set, you can build models using the `run.sh` script, which uses `align2d.py`, `build_model.py`, `evaluate_model.py`, and also runs [PROCHECK](https://www.ebi.ac.uk/thornton-srv/software/PROCHECK/download.html) with the best model obtained as input, if the software is installed.

To use the bash script:
```
bash.sh [--template TEMPLATE] [--target TARGET] [--chains CHAINS] [--dir DIR]

arguments:
  --template TEMPLATE
                        PDB file of the template
  --target TARGET
                        Target sequence file (in PIR format, .ali)
  --chains CHAINS
                        First and last chain to be used (e.g. AB). In case of using just one chain, repeat it's letter (e.g. AA)
  --dir DIR     
                        Path to dir containing input files
```

Example:
```
bash run.sh --target ns3#123.ali --template 5yw1.pdb --chains BB --dir files/basic-example
```

This script generates several output files and logs (see the MODELLER [manual](https://salilab.org/modeller/manual/) for details), including alignment files (`.ali` and `.pap`) and a quality assessment plot such as the one below. Also, a folder named `procheck` is created containing the PROCHECK results. 

![ns3#123-5yw1_dope](https://user-images.githubusercontent.com/25796259/114647974-5f309d80-9cb4-11eb-979b-9c33d5e78170.png)


