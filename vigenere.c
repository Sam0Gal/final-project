#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>

bool check_argc(int a);
bool check_key(string k);

int main(int argc, string argv[])
{
    if (check_argc(argc) ==true)            // check if argc = 2
    {
        string k = argv[1];                     // k is key
        
    
    if (check_key(k)==true)                 // check if key is valid
    {
        // ask user for an input
        printf("plaintext: ");
        string p = get_string();
        
         printf("ciphertext: ");
        for (int i = 0, j = 0, n = strlen(p); i<n; i++)
        {
            int alpha_key, alpha_plain, sum, j2 = j % strlen(k);
            
            // check the i'th char in plaintext
            if (isalpha(p[i]))
            {
                if (islower(k[j2]))
                {
                 alpha_key = k[j2] - 'a';   // to transform from ascii to alphabet
                }
                else
                {
                alpha_key = k[j2] - 'A';
                }
                
                if (islower(p[i]))
                {
                 alpha_plain = p[i] - 'a';
                 sum = (alpha_key + alpha_plain) % 26;     // to get the char number in alphabet
                 printf("%c", sum +'a');                   // to print the char in ascii
                }
                else
                {
                alpha_plain = p[i] - 'A';
                sum = (alpha_key + alpha_plain) % 26;
                printf("%c", sum +'A');
                }

               j++;
            }
            else
            {
                printf("%c", p[i]);
            }
        }
        
        printf("\n");
    }
    else
    {
        printf("enter one argument (after ./vigenere) with alphabet only\n");
        return 1;
    }
    
    }
    else
    {
        printf("enter one argument (after ./vigenere) with alphabet only\n");
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

bool check_key(string k)
{
    int count= 0;
    for (int i = 0; isalpha(k[i]); i++)
    {
        count++;
    }
        if (count == strlen(k))
        return true;
    
    else
    {
        return false;
    }
}