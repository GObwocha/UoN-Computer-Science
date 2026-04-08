//SCS3/2595/2025
//SCS3/150532/2025
//SCS3/2478/2025
//SCS3/2596/2025

//Link to the GitHub account where the project is:
//https://github.com/GObwocha/schoolwork

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_TASKS 100
#define DESC_LEN 100

typedef struct {
  int id;
  char description[DESC_LEN];
  int status; 
} Task;

Task tasks[MAX_TASKS];
int taskCount = 0;

void loadTasksFromFile();
void saveTasksToFile();
void addTask();
void viewTasks();
void markTaskCompleted();
void clearInputBuffer();

int main() {
  int choice;
  loadTasksFromFile();

  while (1) {
    printf("\n--- To-Do List Menu ---\n");
    printf("1. Add New Task\n");
    printf("2. View All Tasks\n");
    printf("3. Mark Task as Completed\n");
    printf("4. Save Tasks to File\n");
    printf("5. Reload Tasks from File\n");
    printf("6. Exit\n");
    printf("Enter your choice: ");

    if (scanf("%d", &choice) != 1) {
      printf("Invalid input. Please enter a number.\n");
      clearInputBuffer();
      continue;
    }
    clearInputBuffer(); 

    switch (choice) {
    case 1:
      addTask();
      break;
    case 2:
      viewTasks();
      break;
    case 3:
      markTaskCompleted();
      break;
    case 4:
      saveTasksToFile();
      break;
    case 5:
      loadTasksFromFile();
      printf("Tasks reloaded from file.\n");
      break;
    case 6:
      printf("Exiting... Include saving? (y/n): ");
      char saveChoice;
      scanf("%c", &saveChoice);
      if (saveChoice == 'y' || saveChoice == 'Y') {
        saveTasksToFile();
      }
      printf("Goodbye!\n");
      exit(0);
    default:
      printf("Invalid choice. Please try again.\n");
    }
  }
  return 0;
}

void clearInputBuffer() {
  int c;
  while ((c = getchar()) != '\n' && c != EOF)
    ;
}

void addTask() {
  if (taskCount >= MAX_TASKS) {
    printf("Task list is full! Cannot add more tasks.\n");
    return;
  }

  Task newTask;
  newTask.id = taskCount + 1;
  newTask.status = 0; 

  printf("Enter task description: ");
  if (fgets(newTask.description, DESC_LEN, stdin) != NULL) {
    size_t len = strlen(newTask.description);
    if (len > 0 && newTask.description[len - 1] == '\n') {
      newTask.description[len - 1] = '\0';
    }
    tasks[taskCount] = newTask;
    taskCount++;
    printf("Task added successfully (ID: %d).\n", newTask.id);
  } else {
    printf("Error reading input.\n");
  }
}

//function to view task
void viewTasks() {
  if (taskCount == 0) {
    printf("No tasks found.\n");
    return;
  }

  printf("\n%-5s %-15s %-50s\n", "ID", "Status", "Description");
  printf("---------------------------------------------------------------------"
         "-----\n");
  for (int i = 0; i < taskCount; i++) {
    printf("%-5d %-15s %-50s\n", tasks[i].id,
           tasks[i].status == 1 ? "Completed" : "Pending",
           tasks[i].description);
  }
}

//function to indicate task is completed
void markTaskCompleted() {
  int id;
  int found = 0;

  viewTasks();
  if (taskCount == 0)
    return;

  printf("\nEnter Task ID to mark as completed: ");
  if (scanf("%d", &id) != 1) {
    printf("Invalid input.\n");
    clearInputBuffer();
    return;
  }
  clearInputBuffer();

  for (int i = 0; i < taskCount; i++) {
    if (tasks[i].id == id) {
      tasks[i].status = 1;
      printf("Task ID %d marked as completed.\n", id);
      found = 1;
      break;
    }
  }

  if (!found) {
    printf("Task with ID %d not found.\n", id);
  }
}

void saveTasksToFile() {
  FILE *fp = fopen(FILE_NAME, "w");
  if (fp == NULL) {
    printf("Error opening file for writing.\n");
    return;
  }

  for (int i = 0; i < taskCount; i++) {
    fprintf(fp, "%d|%d|%s\n", tasks[i].id, tasks[i].status,
            tasks[i].description);
  }

  fclose(fp);
  printf("All tasks saved to '%s'.\n", FILE_NAME);
}

void loadTasksFromFile() {
  FILE *fp = fopen(FILE_NAME, "r");
  if (fp == NULL) {
    return;
  }

  taskCount = 0;
  char line[DESC_LEN + 20]; 

  while (fgets(line, sizeof(line), fp)) {
    if (taskCount >= MAX_TASKS)
      break;

    Task t;
    if (sscanf(line, "%d|%d|%[^\n]", &t.id, &t.status, t.description) == 3) {
      tasks[taskCount++] = t;
    }
  }

  fclose(fp);
}
