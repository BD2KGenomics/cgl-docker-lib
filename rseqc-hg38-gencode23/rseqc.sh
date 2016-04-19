#!/bin/bash
RSEQC_DIR=/opt/RSeQC-2.6.3/scripts
REF_GENE_BED=/opt/RSeQC-2.6.3/gencode.v23.bed

INPUT=$1
SAMPLE_NAME=$2
OUTDIR=/data

echo $INPUT

#Bam stat
python $RSEQC_DIR/bam_stat.py -i $INPUT > $OUTDIR/$SAMPLE_NAME.bam.stat  &

#Genebody coverage
python $RSEQC_DIR/geneBody_coverage.py -r $REF_GENE_BED -i $INPUT -o $OUTDIR/$SAMPLE_NAME &

#Infer distance
python $RSEQC_DIR/inner_distance.py -i $INPUT -o $OUTDIR/$SAMPLE_NAME -r $REF_GENE_BED &

#RPKM count
python $RSEQC_DIR/FPKM_count.py -i $INPUT -r $REF_GENE_BED -o $OUTDIR/$SAMPLE_NAME.rpkm.count &

# Mismatch Profile
python $RSEQC_DIR/mismatch_profile.py -i $INPUT --read-align-length 200 -o $OUTDIR/$SAMPLE_NAME &

# geneBody Coverage
python $RSEQC_DIR/geneBody_coverage.py -i $INPUT -r $REF_GENE_BED -o $OUTDIR/$SAMPLE_NAME &

# Infer Experiment
python $RSEQC_DIR/infer_experiment.py -i $INPUT -r $REF_GENE_BED > $OUTDIR/$SAMPLE_NAME.infer.experiment &

# Inner Distance
python $RSEQC_DIR/inner_distance.py -i $INPUT -r $REF_GENE_BED -o $OUTDIR/$SAMPLE_NAME &

# Junction Saturation
python $RSEQC_DIR/junction_saturation.py -i $INPUT -r $REF_GENE_BED -o $OUTDIR/$SAMPLE_NAME &

# Junction Annotation
python $RSEQC_DIR/junction_annotation.py -i $INPUT -r $REF_GENE_BED -o $OUTDIR/$SAMPLE_NAME &

# Read Distribution
python $RSEQC_DIR/read_distribution.py -i $INPUT -r $REF_GENE_BED > $OUTDIR/$SAMPLE_NAME.read.distribution &

# Read Duplication
python $RSEQC_DIR/read_duplication.py -i $INPUT -o $OUTDIR/$SAMPLE_NAME &

# Read GC
python $RSEQC_DIR/read_GC.py -i $INPUT -o $OUTDIR/$SAMPLE_NAME &

# Read NVC
python $RSEQC_DIR/read_NVC.py -i $INPUT -o $OUTDIR/$SAMPLE_NAME &

# Read Quality
python $RSEQC_DIR/read_quality.py -i $INPUT -o $OUTDIR/$SAMPLE_NAME &

# RPKM Saturation
python $RSEQC_DIR/RPKM_saturation.py -r $REF_GENE_BED -d '1++,1--,2+-,2-+' -i $INPUT -o $OUTDIR/$SAMPLE_NAME &
