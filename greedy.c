#include <math.h>
#include <cs50.h>
#include <stdio.h>

int main(void)
{
    float dollars_change;
    
    int change, coins, quarters = 25, dimes = 10, nickels = 5, pennies = 1;
    coins = 0;
    
    printf("O hai! ");
    do
    {
        printf("How much change is owed? ");
        dollars_change = get_float();
    }
    while (dollars_change<=0);
    
    dollars_change = dollars_change*100;
    dollars_change = round(dollars_change);
    
    change = (int)dollars_change;
    
    {
        
    while (change>=quarters)
    {
        change = change - quarters;
        coins++;
    }
    
    while (change>=dimes)
    {
        change = change - dimes;
        coins++;
    }
    
    while (change>=nickels)
    {
        change = change - nickels;
        coins++;
    }
    
    while (change>=pennies)
    {
        change = change - pennies;
        coins++;
    }
    
     printf("%d\n", coins);
    
    }
    
    return 0;
}