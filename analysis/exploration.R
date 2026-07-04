rm(list=ls())
library(dplyr)
tbl <- read.csv("outputs/latest/refreshing_redintegration.csv")

table <- tbl |> 
    mutate(
        position = as.integer(position + 1),
        interval_index = as.integer(interval_index + 1),
        candidate_index = as.integer(candidate_index + 1),
        refreshing_cycle = as.integer(refreshing_cycle + 1),
        winning = as.integer(winning + 1)
    ) |> 
    select(-simulation)


table3 <- table |> 
    filter(
        trial == 1,
        interval_index == 6
    ) |> 
    select(
        -c(
            trial,
            cycle,
            type,
            interval_index
        )
    )
