rm(list=ls())
Sys.setenv(LANG = "en")

library(dplyr)
library(tidyr)
library(ggplot2)

data <- read.csv(
    "outputs/testing/firstCycle/param_sweep_results.csv",
    check.names = FALSE
)
