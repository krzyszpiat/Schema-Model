rm(list=ls())
Sys.setenv(LANG = "en")

library(dplyr)
library(tidyr)

table <- read.csv("analysis/empiricalData/full_data.csv")

exp2 <- table |> 
  select(
    Subject, 
    Block = BlckNo.Block.,
    Cycle = HebbCycle.Trial.,
    Trial,
    List = ListType.Trial.,
    CRESP = trialTestButtons.CRESP.Trial.,
    RESP = trialTestButtons.RESP.Trial.,
    AwarenessClosed = AwarenessCheck2.RESP
  ) |> 
  filter(
    Block != 99,
    !is.na(Cycle)
  ) |> 
  separate(
    col = CRESP, 
    into = paste0("CRESP", 1:8), 
    sep = "}") %>% 
  separate(
    col = RESP, 
    into = paste0("RESP", 1:8), 
    sep = "}")
  
saveRDS(exp2, "analysis/empiricalData/Exp2.RDS")
