rm(list=ls())
Sys.setenv(LANG = "en")

library(dplyr)

paths <- list.dirs("outputs/R_outputs", recursive = FALSE)
sheets <- list.files(paths, pattern = "\\.csv$")
sheet_dirs <- list.files(paths, pattern = "\\.csv$", full.names = T)

for (i in seq_along(sheets)) {
  
  assign(tools::file_path_sans_ext(sheets[i]), read.csv(sheet_dirs[i]))  

}

