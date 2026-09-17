#include <iostream>
#include <string>
#include <iomanip>
using namespace std;
//--------------------------------------------------------------------------------
// Person class
//--------------------------------------------------------------------------------
//Person class holds all data and behaviour for a single person
class Person {
public:
    string name;
    double kilograms;
    double heightMeters;
    double BMI;
    int age;

    //Default constructor
    Person() : name(""), kilograms(0.0), heightMeters(0.0), BMI(0.0), age(0) {}

    //Parameterized constructor: sets all fields at once
    Person(string n, double kg, double hm, int a = 0)
        : name(n), kilograms(kg), heightMeters(hm), BMI(0.0), age(a) {}

    //Prints a greeting using the person's name
    void Greeting() {
        cout << "Hello, my name is " << name << "." << endl;
    }

    //Calculates BMI using weight / height^2 then prints the result and category
    void calculateBMI() {
        BMI = kilograms / (heightMeters * heightMeters);

        cout << fixed << setprecision(2);
        cout << name << "'s BMI is " << BMI << endl;

        //Determine risk category based on BMI ranges
        string category;
        if (BMI < 18.5) {
            category = "Underweight";
        } else if (BMI < 25.0) {
            category = "Normal weight";
        } else if (BMI < 30.0) {
            category = "Overweight";
        } else {
            category = "Obese";
        }

        cout << name << "'s risk category is " << category << "." << endl;
    }

    //Reads name, weight, and height from the user from input
    void inputData() {
        cout << "Enter name: ";
        cin.ignore();
        getline(cin, name);
        cout << "Enter weight (kg): ";
        cin >> kilograms;
        cout << "Enter height (m): ";
        cin >> heightMeters;
        cout << "Enter age: ";
        cin >> age;
    }
};

//Sorts an array of Person objects in ascending order by BMI using Selection Sort
void selectionSort(Person arr[], int n) {
    for (int i = 0; i < n - 1; i++) {
        //Find the person with the lowest BMI in the remaining unsorted portion
        int minIdx = i;
        for (int j = i + 1; j < n; j++) {
            if (arr[j].BMI < arr[minIdx].BMI) {
                minIdx = j;
            }
        }
        //Swap the found minimum with the current position
        if (minIdx != i) {
            Person temp = arr[i];
            arr[i] = arr[minIdx];
            arr[minIdx] = temp;
        }
    }
}

//Prints the sorted list with rank, name, and BMI
void printSortedList(Person arr[], int n) {
    cout << "Sorted List:" << endl;
    cout << fixed << setprecision(2);
    for (int i = 0; i < n; i++) {
        cout << (i + 1) << ". " << arr[i].name
             << " - BMI: " << arr[i].BMI << endl;
    }
}

//Returns the GCD of two integers using the Euclidean Algorithm
int gcd(int a, int b) {
    while (b != 0) {
        int temp = b;
        b = a % b;
        a = temp;
    }
    return a;
}
//--------------------------------------------------------------------------------
// Q1 class
//--------------------------------------------------------------------------------
class Q1 {
public:
    //Task 1 & 2: Create 3 people, displays their BMI, then sorts and prints them
    void displayPeople() {
        const int SIZE = 3;
        //Create 3 Person objects with preset name, weight, and height
        Person people[SIZE] = {
            Person("Aubrey Graham", 75.0, 1.74),
            Person("CJ Johnson",    110.0, 1.75),
            Person("Rachel Green",  47.0,  1.76)
        };
        //Greet each person and calculate their BMI
        for (int i = 0; i < SIZE; i++) {
            people[i].Greeting();
            people[i].calculateBMI();
            cout << endl;
        }
        //Sort the array by BMI and display the ranked list
        cout << "Sorting people by BMI..." << endl;
        selectionSort(people, SIZE);
        printSortedList(people, SIZE);
        cout << endl;
    }

    //Task 3: Menu that lets the user add people, sort them, or exit
    void runMenu() {
        const int MAX_PEOPLE = 10;
        Person people[MAX_PEOPLE];
        int count = 0;
        //Keep the default people so the sort option works from the start
        people[count] = Person("Aubrey Graham", 75.0, 1.74, 34);
        people[count].BMI = people[count].kilograms / (people[count].heightMeters * people[count].heightMeters);
        count++;
        people[count] = Person("CJ Johnson", 110.0, 1.75, 28);
        people[count].BMI = people[count].kilograms / (people[count].heightMeters * people[count].heightMeters);
        count++;
        people[count] = Person("Rachel Green", 47.0, 1.76, 30);
        people[count].BMI = people[count].kilograms / (people[count].heightMeters * people[count].heightMeters);
        count++;
    
        //Start of menu
        cout << "Welcome to the BMI Program!" << endl;
        //Repeats the menu until the user exits with option 4
        int choice;
        do {
            cout << "\nPlease select an option:" << endl;
            cout << "1. Calculate BMI" << endl;
            cout << "2. Sort people by BMI" << endl;
            cout << "3. Compute GCD of two ages" << endl;
            cout << "4. Exit" << endl;
            cout << "Enter your choice: ";
            cin >> choice;
     
            //If input is not a valid integer, clear the error and discard the bad input
            if (cin.fail()) {
                cin.clear();
                cin.ignore(1000, '\n');
                cout << "Invalid choice. Please try again." << endl;
                continue;
            }
     
            switch (choice) {
                case 1: {
                    //Get user input, calculate BMI, and add the person to the array
                    if (count >= MAX_PEOPLE) {
                        cout << "Maximum number of people reached." << endl;
                        break;
                    }
                    Person p;
                    p.inputData();
                    p.BMI = p.kilograms / (p.heightMeters * p.heightMeters);
                    cout << endl;
                    p.Greeting();
                    p.calculateBMI();
                    people[count++] = p;
                    break;
                }
                case 2: {
                    //Sort all stored people by BMI and display the ranked list
                    if (count == 0) {
                        cout << "No people to sort." << endl;
                        break;
                    }
                    cout << "\nSorting people by BMI..." << endl;
                    selectionSort(people, count);
                    printSortedList(people, count);
                    break;
                }
                case 3: {
                    //Ask for two ages and compute their GCD using the Euclidean Algorithm
                    //The sample output in the assignment does not list this but in the instructions its required
                    int age1, age2;
                    cout << "Enter first age: ";
                    cin >> age1;
                    cout << "Enter second age: ";
                    cin >> age2;
                    cout << "GCD of " << age1 << " and " << age2 << " is: " << gcd(age1, age2) << endl;
                    break;
                }
                case 4:
                    //Exit the program
                    cout << "\nExiting program... Goodbye!" << endl;
                    break;
                default:
                    cout << "Invalid choice. Please try again." << endl;
            }
        } while (choice != 4);
    }
};
//runs the program
int main() {
    
    Q1 program;
    
    program.displayPeople();
    cout << "=====MENU=====" << endl;
    program.runMenu();
    return 0;
}