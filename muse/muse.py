#!/usr/bin/env python

import sys
import re
import os
import string
import shutil
import logging
import subprocess
import tempfile
from multiprocessing import Pool
from argparse import ArgumentParser


def fai_chunk(path, blocksize):
    """A fa.fai file contains chromosome IDs and their length in the first two fields
    This function takes that file and creates a dict called seq_map with chr as key and size as value.
    Then for each chr, it returns a start and end coordinate based on the blocksize, until
    it reaches the end """
    seq_map = {}
    with open( path ) as handle:
        for line in handle:
            tmp = line.split("\t")
            seq_map[tmp[0]] = long(tmp[1])
    # below is a generator which keeps track of where we are in the chromosome and returns
    # different values every time it's called
    # for each chr
    for seq in seq_map:
        # take the chrsize
        l = seq_map[seq]
        # and bite off blocksize sized chunks, except for the last chunck (which ends at chrsize)
        for i in xrange(1, l, blocksize):
            # return chr, startpos, endpos
            yield (seq, i, min(i+blocksize-1, l))

def cmd_caller(cmd):
    logging.info("RUNNING: %s" % (cmd))
    print "running", cmd
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    if len(stderr):
        print stderr
    return p.returncode

def cmds_runner(cmds, cpus):
    p = Pool(cpus)
    values = p.map(cmd_caller, cmds, 1)
    return values

def call_cmd_iter(ref_seq, block_size, tumor_bam, normal_bam, output_base):
    """Generator that yields one Muse call command for each chromosome chunk"""
    template = string.Template("${MUSE} call -f ${REF_SEQ} -r ${INTERVAL} ${TUMOR_BAM} ${NORMAL_BAM} -O ${OUTPUT_BASE}.${BLOCK_NUM}")
    # fai_chunk yields chromosome ranges as chr, startpos, endpos
    # enumerate counts where we are in the return list (which seems a bit silly when you're using yield)
    # the dict replaces placeholders in the template string above with the correct values
    for i, block in enumerate(fai_chunk( ref_seq + ".fai", block_size ) ):
            cmd = template.substitute(
                dict(
                    REF_SEQ=ref_seq,
                    BLOCK_NUM=i,
                    INTERVAL="%s:%s-%s" % (block[0], block[1], block[2]) ),
                    MUSE='MuSEv1.0rc',
                    TUMOR_BAM=tumor_bam,
                    NORMAL_BAM=normal_bam,
                    OUTPUT_BASE=output_base
            )
            yield cmd, "%s.%s.MuSE.txt" % (output_base, i)

def run_muse(args):

    mode_flag = ""
    if args.mode == "wgs":
        mode_flag = "-G"
    else:
        mode_flag = "-E"

    workdir = os.path.abspath(tempfile.mkdtemp(dir=args.workdir, prefix="muse_work_"))

    if not os.path.exists(args.fafile + ".fai"):
        new_ref = os.path.join(workdir, "ref_genome.fasta")
        os.symlink(os.path.abspath(args.fafile),new_ref)
        subprocess.check_call( ["/usr/bin/samtools", "faidx", new_ref] )
        args.fafile = new_ref

    if args.normal_bam_index is None:
        if not os.path.exists(args.normal_bam + ".bai"):
            new_bam = os.path.join(os.path.abspath(workdir), "normal.bam")
            os.symlink(os.path.abspath(args.normal_bam),new_bam)
            subprocess.check_call( ["/usr/bin/samtools", "index", new_bam] )
            args.normal_bam = new_bam
    else:
        new_bam = os.path.join(os.path.abspath(workdir), "normal.bam")
        os.symlink(os.path.abspath(args.normal_bam), new_bam)
        os.symlink(os.path.abspath(args.normal_bam_index), new_bam + ".bai")
        args.normal_bam = new_bam

    if args.tumor_bam_index is None:
        if not os.path.exists(args.tumor_bam + ".bai"):
            new_bam = os.path.join(os.path.abspath(workdir), "tumor.bam")
            os.symlink(os.path.abspath(args.tumor_bam),new_bam)
            subprocess.check_call( ["/usr/bin/samtools", "index", new_bam] )
            args.tumor_bam = new_bam
    else:
        new_bam = os.path.join(workdir, "tumor.bam")
        os.symlink(os.path.abspath(args.tumor_bam), new_bam)
        os.symlink(os.path.abspath(args.tumor_bam_index), new_bam + ".bai")
        args.tumor_bam = new_bam
    # create list of MuSE call commands
    cmds = list(call_cmd_iter(ref_seq=args.fafile,
        block_size=args.blocksize,
        tumor_bam=args.tumor_bam,
        normal_bam=args.normal_bam,
        output_base=os.path.join(workdir, "output.file"))
    )
    # run the MuSE call commands in parallel
    rvals = cmds_runner(list(a[0] for a in cmds), args.cpus)
    if any(rvals):
        raise Exception("MuSE CALL failed")
    #check if rvals is ok
    first = True
    # at this point there are a lot of output.file.N.MuSE.txt call files, one for each chr fragment
    # concatenate those (remove any comment lines)
    merge = os.path.join(workdir, "merge.output")
    with open(merge, "w") as ohandle:
        for cmd, out in cmds:
            with open(out) as handle:
                for line in handle:
                    if first or not line.startswith("#"):
                        ohandle.write(line)
            first = False
            # remove call files unless told otherwise
            if not args.no_clean:
                os.unlink(out)
    # now we're ready to work on the MuSE sump command
    # this can be run without an input SNP file but that's probably not wise (paper unpublished so who knows)
    dbsnp_file = None
    if args.dbsnp:
        new_dbsnp = os.path.join(workdir, "db_snp.vcf")
        os.symlink(os.path.abspath(args.dbsnp),new_dbsnp)
        subprocess.check_call( ["/usr/bin/bgzip", new_dbsnp] )
        subprocess.check_call( ["/usr/bin/tabix", "-p", "vcf", new_dbsnp + ".gz" ])
        dbsnp_file = new_dbsnp + ".gz"
        sump_template = string.Template("${MUSE} sump -I ${MERGE} -O ${OUTPUT} -D ${DBSNP} ${MODE}")
    else:
        sump_template = string.Template("${MUSE} sump -I ${MERGE} -O ${OUTPUT} ${MODE}")

    tmp_out = os.path.join(workdir, "tmp.vcf")
    sump_cmd = sump_template.substitute( dict (
        MUSE=args.muse,
        MERGE=merge,
        OUTPUT=tmp_out,
        DBSNP=dbsnp_file,
        MODE=mode_flag
    ))
    cmd_caller(sump_cmd)

    shutil.copy(tmp_out, args.outfile)

    reown(args)

    if not args.no_clean:
        shutil.rmtree(workdir)

def reown(args):
    """If we are on a docker container, fix output ownership"""
    procfile = "/proc/1/cgroup"
    path = "/data"
    # get ownership of input file
    idfile = args.tumor_bam
    if os.path.exists(procfile):
        for line in open(procfile):
            if "docker" in line:
                uid=os.stat(idfile).st_uid
                gid=os.stat(idfile).st_gid
                os.chown(args.outfile, uid, gid)
                break


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('-f', '--fafile', help='faidx indexed reference sequence file', required=True)
    parser.add_argument('-b', '--blocksize', type=long, help='Parallel Block Size', default=50000000)
    parser.add_argument('-O', '--outfile', help='output file name (VCF)', default='out.vcf')
    parser.add_argument('-D', '--dbsnp', help="""dbSNP vcf file that should be bgzip compressed,
tabix indexed and based on the same reference
genome used in 'MuSE call'""")

    parser.add_argument('-n', '--cpus', type=int, default=8)
    parser.add_argument('-w', '--workdir', default='/data')
    parser.add_argument('--no-clean', action='store_true', default=False)
    parser.add_argument('--mode', choices=['wgs', 'wxs'], default='wgs')
    parser.add_argument('--tumor-bam', dest='tumor_bam', required=True)
    parser.add_argument('--tumor-bam-index', dest='tumor_bam_index', default=None)
    parser.add_argument('--normal-bam', dest='normal_bam', required=True)
    parser.add_argument('--normal-bam-index', dest='normal_bam_index', default=None)
    args = parser.parse_args()
    args.muse = 'MuSEv1.0rc'
    run_muse(args)
    