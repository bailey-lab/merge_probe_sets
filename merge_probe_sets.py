probe_names=set([line.strip() for line in open(snakemake.input['probe_names'])])
mip_arms_files=snakemake.input['mip_arms_files']
output_probe_set=snakemake.params['output_probe_set']
include_exclude=snakemake.params['include_exclude']
merged_mip_arms=open(snakemake.output['merged_mip_arms_file'], 'w')
#merged_probe_info=open(snakemake.output['merged_probe_info'], 'w')
merged_mipsets=open(snakemake.output['merged_mipsets'], 'w')

header=['gene_name', 'mip_family', 'mip_id', 'extension_arm', 'ligation_arm', 'extension_barcode_length', 'ligation_barcode_length', 'mipset', 'chrom', 'begin', 'end']
merged_mip_arms.write('\t'.join(header)+'\n')
arm_dict={}
seen_mips=set([])

def parse_arms_file(arms_file):
	import csv
	marker_reader=csv.DictReader(open(arms_file), delimiter='\t')
	for row in marker_reader:
		mip_id=row['mip_id']
		ligation_arm=row['ligation_arm']
		extension_arm=row['extension_arm']
		arm_tuple=(ligation_arm, extension_arm)
		seen_mips.add(mip_id)
		if ((include_exclude=='include' and mip_id in probe_names) or
		(include_exclude=='exclude' and mip_id not in probe_names)):
			if arm_tuple not in arm_dict:
				arm_dict[arm_tuple]=mip_id
				merged_mipsets.write(mip_id+'\n')
				new_line=[]
				for column in header:
					if column in row and type(row[column])==str:
						new_line.append(row[column])
					else:
						new_line.append('')
				merged_mip_arms.write('\t'.join(new_line)+'\n')
			elif arm_tuple in arm_dict and mip_id!=arm_dict[arm_tuple]:
				print(f'ERROR: the probes {mip_id} and {arm_dict[arm_tuple]}'
				f' both have the same mip arms. Please remove redundant mip ids'
				' and run again')
				exit()

merged_mipsets.write(output_probe_set+'\n')
merged_mipsets.write('mip_arms\n')

for arms_file in mip_arms_files:
	parse_arms_file(arms_file)

unused_mips=probe_names-seen_mips
if len(unused_mips)>0:
	print('WARNING: The following mips from your probe_name list were not found'
	'in any arms file.')
	print('\n'.join(list(unused_mips)))
	print('If you care about these mips, you should either change their names'
	' to match existing arms file entries, or add arms files that contain these'
	'mips.')
