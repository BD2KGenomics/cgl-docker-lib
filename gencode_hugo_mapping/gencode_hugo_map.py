#!/usr/bin/env python2.7
"""
Subsets table of quantification values, output by RSEM, from Gencode/Ensemble names to HUGO

http://www.gencodegenes.org/releases/
http://www.genenames.org/]
"""
import os
import argparse
import pandas as pd
import itertools


def replace_gene_names(table, gene_mappings):
    gene_names = []
    keyerrors = 0.0
    for gene_id in table['gene_id']:
        try:
            gene_names.append(gene_mappings[gene_id])
        except KeyError:
            keyerrors += 1
            table.drop(table[table['gene_id'] == gene_id].index, inplace=True)
    print "Number of unmapped genes: {}, of {} total genes.".format(keyerrors, len(table['gene_id']))
    map_perc = 100 * round(1 - (keyerrors / len(table['gene_id'])), 4) if len(table['gene_id']) != 0 else 0
    print "{}% of genes succesfully mapped.".format(map_perc)
    table['gene_id'] = gene_names

    # Change name from gene_id to gene_name
    cols = list(table.columns)
    cols[0] = 'gene_name'
    table.columns = cols

    return table


def replace_isoform_names(table, isoform_mappings, tabs=True):
    isoform_names = []
    keyerrors = 0.0
    name = 'gene_id/transcript_id' if tabs else 'transcript_id'
    for transcript_id in table[name]:
        try:
            if tabs:
                isoform_names.append(isoform_mappings[transcript_id.split('/')[1]])
            else:
                isoform_names.append(isoform_mappings[transcript_id])
        except KeyError:
            keyerrors += 1
            table.drop(table[table[name] == transcript_id].index, inplace=True)
    print "Number of unmapped isoforms: {}, of {} total genes.".format(keyerrors, len(table[name]))
    map_perc = 100 * round(1 - (keyerrors / len(table[name])), 4) if len(table[name]) != 0 else 0
    print "{}% of isoforms succesfully mapped.".format(map_perc)
    table[name] = isoform_names

    # Change name from transcript_id to transcript_name
    cols = list(table.columns)
    cols[0] = 'transcript_name'
    table.columns = cols

    return table


def main():
    """
    Run this container by moving to the directory where your RSEM files are and:

    docker run -v $(pwd):/data quay.io/ucsc_cgl/gencode_hugo_mapping -g <GENE FILES> -i <ISOFORM FILES>

    Where <GENE FILES> and <ISOFORM FILES> are space separated file names

    Output: File Name with HUGO prepended before the file extension
    """
    parser = argparse.ArgumentParser(description=main.__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-g', '--genes', nargs='+', help='Gene files from RSEM (.tab or .results)')
    parser.add_argument('-i', '--isoforms', nargs='+', help='Isoform files from RSEM (.tab or .results)')
    params = parser.parse_args()

    # Read in mapping table
    assert os.path.isfile('/opt/mapping/attrs.tsv'), 'Cannot find mapping file.'
    id_map = pd.read_table('/opt/mapping/attrs.tsv', sep='\t')
    gene_mappings = {x: y for x, y in itertools.izip(id_map['geneId'], id_map['geneName'])}
    isoform_mappings = {x: y for x, y in itertools.izip(id_map['transcriptId'], id_map['transcriptName'])}

    # Read in gene and isoform files
    genes = {x: pd.read_table(x, sep='\t') for x in params.genes}
    isoforms = {x: pd.read_table(x, sep='\t') for x in params.isoforms}

    # Perform mapping
    for gene in genes:
        replace_gene_names(genes[gene], gene_mappings)

    for isoform in isoforms:
        if '.tab' in isoform:
            replace_isoform_names(isoforms[isoform], isoform_mappings)
        else:
            replace_isoform_names(isoforms[isoform], isoform_mappings, tabs=False)

    # Outut HUGO mappings
    for gene in genes:
        fpath = os.path.join(os.path.splitext(gene)[0] + '.hugo' + os.path.splitext(gene)[1])
        genes[gene].to_csv(fpath, sep='\t', index=False)

    for isoform in isoforms:
        fpath = os.path.join(os.path.splitext(isoform)[0] + '.hugo' + os.path.splitext(isoform)[1])
        isoforms[isoform].to_csv(fpath, sep='\t', index=False)


if __name__ == '__main__':
    main()
