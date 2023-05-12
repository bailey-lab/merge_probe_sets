# merge_probe_sets

## Installation:
Install conda (if you don't already have it) with:
https://github.com/conda-forge/miniforge#mambaforge

Install snakemake in an environment called snakemake with:
```bash
conda create -c conda-forge -c bioconda -n snakemake snakemake
```

## Usage:
 - Download the contents of this git repo to a folder of your machine.
 - Open the merge_probe_sets.yaml file and enter the name of the new project
folder you'd like to create in the output_folder variable (this can be a
relative or absolute path).
 - list locations of arms files you want to use under the "mip_arms_files"
 variable
 - tell the program if you'd like to 'include' or 'exclude' a list of probes
 with the 'include/exclude' variable
 - tell the program where your list of probes of interest is located with the
 variable probe_names_file (an example is provided here, in input_files/mip_ids.txt)
 - Activate snakemake with:
```bash
conda activate snakemake
```
 - Run snakemake with:
```bash
snakemake -s seekdeep_nanopore_general.smk --cores 4
```
