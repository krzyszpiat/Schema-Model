rm(list=ls())
Sys.setenv(LANG = "en")

library(dplyr)
library(tidyr)
library(ggplot2)

data <- read.csv(
    "outputs/testing/firstCycle/param_sweep_results.csv",
    check.names = F
    
)


data_long <- data |> 
    pivot_longer(
        cols = c("0", "1", "2", "3", "4", "5", "6", "7"),
        names_to = "position",
        values_to = "accuracy",
        names_transform = list(position = as.integer)
    ) |> 
    mutate(
        position = as.factor(position + 1),
        threshold = as.factor(threshold),
        decay_rate = as.factor(decay_rate),
        decay_slope = as.factor(decay_slope),
        refresh_rate = as.factor(refresh_rate),
        List = as.factor(type)
    )


data_long_a <- data_long |> 
    group_by(threshold, position, decay_rate) |> 
    summarise(
        accuracy = mean(accuracy)
    )

plot1 <- data_long_a |> 
    ggplot(aes(
        x = position, 
        y = accuracy,
        group = decay_rate,
        color = decay_rate
    )) +
    geom_line(size=2) +
    geom_point(size=4) +
    facet_wrap(~ threshold) +
    scale_color_viridis_d(option = "A", direction = -1) +
    ylim(0,1) +
    #scale_x_continuous(breaks = 1:8) +
    ylab("Accuracy")

plot1


data_long_b <- data_long |> 
    filter(threshold == 40) |> 
    group_by(position, decay_rate, refresh_rate) |> 
    summarise(
        accuracy = mean(accuracy)
    )

plot2 <- data_long_b |> 
    ggplot(aes(
        x = position, 
        y = accuracy,
        group = decay_rate,
        color = decay_rate
    )) +
    geom_line(size=2) +
    geom_point(size=4) +
    facet_wrap(~ refresh_rate) +
    scale_color_viridis_d(option = "A", direction = -1) +
    ylim(0,1) +
    #scale_x_continuous(breaks = 1:8) +
    ylab("Accuracy") +
    ggtitle("Panes = refresh_rate")


plot2


data_long_c <- data_long |> 
    filter(
        threshold == 40,
        refresh_rate == 0.3
    ) |> 
    group_by(position, decay_rate, decay_slope) |> 
    summarise(
        accuracy = mean(accuracy)
    )

plot3 <- data_long_c |> 
    ggplot(aes(
        x = position, 
        y = accuracy,
        group = decay_rate,
        color = decay_rate
    )) +
    geom_line(size=2) +
    geom_point(size=4) +
    facet_wrap(~ decay_slope) +
    scale_color_viridis_d(option = "A", direction = -1) +
    ylim(0,1) +
    #scale_x_continuous(breaks = 1:8) +
    ylab("Accuracy") +
    ggtitle("Panes = decay slope")

plot3


threshold_filter <- 50

data_long_d <- data_long |> 
    filter(
        List == "Filler List",
        threshold == threshold_filter,
        refresh_rate %in% seq(0.3, 0.8, by=.1),
        decay_slope %in% c(0.2, 0.3),
        decay_rate %in% seq(0.1, 0.9, by=.1)
    ) |> 
    group_by(position, decay_rate, decay_slope, refresh_rate) |> 
    summarise(
        accuracy = mean(accuracy)
    )

plot4 <- data_long_d |> 
    ggplot(aes(
        x = position, 
        y = accuracy,
        group = decay_rate,
        color = decay_rate
    )) +
    geom_line(size=2) +
    geom_point(size=4) +
    facet_grid(decay_slope ~ refresh_rate) +
    scale_color_viridis_d(option = "A", direction = -1) +
    ylim(0,1) +
    #scale_x_continuous(breaks = 1:8) +
    ylab("Accuracy") +
    ggtitle(paste0("Columns: refresh rate, Rows: decay slope, Threshold = ", threshold_filter))

plot4
