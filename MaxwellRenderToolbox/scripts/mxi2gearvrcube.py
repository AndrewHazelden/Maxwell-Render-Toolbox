# MXI to GearVR Cubic Panorama Converter for Maxwell Studio
# ----------------------------------------------------------
# 2015-12-11 08.51 AM v0.1
# By Andrew Hazelden 
# Email: andrew@andrewhazelden.com
# Blog: http://www.andrewhazelden.com

# Description
# -----------
# The `mxi2gearvrcube.py` script will convert a set of Maxwell .mxi based LatLong Stereo panoramas into a Gear VR stereo cubemap style horizontal strip panorama. The script uses PyMaxwell, Panotools, and Imagemagick to do the panoramic conversions.


# Script Installation
# -------------------
# The mxi2gearvrcube.py python script can be loaded and run from inside the MaxwellRenderToolbox's scripts folder, or if you want to, you can copy the python script to Maxwell Render's "NextLimit/Maxwell 3/scripts" folder for easier access from PyMaxwell.

# Windows
# C:/Program Files/MaxwellRenderToolbox/scripts/mxi2gearvrcube.py

# Linux
# /opt/MaxwellRenderToolbox/scripts/mxi2gearvrcube.py
# or
# $HOME/MaxwellRenderToolbox/scripts/mxi2gearvrcube.py

# Mac
# /Applications/MaxwellRenderToolbox/scripts/mxi2gearvrcube.py

# How do I use the script?
# ------------------------

# Step 1.
# Render out a set of Left and Right view LatLong Stereo images and save the .mxi files.

# Step 2.
# Launch PyMaxwell and open up the `mxi2gearvrcube.py` python script.

# Step 3.
# Edit the "mxsLeftImagePath" and the "mxsRightImagePath" variable in the main function near the bottom of this script and specify your Maxwell Studio based MXI scene file.

# Step 4. Select the Script > Run menu item in PyMaxwell.

# Step 5. A Gear VR style stereo cubemap has been generated at this point with the name of `<Scene>_GearVR_Stereo.png` and is saved in the same folder as the original .mxi image. The folder where the new Gear VR image has been saved to will be opened up automatically in your desktop file browser.

# -----------------------------------------

from pymaxwell import *
from math import *
import datetime
import platform
import subprocess
import shlex
import os
import sys

# Convert a pair of LatLong Stereo images into a GearVR stereo cubemap output format:
# Example: mrt_latlong2gearvr('/CubeX_L.mxs', '/CubeX_R.mxs', '_GearVR_Stereo', 'png')
def mrt_latlong2gearvr(mxsLeftImagePath, mxsRightImagePath, gearVRImagenamePrefix, outputPanoramaFileExt):
  # Check the current operating system
  mxPlatform = mtr_getPlatform()
  
  # Find out the current scene file
  leftDirName = os.path.dirname(mxsLeftImagePath)
  leftSceneName = os.path.basename(mxsLeftImagePath)
  leftScenePathNoExt = os.path.splitext(mxsLeftImagePath)[0]

  rightDirName = os.path.dirname(mxsRightImagePath)
  rightSceneName = os.path.basename(mxsRightImagePath)
  rightScenePathNoExt = os.path.splitext(mxsRightImagePath)[0]

  # ----------------------------------------------
  # ----------------------------------------------
  # Warp and stitch the cubic images
  
  # Find out the MaxwellRenderToolbox temporary images directory:
  mtr_temp = mtr_tempImagesDirectory()

  # Merged GearVR Stereo cubic panorama imagename
  output_gearvr = leftScenePathNoExt + gearVRImagenamePrefix + '.' + outputPanoramaFileExt

  # Imagemagick path:
  filenameNativePath = ''
  nona = ''
  enblend = ''
  imagemagick = ''
  ffmpeg = ''
  tee = ''
  
  # Check OS platform for Windows/Mac/Linux Paths
  if mxPlatform == 'Windows':
    # Check if the program is running on Windows 
    filenameNativePath = mtr_getMaxwellRenderToolboxBaseFolder() + 'tools' + os.sep
    nona = filenameNativePath + 'panotoolsNG' + os.sep + 'bin' + os.sep + 'nona.exe'
    enblend = filenameNativePath + 'panotoolsNG' + os.sep + 'bin' + os.sep + 'enblend.exe'
    imagemagick = filenameNativePath + 'imagemagick' + os.sep + 'bin' + os.sep + 'imconvert.exe'
    tee = filenameNativePath +'wintee' + os.sep + 'bin' + os.sep + 'wtee.exe'
  elif mxPlatform == 'Mac':
    filenameNativePath = mtr_getMaxwellRenderToolboxBaseFolder() + 'mac_tools' + os.sep 
    nona = filenameNativePath + 'panotoolsNG' + os.sep + 'bin' + os.sep + 'nona'
    enblend = filenameNativePath + 'panotoolsNG' + os.sep + 'bin' + os.sep + 'enblend'
    # Todo: Find the different Imagemagick install directories and check if each of them exists
    imagemagick = '/opt/ImageMagick/bin/convert'
    tee = 'tee'
  elif mxPlatform == 'Linux':
    # Check if the program is running on Linux
    filenameNativePath = os.sep + 'usr' + os.sep + 'bin' + os.sep
    nona = filenameNativePath + 'nona'
    enblend = filenameNativePath + 'enblend'
    imagemagick = filenameNativePath + 'convert'
    tee = 'tee'

    # Create the empty variable as a fallback mode
    # nona = 'nona'
    # enblend = 'enblend'
    # imagemagick = 'convert'
    # tee = 'tee'

  nonaInputExt = 'tif'
  nonaOutputExt = 'tif'
  
  # Stereo Views Present
  viewCount = ['L', 'R']
  for view in viewCount:
    # This is the frame that would be rendered by Maxwell Render
    maxwell_rendered_input_image = ''
    mxiImagetoLoad = ''
    if view == 'L':
      # Left View Imagery
      maxwell_rendered_input_image = leftScenePathNoExt + '.' + outputPanoramaFileExt
      mxiImagetoLoad = mxsLeftImagePath
    else:
      # Right View Imagery
      maxwell_rendered_input_image = rightScenePathNoExt + '.' + outputPanoramaFileExt
      mxiImagetoLoad = mxsRightImagePath
    
    # Find out the current left view scene settings
    scene = Cmaxwell(mwcallback)
    scene.readMXS(mxiImagetoLoad)
    it = CmaxwellCameraIterator()
  
    # Camera Details
    #camera = leftIt.first(scene)
    cam = scene.getActiveCamera()
    camName = cam.getName()
  
    # COPY IMAGE AFTER RENDER '/Users/Andrew/Documents/maxwell/image.png'
    copyImage = scene.getRenderParameter('COPY IMAGE AFTER RENDER')[0]
    
    # COPY MXI AFTER RENDER 'Users/Andrew/Documents/maxwell/image.mxi'
    copyMXI = scene.getRenderParameter('COPY MXI AFTER RENDER')[0]
 
    # Left camera resolution
    # At this point we assume the right camera view is rendered to the same resolution
    res = cam.getResolution()
    width = res[0]
    height = res[1]
  
    # Gear VR Imagery Settings
    cubicResolution = height/2

    # Check to see that the image does exist for real
    if os.path.exists(maxwell_rendered_input_image):
      print('[Maxwell Rendered LatLong Image] "' + maxwell_rendered_input_image + '"')
    else:
      print('[Maxwell Rendered LatLong Image Missing Error] "' + maxwell_rendered_input_image + '"')
      return 0
    
    # The LatLong format panorama converted into a tiff image format
    latLongTiffFrame = mtr_temp + 'mtr_latlong_' + view + '.' + nonaInputExt
  
    # Convert the maxwell image to tiff for the panoramic warping stage
    systemCommand  = '"' + imagemagick + '" '
    systemCommand += '"' + maxwell_rendered_input_image + '" '
    systemCommand += '-density 72 -units pixelsperinch '
    systemCommand += '"' + latLongTiffFrame + '" '
  
    # Redirect the output from the terminal to a log file
    outputLog = mtr_tempImagesDirectory() + 'imagemagickFrameConversionOutputLog.txt'
  
    # Customize the output log command for each platform
    systemCommand += ' ' + '2>&1 | "' + tee + '" -a ' + '"' + outputLog + '"'
  
    # Result: /var/folders/2g/_q1ztb9j0vq8yslt46x7hh_h0000gn/T/MaxwellRenderToolbox/imagmagickFrameConversionOutputLog.txt 

    result = ''
    print('[Imagemagick Frame Conversion to TIFF] ' + systemCommand + '\n')
    if mxPlatform == 'Windows':
      result = os.system('"' + systemCommand + '"')
    else:
      result = os.system(systemCommand)
    #args = shlex.split(systemCommand)
    #print('[Split Args] ' + str(args))
    #result = subprocess.Popen(args, shell=True)

    # Wait for this task to finish
    #result.wait()

    print('[Imagemagick System Result] ' + str(result) + '')
    print('[Imagemagick Progress] Conversion Complete')
  
    # Check if Imagemagick was able to turn the panorama into a tiff frame
    if os.path.exists(latLongTiffFrame):
      print('[Converted LatLong Image] "' + latLongTiffFrame + '"')
    else:
      print('[Converted LatLong Image Missing Error] "' + latLongTiffFrame + '"')
      return 0
  
    # ----------------------------------------------
    # ----------------------------------------------
  
    # Create the LatLong to Cubic Face Panotools PTO project files:
    mtr_generatePanotoolPtoFiles(width, height, cubicResolution, latLongTiffFrame)
  
    # ----------------------------------------------
    # ----------------------------------------------
    ptscriptFile = 'latlong2cubemap.pto'
  
    # Write PT Stitcher scripts
    # 6 Face Cubemap to LatLong Conversion
    systemCommand = '"' + nona + '" '

    # Nona options:
    # -g = gpu warping -v means quiet output
    nona_options = ''

    # Check the preference for the last GPU Accelerated Warping checkbox setting
    # nona_options += ' -g '
    # Disable the GPU warping flag on Mac and Linux as the GPU might be autodetected by nona

    # Remove the file extension for the nona -o image output stage
    nona_output_image_no_ext = mtr_tempImagesDirectory() +  'mtr_nona_warp_' + view + '.'

    systemCommand += ' -o "' + nona_output_image_no_ext + '"'

    # Nona warping options
    # Windows
    systemCommand += ' ' + nona_options + ' -d -r ldr -z LZW -m TIFF_m '

    # Linux
    # Fedora 17 Linux only has hugin 2011 which means GPU warping and the -d (print detailed GPU warping details) don't work
    # Low dynamic range warping, to a Tiff image with LZW compression
    # command += " " + nona_options + " -r ldr -z LZW -m TIFF_m "

    # PT Script
    systemCommand += ' "' + mtr_tempImagesDirectory() + ptscriptFile + '"' 

    # Redirect the output from the terminal to a log file
    outputLog = mtr_tempImagesDirectory() + 'nonaOutputLog.txt'

    # Customize the output log command for each platform
    systemCommand += ' ' + '2>&1 | "' + tee + '" -a ' + '"' + outputLog + '"'
  
    # Result: /var/folders/2g/_q1ztb9j0vq8yslt46x7hh_h0000gn/T/MaxwellRenderToolbox/outputLog.txt 

    result = ''
    print('[Nona Stitcher] ' + systemCommand + '\n')
    if mxPlatform == 'Windows':
      result = os.system('"' + systemCommand + '"')
    else:
      result = os.system(systemCommand)
    #args = shlex.split(systemCommand)
    #print('[Split Args] ' + str(args))
    #result = subprocess.Popen(args, shell=True)

    # Wait for this task to finish
    #result.wait()

    print('[Nona System Result] ' + str(result) + '')
    print('[Nona Progress] Stitching Complete')

  # ----------------------------------------------
  # Imagemagick Cubic View Merging


  # Left Cube Views
  output_back_L = mtr_temp + 'mtr_nona_warp_L.0000' + '.' + nonaOutputExt
  output_bottom_L = mtr_temp + 'mtr_nona_warp_L.0001' + '.' + nonaOutputExt
  output_front_L = mtr_temp + 'mtr_nona_warp_L.0002' + '.' + nonaOutputExt
  output_left_L = mtr_temp + 'mtr_nona_warp_L.0003' + '.' + nonaOutputExt
  output_right_L = mtr_temp + 'mtr_nona_warp_L.0004' + '.' + nonaOutputExt
  output_top_L = mtr_temp + 'mtr_nona_warp_L.0005' + '.' + nonaOutputExt

  # Right Cube Views
  output_back_R = mtr_temp + 'mtr_nona_warp_R.0000' + '.' + nonaOutputExt
  output_bottom_R = mtr_temp +'mtr_nona_warp_R.0001' + '.' + nonaOutputExt
  output_front_R = mtr_temp + 'mtr_nona_warp_R.0002' + '.' + nonaOutputExt
  output_left_R = mtr_temp + 'mtr_nona_warp_R.0003' + '.' + nonaOutputExt
  output_right_R = mtr_temp + 'mtr_nona_warp_R.0004' + '.' + nonaOutputExt
  output_top_R = mtr_temp + 'mtr_nona_warp_R.0005' + '.' + nonaOutputExt
  
  # Check if the OS is Windows, Mac, or Linux. 
  # We need to escape the terminal parenthesis characters on Linux and Mac with \( and \)
  # openParen = " ( ";
  # closeParen = " ) ";
  openParen = ''
  closeParen = ''

  tempDir = ''
  if mxPlatform == 'Windows':
    # Windows
    openParen = " ( "
    closeParen = " ) "
  else:
    # Mac or Linux
    openParen = " \\( "
    closeParen = " \\) "

  # Merge the cubic images:
  # Build the 6 cubic faces into a GearVR horizontal strip layout
  # Note: The \\(  and \\) are for escaping the parenthesis in the Imagemagick commands since they are happening inside the terminal

  systemCommand  = '"' + imagemagick + '" '
  systemCommand += '"' + output_left_R + '" '
  systemCommand += '"' + output_right_R + '" '
  systemCommand += openParen + '"' + output_top_R + '" ' + ' -rotate 180 ' + closeParen
  systemCommand += openParen + '"' + output_bottom_R + '" ' + ' -rotate 180 ' + closeParen
  systemCommand += '"' + output_back_R + '" '
  systemCommand += '"' + output_front_R + '" '

  systemCommand += '"' + output_left_L + '" '
  systemCommand += '"' + output_right_L + '" '
  systemCommand += openParen + '"' + output_top_L + '" ' + ' -rotate 180 ' + closeParen
  systemCommand += openParen + '"' + output_bottom_L + '" ' + ' -rotate 180 ' + closeParen
  systemCommand += '"' + output_back_L + '" '
  systemCommand += '"' + output_front_L + '" '
  systemCommand += '+append '
  # Change the output DPI to 72 DPI
  systemCommand += ' -density 72 -units pixelsperinch '
  systemCommand += '"' + output_gearvr + '" '

  # Redirect the output from the terminal to a log file
  outputLog = mtr_tempImagesDirectory() + 'imagemagickOutputLog.txt'

  # Customize the output log command for each platform
  systemCommand += ' ' + '2>&1 | "' + tee + '" -a ' + '"' + outputLog + '"'

  # Result: /var/folders/2g/_q1ztb9j0vq8yslt46x7hh_h0000gn/T/MaxwellRenderToolbox/outputLog.txt 

  result = ''
  print('[Imagemagick Conversion Command] ' + systemCommand + '\n')
  if mxPlatform == 'Windows':
    result = os.system('"' + systemCommand + '"')
  else:
    result = os.system(systemCommand)
  #args = shlex.split(systemCommand)
  #print('[Split Args] ' + str(args))
  #result = subprocess.Popen(args, shell=True)

  # Wait for this task to finish
  #result.wait()

  print('[GearVR Cubic Face Resolution] ' + str(cubicResolution))
  print('[GearVR Panorama Output] ' + output_gearvr)

  print('\n-------------------------------------------------------------')
  print('LatLong Stereo to GearVR Stereo Cubic Image Conversion Complete')

  return 1

# Find out the MaxwellRenderToolbox temporary images directory:
# Example mtr_temp = mtr_tempImagesDirectory()
def mtr_tempImagesDirectory():
  # Construct the temp directory path
  tempDirPrefix = 'MaxwellRenderToolbox'
  tempDir = ''
  # C:\Users\ADMINI~1\AppData\Local\Temp\MaxwellRenderToolbox\

  mxPlatform = mtr_getPlatform()
  tempDir = ''
  if mxPlatform == 'Windows':
    # Windows Temp Directory
    tempDir = os.getenv('TEMP') + tempDirPrefix + os.sep
  else:
    # Mac and Linux Temp directory
    tempDir = os.getenv('TMPDIR') + tempDirPrefix + os.sep
  
  # Make the MaxwellRenderToolbox folder
  if os.path.isdir(tempDir) == False:
    print('[Creating MaxwellRenderToolbox Temporary Directory] ' + tempDir)
    os.mkdir(tempDir)
  else: 
    print('[MaxwellRenderToolbox Temporary Directory Exists] ' + tempDir)

  return tempDir


# Create the LatLong to Cubic Face Panotools PTO project files:
# Example: mtr_generatePanotoolPtoFiles('2048', '1024', '512', '/latlong_image.png')
def mtr_generatePanotoolPtoFiles(imageWidth, imageHeight, cubicResolution, input_latlong):
  
  # This is the FOV setting for each of the extracted cubemap faces
  outputHorizFov = 90
  
  # This is the FOV for the LatLong Frame
  inputHorizFOV = 360
  
  # ptscript_image_options = ' nPICT ' # Does BMP format on windows / PICT on Mac
  ptscript_image_options = ' n"TIFF_m c:LZW" ' # Tiff Output

  ptscript_mline  = 'm i4' + '\n'  # HQ sinc64 mode
  #ptscript_mline  = 'm i2' + '\n'  # HQ sinc mode
  #ptscript_mline  = 'm i5' + '\n'  # Linear
  #ptscript_mline  = 'm i6' + '\n'  # Nearest neighbour

  # PT Stitcher 'p' = Destination Image Attributes
  ptscript_pline = 'p f0 w' + str(int(cubicResolution)) + ' h' + str(int(cubicResolution)) + ' v' + str(outputHorizFov) + ptscript_image_options + ' \n'

  # PT Stitcher 'i' = Input Image Attributes
  ptscript_iline_back   = 'i f4 w' + str(int(imageWidth)) + ' h' + str(int(imageHeight)) + ' v' + str(inputHorizFOV) + ' r180 y0 p180 b0' + ' n"' + input_latlong + '"' + '\n'
  ptscript_iline_bottom = 'i f4 w' + str(int(imageWidth)) + ' h' + str(int(imageHeight)) + ' v' + str(inputHorizFOV) + ' r0 y0 p90 b0' + ' n"' + input_latlong + '"' + '\n'
  ptscript_iline_front  = 'i f4 w' + str(int(imageWidth)) + ' h' + str(int(imageHeight)) + ' v' + str(inputHorizFOV) + ' r0 y0 p0 b0' + ' n"' + input_latlong + '"' + '\n'
  ptscript_iline_left   = 'i f4 w' + str(int(imageWidth)) + ' h' + str(int(imageHeight)) + ' v' + str(inputHorizFOV) + ' r0 y90 p0 b0' + ' n"' + input_latlong + '"' + '\n'
  ptscript_iline_right  = 'i f4 w' + str(int(imageWidth)) + ' h' + str(int(imageHeight)) + ' v' + str(inputHorizFOV) + ' r0 y-90 p0 b0' + ' n"' + input_latlong + '"' + '\n'
  ptscript_iline_top    = 'i f4 w' + str(int(imageWidth)) + ' h' + str(int(imageHeight)) + ' v' + str(inputHorizFOV) + ' r0 y0 p-90 b0' + ' n"' + input_latlong + '"' + '\n'
  
  # Make an array to hold the 'i' line sourceimage elements
  iLineArray = []
  iLineArray.append(ptscript_iline_back)
  iLineArray.append(ptscript_iline_bottom)
  iLineArray.append(ptscript_iline_front)
  iLineArray.append(ptscript_iline_left)
  iLineArray.append(ptscript_iline_right)
  iLineArray.append(ptscript_iline_top)

  # Make an array to hold the cubic views
  cubicViews = []
  cubicViews.append('back')
  cubicViews.append('bottom')
  cubicViews.append('front')
  cubicViews.append('left')
  cubicViews.append('right')
  cubicViews.append('top')
  
  # Track the array element number
  i = 0
  
  # PTstitcher / nona / PTmender Script Filename
  ptscriptFile = 'latlong2cubemap.pto'

  # Check the OS time
  now = datetime.datetime.now()

  # Add the header to the PTO file
  # Generate the header for each PTO file
  ptscriptText  = '# Panotools Stitching Script - LatLong to GearVR Cubic\n'
  ptscriptText += '# Extract a ' + str(int(cubicResolution)) + ' px cubic view from a ' + str(int(imageWidth)) + 'x' + str(int(imageHeight)) + 'px LatLong panorama\n'
  ptscriptText += '# Created by Maxwell Render Toolbox\n'
  ptscriptText += '# Generated: ' + now.strftime('%Y-%m-%d %H:%M:%S %p') + '\n'
  ptscriptText += '\n'
  
  ptscriptText += '# Destination Image - Cubic View Cubic Face\n'
  ptscriptText += ptscript_pline + '\n'
    
  ptscriptText += '# Interpolation Mode HQ sinc64\n'
  ptscriptText += ptscript_mline + '\n'

  # Generate each camera view's pto file
  ptscriptText += '# Back Image\n'
  ptscriptText += ptscript_iline_back + '\n'
  
  ptscriptText += '# Bottom Image\n'
  ptscriptText += ptscript_iline_bottom + '\n'
  
  ptscriptText += '# Front Image\n'
  ptscriptText += ptscript_iline_front + '\n'
  
  ptscriptText += '# Left Image\n'
  ptscriptText += ptscript_iline_left + '\n'
  
  ptscriptText += '# Right Image\n'
  ptscriptText += ptscript_iline_right + '\n'
  
  ptscriptText += '# Top Image \n'
  ptscriptText += ptscript_iline_top + '\n'


  # Display the output text for the PT Stitcher script
  print('[PT Stitcher Script] ' + ptscriptText)
  # Write the active camera view's .pto file to the temp folder
  mtr_writePTScriptFile(ptscriptFile, ptscriptText)
  

# Write out a pt stitcher script file
# Example: mtr_writePTScriptFile('/script.pto', 'm i4')
def mtr_writePTScriptFile(filename, ptscriptText):
  
  ptscriptFilename = mtr_tempImagesDirectory() + filename
  ptFile = open(ptscriptFilename, 'w')
  ptFile.write(ptscriptText)
  ptFile.close
  
  print('[PT Stitcher PTO File] ' + ptscriptFilename + '')
  print(ptscriptText + '\n\n')
  
      
# Return the base folder of MaxwellRenderToolbox with an included trailing slash
# Example: mtr_directory = mtr_getMaxwellRenderToolboxBaseFolder()
def mtr_getMaxwellRenderToolboxBaseFolder():
  mtr_directory = ''
  mxPlatform = mtr_getPlatform()

  if mxPlatform == 'Windows':
    # Windows
    mtr_directory = 'C:\\Program Files\\MaxwellRenderToolbox\\'
  elif mxPlatform == 'Mac':
    # Mac
    mtr_directory = '/Applications/MaxwellRenderToolbox/'
  else:
    # Linux
    mtr_directory = '/opt/MaxwellRenderToolbox/'

  # print('[MTR Base Directory on ' + mxPlatform + '] ' + mtr_directory)
  return mtr_directory


# Open a folder window up using your desktop file browser
# Example: mtr_openDirectory('/Applications/')
def mtr_openDirectory(filenameNativePath):
  mxPlatform = mtr_getPlatform()
  
  # Convert a path to a file into a directory path
  dirName = ''
  if os.path.isfile(filenameNativePath):
    dirName = os.path.dirname(filenameNativePath)
  else:
    dirName = filenameNativePath
  
  # Check OS platform for Windows/Mac/Linux Paths
  if mxPlatform == 'Windows':
    dirName = dirName.replace("/","\\")
    # Check if the program is running on Windows 
    os.system('explorer "' + dirName + '"')
  elif mxPlatform == 'Linux':
    # Check if the program is running on Linux
    os.system('nautilus "' + dirName + '" &')
  elif mxPlatform == 'Mac':
    # Check if the program is running on Mac
    os.system('open "' + dirName + '" &')
  else:
    # Create the empty variable as a fallback mode
    dirName = ''
    
  print('[Opening the Directory] ' + dirName)
  return dirName
  
  
# Open the MaxwellRenderToolbox temporary images folder window up using your desktop file browser
# Example: mtr_openTempImagesDirectory()
def mtr_openTempImagesDirectory():
  filenameNativePath = ''
  mxPlatform = mtr_getPlatform()
  
  #Check OS platform for Windows/Mac/Linux Paths
  if mxPlatform == 'Windows':
    # Check if the program is running on Windows 
    filenameNativePath = mtr_tempImagesDirectory()
    os.system('explorer "' + filenameNativePath + '"')
  elif mxPlatform == 'Linux':
    # Check if the program is running on Linux
    filenameNativePath = mtr_tempImagesDirectory()
    os.system('nautilus "' + filenameNativePath + '" &')
  elif mxPlatform == 'Mac':
    # Check if the program is running on Mac
    filenameNativePath = mtr_tempImagesDirectory()
    os.system('open "' + filenameNativePath + '" &')
  else:
    # Create the empty variable as a fallback mode
    filenameNativePath = ''
    
  print('[Opening the Temporary Images Directory] ' + filenameNativePath)
  return filenameNativePath
  
  
# Check the operating system
# Example: mxPlatform = mtr_getPlatform()
def mtr_getPlatform():
  import platform

  osPlatform = str(platform.system())

  mxPlatform = ''
  if osPlatform == 'Windows':
    mxPlatform = 'Windows'
  elif osPlatform == 'win32':
    mxPlatform = 'Windows'
  elif osPlatform == 'Darwin':
   mxPlatform = "Mac"
  elif osPlatform== 'Linux':
    mxPlatform =  'Linux'
  elif osPlatform == 'Linux2':
    mxPlatform = 'Linux'
  else:
    mxPlatform = 'Linux'
  
  # print('[Running on ' + mxPlatform + ']')
  return mxPlatform


# This code is the "main" section that is run automatically when the python script is loaded in pyMaxwell:
if __name__ == "__main__":

  # Release Version
  mtr_version = '0.1'
  
  print('-----------------------------------------------')
  print('MXI to GearVR Cubic Panorama Converter v' + mtr_version)
  print('By Andrew Hazelden <andrew@andrewhazelden.com>')
  print('http://www.andrewhazelden.com/blog')
  print('-----------------------------------------------\n')
  
  # Choose a Maxwell Left Camera View MXS to process:
  # mxsLeftImagePath = '/Applications/MaxwellRenderToolbox/examples/stereo/CubeX_L.mxs'
  mxsLeftImagePath = 'C:/Program Files/MaxwellRenderToolbox/examples/stereo/CubeX_L.mxs'
  # mxsLeftImagePath = '/opt/MaxwellRenderToolbox/examples/stereo/CubeX_L.mxs'
  # mxsLeftImagePath = '/home/andrew/MaxwellRenderToolbox/examples/stereo/CubeX_L.mxs'

  # Choose a Maxwell Right Camera View MXS to process:
  # mxsRightImagePath = '/Applications/MaxwellRenderToolbox/examples/stereo/CubeX_R.mxs'
  mxsRightImagePath = 'C:/Program Files/MaxwellRenderToolbox/examples/stereo/CubeX_R.mxs'
  # mxsRightImagePath = '/opt/MaxwellRenderToolbox/examples/stereo/CubeX_R.mxs'
  # mxsRightImagePath = '/home/andrew/MaxwellRenderToolbox/examples/stereo/CubeX_R.mxs'
  
  # Choose the filename prefix for the rendered GearVR cubic panorama - without the file extension or file directory path
  gearVRImagenamePrefix = '_GearVR_Stereo'
  
  # Choose a file format for the converted panorama 
  outputPanoramaFileExt = 'png'
  # outputPanoramaFileExt = 'jpg'
  # outputPanoramaFileExt = 'tga'
  # outputPanoramaFileExt = 'exr'
 
  # Launch the automagic stereo camera set up command
  if os.path.exists(mxsLeftImagePath):
    if os.path.exists(mxsLeftImagePath):
      # Generate the GearVR Stereo Cubic Output
      print('[MXS Left File] ' + mxsLeftImagePath)
      print('[MXS Right File] ' + mxsLeftImagePath)
      ok = mrt_latlong2gearvr(mxsLeftImagePath, mxsRightImagePath, gearVRImagenamePrefix, outputPanoramaFileExt)
      
      if ok == 1:
        # Open the MaxwellRenderToolbox temporary images folder window up using your desktop file browser
        #mtr_openTempImagesDirectory()
        
        # Open a folder window up using your desktop file browser
        mtr_openDirectory(mxsLeftImagePath)
    else:
      print('[MXS Right Image File Not Found] ' + mxsLeftImagePath)
  else:
    print('[MXS Left Image File Not Found] ' + mxsLeftImagePath)

