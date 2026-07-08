rm(list=ls())
Sys.setenv(LANG = "en")

library(dplyr)
library(tidyr)
library(ggplot2)


param_names <- c("threshold", "refresh_threshold", "decay_rate", "decay_slope", "refresh_rate")

# --- 1. Empirical target: Exp2, Cycle 1 --------------------------------------
exp2 <- readRDS("analysis/empiricalData/Exp2.RDS")

emp_target <- exp2 |>
    mutate(
        pos1 = CRESP1 == RESP1, pos2 = CRESP2 == RESP2,
        pos3 = CRESP3 == RESP3, pos4 = CRESP4 == RESP4,
        pos5 = CRESP5 == RESP5, pos6 = CRESP6 == RESP6,
        pos7 = CRESP7 == RESP7, pos8 = CRESP8 == RESP8
    ) |>
    filter(Cycle == 1) |>
    summarise(
        .by = List,
        across(num_range("pos", 1:8), ~ mean(.x, na.rm = TRUE))
    ) |>
    pivot_longer(
        cols = starts_with("pos"),
        names_to = "position", values_to = "emp_acc",
        names_prefix = "pos", names_transform = list(position = as.integer)
    )

# empirical "Random" list = pure simple span -> reference for Filler List
emp_random <- emp_target |> filter(List == "Random") |> select(position, emp_acc)

# --- 2. Simulated curves -----------------------------------------------------
sim <- read.csv("outputs/testing/firstCycle/param_sweep_results.csv",
                check.names = FALSE,
                sep = ","
            )

sim_long <- sim |>
    pivot_longer(
        cols = as.character(0:7),
        names_to = "position", values_to = "sim_acc",
        names_transform = list(position = as.integer)
    ) |>
    mutate(position = position + 1L)   # 0-7 -> 1-8

# Compare the Filler List (never repeated) against empirical Random simple span
sim_filler <- sim_long |> filter(type == "Filler List")

# --- 3. Score each combo by RMSE vs empirical target -------------------------
fits <- sim_filler |>
    left_join(emp_random, by = "position") |>
    summarise(
        .by = all_of(param_names),
        RMSE = sqrt(mean((sim_acc - emp_acc)^2)),
        MAE  = mean(abs(sim_acc - emp_acc))
    ) |>
    arrange(RMSE)

write.csv(fits, "outputs/testing/firstCycle/fit_ranking.csv", row.names = FALSE)

# --- 4. Plot A: top-N best-fitting curves vs empirical -----------------------
N <- 10
top_combos <- head(fits, N) |>
    mutate(combo = sprintf("thr=%g ref_thr=%g dr=%g ds=%g rr=%g (RMSE=%.3f)",
                           threshold, refresh_threshold, decay_rate, decay_slope, refresh_rate, RMSE))

top_curves <- sim_filler |>
    inner_join(top_combos |> select(all_of(param_names), combo, RMSE),
               by = param_names)

plot_fit <- ggplot() +
    geom_line(data = top_curves,
              aes(position, sim_acc, group = combo, color = RMSE), linewidth = 1) +
    geom_line(data = emp_random, aes(position, emp_acc),
              color = "red", linewidth = 2, linetype = "dashed") +
    geom_point(data = emp_random, aes(position, emp_acc),
               color = "red", size = 3) +
    scale_color_viridis_c(option = "D", direction = -1) +
    scale_x_continuous(breaks = 1:8) +
    ylim(0, 1) +
    labs(x = "Serial position", y = "Accuracy",
         title = sprintf("Top %d fitting Filler-List curves vs Exp2 Cycle-1 (red dashed)", N)) +
    theme_minimal(base_size = 13)

ggsave("outputs/testing/firstCycle/fit_topN_curves.png", plot_fit,
       width = 9, height = 6, dpi = 300)

# --- 5. Plot B: RMSE landscape across the whole parameter space --------------
# x = decay_rate, y = decay_slope, fill = RMSE; facet threshold (rows) x refresh_rate (cols)

gridplot <- function(input, gridRow, gridCol){

    gridRname <- rlang::as_label(rlang::enquo(gridRow))
    gridCname <- rlang::as_label(rlang::enquo(gridCol))

    plot <- input |>
        ggplot(aes(factor(decay_rate), factor(decay_slope), fill = RMSE)) +
        geom_tile() +
        facet_grid(
            rows = vars({{gridRow}}),
            cols = vars({{gridCol}}),
            labeller = label_both
        ) +
        scale_fill_viridis_c(option = "A", direction = 1) +
        labs(x = "decay_rate", y = "decay_slope",
            title = sprintf("RMSE landscape. Rows = %s, Cols = %s", gridRname, gridCname)) +
        theme_minimal(base_size = 11) +
        theme(axis.text.x = element_text(angle = 90, vjust = 0.5))

    return(plot)
}

gridplot(fits, threshold, refresh_rate)

gridplot(fits, refresh_threshold, refresh_rate)

grid20 <- gridplot(fits |> filter(threshold == 20), refresh_threshold, refresh_rate)
grid30 <- gridplot(fits |> filter(threshold == 30), refresh_threshold, refresh_rate)
grid40 <- gridplot(fits |> filter(threshold == 40), refresh_threshold, refresh_rate)
grid50 <- gridplot(fits |> filter(threshold == 50), refresh_threshold, refresh_rate)
grid60 <- gridplot(fits |> filter(threshold == 60), refresh_threshold, refresh_rate)


ggsave("outputs/testing/firstCycle/fit_rmse_threshold20.png", grid20, width = 14, height = 9, dpi = 200)
ggsave("outputs/testing/firstCycle/fit_rmse_threshold30.png", grid30, width = 14, height = 9, dpi = 200)
ggsave("outputs/testing/firstCycle/fit_rmse_threshold40.png", grid40, width = 14, height = 9, dpi = 200)
ggsave("outputs/testing/firstCycle/fit_rmse_threshold50.png", grid50, width = 14, height = 9, dpi = 200)
ggsave("outputs/testing/firstCycle/fit_rmse_threshold60.png", grid60, width = 14, height = 9, dpi = 200)
