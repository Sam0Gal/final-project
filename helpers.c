/**
 * helpers.c
 *
 * Helper functions for Problem Set 3.
 */
 
#include <cs50.h>

#include "helpers.h"

/**
 * Returns true if value is in array of n values, else false.
 */
bool search(int value, int values[], int n)
{
    
    int left = 0, right = n - 1;
    
    // TODO: implement a searching algorithm
    while (left <= right)
    {
        int middle = (left + right) / 2;
        
        if (value == values[middle])
        {
            return true;
        }
        
        else if (value > values[middle])
        {
            left = middle + 1;
        }
        else if (value < values[middle])
        {
            right = middle - 1;
        }
        
    }
    return false;
}

/**
 * Sorts array of n values.
 */
void sort(int values[], int n)
{
    // TODO: implement an O(n) sorting algorithm  (counting sort)
    // to initialize all elements to zero
    static int counterarry[65536];
    // adding values to counting array elements
    for (int i = 0; i < n; i++)
    {
        counterarry[values[i]] += 1;
    }
    // sorting values
    for (int i = 0, j = 0; j < n; i++)
    {
        int a = 0;
            while (counterarry[i] > a)
            {
                values[j] = i;
                j++, a++;
            }
    }
    return;
}