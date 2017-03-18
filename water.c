#include <cs50.h>
#include <stdio.h>

int main(void)
{
    
    printf("lenght of shower in minutes is: ");
    int minutes = get_int();
    
    printf("the number of bottles used is: %i\n", minutes * 12);
    
    return 0;
}