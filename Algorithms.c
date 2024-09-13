#include <stdio.h>
int main(){
    int arr[]= {1,3,5,7,8};
    int item =7, n= 5;
    int j = 0;

while (j<n){
    if (arr[j] == item) {
        break;
    }
    j=j+1;
}

printf("Found element %d at position %d\n", item, j);
}
