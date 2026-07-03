rm(list=ls())
table <- read.csv("outputs/latest/test.csv")

table <- table |> 
    mutate(
        position = as.integer(position + 1),
        selected_position = as.integer(selected_position + 1),
        interval_index = as.integer(interval_index + 1)
    ) |> 
    select(-simulation)

table1 <- table |> filter(!is.na(position)) |> 
    select(-c(selected_position, selected_stren))

table2 <- table |> filter(!is.na(selected_position)) |> 
    select(-c(position))
