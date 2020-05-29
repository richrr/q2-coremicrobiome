# Copyright 2016, 2017 Richard Rodrigues, Nyle Rodgers, Mark Williams,
# Virginia Tech
#
# This file is part of Coremic.
#
# Coremic is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Coremic is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Coremic. If not, see <http://www.gnu.org/licenses/>.
from .pval import getpval, correct_pvalues
from .otu import Otu
import pandas as pd
import pkg_resources
import q2templates
import os
import sys


def process(inputs, cfg):
    """Finds the core OTUs"""

    interest_ids = [otu for g in cfg['group']
                    for otu in inputs['mapping_dict'][g]]

    i_indexes = [i for i, id in enumerate(inputs['filtered_data'].ids('sample'))  #.SampleIds
                 if id in interest_ids]

    otus = [Otu(vals, str(name), cfg['min_abundance'], i_indexes)
            for vals, name, md in inputs['filtered_data'].iter(True, 'observation')]
    pvals = list()
    for otu in otus:
        pval = getpval(otu)
        otu.pval = pval
        pvals.append(pval)

    for otu, corrected_pval in zip(otus,
                                   correct_pvalues(pvals, cfg['p_val_adj'])):
        otu.corrected_pval = corrected_pval


    # Filter down to the core
    return [otu for otu in otus
            if (otu.corrected_pval <= cfg['max_p'] and
                otu.interest_frac >= cfg['min_frac'] and
                otu.out_frac <= cfg['max_out_presence'])]


def visualize_in_qzv(core, cfg, output_dir):
    """Visualize in qzv"""
    TEMPLATES = pkg_resources.resource_filename('q2_coremicrobiome', 'coremic_assets')

    outputfile = cfg['outputfile']
    # data
    inppstr = format_inputs_qzv(cfg)
    usr_inputs = q2templates.df_to_html(inppstr, index=False)
    # downloadable file
    inputs_path = os.path.join(output_dir, outputfile+'InputParams.tsv')
    inppstr.to_csv(inputs_path, sep='\t', index=False)

    # results
    outpstr = format_results_qzv(core)
    results = ''
    if len(outpstr.index) == 0:
        results = "<b>No core microbes found.</b> <br>\
        <i>Please try relaxing the following:</i> <br>\
                --p-min-frac Minimum fractional presence in the interest group <br>\
                --p-max-p pvalue cutoff <br>\
        <i>or changing the:</i> <br>\
                normalization using --p-make-relative and/or --p-quantile-normalize <br>\
                method for multiple testing correction using --p-p-val-adj"
    else:
        results = q2templates.df_to_html(outpstr, index=False)
    # downloadable file
    results_path = os.path.join(output_dir, outputfile+'Results.tsv')
    outpstr.to_csv(results_path, sep='\t', index=False)

    index = os.path.join(TEMPLATES, 'index.html')
    q2templates.render(index, output_dir, context={
        'outputfile': outputfile,
        'usr_inputs': usr_inputs,
        'results': results
    })
    return None


def format_inputs_qzv(cfg):
    """Format the input data for a qzv"""
    # Summary of the inputs given
    input_params_list = list()

    input_params_list.append(['Factor', cfg['factor']])
    input_params_list.append(['Group', ', '.join(cfg['group'])])
    input_params_list.append(['Min Abundance', cfg['min_abundance']])
    input_params_list.append(['Min Presence', cfg['min_frac']])
    input_params_list.append(['Max Out Presence', cfg['max_out_presence']])

    p_val_correction_method = 'None'
    if cfg['p_val_adj'] == 'bf':
        p_val_correction_method = 'Bonferroni'
    if cfg['p_val_adj'] == 'bf-h':
        p_val_correction_method = 'Bonferroni Holm'
    if cfg['p_val_adj'] == 'b-h':
        p_val_correction_method = 'Benjamini Hotchberg'
    input_params_list.append(["P-value correction method", p_val_correction_method])
    input_params_list.append(['Max Corrected p-value', cfg['max_p']])

    normaliztns = 'None'
    if cfg['make_relative']:
        normaliztns = "Relativize"
    if cfg['quantile_normalize']:
        normaliztns = "Quantile"
    if cfg['make_relative'] and cfg['quantile_normalize']:
        normaliztns = "Relativize, then Quantile"
    input_params_list.append(['Normalization', normaliztns])

    return pd.DataFrame( input_params_list, columns= ["Parameter", "Value"])


def format_results_qzv(res):
    """Format the result data for a qzv"""
    # Header for results
    header = ['ID', 'p-value', 'Corrected p-value', 'Interest Group Presence',
              'Out Group Presence']
    # Combine header, and information from core OTUs
    tmp_pdf = pd.DataFrame(
                   [[otu.name, otu.pval, otu.corrected_pval, otu.interest_frac,
                   otu.out_frac] for otu in list(sorted(res))]
                   , columns= header)
    sortd_pdf = tmp_pdf.sort_values(by=['Corrected p-value', 'Interest Group Presence'], ascending=[True, False])
    return sortd_pdf
