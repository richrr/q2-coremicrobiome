# q2-coremicrobiome
Qiime2 plugin of COREMIC: CORE MICrobiome [https://doi.org/10.7717/peerj.4395]
This plugin works with qza files from QIIME 2.

* For Biom v1 OTU tables from QIIME 1.x, please use the web-tool: http://coremic2.appspot.com/


Sample usage:
> qiime coremicrobiome full-pipeline --help

> qiime coremicrobiome full-pipeline --i-table /path/to/otu_table_file/table.qza --p-factor Person --p-group Good --p-outputfile coremic.q2 --m-groupfile-file /path/to/meta_data_file/sampleSheet.txt --p-make-relative --o-visualization output.qzv

Please note:
- SampleSheet (map file) should have "SampleID" as the header for first column. Any other string or its variation (e.g. "#SampleID", "SAMPLEID") will NOT work.
- creates "output.qzv" in current directory.


Sample data available at:
> https://github.com/richrr/sample_data/tree/master/q2-coremicrobiome
