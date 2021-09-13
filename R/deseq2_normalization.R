##################################################################################
##### normalization using DESeq2 - get normalized and vst transformed counts #####
##################################################################################
### install DESeq2, tximport packages from Bioconductor
# if (!requireNamespace("BiocManager", quietly = TRUE))
#   install.packages("BiocManager")
# BiocManager::install("DESeq2")
# BiocManager::install("tximport")
library(tidyverse)
library(DESeq2)
library(tximport)

data_path <- "~/Downloads/MS_RNAseq_NAE1"
setwd(data_path)

# loading metadata
metadata <- read_csv(paste0(data_path,"/EPIC_HCvB_metadata_baseline_updated-share.csv"))
colnames(metadata)[1] <- "sampleID"

# loading rsem filelist
files <- list.files(path=paste0(data_path,"/rsem_counts"), pattern="*.genes.results", recursive = TRUE, full.names = TRUE)

# create sample table
sampleTable <- data.frame(sampleID = str_extract(files, "\\d{5}\\w"), CellType = str_extract(files, "CD\\d{1,2}"), files = files) %>% 
  left_join(., metadata, by="sampleID")
row.names(sampleTable) <- paste(sampleTable$sampleID, sampleTable$CellType, sep=".")


# function for loading rsem counts and normalization
getNormCounts <- function(celltypes, files, sampleTable){
  rsem.gene.sub <- tximport(files[grep(celltypes, files)], type = "rsem", txIn = FALSE, txOut = FALSE)
  sampleTable.sub <- sampleTable %>% filter(files %in% files[grep(celltypes, files)]) %>% 
    arrange(match(files, files[grep(celltypes, files)]))
  
  rsem.gene.sub$length[rsem.gene.sub$length == 0] <- 1
  cds.sub <- DESeqDataSetFromTximport(txi=rsem.gene.sub, colData=sampleTable.sub, design=~1)
  cds.sub <- cds.sub[ rowSums(counts(cds.sub)) > 0, ]
  cds.sub <- DESeq(cds.sub)
  return(cds.sub)
}

# run function
celltypes <- c("CD4","CD8","CD14")

deseq_obj <- list()
for (i in celltypes){
  deseq_obj[[i]] <- getNormCounts(i, files, sampleTable)
}


### save count matrix
# normalized counts
write.csv(counts(deseq_obj$CD4, normalized = TRUE), "counts_norm_CD4.csv")
write.csv(counts(deseq_obj$CD8, normalized = TRUE), "counts_norm_CD8.csv")
write.csv(counts(deseq_obj$CD14, normalized = TRUE), "counts_norm_CD14.csv")

# vst(variance stabilization transformation) transformed counts
write.csv(assay(vst(deseq_obj$CD4)), "counts_vst_CD4.csv")
write.csv(assay(vst(deseq_obj$CD8)), "counts_vst_CD8.csv")
write.csv(assay(vst(deseq_obj$CD14)), "counts_vst_CD14.csv")

# rlog transformed counts
write.csv(assay(rlog(deseq_obj$CD4)), "counts_rlog_CD4.csv")
write.csv(assay(rlog(deseq_obj$CD8)), "counts_rlog_CD8.csv")
write.csv(assay(rlog(deseq_obj$CD14)), "counts_rlog_CD14.csv")



