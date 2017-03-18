#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int h, w, space, hash, hash2; // h is height  w is width  hash2 for the second pyramid
    
    
    do
    {
        printf("Height: ");
        h =get_int();
        w=h;
    }
    while (0>h || h>23);
    
    for (; h>0; h--)
 {
    for (space=h; space>1; space--)
    {
        printf(" ");
    }
    for (hash=h; hash<w+1; hash++)
    {
        printf("#");
    }
    
    printf("  ");
    for (hash2=h; hash2<w+1; hash2++)
    {
        printf("#");
    }
    printf("\n");
 }
    
}