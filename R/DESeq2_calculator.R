# Reference: http://bioconductor.org/packages/devel/bioc/vignettes/DESeq2/inst/doc/DESeq2.html
# This code calculates DESeq2 DEG from the matrix with only specific condition
# Example: Rscript inputfile metafile columnname_in_meta condition1 condition2 outputfile
# inputfile = "../data/counts_raw/counts_raw_CD4.csv"
# metafile = "../data/annotation_metadata/EPIC_HCvB_metadata_baseline_updated-share.csv"
# selectedColumn = "DiseaseCourse"
# outputfile = "./result.csv"

library(tidyverse)
library(DESeq2)
library(tximport)

args = commandArgs(trailingOnly=TRUE)
inputFile = args[1]
metaFile = args[2]
selectedColumn = args[3]
outputFile = args[4]

exprData <- read.table(inputFile,sep=",", header=TRUE, row.names=1)
metaData <- read.table(metaFile, sep=",", header=TRUE)
names(exprData) <- sub("^X", "", names(exprData)) # drop "X" string in columns name
exprData <- as.matrix(exprData) # To matrix
row.names(metaData) <- metaData$HCVB_ID # Make index with SampleID

# Make subset from original metadata
metaDataExt <- metaData[metaData$DiseaseCourse=='RR' | metaData$DiseaseCourse=='CIS', c("DiseaseCourse", "Last_Known_Treat_Stat")] # subset RR and CIS
metaDataExt$DiseaseCourse <- factor(metaDataExt$DiseaseCourse)
metaDataExt$Last_Known_Treat_Stat <- factor(metaDataExt$Last_Known_Treat_Stat)

overlapped_samples <- intersect(colnames(exprData),rownames(metaDataExt))

metaDataExt <- metaDataExt[overlapped_samples,] # Selected samples only
exprData <- round(exprData[, overlapped_samples]) # Intersected samples only for expression, make integer

degSet <- DESeqDataSetFromMatrix(countData = exprData, colData = metaDataExt, design = ~ DiseaseCourse) # Perfom DESeq2
degSet <- DESeq(degSet)
res <- results(degSet) # result

print(head(res))