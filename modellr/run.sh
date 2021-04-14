#!/bin/bash

while [[ "$#" -gt 0 ]]; do
    case $1 in
        -r|--target) target="$2"; shift ;;
        -t|--template) template="$2"; shift ;;
        -c|--chains) chains="$2"; shift ;;
        -d|--dir) dir="$2"; shift ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done

echo -e "use 'python modellr/[script.py] -h' to get info about params."
echo -e "log files will be saved in $dir\n"

echo "perform alignment of target and template sequences..."
echo -e "python ./align2d.py --template $template --target $target --chains $chains --dir $dir\n"
python ./align2d.py --template $template --target $target --chains $chains --dir $dir > $dir"/align2d.log"

echo "build models..."
echo -e "python ./build_model.py --template $template --target $target --dir $dir\n"
python ./build_model.py --template $template --target $target --dir $dir > $dir"/build_model.log"

echo "evaluate best model (DOPE score)..."
# get best model name using build_model.log last line
model=$(tail -n 1 $dir"/build_model.log")
echo -e "python ./evaluate_model.py --model $model --template $template --chains $chains --target $target --dir $dir\n"
python ./evaluate_model.py --model $model --template $template --chains $chains --target $target --dir $dir > $dir"/evaluate_model.log"

# to install procheck,
# refer to https://www.ebi.ac.uk/thornton-srv/software/PROCHECK/download.html
# otherwise, just comment all the lines below

################################################## PROCHECK CMDS
echo "run procheck"

# declare aliases
shopt -s expand_aliases
source ~/.bashrc
prodir='/home/mpds/.local/share/procheck'
export prodir
alias procheck=$prodir'/procheck.scr'
alias procheck_comp=$prodir'/procheck_comp.scr'
alias procheck_nmr=$prodir'/procheck_nmr.scr'
alias proplot=$prodir'/proplot.scr'
alias proplot_comp=$prodir'/proplot_comp.scr'
alias proplot_nmr=$prodir'/proplot_nmr.scr'
alias aquapro=$prodir'/aquapro.scr'
alias gfac2pdb=$prodir'/gfac2pdb.scr'
alias viol2pdb=$prodir'/viol2pdb.scr'
alias wirplot=$prodir'/wirplot.scr'

# run procheck
echo -e "procheck $dir/$model 2.0\n"
procheck $dir/$model 2.0
mkdir $dir/procheck  # procheck results folder
mv *.ps *.sum $dir/procheck  # clean up
mv *.log $dir/procheck
name=${target%.ali}
rm *.prm $name.*
################################################## PROCHECK END
