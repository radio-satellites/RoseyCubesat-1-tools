# RoseyCubesat-1-tools
![cubsat](https://github.com/radio-satellites/RoseyCubesat-1-tools/assets/114111180/2c5ea621-2620-4798-9bad-5fba218eb495)

Decode data from RoseyCubesat-1!

# How to decode:

There's a file in the repo called "original.txt." This can be used for testing. 

You need to have some frames from RoseyCubesat-1 to decode. SatNogs DB has this. The script reads satnogs frames from a file (always "original.txt"), and then dumps them to three images called output_rgb.png, output_raw.png, and output_bw.png. RGB contains the usual composite, the RAW file has the original non debayered imagery, and output_bw has the black and white calibrated imagery, which is debayered. This is very much a work-in-progress, and things may change. 

# Example decode:

1. Make sure that the file "original.txt" is present and you have imagery data in it. 
2. Install dependencies, PIL and cv2 with the following commands: pip install Pillow and pip install opencv-python. 
3. Run "decoder.py"
4. You should have imagery!


