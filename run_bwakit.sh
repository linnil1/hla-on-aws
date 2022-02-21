#!/bin/sh
mkdir -p $(dirname "$4");
/usr/local/bin/seqtk mergepe $2 $3 \
  | /usr/local/bin/bwa mem -p -t4 $1 - 2> $4.log.bwamem \
  | /usr/local/bin/k8 /usr/local/bin/bwa-postalt.js -p $4.hla $1.alt \
  | /usr/local/bin/samtools view -1 - > $4.aln.bam;
/usr/local/bin/run-HLA $4.hla > $4.hla.top 2> $4.log.hla;
touch $4.hla.HLA-dummy.gt;
cat $4.hla.HLA*.gt | grep ^GT | cut -f2- > $4.hla.all;
