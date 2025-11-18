# Load your dataset (example with a CSV file)
# iris

datas <- data(iris)

# Display summary statistics
summary(data)

# Display structure of the dataset
str(data)

# Display first few rows
head(data)

# Display last few rows
tail(data)

# Get dimensions (rows, columns)
dim(data)

# Get column names
names(data)

# Check data types of each column
sapply(data, class)

# Display basic info
glimpse(data)  # requires dplyr package