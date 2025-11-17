#include <stdio.h>
#include <string.h>

int main() {
    char name[100];
    
    printf("========================================\n");
    printf("    Welcome to the Greeting Program!    \n");
    printf("========================================\n\n");
    
    printf("Please enter your name: ");
    
    if (fgets(name, sizeof(name), stdin) != NULL) {
        name[strcspn(name, "\n")] = '\0';
        
        printf("\nHello, %s! It's great to meet you!\n", name);
    } else {
        printf("\nError reading input.\n");
        return 1;
    }
    
    return 0;
}