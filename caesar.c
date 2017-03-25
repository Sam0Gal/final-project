#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <stdlib.h>

bool check_argc(int a);
bool check_key(int a);


int main(int argc, string argv[])
{
    
    
    if (check_argc(argc) ==true)            // check if argc = 2
    {
        
        int k = atoi(argv[1]);               // k is key,   To covert k from a string to an int
    
    if (check_key(k)==true)                 // check if key is valid (not less than zero)
    {
        printf("plaintext: ");
        string p = get_string();             // ask user for an input (the plaintext)
        
        printf("ciphertext: ");
         for (int i = 0, n = strlen(p); i<n; i++)
         {
             if (isalpha(p[i]))              // check if the i'th number in plaintext is alphabetic
             {
                if (islower(p[i]))            // check if the letter is small
                {
                  int char_num = ((p[i]-'a')+k)%26;     // To transform from ascii to alphabet
                    char_num +='a';                     // To transform from alphabet to ascii
                    printf("%c", char_num);
                }
                else if (isupper(p[i]))           // check if the letter is capital
                {
                    int char_num = ((p[i]-'A')+k)%26;       // like in line 30
                    char_num +='A';
                    printf("%c", char_num);
                }
             }
             else                       // to print char if it's not alphabetic
             {
                 printf("%c", p[i]);
             }
         }
        printf("\n");
    }
    }
    else
    {
        printf("Usage: ./caesar k\n");
        return 1;
    }
}


bool check_argc(int a)                   // check if argc is valid
{
    if (a == 2)
    {
        return true;
    }
    else
    {
        return false;
    }
}

bool check_key(int a)
{
    if (a >= 0)
    {
        return true;
    }
    else
    {
        return false;
    }
}