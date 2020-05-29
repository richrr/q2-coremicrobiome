# ----------------------------------------------------------------------------
# Copyright (c) 2016-2019, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from setuptools import setup, find_packages

setup(
    name="q2-coremicrobiome",
    packages=find_packages(),
    author="Richard Rodrigues",
    author_email="Dr.RichRodrigues@gmail.com",
    description="Identify core microbiome. Qiime2 Plugin.",
    license='BSD-3-Clause',
    url="http://coremic2.appspot.com/help",
    entry_points={
        'qiime2.plugins': ['q2-coremicrobiome=q2_coremicrobiome.plugin_setup:plugin']
    },
    package_data={'q2_coremicrobiome': ['citations.bib', 'coremic_assets/index.html']}, # non .py files
    zip_safe=False,
)
