/**
 * Copies a BMP piece by piece, just because.
 */
       
#include <stdio.h>
#include <stdlib.h>

#include "bmp.h"

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 4)
    {
        fprintf(stderr, "Usage: ./reize number infile outfile\n");
        return 1;
    }
    
    int n = atoi(argv[1]);
    
    if (n > 100 || n < 1)
    {
        fprintf(stderr, "must be positive intger lees than or equal to 100\n");
        return 2;
    }
    
    // remember filenames
    char *infile = argv[2];
    char *outfile = argv[3];

    // open input file 
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 3;
    }

    // open output file
    FILE *outptr = fopen(outfile, "w");
    if (outptr == NULL)
    {
        fclose(inptr);
        fprintf(stderr, "Could not create %s.\n", outfile);
        return 4;
    }

    // read infile's BITMAPFILEHEADER
    BITMAPFILEHEADER bf;
    fread(&bf, sizeof(BITMAPFILEHEADER), 1, inptr);

    // read infile's BITMAPINFOHEADER
    BITMAPINFOHEADER bi;
    fread(&bi, sizeof(BITMAPINFOHEADER), 1, inptr);

    // ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if (bf.bfType != 0x4d42 || bf.bfOffBits != 54 || bi.biSize != 40 || 
        bi.biBitCount != 24 || bi.biCompression != 0)
    {
        fclose(outptr);
        fclose(inptr);
        fprintf(stderr, "Unsupported file format.\n");
        return 4;
    }
    
    // keep track of the first width and height
    int firstWidth = bi.biWidth;
    int firstHeight = bi.biHeight;
    
    bi.biWidth *= n;
    bi.biHeight *= n;
    
    // determine padding for scanlines
    int firstpadding = (4 - (firstWidth * sizeof(RGBTRIPLE)) % 4) % 4;
    
    int padding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;
    
    // update outfile's header information
    bi.biSizeImage = ((sizeof(RGBTRIPLE) * bi.biWidth) + padding) * abs(bi.biHeight);
    
    bf.bfSize = bi.biSizeImage + sizeof(BITMAPFILEHEADER) + sizeof(BITMAPINFOHEADER);
    
    // write outfile's BITMAPFILEHEADER
    fwrite(&bf, sizeof(BITMAPFILEHEADER), 1, outptr);

    // write outfile's BITMAPINFOHEADER
    fwrite(&bi, sizeof(BITMAPINFOHEADER), 1, outptr);
    
    
    
    // iterate over infile's scanlines
    for (int i = 0, biHeight = abs(firstHeight); i < biHeight; i++)
    {
        
        // iterate over pixels in scanline
        for (int count = 0; count < n - 1; count++)
        {
        
         for (int j = 0; j < firstWidth; j++)
         {
            // temporary storage
            RGBTRIPLE triple;

            // read RGB triple from infile
            fread(&triple, sizeof(RGBTRIPLE), 1, inptr);
            
            // resize horizontally
            for (int k = 0; k < n; k++)
                fwrite(&triple, sizeof(RGBTRIPLE), 1, outptr);
            
         }
         // add padding
         for (int l = 0; l < padding; l++)
            fputc(0x00, outptr);
         
            // return infile cursor back
            fseek(inptr, -firstWidth * 3, SEEK_CUR);
        }
        
        // write pixels once more
        for (int j = 0; j < firstWidth; j++)
        {
            // temporary storage
            RGBTRIPLE triple;

            // read RGB triple from infile
            fread(&triple, sizeof(RGBTRIPLE), 1, inptr);
            
            
            for (int h = 0; h < n; h++)
                fwrite(&triple, sizeof(RGBTRIPLE), 1, outptr);
        }
        
        // add padding
        for (int l = 0; l < padding; l++)
            fputc(0x00, outptr);
        
        // skip over padding, if any
        fseek(inptr, firstpadding, SEEK_CUR);
    }

    // close infile
    fclose(inptr);

    // close outfile
    fclose(outptr);

    // success
    return 0;
}
