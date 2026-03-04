#include<stdio.h>
int  main(){

    int num , i  ;
    printf("enter the number : ") ; 
    scanf("%d" , &num) ;

    for(i = 2 ; i<num ; i++)
    {
        if (num % i == 0){ // 3

            printf("%d is not the prime number" , num);
            break;
        }
    }
    if (num == i)
    {
        printf("%d is the prime" ,num);
    }
    return 0 ;






}