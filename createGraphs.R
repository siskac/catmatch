library(ggplot2)

# total grid search

data <- read.csv(file = "param_search_coat_color_pattern_multi.csv")

plot.loss = ggplot(data, aes(x = epochs, y = val_loss)) + facet_wrap(factor(decay)~factor(learning_rate), scale = "free_y") + 
			geom_smooth(method = "loess", aes(colour = factor(filter_size)), se = FALSE, alpha = 0.5) + 
                        ylab("validation loss") + guides(fill=guide_legend(title="Filter Size"))

plot.acc =  ggplot(data, aes(x = epochs, y = val_acc)) + facet_wrap(factor(decay)~factor(learning_rate), scale = "free_y") + 
                        geom_smooth(method = "loess", aes(colour = factor(filter_size)), se = FALSE, alpha = 0.5) + 
                        ylab("validation accuracy") + guides(fill=guide_legend(title="Filter Size"))
