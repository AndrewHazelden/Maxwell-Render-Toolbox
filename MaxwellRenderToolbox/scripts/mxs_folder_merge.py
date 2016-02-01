# MXS Folder Merge for PyMaxwell
# ---------------------------------
# 2016-01-31 20.15 PM
# By Andrew Hazelden 
# Email: andrew@andrewhazelden.com
# Blog: http://www.andrewhazelden.com

# Description
# -----------
# This script will take a folder full of .mxs scene files and merge all of the cameras and mesh elements into a single mxs document.


# How do I use the script?
# ------------------------

# Step 1. Launch PyMaxwell and open up the `mxs_folder_merge.py` python script.

# Step 2. Edit the "mxsFilePath" variable in the main function near the bottom of this script and specify a directory that holds your Maxwell Studio based MXS scene files.

# The "mxsOutputFilenamePrefix" variable lets you specify the prefix part of the newly merged mxs document. When the script is run, a new folder called "Merged" will be created in the "mxsFilePath" folder that contains the newly generated mxs scene output. The final file name will be formated like this "<prefix>_merged.mxs".

# Step 3. Select the Script > Run menu item in PyMaxwell.

# Step 4. A new desktop folder window will open when the script completes that shows the newly merged .mxs scene file.


from pymaxwell import *
from math import *
import datetime
import platform
import subprocess
import shlex
import os
import sys


# Process the MXS files and send them off to be rendered
def mrt_processMXS(mxsNumber, mxsFilePath, scene):
  # Find out the current scene file
  dirName = os.path.dirname(mxsFilePath)
  mxsName = os.path.basename(mxsFilePath)
  mxsNameNoExt = os.path.splitext(mxsName)[0]
  mxsPathNoExt = os.path.splitext(mxsFilePath)[0]
  
  mxs = CmaxwellMxi()
  
  # Check the operating system
  mrtPlatform = mrt_getPlatform()

  # Load the MXS data into Maxwell
  scene.readMXS(mxsFilePath)

  info,ok = scene.getSceneInfo()
  print('[Scene Info] ' + str(info) + '\n')

  # Add a newline between each time the mrt_processMXS() function is run on a directory of MXS files
  print('\n')
  
  return 1
  
  
# Save an MXS scene export
# Example: mrt_saveMXS(scene, mxsPathNoExt, '_Cubic')
def mrt_saveMXS(scene, mxsPathNoExt, mxsNameAddon):

  mxsFilename = mxsPathNoExt + mxsNameAddon + '.mxs'
  ok = scene.writeMXS(mxsFilename)
  if ok == 0:
    print('[Write Error While Saving File] ' + mxsFilename)
    return 0
  else:
    print('[Saved MXS File] ' + mxsFilename)
    return 1
    
  print('\n')


# Return the base folder of MaxwellRenderToolbox with an included trailing slash
# Example: mrt_directory = mrt_getMaxwellRenderToolboxBaseFolder()
def mrt_getMaxwellRenderToolboxBaseFolder():
  mrt_directory = ''
  mrtPlatform = mrt_getPlatform()

  if mrtPlatform == 'Windows':
    # Windows
    mrt_directory = 'C:\\Program Files\\MaxwellRenderToolbox\\'
  elif mrtPlatform == 'Mac':
    # Mac
    mrt_directory = '/Applications/MaxwellRenderToolbox/'
  else:
    # Linux
    mrt_directory = '/opt/MaxwellRenderToolbox/'

  # print('[MTR Base Directory on ' + mrtPlatform + '] ' + mrt_directory)
  return mrt_directory


# Open the MaxwellRenderToolbox temporary images folder window up using your desktop file browser
# Example: mrt_openTempImagesDirectory()
def mrt_openTempImagesDirectory():
  filenameNativePath = ''
  mrtPlatform = mrt_getPlatform()
  
  # Check OS platform for Windows/Mac/Linux Paths
  if mrtPlatform == 'Windows':
    # Check if the program is running on Windows 
    filenameNativePath = mrt_tempImagesDirectory()
    os.system('explorer "' + filenameNativePath + '"')
  elif mrtPlatform == 'Linux':
    # Check if the program is running on Linux
    filenameNativePath = mrt_tempImagesDirectory()
    os.system('nautilus "' + filenameNativePath + '" &')
  elif mrtPlatform == 'Mac':
    # Check if the program is running on Mac
    filenameNativePath = mrt_tempImagesDirectory()
    os.system('open "' + filenameNativePath + '" &')
  else:
    # Create the empty variable as a fallback mode
    filenameNativePath = ''
    
  print('[Opening the Temporary Images Directory] ' + filenameNativePath)
  return filenameNativePath



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
    tempDir = os.getenv('TEMP') + os.sep + tempDirPrefix + os.sep
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
# Example: mrtPlatform = mrt_getPlatform()
def mrt_getPlatform():
  import platform

  osPlatform = str(platform.system())

  mrtPlatform = ''
  if osPlatform == 'Windows':
    mrtPlatform = 'Windows'
  elif osPlatform == 'win32':
    mrtPlatform = 'Windows'
  elif osPlatform == 'Darwin':
   mrtPlatform = "Mac"
  elif osPlatform== 'Linux':
    mrtPlatform =  'Linux'
  elif osPlatform == 'Linux2':
    mrtPlatform = 'Linux'
  else:
    mrtPlatform = 'Linux'
  
  # print('Running on ' + mrtPlatform + '\n')
  return mrtPlatform


# -------------------------------------------------------------------
# -------------------------------------------------------------------
# This code is the "main" section that is run automatically when the python script is loaded in pyMaxwell:
if __name__ == "__main__":

  # Release Version
  mrt_version = '0.1'
  
  print('-----------------------------------------------')
  print('Maxwell MXS Folder Merge v' + mrt_version + ' on ' + mrt_getPlatform())
  print('By Andrew Hazelden <andrew@andrewhazelden.com>')
  print('http://www.andrewhazelden.com/blog')
  print('-----------------------------------------------\n')

  # MXS scene file extension
  mxsFileExt = 'mxs'
  
  # ------------------------------------------
  # Build a list of Maxwell MXS Files to Merge
  # ------------------------------------------

  # mxsFilePath = '/Applications/MaxwellRenderToolbox/examples/mxs_merge/'
  mxsFilePath = 'C:/Program Files/MaxwellRenderToolbox/examples/mxs_merge/'
  # mxsFilePath = '/opt/MaxwellRenderToolbox/examples/mxs_merge/'

  mxsOutputFilenamePrefix = 'coil_scene'

  # Check if we are going to process 1 MXS file or a whole directory of MXS files
  if os.path.isfile(mxsFilePath):
    # Launch the MXS single file processing command
    print('[Error Please Select a Folder] ' + mxsFilePath)
  elif os.path.isdir(mxsFilePath):
    print('[Entering MXS Directory Processing Mode]')
    
    # Build a list of MXS files in the current directory
    baseDir = os.path.dirname(mxsFilePath)
        
    # Make the "Merged" output folder
    mergeDir = baseDir + os.sep + "Merged"
    if os.path.isdir(mergeDir) == False:
      print('[Creating "Merged" Directory] ' + mergeDir)
      os.mkdir(mergeDir)
    else: 
      print('[The "Merged" Directory Exists] ' + mergeDir)
    
    
    print('[Base Directory] ' + baseDir + '\n')
    mxsFileList = getFilesFromPath(mxsFilePath, mxsFileExt)
    mxsNumber=0

    # Load the Maxwell C API function
    scene = Cmaxwell(mwcallback)


    # Iterate through each of the active MXS files is the current directory
    for file in mxsFileList:
      mxsNumber += 1
      mxsFileDirPath = mxsFilePath + file
      print('[Loaded MXS File #' + str(mxsNumber) + '] ' + mxsFileDirPath)
      # Load the MXS Image data into Maxwell
      ok = mrt_processMXS(mxsNumber, mxsFileDirPath, scene)


    # Save an MXS Scene Export
    mxsMergedFilename = mergeDir + os.sep + mxsOutputFilenamePrefix
    ok = mrt_saveMXS(scene, mxsMergedFilename, '_merged')
    
    if ok == 1:
      # Open a folder window up using your desktop file browser
      mrt_openDirectory(mergeDir)
  else:
    print('[MXS File Not Found] ' + mergeDir)
    
  print('\n-------------------------------------------------------------')
  print('MXS Folder Merge Job Complete')

