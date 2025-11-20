#Load data from IRIS repo
data<-iris

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

boxplot(iris$Sepal.Length,
        main = "Box Plot of Sepal Length",
        ylab = "Sepal Length (cm)",
        col = "steelblue")


boxplot(Sepal.Length ~ Species,
        data = iris,
        main = "Sepal Length by Species",
        xlab = "Species",
        ylab = "Sepal Length (cm)",
        col = c("setosa" = "#00AFBB", "versicolor" = "#E7B800", "virginica" = "#FC4E07"))

boxplot(Sepal.Width ~ Species,
        data = iris,
        main = "Sepal Width by Species",
        xlab = "Species",
        ylab = "Sepal Width (cm)",
        col = c("setosa" = "#00AFBB", "versicolor" = "#E7B800", "virginica" = "#FC4E07"))

boxplot(Petal.Width ~ Species,
        data = iris,
        main = "Petal Width by Species",
        xlab = "Species",
        ylab = "Petal Width (cm)",
        col = c("setosa" = "#00AFBB", "versicolor" = "#E7B800", "virginica" = "#FC4E07"))


boxplot(Petal.Length ~ Species,
        data = iris,
        main = "Petal Length by Species",
        xlab = "Species",
        ylab = "Petal Length (cm)",
        col = c("setosa" = "#00AFBB", "versicolor" = "#E7B800", "virginica" = "#FC4E07"))
