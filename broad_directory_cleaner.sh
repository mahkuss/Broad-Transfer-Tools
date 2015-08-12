#!bin/bash 
# Author: Brandi Davis-Dusenberry
# Purpose: clean up and organization of seq files from wget from the broad
# Usage: run this script from within the folder 
# edited 5/2/2015 by Rob Moccia to fix bug that placed unmapped bams into /log folder
#####################

##first put all alignment summary files into one folder.  these tell number of reads aligned etc.
mkdir ./alignment_summary
mv *alignment_summary_metrics ./alignment_summary
#
##move unmultiplexed fastq files into folder
mkdir ./fastq
mv *1.1.fastq ./fastq
mv *1.2.fastq ./fastq
mv *2.1.fastq ./fastq
mv *2.2.fastq ./fastq
#
#move demultiplexed fastq files into folder
mv *unmapped.1.fastq ./fastq
mv *unmapped.2.fastq ./fastq
#
#move unmatched fastq files into folder
mv *unmatched*.fastq ./fastq
#
#move qc pdf plots into one folder
mkdir ./QC_plots
mv *.pdf ./QC_plots
#
#move bam and bai files into one folder. 
mkdir ./Bam
mv *.bam ./Bam
mv *.bai ./Bam
#
##move log files into dir.
mkdir ./logs
mv *metrics ./logs
mv *log ./logs
mv 1* ./logs
mv 2* ./logs
mv i* ./logs
mv MA* ./logs
#
##move unmapped bam back up 
mv ./Bam/*unmapped.bam ./
