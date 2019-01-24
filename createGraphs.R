library(gridExtra)
library(ggplot2)

data <- read.csv(file = "param_search_coat_color_pattern_multi.csv")

plt.acc = ggplot(data, aes(x = epochs, y = val_acc)) + facet_grid(.~factor(learning_rate)) + geom_line(aes(colour = factor(decay))) + 
		 labs(colour="decay") + ylab("validation accuracy")
plt.loss = ggplot(data, aes(x = epochs, y = val_loss)) + facet_grid(.~factor(learning_rate)) + geom_line(aes(colour = factor(decay))) + 
		  labs(colour="decay") + ylab("validation loss")

grid.arrange(plt.acc, plt.loss)

plt.acc.zoomedin = ggplot(data[data$learning_rate < 0.005,], aes(x = epochs, y = val_acc)) + facet_grid(.~factor(learning_rate)) + 
			  geom_line(aes(colour = factor(decay))) + labs(colour="decay") + ylab("validation accuracy")
plt.loss.zoomedin = ggplot(data[data$learning_rate < 0.005,], aes(x = epochs, y = val_loss)) + facet_grid(.~factor(learning_rate)) + 
                           geom_line(aes(colour = factor(decay))) + labs(colour="decay") + ylab("validation loss")

grid.arrange(plt.acc.zoomedin, plt.loss.zoomedin)
