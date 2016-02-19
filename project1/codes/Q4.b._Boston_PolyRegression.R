library('Metrics');
data <- na.omit(read.csv("housing_data.csv", header = FALSE, fill = TRUE));
colnames(data) <- c("C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9", "C10", "C11", "C12", "C13", "C14");
set.seed(10);
whole_data_list <- split(data, sample(1:10, nrow(data), replace = TRUE));
mean_rmse_vec <- numeric();

# Poly degree
for (k in 1:7) {
  rmse_vec <- numeric();
  # Ten fold
  for (i in 1:10) {
    test_data_set <- whole_data_list[[i]]
    if (i == 10) {
      index = 1;
    } else {
      index = i + 1;
    }
    training_data_set <- whole_data_list[[index]]
    for (j in 1:10) {
      if (j != i && j != index) {
        training_data_set <- rbind(training_data_set, whole_data_list[[j]]);
      }
    }
    
    if (k == 1) {
      reg <- lm(C14 ~ C1 + C2 + C5 + C6 + C8 + C9 + C10 + C11 + C12 + C13, data = training_data_set);
      predicted = predict(reg, test_data_set);
      rmse_vec <- c(rmse_vec, rmse(test_data_set$C14, predicted));
    } else {
      reg <- lm(C14 ~ poly(C1, k) + poly(C2, k) + poly(C5, k) + poly(C6, k) + poly(C8, k) + poly(C9, k) + poly(C10, k) + poly(C11, k) + poly(C12, k) + poly(C13, k), data = training_data_set);
      predicted = predict(reg, test_data_set);
      rmse_vec <- c(rmse_vec, rmse(test_data_set$C14, predicted));
    }
  }
  mean_rmse_vec <- c(mean_rmse_vec, mean(rmse_vec));
}

degree <- c(1, 2, 3, 4, 5, 6, 7);
plot(degree, mean_rmse_vec, xlim = c(1,7), xlab = "Degree", ylab = "Mean RMSE", main = "Mean RMSE vs. Degree");
plot(degree[1:4], mean_rmse_vec[1:4], xlab = "Degree", ylab = "Mean RMSE", main = "Mean RMSE vs. Degree (4 points)")