#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>
#include <time.h>
#include <signal.h>
#include <unistd.h>

// Funtior to quit execution if there a time out
void time_out(int signal){
    printf("\nExecution time exeded... Time-out Error !!!\n");

    // Save time out in the file
    FILE *file;
    file = fopen("rec_result.txt", "a+");
    fprintf(file, "%d\n", -1);
    fclose(file);

    // Exit code
    _exit(1);
}

// Function to remove whitespace
void remove_whitespace(char *str){

    // Auxialiar variables to remove white spaces
    char *writer = str;
    char *reader = str;

    // Loop until the end of the string
    while(*reader != '\0'){

        // Check if is not an whitespace
        if(!isspace((unsigned char)*reader)){

            // Copy the non-whitespace character and move forward
            *writer = *reader;
            writer++;
        }

        // Allway move the reader pointer forward
        reader++;
    }

    // Add null terminettor at the new end of the string
    *writer = '\0';
}

// Function to realoquete string buffer length
char* realoc_buffer(char *str){
    
    // Get new string size
    size_t new_len = strlen(str);

    // Resize the buffer
    char *resized_buffer = realloc(str, new_len + 1);

    // Check if the realocation worked
    if (resized_buffer == NULL) {
        printf("Failed to reallocate memory\n");
        free(str);
        return NULL;
    }

    return resized_buffer;
}

// LCS dynamic function
int lcs_dp(char* a, char* b, int x, int y) {
    
    // Dynamically allocate a 2D array (DP table)
    int** dp = (int**)malloc((x + 1) * sizeof(int*));
    
    for (int i = 0; i <= x; i++) {
        dp[i] = (int*)malloc((y + 1) * sizeof(int));
    }

    // Fill the DP table
    for (int i = 0; i <= x; i++) {
        for (int j = 0; j <= y; j++) {
            
            // Base case: empty string has LCS 0 with any string
            if (i == 0 || j == 0) {
                dp[i][j] = 0;
            
            // When characters match take diagonal value + 1
            } else if (a[i - 1] == b[j - 1]) {
                dp[i][j] = dp[i - 1][j - 1] + 1;
            
            // When characters don't match, take maximum of top or left cellt
            } else {
                dp[i][j] = (dp[i - 1][j] > dp[i][j - 1]) ? dp[i - 1][j] : dp[i][j - 1];
            }
        }
    }

    int result = dp[x][y];

    // Free allocated memory
    for (int i = 0; i <= x; i++) {
        free(dp[i]);
    }
    free(dp);

    return result;
}

// Main function
int main(int argc, char** argv){

    // Check if we have the correct number of parameters
    if(argc < 2){
        printf("Incorrect number of arguments!!\n");
        printf("Correct use: %s <file_path.txt>\n", argv[0]);

        return 0;
    }

    FILE *file;

    // Variables for the first line
    char *line_a = NULL;
    size_t size_a = 0;

    // Variables for the second line
    char *line_b = NULL;
    size_t size_b = 0;

    // Open the file
    file = fopen(argv[1], "r");

    // Check if the file was opened successfully
    if (file == NULL) {
        perror("Error opening file");
        return 1;
    }

    // Read the first line
    if (getline(&line_a, &size_a, file) == -1) {
        printf("Could not read the first line or file is empty.\n");
        fclose(file);     
        free(line_a);
        return 1;
    }

    // Read the second line
    if (getline(&line_b, &size_b, file) == -1) {
        printf("Could not read the first line or file is empty.\n");
        fclose(file);     
        free(line_b);
        return 1;
    }

    // Remove whitespace
    remove_whitespace(line_a);
    remove_whitespace(line_b);

    // Realocate buffer sizes for the new string length
    line_a = realoc_buffer(line_a);
    line_b = realoc_buffer(line_b);

    // Register alarm signal
    signal(SIGALRM, time_out);

    // Set alarm for 1 hour
    printf("Seting 1 hour time-out\n");
    alarm(3600);

    // Record start time
    clock_t start = clock();

    // Call LCS function
    int aux = lcs_dp(line_a, line_b, strlen(line_a), strlen(line_b));

    // Record end time
    clock_t end = clock();

    // Turn off alarm
    alarm(0);

    // Calculate time taken
    double time_taken = ((double) (end - start)) / CLOCKS_PER_SEC;

    // Free the alocated lines before finishing the algorithm
    free(line_a);
    free(line_b);

    printf("%f\n", time_taken);

    // Save the result of execution in a file
    file = fopen("dp_result.txt", "a+");
    fprintf(file, "%f\n", time_taken);
    fclose(file);
    
    return 0;
}