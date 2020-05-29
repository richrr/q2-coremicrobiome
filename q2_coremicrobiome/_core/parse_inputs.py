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

import biom
import pandas as pd
from numpy import array, append
from itertools import groupby

import qiime2

from biom.table import Table




# groupfile delimitere
DELIM = '\t'


def read_table(table_file, do_relativize=False, do_quantile_normalize=False):
    """Read in the input datafile
    """

    parsed_table = table_file

    # allow: 1)relativize w/wo 2)quantile
    # not doing rarefy for now: when needed will need to add a sequence threshold arg.

    data = table_file
    if do_relativize:
        data = data.norm(axis='sample', inplace=False)
    if do_quantile_normalize:
        data = [d for d in data.iter_data(True,'observation')]
        data = quantile_normalize(data)
        data = biom.table.Table(data, list(parsed_table.ids('observation')), list(parsed_table.ids('sample')))
    #print(data)
    return data


def relativize_columns(data):
    """Adjust the given two dimensional array so that the sum of the values in
    each column in one"""
    for i in range(len(data[0])):
        total = sum([row[i] for row in data])
        for row in data:
            row[i] = row[i] / float(total)
    return data


def quantile_normalize(data):
    """Quantile normalize the data"""
    columns = [[row[i] for row in data] for i in range(len(data[0]))]
    sorted_columns = [sorted(column) for column in columns]
    distribution = [(sum([column[i] for column in sorted_columns]) /
                     len(sorted_columns))
                    for i in range(len(sorted_columns[0]))]
    result = [
        [newval for newval, column_i
         in sorted([(distribution[dist_i], column_i)
                    for dist_i, (column_i, val)
                    in enumerate(sorted(enumerate(column),
                                        key=lambda x: x[1]))],
                   key=lambda x: x[1])]
        for column in columns]
    return [array([column[i] for column in result])
            for i in range(len(result[0]))]



def parse_groupfile(groupfile, factor):
    """Turn the groupfile in to a dictionary from factor labels to sample ids
    """
    #groupfile = read_file(groupfile) # takes filename, returns list
    #print(groupfile.to_string())

    # https://note.nkmk.me/en/python-pandas-list/
    groupfile = groupfile.reset_index().T.reset_index().T.values.tolist()

    groupfile = [DELIM.join(map(str, l)) for l in groupfile]
    #print(groupfile)

    # It is assumed that the first line is the header
    labels = groupfile[0].strip().strip('#').split(DELIM)
    if 'SampleID' not in labels:
        raise ValueError('"SampleID" not in the headers of the groupfile')
    if factor not in labels:
        raise ValueError('"%s" not in the headers of the groupfile' % factor)

    index_sampleid = labels.index('SampleID')
    index_categ = labels.index(factor)
    local_dict = dict()
    for l in groupfile[1:]:
        if not l or l.strip()[0] == '#':  # Line is blank or comment
            continue
        split_line = l.strip().split(DELIM)
        if len(split_line) <= max(index_sampleid, index_categ):
            raise ValueError("Malformed groupfile")
        key, val = map(split_line.__getitem__,
                       [index_categ, index_sampleid])
        if key in local_dict:
            local_dict[key].append(val)
        else:
            local_dict[key] = [val]
    return local_dict


def parse_inputs(params, groupfile, datafiles):
    """Validate that the given inputs are usable and parse them into usable
    formats"""

    errors_list = list()

    groupfile = groupfile.to_dataframe()

    try:
        mapping_dict = parse_groupfile(groupfile, params['factor'])
        for l in params['group']:
            if l not in mapping_dict.keys():
                errors_list.append(
                    'Interest group label %s is not in groupfile' % l)

        out_group = list(mapping_dict.keys())
        [out_group.remove(l) for l in params['group']]
    except ValueError as e:
        errors_list.append(e.message)
        mapping_dict = dict()
        out_group = None


    try:
        filtered_data = read_table(datafiles, params['make_relative'], params['quantile_normalize'])
    except ValueError as e:
        errors_list.append('Datafile could not be read: %s' % e.message)
        filtered_data = None

    if params['max_p'] < 0 or params['max_p'] > 1:
        errors_list.append('Maximum p-value must be in the range zero to one')
    if params['min_frac'] < 0 or params['min_frac'] > 1:
        errors_list.append('Minimum interest group presence must be in range' +
                           ' zero to one')
    if params['max_out_presence'] < 0 or params['max_out_presence'] > 1:
        errors_list.append('Maximum out-group presence must be in range' +
                           ' zero to one')


    return (errors_list, mapping_dict, out_group, filtered_data)
