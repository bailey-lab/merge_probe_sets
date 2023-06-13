import json
probe_names=set([line.strip() for line in open(snakemake.input['probe_names'])])
mip_arms_files=snakemake.input['mip_arms_files']
output_probe_set=snakemake.params['output_probe_set'].split('/')[-1]
include_exclude=snakemake.params['include_exclude']
merged_mip_arms=open(snakemake.output['merged_mip_arms_file'], 'w')
#merged_probe_info=open(snakemake.output['merged_probe_info'], 'w')
merged_mipsets=open(snakemake.output['merged_mipsets'], 'w')
call_info=snakemake.output['call_info']

header=['gene_name', 'mip_family', 'mip_id', 'extension_arm', 'ligation_arm', 'extension_barcode_length', 'ligation_barcode_length', 'mipset', 'chrom', 'begin', 'end']
merged_mip_arms.write('\t'.join(header)+'\n')
arm_dict={}
seen_mips=set([])

def parse_arms_file(arms_file):
	import csv
	marker_reader=csv.DictReader(open(arms_file), delimiter='\t')
	for row in marker_reader:
		mip_family=row['mip_family']
		ligation_arm=row['ligation_arm']
		extension_arm=row['extension_arm']
		arm_tuple=(ligation_arm, extension_arm)
		seen_mips.add(mip_family)
		if ((include_exclude=='include' and mip_family in probe_names) or
		(include_exclude=='exclude' and mip_family not in probe_names)):
			if arm_tuple not in arm_dict:
				arm_dict[arm_tuple]=mip_family
				merged_mipsets.write(mip_family+'\n')
				new_line=[]
				for column in header:
					if column in row and type(row[column])==str:
						new_line.append(row[column])
					else:
						new_line.append('')
				merged_mip_arms.write('\t'.join(new_line)+'\n')
			elif arm_tuple in arm_dict and mip_family!=arm_dict[arm_tuple]:
				print(f'ERROR: the probes {mip_family} and {arm_dict[arm_tuple]}'
				f' both have the same mip arms. Please remove redundant mip ids'
				' and run again')
				exit()

def parse_call_info(arms_file, overall_json_dict):
	call_info_file='/'.join(arms_file.split('/')[:-1])+'/call_info.json'
	json_dict=json.load(open(call_info_file))
	for gene in json_dict:
		for mip_family in json_dict[gene]:
			if ((include_exclude=='include' and mip_family in probe_names) or
			(include_exclude=='exclude' and mip_family not in probe_names)):
				if mip_family not in overall_json_dict:
					if gene not in overall_json_dict:
						overall_json_dict[gene]={}
					if mip_family not in overall_json_dict[gene]:
						overall_json_dict[gene][mip_family]=json_dict[gene][mip_family]
	return overall_json_dict

merged_mipsets.write(output_probe_set+'\n')
merged_mipsets.write('mip_arms\n')

overall_json_dict={}
for arms_file in mip_arms_files:
	overall_json_dict=parse_call_info(arms_file, overall_json_dict)
	parse_arms_file(arms_file)

json.dump(overall_json_dict, open(call_info, 'w'))
unused_mips=probe_names-seen_mips

if len(unused_mips)>0:
	print('WARNING: The following mips from your probe_name list were not found'
	'in any arms file.')
	print('\n'.join(list(unused_mips)))
	print('If you care about these mips, you should either change their names'
	' to match existing arms file entries, or add arms files that contain these'
	'mips.')
