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
