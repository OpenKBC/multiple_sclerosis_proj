# Reference: http://bioconductor.org/packages/devel/bioc/vignettes/DESeq2/inst/doc/DESeq2.html
#
# This code calculates DESeq2 DEG from the matrix with only specific condition
# Example: Rscript inputfile metafile columnname_in_meta condition1 condition2 outputfile
# inputfile = "./sample_CD4_ext.csv"
# metafile = "./sample_CD4_meta.csv"
# outputfile = "./CD4_DEG.csv"

#library(tidyverse)
library(DESeq2)
library(tximport)

args = commandArgs(trailingOnly=TRUE)
inputFile = args[1]
metaFile = args[2]
outputFile = args[3]

exprData <- read.table(inputFile,sep=",", header=TRUE, row.names=1)
metaData <- read.table(metaFile, sep=",", header=TRUE, row.names=1)

names(exprData) <- sub("^X", "", names(exprData)) # drop "X" string in columns name
exprData <- as.matrix(exprData) # To matrix
metaData$conditions <- factor(metaData$conditions)

exprData <- round(exprData) # Intersected samples only for expression, make integer

degSet <- DESeqDataSetFromMatrix(countData = exprData, colData = metaData, design = ~ conditions) # Perfom DESeq2
degSet <- DESeq(degSet)
res <- results(degSet) # result

write.table(res, file = outputFile, row.names = TRUE, col.names = TRUE,)