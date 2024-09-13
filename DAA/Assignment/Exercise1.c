//PSEUDOCODE
// FINDING THE LARGEST OR MAXIMUM ELEMENT IN AN ARRAY
// 1. Input an array with n elements
// 2. Initialize element in index 0 to be the largest number in that array. (largest [0])
// 3. For each element in the array, check if that element is greater than the largest element. 
//   element > largest
// 4. If it is, set element to largest. 
// 5. If it is not, move to the next element in the array. 
// 6. Return the largest element. 

#include <stdio.h>

int findMaximum(int arr[], int n) {
    //  Initialize max_element to the first element of the array
    int max_element = arr[0];
    
    // Loop through the array starting from the second element
    for (int i = 1; i < n; i++) {
        if (arr[i] > max_element) {
            max_element = arr[i]; // Update max_element if a larger value is found
        }
    }
    
    //  Return the maximum element
    return max_element;
}

int main() {
    int arr[] = {12, 45, 2, 67, 89, 34, 90};
    int n = sizeof(arr) / sizeof(arr[0]);
    
    int max = findMaximum(arr, n);
    printf("The maximum element in the array is: %d\n", max);
    
    return 0;
}
