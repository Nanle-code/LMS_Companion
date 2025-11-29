#Load data from IRIS repo
data<-iris
#data.frame()

#Run a brief decription of the dataset
summary(data)

#show the  structure of the data set
str(data)

# Show the first 5 rows of the dataframe
head(data)

#show the bottom 5 row of the dataframe
tail(data)

#Quick identification and undertanting of the dataframe 
dim(data)
col_names <- names(data)
col_names
class(col_names)
col_names[1]

#Run a class funtion on the data set columns to know thier datatypes
sapply(data, class)

install.packages("psych")
library(psych)

pairs.panels(iris[, 1:4], 
             method = "spearman", 
             hist.col = "#00AFBB", 
             density = TRUE, 
             ellipses = TRUE, 
             main = "Scatterplot Matrix with Correlation and Histograms")

boxplot(data$Sepal.Length,
        main = "Box Plot of Sepal Length",
        ylab = "Sepal Length (cm)",
        col = "steelblue")


boxplot(Sepal.Length ~ Species,
        data = data,
        main = "Sepal Length by Species",
        xlab = "Species",
        ylab = "Sepal Length (cm)",
        col = c("setosa" = "#00AFBB", "versicolor" = "#E7B800", "virginica" = "#FC4E07"))

boxplot(Sepal.Width ~ Species,
        data = data,
        main = "Sepal Width by Species",
        xlab = "Species",
        ylab = "Sepal Width (cm)",
        col = c("setosa" = "#00AFBB", "versicolor" = "#E7B800", "virginica" = "#FC4E07"))

boxplot(Petal.Width ~ Species,
        data = data,
        main = "Petal Width by Species",
        xlab = "Species",
        ylab = "Petal Width (cm)",
        col = c("setosa" = "#00AFBB", "versicolor" = "#E7B800", "virginica" = "#FC4E07"))


boxplot(Petal.Length ~ Species,
        data = data,
        main = "Petal Length by Species",
        xlab = "Species",
        ylab = "Petal Length (cm)",
        col = c("setosa" = "#00AFBB", "versicolor" = "#E7B800", "virginica" = "#FC4E07"))


# Histogram for Sepal Length
hist(iris$Sepal.Length,
     main = "Histogram of Sepal Length",
     xlab = "Sepal Length (cm)",
     ylab = "Frequency",
     col = "skyblue",
     border = "black")

# Histogram for Sepal Width
hist(data$Sepal.Width,
     main = "Histogram of Sepal Width",
     xlab = "Sepal Width (cm)",
     ylab = "Frequency",
     col = "lightgreen",
     border = "black")

# Histogram for Petal Length
hist(data$Petal.Length,
     main = "Histogram of Petal Length",
     xlab = "Petal Length (cm)",
     ylab = "Frequency",
     col = "salmon",
     border = "black")

# Histogram for Petal Width
hist(data$Petal.Width,
     main = "Histogram of Petal Width",
     xlab = "Petal Width (cm)",
     ylab = "Frequency",
     col = "gold",
     border = "black")


plot(Petal.Width ~ Petal.Length, data = data,
     main = "Iris Petal Length vs. Width",
     xlab = "Petal Length (cm)",
     ylab = "Petal Width (cm)",
     col = "dodgerblue1",
     pch = 16)


# Calculate the mean for each column
sapply(data[, 1:4], mean, na.rm=TRUE)

# Calculate the median for each column
sapply(data[, 1:4], median, na.rm=TRUE)

#Calculate the standard deviation for each column
sapply(iris[, 1:4], sd, na.rm = TRUE)

#install 
install.packages("class")
# Load the library
library(class)


# Shuffle the data to ensure random sampling
set.seed(123) 
data_sample <- data[sample(nrow(iris)), ]

# Separate the features (input) and the target variable (species)
# The first 4 columns are features, the 5th is the species
featues_x <- data_sample[, 1:4]
label_y <- data_sample[, 5]


# Determine the split point (e.g., 70% for training)
train_size <- floor(0.7 * nrow(data_sample))
x_train <- feature_x[1:train_size, ]
x_test <- feature_x[(train_size + 1):nrow(feature_x), ]
y_train <- label_y[1:train_size]
y_test <- label_y[(train_size + 1):nrow(label_y)]


# Choose a value for k (e.g., 7)
k <- 7

# Use the knn() function from the class package
# The function takes the training features, testing features, training labels, and the value of k
predictions <- knn(train = x_train, test = x_test, cl = y_train, k = k)


# Calculate the accuracy
accuracy <- mean(predictions == y_test)

# Print the accuracy
print(paste("Accuracy:", round(accuracy * 100, 2), "%"))

# for k=1
predictions_k1 <- knn(train = x_train, test = x_test, cl = y_train, k = 1)
accuracy_k1 <- mean(predictions_k1 == y_test)
print(paste("Accuracy for k=1:", round(accuracy_k1 * 100, 2), "%"))

# for k=5
predictions_k5 <- knn(train = x_train, test = x_test, cl = y_train, k = 5)
accuracy_k5 <- mean(predictions_k5 == y_test)
print(paste("Accuracy for k=5:", round(accuracy_k5 * 100, 2), "%"))