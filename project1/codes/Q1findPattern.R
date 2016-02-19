data <- read.csv("network_backup_dataset.csv", header = TRUE, fill = TRUE);
work_flows = c("work_flow_0", "work_flow_1", "work_flow_2", "work_flow_3", "work_flow_4");
days = c("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday");
for (i in 0:4) {
  work_flow <- data[data$Work.Flow.ID == paste(c("work_flow_", i), collapse = "") & data$Week.. < 4, ];
  vector = numeric();
  for (j in 1:20) {
    index = j %% 7;
    week_number = as.integer(j / 7) + 1;
    if (index == 0) {
      index = 7;
      week_number = as.integer(j / 7);
    }
    vector[j] <- sum(work_flow[work_flow$Week.. == (week_number) & work_flow$Day.of.Week == days[index], 6], na.rm = TRUE);
  }
  plot(c(1:20), vector, type = 'b', ylim = c(0, max(vector) + 1), main = paste(c("Copy Size Over Time For Work Flow", i), collapse = " "), xlab = "Time (Day)", ylab = "Copy Size (GB)");
}
