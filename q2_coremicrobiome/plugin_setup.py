# ----------------------------------------------------------------------------
# https://github.com/qiime2/q2-diversity/blob/master/q2_diversity/plugin_setup.py
# https://github.com/gavinmdouglas/q2-picrust2/blob/master/q2_picrust2/plugin_setup.py
# Copyright (c) 2016-2019, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from qiime2.plugin import (Plugin, Str, Properties, Choices, Int, Bool, Range,
                           Float, Set, Visualization, Metadata, MetadataColumn,
                           Categorical, Numeric, Citations, TypeMatch)


from q2_types.feature_table import FeatureTable, Frequency, RelativeFrequency
from q2_types.sample_data import SampleData
from q2_types.feature_data import FeatureData

import q2_coremicrobiome



citations = Citations.load('citations.bib', package='q2_coremicrobiome')


plugin = Plugin(
    name='coremicrobiome',
    version=  '1',
    website='https://github.com/richrr/coremicro',
    package='q2_coremicrobiome',
    description=('This QIIME 2 plugin calculates coremicrobiome '
                 'using presence/absence data. '
                 'Refer http://coremic2.appspot.com/help for online tool.'),
    short_description='Plugin for exploring coremicrobiome.',
    citation_text='Rodrigues RR, Rodgers NC, Wu X, Williams MA. (2018) '
    			   'COREMIC: a web-tool to search for a niche associated '
    			   'CORE MICrobiome. PeerJ 6:e4395'
    #citations=[citations['Rodrigues2018']]
)


# https://dev.qiime2.org/latest/actions/visualizers/
# you do not provide outputs or output_descriptions when making this call, as Visualizers, by definition, only return a single visualization. Since the visualization output path is a required parameter, you do not include this in an outputs list
T = TypeMatch([Frequency, RelativeFrequency])
plugin.visualizers.register_function(
    function=q2_coremicrobiome.full_pipeline,
    inputs={'table': FeatureTable[T]},
    parameters={
            	'groupfile': Metadata,
            	'factor': Str,
            	'group': Str,
            	'outputfile': Str,
            	'max_out_presence': Float,
    			'max_p': Float,
    			'min_frac': Float,
    			'min_abundance': Float,
    			'p_val_adj': Str,
    			'make_relative': Bool,
    			'quantile_normalize': Bool
    },
    input_descriptions={
        'table': 'path to the feature (OTU) table containing the data to be analyzed.'
    },
    parameter_descriptions={
        'groupfile': ('Tab delimited file mapping each "SampleID" to a group. '
                      'Requires "SampleID" as the first column on first line '
                      'to indicate sample ids. e.g. QIIME mapping file.'
                      'Make sure the header does not have #'),
        'factor': ('The factor with which the interest group is identified. '
                   'For example, to calculate the core microbome of "Good" people '
                   'under the "Person" column, enter "Person".'
                   'This should be a column header in the groupfile.'),
        'group': ('The value in the factor column specifying the interest group. '
                  'For example, to calculate the core microbiome of "Good" people under '
                  'the "Person" column, enter "Good". All samples not matching this value '
                  'in the specified column will be considered to be a part of the out group. '
                  'Multiple values may be specified that are separated by a comma and optional whitespace.'
                  'For example, to use all people who are either "Good" or "Neutral" as '
                  'the interest group, enter "Good,Neutral" or "Good, Neutral".'),
        'outputfile': ('outputfile. default is coremic '),
        'max_out_presence': ('Maximum fractional presence in the out group; defaults to 1.0 (100%%)'),
        'max_p': ('Maximum p-value to include in the results; defaults to 0.05'),
        'min_frac': ('Minimum fractional presence in the interest group; defaults to 0.9 (90%%)'),
        'min_abundance': ('Any abundance greater than this value is considered to indicate that the '
                   'corresponding OTU is present; defaults to 0'),
        'p_val_adj': ('The method to use for correcting for multiple testing; valid options are "none", "bf" '
                   '(Bonferroni), "bf-h" (Bonferroni-Holm), "b-h" (Benjamini-Hochberg, the default)'),
        'make_relative': ('Convert the input datatable to relative abundance. I.E. abundance values are a '
                  'percentage of each sample. If this is set then the maximum absent abundance should '
                  'also be a relative (0 to 1) value. default is False'),
        'quantile_normalize': ('Quantile normalize the columns of the input datatable before processing. '
                  'This will occur after relativising if both are selected. Ties are broken in an '
                  'arbitrary but deterministic fashion.')
    },
    name='Full pipeline for core mirobiome',
    description=("QIIME2 Plugin for computing core mcirobiome for the group of interest."),
    citations=[citations['Rodrigues2018']]
)
