### install DESeq2, tximport packages from Bioconductor
if (!requireNamespace("BiocManager", quietly = TRUE))
  install.packages("BiocManager", repos='http://cran.us.r-project.org')
  BiocManager::install("DESeq2")
  BiocManager::install("tximport")
  BiocManager::install("AnnotationDbi")
  BiocManager::install("org.Hs.eg.db")