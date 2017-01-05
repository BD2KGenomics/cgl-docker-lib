#!/usr/bin/env bash
# Author: Robert Baertsch

export SAMPLE=$1
cd /data
sed /^uc0/d /data/rsem_gene.tab |awk -F'\t' '{OFS="\t";split($1,a,"|");$1=a[1];print $0}' | grep -v "SLC35E2" $first |awk -F'\t' '$1!="?"{OFS="\t";print $0}'  > /data/rsem.genes.results
awk -F'\t' '{OFS="\t";split($2,a,"|");$2=a[1];gn=$2"/"$1;$1=gn;print $0}' /data/rsem_isoform.tab | grep -v "SLC35E2" $first |awk -F'\t' '$1!="?"{OFS="\t";print $0}' > /data/rsem.isoform.results

# gene
echo perl /opt/cgl-docker-lib/quartile_norm.pl -c 5 -q 75 -t 1000 -o /data/rsem.genes.normalized_results /data/rsem.genes.results
awk -F'\t' 'NR==1{$7="'${SAMPLE}'"}{OFS="\t";print $1,$7}' /data/rsem.genes.results > /data/rsem.genes.raw_fpkm.tab
awk -F'\t' 'NR==1{$6="'${SAMPLE}'"}{OFS="\t";print $1,$6}' /data/rsem.genes.results > /data/rsem.genes.raw_tpm.tab
awk -F'\t' 'NR==1{$5="'${SAMPLE}'"}{OFS="\t";print $1,$5}' /data/rsem.genes.results > /data/rsem.genes.raw_counts.tab
perl /opt/cgl-docker-lib/quartile_norm.pl -c 7 -q 75 -t 1000 -o /data/rsem.c7.temp /data/rsem.genes.results
awk -F'\t' 'NR==1{$2="'${SAMPLE}'"}{OFS="\t";print $1,$2}' /data/rsem.c7.temp > /data/rsem.genes.norm_fpkm.tab
perl /opt/cgl-docker-lib/quartile_norm.pl -c 6 -q 75 -t 1000 -o /data/rsem.c6.temp /data/rsem.genes.results
awk -F'\t' 'NR==1{$2="'${SAMPLE}'"}{OFS="\t";print $1,$2}' /data/rsem.c6.temp > /data/rsem.genes.norm_tpm.tab
perl /opt/cgl-docker-lib/quartile_norm.pl -c 5 -q 75 -t 1000 -o /data/rsem.c5.temp /data/rsem.genes.results
awk -F'\t' 'NR==1{$2="'${SAMPLE}'"}{OFS="\t"; print $1,$2}' /data/rsem.c5.temp > /data/rsem.genes.norm_counts.tab

# isoform
awk -F'\t' 'NR==1{$7="'${SAMPLE}'"}{OFS="\t";print $1,$7}' /data/rsem.isoform.results > /data/rsem.isoform.raw_fpkm.tab
awk -F'\t' 'NR==1{$6="'${SAMPLE}'"}{OFS="\t";print $1,$6}' /data/rsem.isoform.results > /data/rsem.isoform.raw_tpm.tab
awk -F'\t' 'NR==1{$5="'${SAMPLE}'"}{OFS="\t";print $1,$5}' /data/rsem.isoform.results > /data/rsem.isoform.raw_counts.tab
perl /opt/cgl-docker-lib/quartile_norm.pl -c 7 -q 75 -t 1000 -o /data/rsem.isoform.c7.temp /data/rsem.isoform.results
awk -F'\t' 'NR==1{$2="'${SAMPLE}'"}{OFS="\t";print $1,$2}' /data/rsem.isoform.c7.temp > /data/rsem.isoform.norm_fpkm.tab
perl /opt/cgl-docker-lib/quartile_norm.pl -c 6 -q 75 -t 1000 -o /data/rsem.isoform.c6.temp /data/rsem.isoform.results
awk -F'\t' 'NR==1{$2="'${SAMPLE}'"}{OFS="\t";print $1,$2}' /data/rsem.isoform.c6.temp > /data/rsem.isoform.norm_tpm.tab
perl /opt/cgl-docker-lib/quartile_norm.pl -c 5 -q 75 -t 1000 -o /data/rsem.isoform.c5.temp /data/rsem.isoform.results
awk -F'\t' 'NR==1{$2="'${SAMPLE}'"}{OFS="\t";print $1,$2}' /data/rsem.isoform.c5.temp > /data/rsem.isoform.norm_counts.tab
