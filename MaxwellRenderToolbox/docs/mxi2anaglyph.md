# MXI to Anaglyph Stereo Converter v0.1 #
2015-12-13 08.51 AM
----
By Andrew Hazelden  
Email: [andrew@andrewhazelden.com](mailto:andrew@andrewhazelden.com)  
Blog: [http://www.andrewhazelden.com](http://www.andrewhazelden.com)

![Anaglyph Stere Image](images/cubex_anaglyph.png)

## Description ##
The `mxi2anaglyph.py` script will convert a set of Maxwell .mxi based stereo images or panoramas into a red/cyan format anaglyph image. The script uses PyMaxwell, and Imagemagick to do the conversions.

![MXI to Anaglyph Screenshot](images/mxi2anaglyph_pymaxwell.png)

## How do I use the script? ##

Step 1. Render out a set of Left and Right view Stereo images and save the .mxi files.

Step 2. Launch PyMaxwell and open up the `mxi2anaglyph.py` python script.

Step 3. Edit the "mxiLeftImagePath" and the "mxiRightImagePath" variable in the main function near the bottom of this script and specify your Maxwell Studio based MXI scene file.

Step 4. Select the **Script > Run** menu item in PyMaxwell.

Step 5. An anaglyph stereo image has been generated at this point with the name of `<Scene_L>_anaglyph.png` and is saved in the same folder as the original .mxi image. The folder where the new anaglyph image has been saved to will be opened up automatically in your desktop file browser.
