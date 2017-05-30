#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

int main(int argc, char *argv[])
{
    // check arguments
    if (argc != 2)
    {
        fprintf(stderr, "USAGE: ./recover raw_file\n");
        return 1;
    }
    
    FILE *card = fopen(argv[1], "r");
    
    // check whether the pointer equals to null
    if (card == NULL)
    {
        fprintf(stderr, "could not open file\n");
        return 2;
    }
    // array for reading to and writing from it
    uint8_t buffer[512];
    // keep track of order of the found JPGs 
    int tracker = 0;
    // char array to put filename in
    char filename[8];

    FILE *img = NULL;
    
    // iterate over until we reach EOF
    while (fread(buffer, 512, 1, card) == 1)
    {
        
    // check if that is the start of a JPEG
        if(buffer[0] == 0xff &&
        buffer[1] == 0xd8 &&
        buffer[2] == 0xff &&
        (buffer[3] & 0xf0) == 0xe0)
        {
            // check if we've already found a JPEG
            if (tracker -1 > 0)
            {
                fclose(img);
                
            }
            // make JPEG file
            sprintf(filename, "%03i.jpg", tracker);
            tracker++;
            
        // open file
            img = fopen(filename, "w");
            // check if img pointer returns null
            if (img == NULL)
            {
                fprintf(stderr, "could not open\n");
                return 3;
            }
            // write from buffer to the file
            fwrite(buffer, 512, 1, img);
            // start from the top of the loop again
            continue;
            
        }
    // write to the currently opened file
        if (tracker -1 >= 0)
            fwrite(buffer, 512, 1, img);
    }
    fclose(card);
    return 0;
}