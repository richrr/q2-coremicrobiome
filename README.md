# q2-coremicrobiome
Qiime2 plugin of COREMIC: CORE MICrobiome [https://doi.org/10.7717/peerj.4395]
This plugin works with qza files from QIIME 2.

* For Biom v1 OTU tables from QIIME 1.x, please use the web-tool: http://coremic2.appspot.com/


Sample commands:
> qiime coremicrobiome full-pipeline --help

> qiime coremicrobiome full-pipeline --i-table /path/to/otu_table_file/table.qza --p-factor Person --p-group Good --p-outputfile coremic.q2 --m-groupfile-file /path/to/meta_data_file/sampleSheet.txt --p-make-relative --o-visualization output.qzv

* creates "output.qzv" in current directory.
