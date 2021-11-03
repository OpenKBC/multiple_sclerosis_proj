# ID converter from Ensembl ID to Entrez ID, please cleanup data by using python code before using this code
# Only working with csv file
# Usage Rscript
# Rscript IDconverter.R path/counts_norm_CD8.csv path/outputfile.csv

library("AnnotationDbi")
library("org.Hs.eg.db")

inputPath = Sys.getenv("efspoint")
step1Input = Sys.getenv("startFile")
inputFile = gsub(".csv", ".step1.csv", step1Input) # File from step1
inputFile = paste(inputPath,inputFile,sep="") # Full path with file name

#str_split
data<-read.table(inputFile, row.names=1, sep=',', header=TRUE) # Read data
names(data) <- sub("^X", "", names(data)) # drop "X" string in columns name

### Warning ###
# Entrez ID might duplicate for Ensemble ID
entrez = mapIds(org.Hs.eg.db,  keys=row.names(data), column="ENTREZID", keytype="ENSEMBL", multiVals="first")
row.names(data)<-make.names(entrez, unique=TRUE)
row.names(data) <- sub("^X", "", row.names(data)) # drop "X" string in index name

outputFile = gsub('.csv','.step2.csv',step1Input) # File name replacement for output
outputFile = paste(inputPath,outputFile,sep="") # Full path with file name
write.table(data, outputFile, sep=',', row.names = TRUE, col.names = TRUE) # Write result