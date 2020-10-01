# q2-coremicrobiome
Qiime2 plugin of COREMIC: CORE MICrobiome [https://doi.org/10.7717/peerj.4395]. This plugin works with qza files from QIIME 2.

* For Biom v1 OTU tables from QIIME 1.x, please use the web-tool: http://coremic2.appspot.com/

Install from conda:
> conda install -c richrr q2-coremicrobiome

Sample usage:
> qiime coremicrobiome full-pipeline --help

> qiime coremicrobiome full-pipeline --i-table /path/to/otu_table_file/table.qza --p-factor Person --p-group Good --p-outputfile coremic.q2 --m-groupfile-file /path/to/meta_data_file/sampleSheet.txt --p-make-relative --o-visualization output.qzv

Please note:
- SampleSheet (map file) should have "SampleID" as the header for first column. Any other string or its variation (e.g. "#SampleID", "SAMPLEID") will NOT work.
- creates "output.qzv" in current directory.


Sample data available at:
> https://github.com/richrr/sample_data/tree/master/q2-coremicrobiome

To get sample data and test the qiime plugin, in Unix or Mac terminal:
> mkdir dataset1
> cd dataset1
> wget https://raw.githubusercontent.com/richrr/sample_data/master/q2-coremicrobiome/dataset1/map-file.txt
> wget -O table.w.taxaname.qza https://github.com/richrr/sample_data/blob/master/q2-coremicrobiome/dataset1/table.w.taxaname.qza?raw=true
> qiime coremicrobiome full-pipeline --i-table table.w.taxaname.qza --p-factor Plant --p-group Sw --p-outputfile coremic.q2 --m-groupfile-file map-file.txt --p-make-relative --o-visualization swg.qzv
OR
> mkdir dataset2
> cd dataset2
> wget https://raw.githubusercontent.com/richrr/sample_data/master/q2-coremicrobiome/dataset2/map-file.txt
> wget -O table.qza https://github.com/richrr/sample_data/blob/master/q2-coremicrobiome/dataset2/table.qza?raw=true
> qiime coremicrobiome full-pipeline --i-table table.qza --p-factor SampleType --p-group Leaf --p-outputfile out.Leaf. --m-groupfile-file map-file.txt --p-make-relative --p-quantile-normalize --o-visualization output.Leaf.qzv


