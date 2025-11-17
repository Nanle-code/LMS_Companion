#include <stdio.h>
#include <string.h>

const int PASS_THRESHOLD = 40;
struct Student
{
    /* data */
    char name[100]; // Character array to store the student's name (max 99 characters + null terminator)
    int rollNumber; // Integer to store the student's roll number
    float marks;
};

int main()
{
    char name[100];

    struct Student student1;

    printf("========================================\n");
    printf("    Welcome to the Greeting Program!    \n");
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

    struct Student student2[100];
    int studentCount = 0;

    do
    {
        printf("\nEnter information for Student %d:\n", studentCount + 1);

        // Get student name
        printf("Name: ");
        fgets(student2[studentCount].name, sizeof(student2[studentCount].name), stdin);
        student2[studentCount].name[strcspn(student2[studentCount].name, "\n")] = 0; // Remove trailing newline

        // Get student age
        printf("Rollnumber: ");
        scanf("%d", &student2[studentCount].rollNumber);

        // Get student GPA
        printf("Marks: ");
        scanf("%f", &student2[studentCount].marks);
    } while (1);

    return 0;
}