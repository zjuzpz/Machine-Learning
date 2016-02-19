
library("MASS")
library(mlbench)
networkData <- read.csv("network_backup_dataset.csv", header = TRUE, fill = TRUE);
randomData <- read.csv("random_data_backup_dataset.csv", header = TRUE, fill = TRUE);
#summary(randomData)
#plot(Size.of.Backup..GB.~., data = networkData)
#plot(Size.of.Backup..GB.~., data = randomData)
lm.fit = lm(Size.of.Backup..GB.~., data = randomData)
#lm.fit = lm(Size.of.Backup..GB.~Week.., data = randomData)
#lm.fit = lm(Size.of.Backup..GB.~Day.of.Week, data = randomData)
#lm.fit = lm(Size.of.Backup..GB.~Backup.Start.Time...Hour.of.Day, data = randomData)
#lm.fit = lm(Size.of.Backup..GB.~Work.Flow.ID, data = randomData)
#lm.fit = lm(Size.of.Backup..GB.~File.Name, data = randomData)
#lm.fit = lm(Size.of.Backup..GB.~Backup.Time..hour., data = randomData)

#plot(lm.fit)
summary(lm.fit)
lm.predict <- predict(lm.fit)
sqrt(mean((lm.predict-randomData$Size.of.Backup..GB.)^2))
plot(randomData$Size.of.Backup..GB., col="red", main="Linear regression - Fitted values(blue) and actual values(red) scattered plot over time", cex = 0.1)
par(new=TRUE)
plot(lm.predict, col="blue", axes=FALSE, ann=FALSE, cex = 0.1 )

plot(lm.predict-randomData$Size.of.Backup..GB., col="red", main="Linear regression - residuals versus fitted values plot", cex = 0.1)

# 10-fold validation

d <- split(randomData,rep(1:10))
lm.fit1 = lm(Size.of.Backup..GB.~., data = rbind(d[[2]], d[[3]], d[[4]], d[[5]], d[[6]], d[[7]], d[[8]], d[[9]], d[[10]]))
lm.fit2 = lm(Size.of.Backup..GB.~., data = rbind(d[[1]], d[[3]], d[[4]], d[[5]], d[[6]], d[[7]], d[[8]], d[[9]], d[[10]]))
lm.fit3 = lm(Size.of.Backup..GB.~., data = rbind(d[[1]], d[[2]], d[[4]], d[[5]], d[[6]], d[[7]], d[[8]], d[[9]], d[[10]]))
lm.fit4 = lm(Size.of.Backup..GB.~., data = rbind(d[[1]], d[[2]], d[[3]], d[[5]], d[[6]], d[[7]], d[[8]], d[[9]], d[[10]]))
lm.fit5 = lm(Size.of.Backup..GB.~., data = rbind(d[[1]], d[[2]], d[[3]], d[[4]], d[[6]], d[[7]], d[[8]], d[[9]], d[[10]]))
lm.fit6 = lm(Size.of.Backup..GB.~., data = rbind(d[[1]], d[[2]], d[[3]], d[[4]], d[[5]], d[[7]], d[[8]], d[[9]], d[[10]]))
lm.fit7 = lm(Size.of.Backup..GB.~., data = rbind(d[[1]], d[[2]], d[[3]], d[[4]], d[[5]], d[[6]], d[[8]], d[[9]], d[[10]]))
lm.fit8 = lm(Size.of.Backup..GB.~., data = rbind(d[[1]], d[[2]], d[[3]], d[[4]], d[[5]], d[[6]], d[[7]], d[[9]], d[[10]]))
lm.fit9 = lm(Size.of.Backup..GB.~., data = rbind(d[[1]], d[[2]], d[[3]], d[[4]], d[[5]], d[[6]], d[[7]], d[[8]], d[[10]]))
lm.fit10 = lm(Size.of.Backup..GB.~., data = rbind(d[[1]], d[[2]], d[[3]], d[[4]], d[[5]], d[[6]], d[[7]], d[[8]], d[[9]]))

#plot(lm.fit)
#summary(lm.fit)
#abline(lm.fit, col = 'red')

lm.predict1 <- predict(lm.fit1, d[[1]])
lm.predict2 <- predict(lm.fit2, d[[2]])
lm.predict3 <- predict(lm.fit3, d[[3]])
lm.predict4 <- predict(lm.fit4, d[[4]])
lm.predict5 <- predict(lm.fit5, d[[5]])
lm.predict6 <- predict(lm.fit6, d[[6]])
lm.predict7 <- predict(lm.fit7, d[[7]])
lm.predict8 <- predict(lm.fit8, d[[8]])
lm.predict9 <- predict(lm.fit9, d[[9]])
lm.predict10 <- predict(lm.fit10, d[[10]])

MSE <- vector("numeric", 10)
MSE[1] <- sqrt(mean((lm.predict1-randomData$Size.of.Backup..GB.)^2))
MSE[2] <- sqrt(mean((lm.predict2-randomData$Size.of.Backup..GB.)^2))
MSE[3] <- sqrt(mean((lm.predict3-randomData$Size.of.Backup..GB.)^2))
MSE[4] <- sqrt(mean((lm.predict4-randomData$Size.of.Backup..GB.)^2))
MSE[5] <- sqrt(mean((lm.predict5-randomData$Size.of.Backup..GB.)^2))
MSE[6] <- sqrt(mean((lm.predict6-randomData$Size.of.Backup..GB.)^2))
MSE[7] <- sqrt(mean((lm.predict7-randomData$Size.of.Backup..GB.)^2))
MSE[8] <- sqrt(mean((lm.predict8-randomData$Size.of.Backup..GB.)^2))
MSE[9] <- sqrt(mean((lm.predict9-randomData$Size.of.Backup..GB.)^2))
MSE[10] <- sqrt(mean((lm.predict10-randomData$Size.of.Backup..GB.)^2))

MSE
mean(MSE)
