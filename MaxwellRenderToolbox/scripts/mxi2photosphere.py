# MXI 2 Photosphere for PyMaxwell
# ---------------------------------
# 2015-12-10 11.15 AM v0.1
# By Andrew Hazelden 
# Email: andrew@andrewhazelden.com
# Blog: http://www.andrewhazelden.com

# Description
# -----------
# This script will embed the Google Photosphere EXIF metadata into a LatLong panorama


# How do I use the script?
# ------------------------

# Step 1.
# Render out a LatLong format panoramic image and save the .mxi file.

# Step 2.
# Launch PyMaxwell and open up the `mxi2photosphere.py.py` python script.

# Step 3.
# Edit the "mxiImagePath" variable in the main function near the bottom of this script and specify your Maxwell Studio based MXI scene file.

# Step 4. Select the Script > Run menu item in PyMaxwell.
# -----------------------------------------

from pymaxwell import *
from math import *
import datetime
import platform
import subprocess
import shlex
import os
import sys


# Process the MXI image and save out a JPEG frame with the EXIF Metadata embedded in it
def mrt_processMXI(mxiNumber, mxiImagePath, headingDegrees):
  # Find out the current scene file
  dirName = os.path.dirname(mxiImagePath)
  mxiName = os.path.basename(mxiImagePath)
  mxiNameNoExt = os.path.splitext(mxiName)[0]
  mxiPathNoExt = os.path.splitext(mxiImagePath)[0]
  
  mxi = CmaxwellMxi()
  
  # Check the operating system
  mtrPlatform = mtr_getPlatform()

  # Load the MXI Image data into Maxwell
  readHeaderOnly = 0
  selectedChannels = FLAG_NONE

  if mxi.read(mxiImagePath, readHeaderOnly, selectedChannels).failed():
    print('[Failed to Read MXI File] ' + mxiImagePath)
    return 0

  # Read the image dimensions
  width = int(mxi.xRes())
  height = int(mxi.yRes())

  # Read the SL sampling level and round it to 3 decimal places
  samplingLevel = round(mxi.getSamplingLevel(), 3)

  print( '[MXI] ' + mxiName + ' [Image Dimensions] ' + str(width) + 'x' + str(height) + ' px' + ' [SL] ' + str(samplingLevel) + ' [Heading Angle] ' + str(headingDegrees) + ' degrees')
  
  # Export a new JPEG image from the MXI file
  imageExt = 'jpg'
  bitdepth = 8
  imageNameNoExt = mxiNameNoExt + '_'
  imageFileName = dirName + os.sep + imageNameNoExt + 'render' + '.' + imageExt
  
  if not mxi.extractChannels(imageNameNoExt,dirName,imageExt,bitdepth):
    print('[Error Writing Image to Disk] ' + imageFilePath)
    return 0
  else:
    print('[Writing Image to Disk] ' + imageFileName)
    
  # Generate the Args file for Exiftool
  exifArgsFilePath = mtr_writeExiftoolArgsFile(imageFileName, width, height, headingDegrees)
  
  filenameNativePath = ''
  exiftool = ''
  tee = ''
  if mtrPlatform == 'Windows':
    filenameNativePath = mtr_getMaxwellRenderToolboxBaseFolder() + 'tools' + os.sep
    tee = filenameNativePath + 'wintee' + os.sep + 'bin' + os.sep + 'wtee.exe'
    exiftool = filenameNativePath + 'exiftool' + os.sep + 'exiftool.exe'
  elif mtrPlatform == 'Mac':
    filenameNativePath = mtr_getMaxwellRenderToolboxBaseFolder() + 'mac_tools' + os.sep
    exiftool = filenameNativePath + 'exiftool' + os.sep + 'exiftool'
    tee = 'tee'
  else:
    # Linux
    filenameNativePath = mtr_getMaxwellRenderToolboxBaseFolder() + 'linux_tools' + os.sep
    exiftool = os.sep + 'usr' + os.sep + 'bin' + os.sep + 'exiftool'
    #exiftool = 'exiftool'
    tee = 'tee'
  
  
  command  = '"' + exiftool + '"' 
  command += ' -overwrite_original'
  
  # Note add the exiftool -q (quiet) option to skip outputting the status text
  command += ' -q -q '
  
  command += " -@ " + '"' + exifArgsFilePath + '"'
  command += ' "' + imageFileName + '" '
  
  # Redirect the output from the terminal to a log file
  outputLog = mtr_tempImagesDirectory() + 'exiftoolOutputLog.txt'
  
  # Customize the output log command for each platform
  command += ' ' + '2>&1 | "' + tee + '" -a ' + '"' + outputLog + '"'
  
  # Result: /var/folders/2g/_q1ztb9j0vq8yslt46x7hh_h0000gn/T/MaxwellRenderToolbox/exiftoolOutputLog.txt 
  
  result = ''
  print('[Adding Exif Data] ' + command + '\n')
  result = os.system(command)
  #args = shlex.split(command)
  #print (args)
  #result = subprocess.Popen(args, shell=True)
  
  # Wait for this task to finish
  #result.wait()


  # Open the folder that holds the image using your desktop file browser
  mtr_openDirectory(imageFileName)
      
  # Add a newline between each time the mrt_processMXI() function is run on a directory of MXI files
  print('\n')


# Write out an args file for Exiftool
# Example: mtr_writeExiftoolArgsFile('/latlong.mxi', 2048, 1024, 180 )  
def mtr_writeExiftoolArgsFile(mxiImagePath, width, height, headingDegrees):
  import os
  import platform

  # Camera focus distance
  # focalLength = 0

  # Rendered Camera's F-stop value
  fStopNumber = 3.5

  # Find out the exposure time based upon getting the frame rate*2e()
  exposureTime = 1

  # Get the current Softimage scene filename  
  mxiImageFile = os.path.basename(mxiImagePath)
  
  # Maxwell Release number - like "3.2.0.2"
  mxVersion = getPyMaxwellVersion()
  
  # Check the operating system
  mtrPlatform = mtr_getPlatform()

  # Write in the name of the MTR user
  exifOwnerName= 'Maxwell Render Toolbox User'
  # exifOwnerName = mtr_getEXIFOwnerName()

  exifScriptText  = '-n\n'
  exifScriptText += '-UsePanoramaViewer=True\n'
  exifScriptText += '-ProjectionType=equirectangular\n'
  exifScriptText += '-PoseHeadingDegrees=' + str(headingDegrees) + '\n'
  exifScriptText += '-CroppedAreaLeftPixels=0\n'
  exifScriptText += '-FullPanoWidthPixels=' + str(int(width)) + '\n'
  exifScriptText += '-CroppedAreaImageHeightPixels=' + str(int(height)) + '\n'
  exifScriptText += '-FullPanoHeightPixels=' + str(int(height)) + '\n'
  exifScriptText += '-CroppedAreaImageWidthPixels=' + str(int(width)) + '\n'
  exifScriptText += '-CroppedAreaTopPixels=0\n'
  exifScriptText += '-LargestValidInteriorRectLeft=0\n'
  exifScriptText += '-LargestValidInteriorRectTop=0\n'
  exifScriptText += '-LargestValidInteriorRectWidth=' + str(int(width)) + '\n'
  exifScriptText += '-LargestValidInteriorRectHeight=' + str(int(height)) + '\n'
  exifScriptText += '-xmp:CreatorTool=Maxwell Render Toolbox\n'
  exifScriptText += '-xmp:Software=Maxwell Render v' + str(mxVersion) +  ' on ' + mtrPlatform + '\n'
  exifScriptText += '-xmp:Lens=Equirectangular 360 Degree Lens Shader\n'
  exifScriptText += '-xmp:Model=Maxwell Render Toolbox\n'
  exifScriptText += '-xmp:Make=Andrew Hazelden\n'
  exifScriptText += '-xmp:OwnerName=' + exifOwnerName + '\n'
  exifScriptText += '-xmp:SerialNumber=MTR0002015\n'
  exifScriptText += '-xmp:Title=' + mxiImageFile + '\n'
  exifScriptText += '-xmp:Category=Panorama\n'
  exifScriptText += '-xmp:Marked=Copyrighted\n'
  #exifScriptText += '-exif:ExposureTime=' + str(exposureTime) + '\n'
  ## exifScriptText += '-exif:FocalLength=' + str(focalLength) + '\n'
  ## exifScriptText += '-exif:FocalLengthIn35mmFormat=' + str(focalLength) + '\n'
  #exifScriptText += '-exif:FNumber=' + str(fStopNumber) + '\n'
  exifScriptText += '-exif:ImageWidth=' + str(int(width)) + '\n'
  exifScriptText += '-exif:ImageHeight=' + str(int(height)) + '\n'
  exifScriptText += '\n'

  exifFilename = ( mtr_tempImagesDirectory() + 'exif-args.txt' )
  exifFile = open(exifFilename, 'w')
  exifFile.write(exifScriptText)
  exifFile.close

  print('[Exiftool Args file] ' + exifFilename + '\n')
  print(exifScriptText + '\n\n')

  # Return the Windows formatted file path
  return exifFilename


# Return the base folder of MaxwellRenderToolbox with an included trailing slash
# Example: mtr_directory = mtr_getMaxwellRenderToolboxBaseFolder()
def mtr_getMaxwellRenderToolboxBaseFolder():
  mtr_directory = ''
  mtrPlatform = mtr_getPlatform()

  if mtrPlatform == 'Windows':
    # Windows
    mtr_directory = 'C:\\Program Files\\MaxwellRenderToolbox\\'
  elif mtrPlatform == 'Mac':
    # Mac
    mtr_directory = '/Applications/MaxwellRenderToolbox/'
  else:
    # Linux
    mtr_directory = '/opt/MaxwellRenderToolbox/'

  # print('[MTR Base Directory on ' + mtrPlatform + '] ' + mtr_directory)
  return mtr_directory


# Open the MaxwellRenderToolbox temporary images folder window up using your desktop file browser
# Example: mtr_openTempImagesDirectory()
def mtr_openTempImagesDirectory():
  filenameNativePath = ''
  mtrPlatform = mtr_getPlatform()
  
  # Check OS platform for Windows/Mac/Linux Paths
  if mtrPlatform == 'Windows':
    # Check if the program is running on Windows 
    filenameNativePath = mtr_tempImagesDirectory()
    os.system('explorer "' + filenameNativePath + '"')
  elif mtrPlatform == 'Linux':
    # Check if the program is running on Linux
    filenameNativePath = mtr_tempImagesDirectory()
    os.system('nautilus "' + filenameNativePath + '" &')
  elif mtrPlatform == 'Mac':
    # Check if the program is running on MAC
    filenameNativePath = mtr_tempImagesDirectory()
    os.system('open "' + filenameNativePath + '" &')
  else:
    # Create the empty variable as a fallback mode
    filenameNativePath = ''
    
  print('[Opening the Temporary Images Directory] ' + filenameNativePath)
  return filenameNativePath


# Open a folder window up using your desktop file browser
# Example: mtr_openDirectory('/Applications/')
def mtr_openDirectory(filenameNativePath):
  mtrPlatform = mtr_getPlatform()
  
  # Convert a path to a file into a directory path
  dirName = ''
  if os.path.isdir(filenameNativePath):
    dirName = filenameNativePath
  else:
    # print('[Selecting the Parent Folder]')
    dirName = os.path.dirname(filenameNativePath)
  
  # Check OS platform for Windows/Mac/Linux Paths
  if mtrPlatform == 'Windows':
    # Check if the program is running on Windows 
    os.system('explorer "' + dirName + '"')
  elif mtrPlatform == 'Linux':
    # Check if the program is running on Linux
    os.system('nautilus "' + dirName + '" &')
  elif mtrPlatform == 'Mac':
    # Check if the program is running on MAC
    os.system('open "' + dirName + '" &')
  else:
    # Create the empty variable as a fallback mode
    dirName = ''
    
  print('[Opening the Directory] ' + dirName)
  return dirName
  

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
  
  
# Check the operating system
# Example: mtrPlatform = mtr_getPlatform()
def mtr_getPlatform():
  import platform

  osPlatform = str(platform.system())

  mtrPlatform = ''
  if osPlatform == 'Windows':
    mtrPlatform = 'Windows'
  elif osPlatform == 'win32':
    mtrPlatform = 'Windows'
  elif osPlatform == 'Darwin':
   mtrPlatform = "Mac"
  elif osPlatform== 'Linux':
    mtrPlatform =  'Linux'
  elif osPlatform == 'Linux2':
    mtrPlatform = 'Linux'
  else:
    mtrPlatform = 'Linux'
  
  # print('Running on ' + mtrPlatform + '\n')
  return mtrPlatform


# -------------------------------------------------------------------
# -------------------------------------------------------------------
# This code is the "main" section that is run automatically when the python script is loaded in pyMaxwell:
if __name__ == "__main__":

  # Release Version
  mtr_version = '0.1'
  
  print('-----------------------------------------------')
  print('Maxwell MXI 2 Photosphere v' + mtr_version + ' on ' + mtr_getPlatform())
  print('By Andrew Hazelden <andrew@andrewhazelden.com>')
  print('http://www.andrewhazelden.com/blog')
  print('-----------------------------------------------\n')

  # MXI scene file extension
  mxiFileExt = 'mxi'
  
  # ------------------------------------------
  # Process a single Maxwell MXI File
  # ------------------------------------------
  # mxiImagePath = '/Applications/MaxwellRenderToolbox/examples/stereo/CubeX_L.mxi'
  # mxiImagePath = 'C:/Program Files/MaxwellRenderToolbox/examples/stereo/CubeX_L.mxi'
  # mxiImagePath = '/opt/MaxwellRenderToolbox/examples/stereo/CubeX_L.mxi'

  # ---------------------------------------------------
  # Or process a whole directory of Maxwell MXI files
  # ---------------------------------------------------
  mxiImagePath = '/Applications/MaxwellRenderToolbox/examples/stereo/'
  # mxiImagePath = 'C:/Program Files/MaxwellRenderToolbox/examples/stereo/'
  # mxiImagePath = '/opt/MaxwellRenderToolbox/examples/stereo/'

  # Google Photosphere panorama default heading angle in degrees
  headingDegrees = 0

  # Check if we are going to process 1 MXI file or a whole directory of MXI files
  if os.path.isfile(mxiImagePath):
    # Launch the MXI single file processing command
    mxiNumber = 1
    print('[Entering MXI Single File Processing Mode]\n')

    # Load the MXI Image data into Maxwell
    print('[MXI File #' + str(mxiNumber) + '] ' + mxiImagePath)
    ok = mrt_processMXI(mxiNumber, mxiImagePath, headingDegrees)
  elif os.path.isdir(mxiImagePath):
    print('[Entering MXI Directory Processing Mode]')
    
    # Build a list of MXI files in the current directory
    print('[Base Directory] ' + os.path.dirname(mxiImagePath) + '\n')
    mxiFileList = getFilesFromPath(mxiImagePath, mxiFileExt)
    mxiNumber=0

    # Iterate through each of the active MXI files is the current directory
    for file in mxiFileList:
      mxiNumber += 1
      mxiFileDirPath = mxiImagePath + file
      print('[MXI File #' + str(mxiNumber) + '] ' + mxiFileDirPath)
      # Load the MXI Image data into Maxwell
      ok = mrt_processMXI(mxiNumber, mxiFileDirPath, headingDegrees)
  else:
    print('[MXI File Not Found] ' + mxiImagePath)
    
  print('\n-------------------------------------------------------------')
  print('Google Photosphere Metadata Editing Complete')
  