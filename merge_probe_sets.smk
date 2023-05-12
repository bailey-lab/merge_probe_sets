configfile: 'merge_probe_sets.yaml'

rule all:
	input:
		merged_mip_arms_file=config['output_folder']+'/mip_ids/mip_arms',
		copied_yaml=config['output_folder']+'/run_settings/merge_probe_sets.yaml'

rule copy_files:
	input:
		snakemake='merge_probe_sets.smk',
		yaml='merge_probe_sets.yaml',
		python='merge_probe_sets.py'
	output:
		snakemake=config['output_folder']+'/run_settings/merge_probe_sets.smk',
		yaml=config['output_folder']+'/run_settings/merge_probe_sets.yaml',
		python=config['output_folder']+'/run_settings/merge_probe_sets.py'
	shell:
		'''
		cp {input.snakemake} {output.snakemake}
		cp {input.yaml} {output.yaml}
		cp {input.python} {output.python}
		'''

rule merge_probe_sets:
	input:
		probe_names=config['probe_names_file'],
		mip_arms_files=config['mip_arms_files']
	params:
		output_probe_set=config['output_folder'],
		include_exclude=config['include_exclude']
	output:
		merged_mip_arms_file=config['output_folder']+'/mip_ids/mip_arms',
#		merged_probe_info=config['output_folder']+'/mip_ids/'+config['merged_probe_info_file'],
		merged_mipsets=config['output_folder']+'/mip_ids/mipsets.csv'
	script:
		'merge_probe_sets.py'
