rm(list=ls())
Sys.setenv(LANG = "en")

library(dplyr)
library(tidyr)
library(ggplot2)

paths <- list.dirs("outputs/R_outputs", recursive = FALSE)
# choose a path:
paths <- "outputs/R_outputs/ref plus nonorthogonal"

sheets <- list.files(paths, pattern = "\\.csv$")
sheet_dirs <- list.files(paths, pattern = "\\.csv$", full.names = T)

for (i in seq_along(sheets)) {assign(tools::file_path_sans_ext(sheets[i]), read.csv(sheet_dirs[i]))}

# Hebb plot
trials |>  
  summarise(
    .by = c(cycle, type),
    mean = mean(accuracy)
  ) |> 
  mutate(cycle = cycle + 1) |> 
  ggplot(aes(y=mean, x=cycle, group = type)) +
  geom_line(aes(color = type)) +
  ylim(0,1)

encoding |> 
  summarise(
    .by = (cycle),
    mean(encoding_strength)
  )

ret <- retrieval |> 
  mutate(
    output_position = output_position + 1,
    candidate_position = candidate_position + 1
  ) |> 
  pivot_wider(
    id_cols = c(simulation, trial, cycle, type, output_position), 
    names_from = candidate_position, 
    values_from = similarity) |> 
  filter(simulation == 1) |> 
  mutate(cycle = cycle + 1)

ret1.f1 <- ret |> 
  filter(trial == 1) |> 
  select(-c(1:4))
