rm(list=ls())
library(dplyr)
table <- read.csv("outputs/latest/refreshing_redintegration.csv")

table <- table |> 
    mutate(
        position = as.integer(position + 1),
        #selected_position = as.integer(selected_position + 1),
        interval_index = as.integer(interval_index + 1),
        candidate_index = as.integer(candidate_index + 1),
        refreshing_cycle = as.integer(refreshing_cycle + 1)
    ) |> 
    select(-simulation)

# table1 <- table |> filter(!is.na(candidate_index)) |> 
#     select(-c(selected_position, selected_stren))

# #View(table)

# table2 <- table |> filter(!is.na(selected_position)) |> 
#     select(-c(trial))

table3 <- table |> 
    filter(
        trial == 1,
        interval_index == 4
    ) |> 
    select(
        -c(
            trial,
            cycle,
            type,
            interval_index
        )
    )
