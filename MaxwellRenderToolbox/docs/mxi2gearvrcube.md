# MXI to GearVR Cubic Panorama Converter v0.1#
2015-12-11 1.08 AM
----
By Andrew Hazelden  
Email: [andrew@andrewhazelden.com](mailto:andrew@andrewhazelden.com)  
Blog: [http://www.andrewhazelden.com](http://www.andrewhazelden.com)  

## Description ##
The `mxi2gearvrcube.py` script will embed the Google Photosphere EXIF metadata into a LatLong panorama. This makes it easier to view the panoramic rendering on Google+ and on a Google Cardboard HMD display.

![MXI to GearVR Cubic Panorama Converter Screenshot](images/mxi2gearvrcube.png)

## How do I use the script? ##

Step 1.Render out a set of Left and Right view LatLong Stereo images and save the .mxi files.

Step 2. Launch PyMaxwell and open up the `mxi2gearvrcube.py` python script.

Step 3. Edit the "mxiLeftImagePath" and the "mxiRightImagePath" variable in the main function near the bottom of this script and specify your Maxwell Studio based MXI scene file. You can specify the 

Step 4. Select the **Script > Run** menu item in PyMaxwell.

Step 5. A Gear VR style stereo cubemap has been generated at this point with the name of `<Scene>_GearVR.png` and is saved in the same folder as the original .mxi image. The folder where the new Gear VR image has been saved to will be opened up automatically in your desktop file browser.