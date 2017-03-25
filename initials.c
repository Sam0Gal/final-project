#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>

int main(void)
{
    string name = GetString();
    
    
    int n = strlen(name);
    for (int i=0; i<n; i++)
    {
        if (isalpha(name[i]))
        {
            printf("%c", toupper(name[i]));
            
            while (isalpha(name[i+1]))
            {
                i++;
            }
        }
        
    }
    printf("\n");
}
