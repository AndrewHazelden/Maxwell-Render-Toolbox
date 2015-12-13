# MXI to Anaglyph Stereo Converter for Maxwell Studio
# ----------------------------------------------------------
# 2015-12-13 08.31 AM v0.1
# By Andrew Hazelden 
# Email: andrew@andrewhazelden.com
# Blog: http://www.andrewhazelden.com

# Description
# -----------
# The `mxi2anaglyph.py` script will convert a set of Maxwell .mxi based stereo images or panoramas into a red/cyan format anaglyph image. The script uses PyMaxwell, and Imagemagick to do the conversions.


# Script Installation
# -------------------
# The mxi2anaglyph.py python script can be loaded and run from inside the MaxwellRenderToolbox's scripts folder, or if you want to, you can copy the python script to Maxwell Render's "NextLimit/Maxwell 3/scripts" folder for easier access from PyMaxwell.

# Windows
# C:/Program Files/MaxwellRenderToolbox/scripts/mxi2anaglyph.py

# Linux
# /opt/MaxwellRenderToolbox/scripts/mxi2anaglyph.py
# or
# $HOME/MaxwellRenderToolbox/scripts/mxi2anaglyph.py

# Mac
# /Applications/MaxwellRenderToolbox/scripts/mxi2anaglyph.py

# How do I use the script?
# ------------------------

# Step 1. Render out a set of Left and Right view Stereo images and save the .mxi files.

# Step 2. Launch PyMaxwell and open up the `mxi2anaglyph.py` python script.

# Step 3. Edit the "mxiLeftImagePath" and the "mxiRightImagePath" variable in the main function near the bottom of this script and specify your Maxwell Studio based MXI scene file.

# Step 4. Select the Script > Run menu item in PyMaxwell.

# Step 5. An anaglyph stereo image has been generated at this point with the name of `<Scene>_anaglyph.png` and is saved in the same folder as the original .mxi image. The folder where the new anaglyph image has been saved to will be opened up automatically in your desktop file browser.

# -----------------------------------------

from pymaxwell import *
from math import *
import datetime
import platform
import subprocess
import shlex
import os
import sys

# Convert a pair of stereo images into the anaglyph output format:
# Example: mrt_anaglyphConverter('/CubeX_L.mxs', '/CubeX_R.mxs', '_anagylph', 'png')
def mrt_anaglyphConverter(mxiLeftImagePath, mxiRightImagePath, imagenamePrefix, outputFileExt):
  # Check the current operating system
  mxPlatform = mrt_getPlatform()
  
  # Export a new PNG image from the MXI file
  imageExt = 'png'
  bitdepth = 8
  
  # Find out the current scene file
  leftDirName = os.path.dirname(mxiLeftImagePath)
  leftMxiFilePathNoExt = os.path.splitext(mxiLeftImagePath)[0]
  leftMxiName = os.path.basename(mxiLeftImagePath)
  leftMxiNameNoExt = os.path.splitext(leftMxiName)[0]
  leftImageFilename = leftDirName + os.sep + leftMxiNameNoExt + '_render' + '.' + imageExt
  
  rightDirName = os.path.dirname(mxiRightImagePath)
  rightMxiFilePathNoExt = os.path.splitext(mxiRightImagePath)[0]
  rightMxiName = os.path.basename(mxiRightImagePath)
  rightMxiNameNoExt = os.path.splitext(rightMxiName)[0]
  rightImageFilename = rightDirName + os.sep + rightMxiNameNoExt + '_render' + '.' + imageExt

  mxi = CmaxwellMxi()
  
  # Check the operating system
  mrtPlatform = mrt_getPlatform()

  # Load the MXI Image data into Maxwell
  readHeaderOnly = 0
  selectedChannels = FLAG_NONE
  
  # Left View
  # ------------
  if mxi.read(mxiLeftImagePath, readHeaderOnly, selectedChannels).failed():
    print('[Failed to Read MXI File] ' + mxiLeftImagePath)
    return 0

  # Read the image dimensions
  width = int(mxi.xRes())
  height = int(mxi.yRes())

  # Read the SL sampling level and round it to 3 decimal places
  samplingLevel = round(mxi.getSamplingLevel(), 3)

  print( '[Left MXI] ' + leftMxiName + ' [Image Dimensions] ' + str(width) + 'x' + str(height) + ' px' + ' [SL] ' + str(samplingLevel))

  if not mxi.extractChannels(leftMxiNameNoExt + '_', leftDirName ,imageExt, bitdepth):
    print('[Left Error Writing Image to Disk] ' + leftImageFilename)
    return 0
  else:
    print('[Left Writing Image to Disk] ' + leftImageFilename)
  
  # Right View
  # ------------
  if mxi.read(mxiRightImagePath, readHeaderOnly, selectedChannels).failed():
    print('[Failed to Read MXI File] ' + mxiRightImagePath)
    return 0

  # Read the image dimensions
  width = int(mxi.xRes())
  height = int(mxi.yRes())

  # Read the SL sampling level and round it to 3 decimal places
  samplingLevel = round(mxi.getSamplingLevel(), 3)

  print( '[Right MXI] ' + rightMxiName + ' [Image Dimensions] ' + str(width) + 'x' + str(height) + ' px' + ' [SL] ' + str(samplingLevel))

  if not mxi.extractChannels(rightMxiNameNoExt + '_', rightDirName, imageExt, bitdepth):
    print('[Right Error Writing Image to Disk] ' + rightImageFilename)
    return 0
  else:
    print('[Right Writing Image to Disk] ' + rightImageFilename)
  
  # ----------------------------------------------
  # ----------------------------------------------
  
  # Rendered Anaglyph Output
  output_anaglyph = leftMxiFilePathNoExt + imagenamePrefix + '.' + outputFileExt

  # Imagemagick path:
  filenameNativePath = ''
  imagemagick = ''
  tee = ''
  
  # Check OS platform for Windows/Mac/Linux Paths
  if mxPlatform == 'Windows':
    # Check if the program is running on Windows 
    filenameNativePath = mrt_getMaxwellRenderToolboxBaseFolder() + 'tools' + os.sep
    imagemagick = filenameNativePath + 'imagemagick' + os.sep + 'bin' + os.sep + 'imconvert.exe'
    tee = filenameNativePath +'wintee' + os.sep + 'bin' + os.sep + 'wtee.exe'
  elif mxPlatform == 'Mac':
    filenameNativePath = mrt_getMaxwellRenderToolboxBaseFolder() + 'mac_tools' + os.sep 
    # Todo: Find the different Imagemagick install directories and check if each of them exists
    imagemagick = '/opt/ImageMagick/bin/convert'
    tee = 'tee'
  elif mxPlatform == 'Linux':
    # Check if the program is running on Linux
    filenameNativePath = os.sep + 'usr' + os.sep + 'bin' + os.sep
    imagemagick = filenameNativePath + 'convert'
    tee = 'tee'

    # Create the empty variable as a fallback mode
    # imagemagick = 'convert'
    # tee = 'tee'


    # Check to see that the image does exist for real
    if os.path.exists(leftImageFilename):
      print('[Maxwell Rendered Left Image] "' + leftImageFilename + '"')
      if os.path.exists(rightImageFilename):
        print('[Maxwell Rendered Right Image] "' + rightImageFilename + '"')
      else:
        print('[Maxwell Rendered Right Image Missing Error] "' + rightImageFilename + '"')
        return 0
    else:
      print('[Maxwell Rendered Left Image Missing Error] "' + leftImageFilename + '"')
      return 0
  
  # ----------------------------------------------
  # ----------------------------------------------
  # Imagemagick Stereo View Merging

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

  # Merge the left and right view images:
  # Note: The \\(  and \\) are for escaping the parenthesis in the Imagemagick commands since they are happening inside the terminal

  systemCommand  = '"' + imagemagick + '" '
  systemCommand += ' -compose copy_red -composite '
  systemCommand += '"' + rightImageFilename + '" '
  systemCommand += '"' + leftImageFilename + '" '
  systemCommand += '+append '
  # Change the output DPI to 72 DPI
  systemCommand += ' -density 72 -units pixelsperinch '
  systemCommand += '"' + output_anaglyph + '" '

  # Redirect the output from the terminal to a log file
  outputLog = mrt_tempImagesDirectory() + 'imagemagickAnaglyphOutputLog.txt'

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

  print('[Anaglyph Output] ' + output_anaglyph)
  print('\n-------------------------------------------------------------')
  print('MXI to Anaglyph Stereo Image Conversion Complete')

  return 1

# Find out the MaxwellRenderToolbox temporary images directory:
# Example mrt_temp = mrt_tempImagesDirectory()
def mrt_tempImagesDirectory():
  # Construct the temp directory path
  tempDirPrefix = 'MaxwellRenderToolbox'
  tempDir = ''
  # C:\Users\ADMINI~1\AppData\Local\Temp\MaxwellRenderToolbox\

  mxPlatform = mrt_getPlatform()
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
  
      
# Return the base folder of MaxwellRenderToolbox with an included trailing slash
# Example: mrt_directory = mrt_getMaxwellRenderToolboxBaseFolder()
def mrt_getMaxwellRenderToolboxBaseFolder():
  mrt_directory = ''
  mxPlatform = mrt_getPlatform()

  if mxPlatform == 'Windows':
    # Windows
    mrt_directory = 'C:\\Program Files\\MaxwellRenderToolbox\\'
  elif mxPlatform == 'Mac':
    # Mac
    mrt_directory = '/Applications/MaxwellRenderToolbox/'
  else:
    # Linux
    mrt_directory = '/opt/MaxwellRenderToolbox/'

  # print('[MTR Base Directory on ' + mxPlatform + '] ' + mrt_directory)
  return mrt_directory


# Open a folder window up using your desktop file browser
# Example: mrt_openDirectory('/Applications/')
def mrt_openDirectory(filenameNativePath):
  mxPlatform = mrt_getPlatform()
  
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
# Example: mrt_openTempImagesDirectory()
def mrt_openTempImagesDirectory():
  filenameNativePath = ''
  mxPlatform = mrt_getPlatform()
  
  #Check OS platform for Windows/Mac/Linux Paths
  if mxPlatform == 'Windows':
    # Check if the program is running on Windows 
    filenameNativePath = mrt_tempImagesDirectory()
    os.system('explorer "' + filenameNativePath + '"')
  elif mxPlatform == 'Linux':
    # Check if the program is running on Linux
    filenameNativePath = mrt_tempImagesDirectory()
    os.system('nautilus "' + filenameNativePath + '" &')
  elif mxPlatform == 'Mac':
    # Check if the program is running on Mac
    filenameNativePath = mrt_tempImagesDirectory()
    os.system('open "' + filenameNativePath + '" &')
  else:
    # Create the empty variable as a fallback mode
    filenameNativePath = ''
    
  print('[Opening the Temporary Images Directory] ' + filenameNativePath)
  return filenameNativePath
  
  
# Check the operating system
# Example: mxPlatform = mrt_getPlatform()
def mrt_getPlatform():
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
  mrt_version = '0.1'
  
  print('-----------------------------------------------')
  print('MXI to Anaglyph Stereo Converter v' + mrt_version)
  print('By Andrew Hazelden <andrew@andrewhazelden.com>')
  print('http://www.andrewhazelden.com/blog')
  print('-----------------------------------------------\n')
  
  # Choose a Maxwell Left Camera View MXI to process:
  # mxiLeftImagePath = '/Applications/MaxwellRenderToolbox/examples/stereo/CubeX_L.mxi'
  mxiLeftImagePath = 'C:/Program Files/MaxwellRenderToolbox/examples/stereo/CubeX_L.mxi'
  # mxiLeftImagePath = '/opt/MaxwellRenderToolbox/examples/stereo/CubeX_L.mxi'
  # mxiLeftImagePath = '/home/andrew/MaxwellRenderToolbox/examples/stereo/CubeX_L.mxi'

  # Choose a Maxwell Right Camera View MXI to process:
  # mxiRightImagePath = '/Applications/MaxwellRenderToolbox/examples/stereo/CubeX_R.mxi'
  mxiRightImagePath = 'C:/Program Files/MaxwellRenderToolbox/examples/stereo/CubeX_R.mxi'
  # mxiRightImagePath = '/opt/MaxwellRenderToolbox/examples/stereo/CubeX_R.mxi'
  # mxiRightImagePath = '/home/andrew/MaxwellRenderToolbox/examples/stereo/CubeX_R.mxi'
  
  # Choose the filename prefix for the rendered anaglyph stereo image - without the file extension or file directory path
  imagenamePrefix = '_anaglyph'
  
  # Choose a file format for the converted panorama 
  outputFileExt = 'png'
  # outputFileExt = 'jpg'
  # outputFileExt = 'tga'
  # outputFileExt = 'exr'
 
  # Launch the automagic stereo camera set up command
  if os.path.exists(mxiLeftImagePath):
    if os.path.exists(mxiLeftImagePath):
      # Generate the GearVR Stereo Cubic Output
      print('[MXI Left File] ' + mxiLeftImagePath)
      print('[MXI Right File] ' + mxiLeftImagePath)
      ok = mrt_anaglyphConverter(mxiLeftImagePath, mxiRightImagePath, imagenamePrefix, outputFileExt)
      
      if ok == 1:
        # Open the MaxwellRenderToolbox temporary images folder window up using your desktop file browser
        #mrt_openTempImagesDirectory()
        
        # Open a folder window up using your desktop file browser
        mrt_openDirectory(mxiLeftImagePath)
    else:
      print('[MXI Right Image File Not Found] ' + mxiLeftImagePath)
  else:
    print('[MXI Left Image File Not Found] ' + mxiLeftImagePath)

