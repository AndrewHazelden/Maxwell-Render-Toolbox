# MXS to Render for PyMaxwell
# ---------------------------------
# 2015-12-14 09.28 AM v0.1
# By Andrew Hazelden 
# Email: andrew@andrewhazelden.com
# Blog: http://www.andrewhazelden.com

# Description
# -----------
# The `mxs2render.py` script will scan the current directory and allow you to render all of the MXS files to a custom target SL level. You can customize many of the settings that will be used for each of the renderings. The "Try to Resume" option will be enabled to allow you to progressively refine scenes with existing .mxi images.


# How do I use the script?
# ------------------------

# Step 1. Export a set of .mxs files to a directory.

# Step 2. Launch PyMaxwell and open up the `mxs2render.py` python script.

# Step 3. Edit the "mxsFilePath" variable in the main function near the bottom of this script and specify your Maxwell Studio based MXS scene file. You can also specify a directory of MXS files and they will be processed one at a time. If you want to override any of the default render settings you can do it in the main function of the code as well using the different variables that are commented out.

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


# Process the MXS files and send them off to be rendered
def mrt_processMXS(mxsNumber, mxsFilePath, samplingLevel, camera, dependencies, threads, priority, timelimit, script, renderPass, resolution, extraCommandLineOptions):
  # Find out the current scene file
  dirName = os.path.dirname(mxsFilePath)
  mxsName = os.path.basename(mxsFilePath)
  mxsNameNoExt = os.path.splitext(mxsName)[0]
  mxsPathNoExt = os.path.splitext(mxsFilePath)[0]
  
  mxs = CmaxwellMxi()
  
  # Check the operating system
  mrtPlatform = mrt_getPlatform()

  # Load the MXS data into Maxwell
  # Find out the current left view scene settings
  scene = Cmaxwell(mwcallback)
  scene.readMXS(mxsFilePath)
  it = CmaxwellCameraIterator()

  # Camera Details
  #camera = leftIt.first(scene)
  cam = scene.getActiveCamera()
  camName = cam.getName()

  # Check the scene's render resolution
  res = cam.getResolution()
  mxsWidth = res[0]
  mxsHeight = res[1]

  # Read the scene's SL sampling level and round it to 3 decimal places
  
  # MXS Scene Render Option Values
  mxsTimelimit = scene.getRenderParameter('STOP TIME')[0] / 60
  mxsSamplingLevel = round(scene.getRenderParameter('SAMPLING LEVEL')[0], 3)
  
  print( '[MXS Scene] ' + mxsName + ' [Image Dimensions] ' + str(mxsWidth) + 'x' + str(mxsHeight) + ' px' + ' [Time Limit] ' + str(mxsTimelimit) + ' [SL] ' + str(mxsSamplingLevel))
  
  customOverrideString = '[Custom Overrides] '
  
  # Prepare the command line rendering string
  # ------------------------------------------
  
  maxwellTool = ''
  tee = ''
  if mrtPlatform == 'Windows':
    maxwellTool = 'C:\Program Files\Next Limit\Maxwell 3\Maxwell.exe'
    filenameNativePath = mrt_getMaxwellRenderToolboxBaseFolder() + 'tools' + os.sep
    tee = filenameNativePath +'wintee' + os.sep + 'bin' + os.sep + 'wtee.exe'
  elif mrtPlatform == 'Mac':
    maxwellTool = '/Applications/Maxwell 3/Maxwell.app/Contents/MacOS/Maxwell'
    filenameNativePath = mrt_getMaxwellRenderToolboxBaseFolder() + 'mac_tools' + os.sep 
    tee = 'tee'
  else:
    # Linux - Maxwell needs to be located in the system environment $PATH variable
    filenameNativePath = os.sep + 'usr' + os.sep + 'bin' + os.sep
    maxwellTool = 'Maxwell'
    tee = 'tee'
  
  command  = '"' + maxwellTool + '"' 
  command += ' -mxs:"' + mxsFilePath + '"' 
  
  # Maxwell CPU priority mode - either 'low' or 'normal'
  if priority == 'low' or priority == 'normal':
    command += ' -priority:' + priority
  else:
    # Fallback to low if an invalid state is chosen
    command += ' -priority:' + 'low'
  
  customOverrideString += ' [Priority] ' + str(priority)
  
  # Try to resume an existing .mxi file for progressive rendering
  command += ' -trytoresume'
  customOverrideString += ' [Try to Resume] ' + 'Yes'
  
  # Allow the user to define a custom SL level if the setting is set to something other than samplingLevel == ''
  if samplingLevel == '':
    # No SL Override
    customOverrideString += ' '
  else:
    command += ' -sl:' + str(samplingLevel)
    customOverrideString += ' [SL] ' + str(samplingLevel)
    
    
  # Custom camera view override
  if not camera == '':
    command += ' -camera:"' + camera + '"'
    customOverrideString += ' [Camera] ' + camera
    
  # Add any extra scene dependencies
  if not dependencies == '':
    command += ' -dependencies:"' + dependencies + '"'
    customOverrideString += ' [Dependencies] ' + dependencies
  
  # Render threads
  if not threads == '':
    command += ' -threads:' + str(threads)
    customOverrideString += ' [Threads] ' + str(threads)
    
  # Time Limit
  if not timelimit == '':
    command += ' -time:' + str(timelimit)
    customOverrideString += ' [Time Limit] ' + str(timelimit)
    
  # Maxwell Render Script
  if not script == '':
    command += ' -script:"' + script + '"' 
    customOverrideString += ' [Script] ' + script
  
  # Render Passes
  if not renderPass == '':
    command += ' -pass:' + str(renderPass)
    customOverrideString += ' [Render Pass] ' + str(renderPass)
  
  # Resolution
  if not resolution == '':
    command += ' -res:' + str(resolution)
    customOverrideString += ' [Resolution] ' + str(resolution)
    
  # Exit Maxwell automatically when a rendering finishes
  # command +=  ' -nowait'
  
  # Hide the Maxwell GUI and run a new rendering using the console mode
  # command +=  ' -nogui'

  # Add any extra command line options here
  command += ' ' + str(extraCommandLineOptions) + ' '

  # Extra Options
  # -display
  # -o:/var/folders/bw/lwzlw2bx5jx1z514r88mq5980000gp/T/maxwellstudiotmp/default.png
  
  # List a summary of the custom render overrides
  print(customOverrideString)
  
  # Redirect the output from the terminal to a log file
  outputLog = mrt_tempImagesDirectory() + 'maxwellRenderOutputLog.txt'
  
  # Customize the output log command for each platform
  command += ' ' + '2>&1 | "' + tee + '" -a ' + '"' + outputLog + '"'
  
  # Result: /var/folders/2g/_q1ztb9j0vq8yslt46x7hh_h0000gn/T/MaxwellRenderToolbox/maxwellRenderOutputLog.txt 
  
  result = ''
  print('[Launching Maxwell Render] ' + command + '\n')
  if mrtPlatform == 'Windows':
    result = os.system('"' + command + '"')
  else:
    result = os.system(command)
  #args = shlex.split(command)
  #print (args)
  #result = subprocess.Popen(args, shell=True)
  
  # Wait for this task to finish
  #result.wait()

  # Add a newline between each time the mrt_processMXS() function is run on a directory of MXS files
  print('\n')
  
  return 1


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
  print('Maxwell MXS 2 Render v' + mrt_version + ' on ' + mrt_getPlatform())
  print('By Andrew Hazelden <andrew@andrewhazelden.com>')
  print('http://www.andrewhazelden.com/blog')
  print('-----------------------------------------------\n')

  # MXS scene file extension
  mxsFileExt = 'mxs'
  
  # Sampling level
  # ---------------
  # Choose a sampling level override for each the MXS renderings. Leave this variable empty to use the default sampling level that is present in each of the .mxs files.
  
  samplingLevel = ''
  # samplingLevel = '6'  # Super Rough Draft Quality
  # samplingLevel = '8'  # Rough Draft Quality
  # samplingLevel = '10' # Draft Quality
  # samplingLevel = '16' # Medium Quality
  # samplingLevel = '18' # Fine Quality
  # samplingLevel = '24' # Extra Fine Quality

  
  # Time Limit
  # -----------
  # Choose a maximum render time limit (in minutes) per frame for the rendering.  Leave this variable empty to use the default time limit that is present in each of the .mxs files.
  
  timelimit = ''
  # timelimit = '1'    # 1 minute
  # timelimit = '5'    # 5 minutes
  # timelimit = '10'   # 10 minutes
  # timelimit = '30'   # 30 minutes
  # timelimit = '60'   # 1 hour
  # timelimit = '120'  # 2 hours
  # timelimit = '240'  # 4 hours
  # timelimit = '360'  # 6 hours
  # timelimit = '720'  # 12 hours
  # timelimit = '1440' # 24 hours
  
  # Camera Override
  # -----------------
  # Choose a custom camera view to use when rendering the MXS files. Leave this variable empty to use the active camera in each of the scenes
  
  camera = ''
  # camera = 'Camera'
  
  
  # Scene Dependencies
  # -------------------
  # Provide an extra folder reference for MXS scene dependencies like textures or scene references. Leave this variable empty to skip using it.
  
  dependencies = ''
  
  # Render Pass
  # -----------
  # Choose the specific render passes to generate using a value from 0-5. Leave this variable empty to skip using it.
  
  renderPass = ''
  # renderPass = '0' # Render All Layers
  # renderPass = '1' # Render Diffuse Layer
  # renderPass = '2' # Render Reflections Layer
  # renderPass = '3' # Render Refractions Layer 
  # renderPass = '4' # Render Diffuse and Reflections Layer
  # renderPass = '5' # Render Reflections and Refractions Layer
  
  
  # Render Threads
  # --------------
  # Choose how many threads will be used for the rendering. Leave this variable empty to use the current setting in the mxs scene files. Setting threads = '0' will use all available treads on the system. 
  
  threads = ''
  # threads = '0'
  # threads = '8'
  # threads = '16'
  # threads = '32'
  # threads = '64'
  
  # CPU Priority
  # -------------
  # Choose how intensely you want Maxwell to run on the CPU. Setting the priority to 'low' will allow you to still use the computer productively in the background. Setting the priority to 'normal' will got a lot of the CPU and might make the computer less responsive.
  
  # priority = ''
  priority = 'low'
  # priority = 'normal'
  
  
  # Render Resolution
  # -----------------
  # Choose a render time resolution override by specifying the width and height value like  Width x Height (1920x1080). Leave this variable empty to skip using it.
  
  resolution = ''
  # resolution = "320x240"
  # resolution = "640x480"
  # resolution = "1280x720"
  # resolution = "1920x1080"
  # resolution = "2048x1024"
  # resolution = "3840x2160"
  # resolution = "4096x2048"
  
  # Maxwell Render Script
  # ---------------------
  # Run a script when a Maxwell Render job completes.  Leave this variable empty to skip using it.
  
  script = ''
  
  # Extra Command Line Options
  # ---------------------------
  # Add any extra command line options here with a space between each flag. 
  # This section is typically used to add things like the -nowait command that tells Maxwell to quit when a rendering finishes, or -nogui to run a rendering job without showing the Maxwell Render GUI.
  
  # extraCommandLineOptions = ' '
  extraCommandLineOptions = ' -nowait '
  # extraCommandLineOptions = ' -nogui -nowait '
  
  # ------------------------------------------
  # Process a single Maxwell MXS File
  # ------------------------------------------
  # mxsFilePath = '/Applications/MaxwellRenderToolbox/examples/stereo/CubeX.mxs'
  # mxsFilePath = 'C:/Program Files/MaxwellRenderToolbox/examples/stereo/CubeX.mxs'
  # mxsFilePath = '/opt/MaxwellRenderToolbox/examples/stereo/CubeX.mxs'

  # ---------------------------------------------------
  # Or process a whole directory of Maxwell MXS files
  # ---------------------------------------------------
  # mxsFilePath = '/Applications/MaxwellRenderToolbox/examples/stereo/'
  mxsFilePath = 'C:/Program Files/MaxwellRenderToolbox/examples/stereo/'
  # mxsFilePath = '/opt/MaxwellRenderToolbox/examples/stereo/'


  # Check if we are going to process 1 MXS file or a whole directory of MXS files
  if os.path.isfile(mxsFilePath):
    # Launch the MXS single file processing command
    mxsNumber = 1
    print('[Entering MXS Single File Processing Mode]\n')

    # Load the MXS Image data into Maxwell
    print('[MXS File #' + str(mxsNumber) + '] ' + mxsFilePath)
    ok = mrt_processMXS(mxsNumber, mxsFilePath, samplingLevel, camera, dependencies, threads, priority, timelimit, script, renderPass, resolution, extraCommandLineOptions)

    if ok == 1:
      # Open the MaxwellRenderToolbox temporary images folder window up using your desktop file browser
      #mrt_openTempImagesDirectory()
          
      # Open a folder window up using your desktop file browser
      mrt_openDirectory(mxsFilePath)
  elif os.path.isdir(mxsFilePath):
    print('[Entering MXS Directory Processing Mode]')
    
    # Build a list of MXS files in the current directory
    print('[Base Directory] ' + os.path.dirname(mxsFilePath) + '\n')
    mxsFileList = getFilesFromPath(mxsFilePath, mxsFileExt)
    mxsNumber=0

    # Iterate through each of the active MXS files is the current directory
    for file in mxsFileList:
      mxsNumber += 1
      mxsFileDirPath = mxsFilePath + file
      print('[MXS File #' + str(mxsNumber) + '] ' + mxsFileDirPath)
      # Load the MXS Image data into Maxwell
      ok = mrt_processMXS(mxsNumber, mxsFileDirPath, samplingLevel, camera, dependencies, threads, priority, timelimit, script, renderPass, resolution, extraCommandLineOptions)

      if ok == 1 and mxsNumber == 1:
        # Open the MaxwellRenderToolbox temporary images folder window up using your desktop file browser
        #mrt_openTempImagesDirectory()
        
        # Open a folder window up using your desktop file browser
        mrt_openDirectory(mxsFileDirPath)
  else:
    print('[MXS File Not Found] ' + mxsFilePath)
    
  print('\n-------------------------------------------------------------')
  print('MXS 2 Render Job Complete')

