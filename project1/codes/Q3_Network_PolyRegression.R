library('Metrics');
data <- na.omit(read.csv("network_backup_dataset.csv", header = TRUE, fill = TRUE));
data$Week.. <- as.numeric(data$Week..) - 1;
data$Day.of.Week <- as.numeric(data$Day.of.Week) - 1;
data$Work.Flow.ID <- as.numeric(data$Work.Flow.ID) - 1;
data$File.Name <- as.numeric(data$File.Name) - 1;
work_flows = sort(unique(data[, 4]));
days = sort(unique(data[, 2]));
# mean_rmse <- numeric();

work_flow <- data[data$Work.Flow.ID == work_flows[3], ];
print(work_flow[1, 4]);
row_count <- nrow(work_flow);
set.seed(10);
whole_data_list <- split(data, sample(1:10, nrow(data), replace = TRUE))
work_flow_list <- split(work_flow, sample(1:10, row_count, replace = TRUE))

# 
# for (i in 1:10) {
#   test_work_flow_set <- work_flow_list[[i]];
#   if (i == 10) {
#     index = 1;
#   } else {
#     index = i + 1;
#   }
#   training_work_flow_set <- work_flow_list[[index]];
#   for (j in 1:10) {
#     if (j != i && j != index) {
#       training_work_flow_set <- rbind(training_work_flow_set, work_flow_list[[j]]);
#     }
#   }
#   
#   fit1 <- lm(Size.of.Backup..GB. ~   Day.of.Week + Backup.Start.Time...Hour.of.Day+Backup.Time..hour., data=training_work_flow_set);
#   # fit1 <- lm(Size.of.Backup..GB. ~  Day.of.Week, data=training_set);
#   # fit1 <- lm(Size.of.Backup..GB. ~ poly(Day.of.Week, 2) + poly(Backup.Start.Time...Hour.of.Day, 2) + poly(File.Name, 2) + poly(Backup.Time..hour., 2), data=training_set);
#   # fit1 <- lm(Size.of.Backup..GB. ~ poly(Day.of.Week, 3) + poly(Backup.Start.Time...Hour.of.Day, 3) + poly(File.Name, 3) + poly(Backup.Time..hour., 3), data=training_set);
#   # fit1 <- lm(Size.of.Backup..GB. ~ poly(Day.of.Week, 4) + poly(Backup.Start.Time...Hour.of.Day, 4) + poly(File.Name, 4) + poly(Backup.Time..hour., 4), data=training_set);
#   summary(fit1);
#   predicted = predict(fit1, test_work_flow_set);
#   library('Metrics');
#   RMSE <- c(RMSE, rmse(test_work_flow_set$Size.of.Backup..GB., predicted));
# }
# # mean_rmse <- c(mean_rmse, mean(RMSE));
# mean_rmse <- mean(RMSE)
# print(mean_rmse)
# 
# for (i in 1:10) {
#   test_data_set <- whole_data_list[[i]]
#   test_work_flow_set <- work_flow_list[[i]];
#   if (i == 10) {
#     index = 1;
#   } else {
#     index = i + 1;
#   }
#   training_work_flow_set <- work_flow_list[[index]];
#   training_data_set <- whole_data_list[[index]]
#   for (j in 1:10) {
#     if (j != i && j != index) {
#       training_work_flow_set <- rbind(training_work_flow_set, work_flow_list[[j]]);
#       training_data_set <- rbind(training_data_set, whole_data_list[[j]]);
#     }
#   }
#   
#   fit1 <- lm(Size.of.Backup..GB. ~   Day.of.Week + Backup.Start.Time...Hour.of.Day+Backup.Time..hour., data=training_work_flow_set);
#   fit2 <- lm(Size.of.Backup..GB. ~ poly(Day.of.Week, 2) + poly(Backup.Start.Time...Hour.of.Day, 2) + poly(File.Name, 2) + poly(Backup.Time..hour., 2), data=training_data);
#   predicted = predict(fit1, test_set);
#   library('Metrics');
#   RMSE <- c(RMSE, rmse(test_set$Size.of.Backup..GB., predicted));
# }
# # mean_rmse <- c(mean_rmse, mean(RMSE));
# mean_rmse <- mean(RMSE)
# print(mean_rmse)

RMSE1 <- numeric();
RMSE2 <- numeric();
RMSE3 <- numeric();
RMSE4 <- numeric();
RMSE5 <- numeric();
RMSE6 <- numeric();

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
  reg1 <- lm(Size.of.Backup..GB. ~  Backup.Time..hour. + Work.Flow.ID, data=training_data_set);
  reg2 <- lm(Size.of.Backup..GB. ~ poly(Work.Flow.ID, 2)  + poly(Backup.Time..hour., 2), data=training_data_set);
  reg3 <- lm(Size.of.Backup..GB. ~ poly(Work.Flow.ID, 3)  + poly(Backup.Time..hour., 3), data=training_data_set);
  reg4 <- lm(Size.of.Backup..GB. ~ poly(Work.Flow.ID, 4)  + poly(Backup.Time..hour., 4), data=training_data_set);
  
  predicted = predict(reg1, test_data_set);
  RMSE1 <- c(RMSE1, rmse(test_data_set$Size.of.Backup..GB., predicted));
 
  predicted = predict(reg2, test_data_set);
  RMSE2 <- c(RMSE2, rmse(test_data_set$Size.of.Backup..GB., predicted));
  
  predicted = predict(reg3, test_data_set);
  RMSE3 <- c(RMSE3, rmse(test_data_set$Size.of.Backup..GB., predicted));
  
  predicted = predict(reg4, test_data_set);
  RMSE4 <- c(RMSE4, rmse(test_data_set$Size.of.Backup..GB., predicted));
  
}
# mean_rmse <- c(mean_rmse, mean(RMSE));
mean_rmse1 <- mean(RMSE1)
print(mean_rmse1)

mean_rmse2 <- mean(RMSE2)
print(mean_rmse2)

mean_rmse3 <- mean(RMSE3)
print(mean_rmse3)

mean_rmse4 <- mean(RMSE4)
print(mean_rmse4)

rmse <- numeric();
rmse <- c(rmse, RMSE1[1], RMSE2[1], RMSE3[1], RMSE4[1])
degree <- numeric();
degree <- c(degree, 1, 2, 3, 4)
plot(degree, rmse, xlim = c(1,4), xlab = "Degree", ylab = "RMSE", main = "RMSE vs. Degree (fixed)")

rmse_mean <- numeric();
rmse_mean <- c(rmse_mean, mean_rmse1,mean_rmse2, mean_rmse3,mean_rmse4)
plot(degree, rmse_mean, xlim = c(1,4), xlab = "Degree", ylab = "Mean RMSE", main = "Mean RMSE vs. Degree")

