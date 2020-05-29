# template: https://github.com/gavinmdouglas/q2-picrust2/blob/master/q2_picrust2/_full_pipeline.py

import qiime2
import biom
import os
import sys


from qiime2.plugin import (Plugin, Str, Properties, Choices, Int, Bool, Range,
                           Float, Set, Visualization, Metadata, MetadataColumn,
                           Categorical, Numeric, Citations)



import q2_coremicrobiome
from ._core.process_data import process, visualize_in_qzv
from ._core.parse_inputs import parse_inputs
import logging

import skbio



# 'Runs Coremic analysis to find the core microbiome of the given interest group'
def full_pipeline(output_dir: str,  # Index files with different extensions can be created by the function (e.g., index.html, index.tsv, index.png)

                  table: biom.Table,  # ('datafiles', nargs='+', metavar='datafile', help='BIOM file containing the data to be analyzed')

                  factor: str, # ('factor', help=('The factor with which the interest group is identified. This should be a column head in the groupfile'))

                  group: str, # ('group', help=('The value in the factor column specifying the interest group. Multiple values may be specified with commas separating them'))  # map(lambda s: s.strip(), args.group.split(','))

                  outputfile: str='coremic', #'q2coremic_output.tsv',

                  groupfile: Metadata = None, # groupfile: Metadata, # ('groupfile', help=('Tab delimited file mapping each SampleID to a group'))

                  max_out_presence: float = 1.0, # ('--max_out_presence', type=float, metavar='presence', default=1.0, help=('Maximum fractional presence in the out group; defaults to 1.0 (100%%)'))

                  max_p: float = 0.05, # ('--max_p_val', type=float, metavar='pval', default=0.05, help=('Maximum p-value to include in the results; defaults to 0.05'))

                  min_frac: float = 0.9, # ('--min_presence', type=float, metavar='presence', default=0.9, help=('Minimum fractional presence in the interest group; defaults to 0.9 (90%%)'))

                  min_abundance: float = 0.0, # ('--max_absent_abundance', type=float, metavar='abundance', default=0.0, help=('Any abundance greater than this value is considered to indicate that the corresponding OTU is present; defaults to 0'))

                  p_val_adj: str = "b-h", # ('--p_val_correction', default='b-h', choices=['none', 'bf', 'bf-h', 'b-h'], help=('The method to use for correcting for multiple testing; valid options are "none", "bf" (Bonferroni), "bf-h" (Bonferroni-Holm), "b-h" (Benjamini-Hochberg, the default)'))

                  make_relative: Bool = False, # ('--relative', dest='relative', action='store_true', help=('Convert the input datatable to relative abundance, rather than absolute abundance. I.E. abundance values are a percentage of each sample. If this is set then the maximum absent abundance should also be a relative (0 to 1) value.'))

                  quantile_normalize: Bool = False # ('--quantile-normalize', dest='quantile_normalize', action='store_true', help=('Quantile normalize the columns of the input datatable before processing. This will occur after relativising if both are selected. Ties are broken in an arbitrary but deterministic fashion.'))

                  ) -> None: #-> skbio.DistanceMatrix: #-> str:  #(biom.Table, biom.Table, biom.Table, biom.Table):


    datafiles = table
    groupfile = groupfile

    cfg = {
        'factor': factor,
        'group': list(map(lambda s: s.strip(), group.split(','))),
        'min_abundance': min_abundance,
        'max_p': max_p,
        'min_frac': min_frac,
        'max_out_presence': max_out_presence,
        'p_val_adj': p_val_adj,
        'make_relative': make_relative,
        'quantile_normalize': quantile_normalize,
        'outputfile': outputfile
    }

    errors_list, mapping_dict, out_group, filtered_data = parse_inputs(cfg, groupfile, datafiles)
    if len(errors_list) > 0:
        logging.error(errors_list)
        exit(1)

    inputs = {
        'mapping_dict': mapping_dict,
        'filtered_data': filtered_data,
    }
    core = process(inputs, cfg)

    visualize_in_qzv(core, cfg, output_dir)

    return None
