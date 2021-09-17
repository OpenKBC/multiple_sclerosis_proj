# ID converter from Ensembl ID to Entrez ID, please cleanup data by using python code before using this code
# Only working with csv file
# Usage Rscript
# Rscript IDconverter.R path/counts_norm_CD8.csv path/outputfile.csv

library("AnnotationDbi")
library("org.Hs.eg.db")

args = commandArgs(trailingOnly=TRUE)
inputFile = args[1] # with path
outputFile = args[2] # with path

#str_split
data<-read.table(inputFile, row.names=1, sep=',', header=TRUE) # Read data
names(data) <- sub("^X", "", names(data)) # drop "X" string in columns name

### Warning ###
# Entrez ID might duplicate for Ensemble ID
entrez = mapIds(org.Hs.eg.db,  keys=row.names(data), column="ENTREZID", keytype="ENSEMBL", multiVals="first")
row.names(data)<-make.names(entrez, unique=TRUE)
row.names(data) <- sub("^X", "", row.names(data)) # drop "X" string in index name
write.table(data, outputFile, sep=',', row.names = TRUE, col.names = TRUE) # Write result