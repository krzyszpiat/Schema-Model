rm(list=ls())
Sys.setenv(LANG = "en")

library(dplyr)
library(tidyr)
library(ggplot2)

exp2 <- readRDS("analysis/empiricalData/Exp2.RDS")
exp1b <- readRDS("analysis/empiricalData/Exp1b.RDS")
exp1a <- readRDS("analysis/empiricalData/Exp1a.RDS")

makePlot <- function(input, title){

exp2_Acc <- input |> 
    mutate(
        pos1 = CRESP1 == RESP1,
        pos2 = CRESP2 == RESP2,
        pos3 = CRESP3 == RESP3,
        pos4 = CRESP4 == RESP4,
        pos5 = CRESP5 == RESP5,
        pos6 = CRESP6 == RESP6,
        pos7 = CRESP7 == RESP7,
        pos8 = CRESP8 == RESP8
    ) |> 
    select(-c(paste0("CRESP", 1:8), paste0("RESP", 1:8)))

exp2_curves <- exp2_Acc |> 
    summarise(
        .by = c(Cycle, List),
        across(num_range("pos", 1:8), ~ mean(.x, na.rm = T))
    )

exp2_long <- exp2_curves |>
  pivot_longer(
    cols = starts_with("pos"),
    names_to = "position",
    values_to = "accuracy",
    names_prefix = "pos",
    names_transform = list(position = as.integer)
  ) |> 
    mutate(
        Cycle = as.factor(Cycle),
        position = as.factor(position)
    )


plot_theme <- theme(
  strip.text   = element_text(size = 16),
  plot.title   = element_text(size = 20, hjust = 0.5),
  axis.title.x = element_blank(),
  axis.title.y = element_text(size = 14),
  axis.text.x  = element_text(size = 13)
)

plot <- exp2_long |> 
    ggplot(aes(
        x = position, 
        y = accuracy, 
        color=Cycle, 
        group=Cycle,
        alpha=Cycle
    )) +
    geom_line(size=2) +
    geom_point(size=4) +
    facet_wrap(~ List) +
    scale_color_viridis_d(option = "A", direction = -1) +
    ylim(0,1) +
    #scale_x_continuous(breaks = 1:8) +
    ylab("Accuracy") +
    plot_theme +
    ggtitle(title)

return(plot)}

plot1 <- makePlot(exp2, "Exp2, full dataset")

exp2a <- exp2 |> filter(AwarenessClosed == "t")
exp2n <- exp2 |> filter(AwarenessClosed == "n")

plot2 <- makePlot(exp2a, "Exp2, aware participants")
plot3 <- makePlot(exp2n, "Exp2, non-aware participants")

plot4 <- makePlot(exp1b, "Exp1b")
plot5 <- makePlot(exp1a, "Exp1a")

ggsave("analysis/Exp2_Full.png", plot1, width = 8, height = 5, dpi = 300)
ggsave("analysis/Exp2_Aware.png", plot2, width = 8, height = 5, dpi = 300)
ggsave("analysis/Exp2_NonAware.png",   plot3,   width = 8, height = 5, dpi = 300)

ggsave("analysis/Exp1b.png",   plot4,   width = 8, height = 5, dpi = 300)
ggsave("analysis/Exp1a.png",   plot5,   width = 8, height = 5, dpi = 300)
