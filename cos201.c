#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <stdbool.h>
// #include <math.h>

const int PASS_THRESHOLD = 40;
const int MAX_NAME = 100;
// struct Student
// {
//     /* data */
//     char name[100]; // Character array to store the student's name (max 99 characters + null terminator)
//     int rollNumber; // Integer to store the student's roll number
//     float marks;
// };

typedef struct
{
    char name[MAX_NAME];
    int rollNumber;
    float marks;
} Student;

// Function definition
bool is_integer(const char *input);                           // Checks if a string represents a valid integer
void createStudent(Student **students, int *count);           // Adds a new student to the array
void updateStudent(Student *students, int count);             // Updates an existing student's information
void deleteStudent(Student **students, int *count);           // Deletes a student from the array
void viewStudents(Student *students, int count);              // Displays all students in the array
void saveStudentsToFile(Student *students, int count);        // Saves student data to a file
int searchStudent(Student student[], int size, int searchId);
// int pot (Student student); // Searches for a student by ID

// Implementation
int main()
{
    char name[MAX_NAME];

    Student student1;

    printf("========================================\n");
    printf("    Welcome to the Student portal!    \n");
    printf("========================================\n\n");

    printf("Please enter your name: ");

    if (fgets(name, sizeof(name), stdin) != NULL)
    {
        name[strcspn(name, "\n")] = '\0';

        printf("\nWelcome, %s! It's great to meet you!\n", name);
    }
    else
    {
        printf("\nError reading input.\n");
        return 1;
    }

    printf("========================================\n");
    printf("    Enter your Exam mark    \n");
    printf("========================================\n\n");

    float marks;

    printf("Please enter your marks: ");
    if (scanf("%f", &marks) != 1)
    {
        printf("\nInvalid input. Please enter a numeric value for marks.\n");
        return 1;
    }
    if (marks >= PASS_THRESHOLD)
    {
        printf("\nCongratulations, %s! You have passed the exam with %.2f marks.\n", name, marks);
    }
    else
    {
        printf("\nSorry, %s. You have not passed the exam. You scored %.2f marks. Better luck next time!\n", name, marks);
    }

    printf("========================================\n");
    printf("    Student Record Management    \n");
    printf("========================================\n\n");

    Student *students2 = NULL;
    int studentCount = 0;
    int choice;
    float average = 0.0;
    int searchId = 0;
    int result = 0;
    float total = 0;

    while (1)
    {
        printf("\n===== STUDENT MANAGEMENT SYSTEM =====\n");
        printf("1. Add Student\n");
        printf("2. Modify Student\n");
        printf("3. Delete Student\n");
        printf("4. Display All Students\n");
        printf("5. Save to File\n");
        printf("6. Search Student by ID\n");
        printf("7. Calculate Average Score\n");
        printf("10. Exit\n");
        printf("Enter your choice: ");
        scanf("%d", &choice);
        getchar(); // clear input buffer

        switch (choice)
        {
        case 1:
            createStudent(&students2, &studentCount);
            viewStudents(students2, studentCount);
            break;
        case 2:
            updateStudent(students2, studentCount);
            viewStudents(students2, studentCount);
            break;
        case 3:
            deleteStudent(&students2, &studentCount);
            viewStudents(students2, studentCount);
            break;
        case 4:
            viewStudents(students2, studentCount);
            break;
        case 5:
            saveStudentsToFile(students2, studentCount);
            break;

        case 6:

            printf("Enter Student ID to search: ");
            scanf("%d", &searchId);
            result = searchStudent(students2, studentCount, searchId);
            if (result == -1)
            {
                printf("Student not found.\n");
            }
            
            break;

        case 7:
            // Average Score

            for (int i = 0; i < studentCount; i++)
            {
                
                total += students2[i].marks;
                
                average = total / studentCount;
            }
            printf("Total score is: %.2f\n", total);
            printf("The average score is: %.2f\n", average);
            break;

        case 10:
            printf("Exiting program...\n");
            free(students2);
            return 0;
        default:
            printf("Invalid choice! Try again.\n");
        }
    }

    return 0;
}

/**
 * @brief Create a Student object
 *
 * @param students
 * @param count
 */
void createStudent(Student **students, int *count)
{
    *students = realloc(*students, (*count + 1) * sizeof(Student));

    Student *newStudent = &((*students)[*count]);

    printf("Enter Student ID: ");
    scanf("%d", &newStudent->rollNumber);
    getchar();

    printf("Enter Student Name: ");
    fgets(newStudent->name, MAX_NAME, stdin);
    newStudent->name[strcspn(newStudent->name, "\n")] = '\0';

    printf("Enter Student Score: ");
    scanf("%f", &newStudent->marks);

    (*count)++;
    printf("Student added successfully!\n");
    // viewStudents(*students, *count);
}

/**
 * @brief Update an existing Student object
 *
 * @param students
 * @param count
 */
void updateStudent(Student *students, int count)
{
    if (count == 0)
    {
        printf("No students available to modify.\n");
        return;
    }

    int id;
    printf("Enter Student ID to modify: ");
    scanf("%d", &id);

    for (int i = 0; i < count; i++)
    {
        if (students[i].rollNumber == id)
        {
            printf("Enter new name: ");
            getchar();
            fgets(students[i].name, MAX_NAME, stdin);
            students[i].name[strcspn(students[i].name, "\n")] = '\0';

            printf("Enter new marks: ");
            scanf("%f", &students[i].marks);

            printf("Record updated successfully!\n");
            return;
        }
    }

    printf("Student with ID %d not found.\n", id);
}

/**
 * @brief Delete a Student object
 *
 * @param students
 * @param count
 */
void deleteStudent(Student **students, int *count)
{
    if (*count == 0)
    {
        printf("No students available to delete.\n");
        return;
    }

    int id;
    printf("Enter Student ID to delete: ");
    scanf("%d", &id);

    for (int i = 0; i < *count; i++)
    {
        if ((*students)[i].rollNumber == id)
        {
            // Shift elements left
            for (int j = i; j < *count - 1; j++)
            {
                (*students)[j] = (*students)[j + 1];
            }

            (*count)--;
            *students = realloc(*students, (*count) * sizeof(Student));

            printf("Student deleted successfully!\n");
            return;
        }
    }

    printf("Student with ID %d not found.\n", id);
}

/**
 * @brief Display all Student objects
 *
 * @param students
 * @param count
 */
void viewStudents(Student *students, int count)
{
    if (count == 0)
    {
        printf("No student records available.\n");
        return;
    }

    printf("\n====== STUDENT LIST ======\n");
    for (int i = 0; i < count; i++)
    {
        printf("Roll Number: %d | Name: %s | Marks: %.2f\n",
               students[i].rollNumber, students[i].name, students[i].marks);
    }
}

void saveStudentsToFile(Student *students, int count)
{
    char filename[100];
    printf("Provide a filename e.g (backup.txt, please include the .txt): ");
    if (fgets(filename, sizeof(filename), stdin) != NULL)
    {
        filename[strcspn(filename, "\n")] = '\0';
        FILE *file = fopen(filename, "w");
        if (file == NULL)
        {
            printf("Error opening file for writing.\n");
        }

        for (int i = 0; i < count; i++)
        {
            fprintf(file, "%d,%s,%.2f\n", students[i].rollNumber, students[i].name, students[i].marks);
        }

        fclose(file);
        printf("Student data saved to %s successfully.\n", filename);
    }
    else
    {
        printf("\nError reading input.\n");
    }
    return;
}

bool is_integer(const char *input)
{
    // Handle potential newline character from fgets
    size_t len = strlen(input);
    if (len > 0 && input[len - 1] == '\n')
    {
        len--;
    }

    if (len == 0)
    {
        return false; // Empty input is not a number
    }

    // Check for an optional sign at the beginning
    int start_index = 0;
    if (input[0] == '+' || input[0] == '-')
    {
        if (len == 1)
        {
            return false; // Sign alone is not a number
        }
        start_index = 1;
    }

    // Loop through the characters to check if they are all digits
    for (size_t i = start_index; i < len; i++)
    {
        if (!isdigit((unsigned char)input[i]))
        {
            return false; // Found a non-digit character
        }
    }

    return true; // All characters are digits
}

// char *create_string(const Student students[], int size, int targetId)
// {
//     for (int i = 0; i < size; i++)
//     {
//         // Compare the target ID with the current student's ID
//         if (students[i].rollNumber == targetId)
//         {
//             return i; // Return the index if a match is found
//         }
//     }
//     return -1; // Return -1 if no match is found after traver
// }

int searchStudent(Student *student, int size, int searchId)
{
    for (int i = 0; i < size; i++)
    {
        if (student[i].rollNumber == searchId)
        { // Compare the 'rollNumber' field
            printf("Product found at index %d: Roll Number=%d, Name=%s, Marks=%.2f\n",
                   i,
                   student[i].rollNumber,
                   student[i].name,
                   student[i].marks);

            return 1;
        }
    }
    return -1; // Return -1 if not found
}