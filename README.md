# merge_probe_sets
This program is for people who want to run miptools wrangler on a subset of
probes from several different probesets. It takes (or excludes) a subset of
probes of interest from several different mip_arms files, and produces a new
project folder containing a merged mip_arms file and mipsets.csv file that have
only the probes you want. This new merged folder can then serve as a project
folder for running miptools wrangler. For each merger, you'll need to provide
(in the merge_probe_sets.yaml file):
 - a list of mip_arms files you'd like to merge
 - a list of probes of interest (to include or exclude for your merger)

## Installation:
Install conda (if you don't already have it) with:
https://github.com/conda-forge/miniforge#mambaforge

Install snakemake in an environment called snakemake with:
```bash
conda create -c conda-forge -c bioconda -n snakemake snakemake
```

## Usage:
 - Download the contents of this git repo to a folder on your machine and cd
 into that folder (so that "ls" shows merge_probe_sets.smk).
 - Open the merge_probe_sets.yaml file and enter the name of the new project
folder you'd like to create in the "output_folder" variable (this can be a
relative or absolute path). Use a text editor that outputs unix line endings
(e.g. vscode, notepad++, gedit, micro, emacs, vim, vi, etc.).
 - list locations of arms files you want to use under the "mip_arms_files"
 variable
 - tell the program if you'd like to "include" or "exclude" a list of probes
 with the "include/exclude" variable
 - tell the program where your list of probes of interest is located with the
 variable "probe_names_file" (an example is provided here, in
 input_files/mip_ids.txt)
 - Activate snakemake with:
```bash
conda activate snakemake
```
 - Run snakemake with:
```bash
snakemake -s merge_probe_sets.smk --cores 4
```
