/**
 * Implements a dictionary's functionality.
 */

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#include "dictionary.h"
// a counter to determine the number of words in the dictionary
unsigned int counter = 0;

// the trie
typedef struct node
    {
        bool is_word;
        struct node *leaves[27];
    }
    node;
    
    node* root = NULL;

/**
 * Returns true if word is in dictionary else false.
 */
bool check(const char *word)
{
    node *current = root;
    for (int i = 0, n = strlen(word); i < n; i++)
    {
        if (word[i] == '\'')
            {
                if (current -> leaves[26] != NULL)
                        current = current -> leaves[26];
                else
                    return false;
                continue;
            }
            
        if (current -> leaves[tolower(word[i]) - 'a'] != NULL)
                current = current -> leaves[tolower(word[i]) - 'a'];
        else
            return false;
    }
    if (current -> is_word == true)
        return true;
            
return false;
}

/**
 * Loads dictionary into memory. Returns true if successful else false.
 */
bool load(const char *dictionary)
{
    // allocate memory and set it to zero (or NULL)
    root = calloc(sizeof(node), 1);
    // a pointer to keep track of the last allocated node
    node *current = NULL;
    FILE *dict_p = fopen(dictionary, "r");
    if (dict_p == NULL)
        return false;
    
    char word[45];
    // iterate over until the end of the file
    while (fscanf(dict_p, "%s", word) != EOF)
    {
        current = root;
        // insert word into the trie char by char
        for (int i = 0, n = strlen(word); i < n; i++)
        {
            if (word[i] == '\'')
            {
                if (current -> leaves[26] == NULL)
                {
                    // allocate a new node
                    node *new_node = calloc(sizeof(node), 1);
                    current -> leaves[26] = new_node;
                    current = current -> leaves[26];
                }
                else
                    current = current -> leaves[26];
            }
            
            
            else if (current -> leaves[word[i] - 'a'] == NULL)
            {
                node *new_node = calloc(sizeof(node), 1);
                current -> leaves[word[i] - 'a'] = new_node;
                
                current = new_node;
            }
            else
                current = current -> leaves[word[i] - 'a'];
        }
        current -> is_word = true;
        // to determine the size of dictionary
        counter++;
    }
    // close the dictionary
    fclose(dict_p);
    return true;
    
}

/**
 * Returns number of words in dictionary if loaded else 0 if not yet loaded.
 */
unsigned int size(void)
{
    return counter;
}

/**
 * Unloads dictionary from memory. Returns true if successful else false.
 */
void free_trie(node *current);
bool unload(void)
{
    node *current = root;
    free_trie(current);
    return true;
}

void free_trie(node *current)
{    for (int i = 0; i < 27; i++)
    {
        if (current -> leaves[i] == NULL)
            continue;

        else
            free_trie(current -> leaves[i]);
    }
    free(current);
}