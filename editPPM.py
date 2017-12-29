# Anil Vishwakarma
# 11/14/2017
# CS - 524 Programming Language
# Program reads PPM file provided by user and manipulates image in PPM format
# Python Version 3.6.3

class PPMImage:    
    
    def processPPMFile(self,ppmFileData):
        self.ppmType=ppmFileData[0]
        self.ppmColumns=int(ppmFileData[1])
        self.ppmRows=int(ppmFileData[2])
        self.ppmColour=int(ppmFileData[3])
        self.ppmPixels = ppmFileData[4].split()
        
    def __init__(self, inputFile):
        self.inputFile = inputFile
        #Read in data of image
        data = open(self.inputFile,"r")
        self.ppmFileData = data.read().split(None, 4)
        self.processPPMFile(self.ppmFileData)
        
    def writetofile(self):
        dataout= open(self.inputFile.replace('.ppm','_Filtered.ppm'), "wb")
        dataout.write(bytearray('{}\n{} {}\n{}\n'.format(self.ppmType,
                                                 self.ppmColumns, self.ppmRows,
                                                 self.ppmColour).encode()))
        
        for pos in range(self.ppmRows * self.ppmColumns * 3):
            dataout.write(bytearray(str(self.ppmPixels[pos]).encode()))
            dataout.write(b' ')
        
        print("Filtered output written to ",self.inputFile.replace('.ppm','_Filtered.ppm'))

    def grey_scale(self):
        for row in range(self.ppmRows):
            for column in range(self.ppmColumns):
                start = row * self.ppmColumns * 3 + column * 3
                end = start + 3
                r, g, b = self.ppmPixels[start:end]
                brightness = int(round( (int(r) + int(g) + int(b)) / 3.0 ))
                self.ppmPixels[start:end] = brightness, brightness, brightness
    
    def flipImageHorizontally(self):
        pixels = list(self.ppmPixels)
        ppmPixelStart = 0
        for row in range(self.ppmRows):
            for column in  reversed(range(self.ppmColumns)):
                start = row * self.ppmColumns * 3 + column * 3
                end = start + 3
                self.ppmPixels[ppmPixelStart:ppmPixelStart+3]=pixels[start:end]
                ppmPixelStart+=3

    
    def flipImageVertically(self):
        pixels = list(self.ppmPixels)
        ppmPixelStart = 0
        for row in reversed(range(self.ppmRows)):
            for column in  range(self.ppmColumns):
                start = row * self.ppmColumns * 3 + column * 3
                end = start + 3
                self.ppmPixels[ppmPixelStart:ppmPixelStart+3]=pixels[start:end]
                ppmPixelStart += 3
    
    def flattenRed(self):
        for row in range(self.ppmRows):
            for column in  range(self.ppmColumns):
                start = row * self.ppmColumns * 3 + column * 3
                redIndex = start
                self.ppmPixels[redIndex] = 0
 
    def flattenGreen(self):
        for row in range(self.ppmRows):
            for column in  range(self.ppmColumns):
                start = row * self.ppmColumns * 3 + column * 3
                greenIndex = start + 1
                self.ppmPixels[greenIndex] = 0       
 
    def flattenBlue(self):
        for row in range(self.ppmRows):
            for column in  range(self.ppmColumns):
                start = row * self.ppmColumns * 3 + column * 3
                blueIndex = start + 2
                self.ppmPixels[blueIndex] = 0
    
    def horizontalBlur(self):
        for row in range(self.ppmRows):
            redValues = 0
            greenValues = 0
            blueValues = 0
            concatCount = 0
            for index,column in  enumerate(range(self.ppmColumns)):
                start = row * self.ppmColumns * 3 + column * 3
                if(index !=0 and (index % 3 == 0 or index == (self.ppmColumns-1))):
                    
                    blurIndex = start - 9
                    while (blurIndex < start):
                        self.ppmPixels[blurIndex] = int(redValues/concatCount)
                        self.ppmPixels[blurIndex + 1] = int(greenValues/concatCount)
                        self.ppmPixels[blurIndex + 2] = int(blueValues/concatCount)
                        blurIndex += 3
                    redValues = 0
                    greenValues = 0
                    blueValues = 0
                    concatCount = 0
                                        
                #Concatenate RGB values.
                redValues += int(self.ppmPixels[start])
                greenValues += int(self.ppmPixels[start+1])
                blueValues += int(self.ppmPixels[start+2])
                concatCount += 1
    
               
      
def main():
    # Enter the name of a PPM image file to modify 
    inputFile = input("Enter the name of the PPM Image File: ")
    ppmImage = PPMImage(inputFile) 
    
    #List of available options
    print("\nList of filters that can be applied to PPM Image\n")
    print("1: Flip image horizontally")
    print("2: Flip image vertically")
    print("3: Convert to greyscale")
    print("4: Flatten Red")
    print("5: Flatten Green")
    print("6: Flatten Blue")
    print("7: Horizontal blur")
    optionCount = 1
    while(optionCount<8):
       option = input(str("Do you want ["+str(optionCount)+"]? (y/n)"))
       if(option == 'y' or option == 'Y'):
           if(optionCount==1):
               ppmImage.flipImageHorizontally()
           if(optionCount==2):
               ppmImage.flipImageVertically()
           if(optionCount==3):
               ppmImage.grey_scale()
           if(optionCount==4):
               ppmImage.flattenRed()
           if(optionCount==5):
               ppmImage.flattenGreen()
           if(optionCount==6):
               ppmImage.flattenBlue()
           if(optionCount==7):
               ppmImage.horizontalBlur()                 
           print("Option ",optionCount," Executed")
       optionCount += 1
 
    ppmImage.writetofile()

# call main    
if __name__ == "__main__":
    main()