Frequently Asked Questions

This page contains questions I'm frequently asked about wintee.

1. How do I use wintee?

    I have tried to maintain the interface in the GNU version of tee within wintee for consistency and familiarity. 

    Wintee will take any input from standard input and copy the data to standard out and any files specified on the command line. The most common way for people to use wintee will be to pipe the output of some command into wintee using the "|" operator on the command line. 

    For example: 

    echo Hello world | wintee output1.txt output2.txt 

    would save the text Hello world into files named output1.txt and output2.txt and would also display the text Hello world on the standard output device (most likely the console). This is in fact the way in which I always use wintee as it allows me to see the output of the command being executed and saves a copy of the output for later review. 

    There are a couple of command parameters that wintee accepts: 

Parameter 	Purpose
a 	append to the given file(s), do not overwrite
i 	ignore interrupt signals
? 	display the help screen and exit
--version 	output version information and exit
--help 	display the help screen and exit

    By default wintee will replace any file specified as a command parameter. To avoid losing any previous contents of the output file(s) use the -a parameter to force wintee to append the output to the end of the files. Currently the append setting is global to all of the files specified, but I can see where a person would want to overwrite one file but append to a different file such as a networked syslog file. 

    Specifying the -i command parameter causes wintee to ignore all interrupt signal with the exception of the kill signals which cannot be ignored. This is useful if you have multiple console windows running and you want to avoid accidentally causing a problem by pressing

    <ctrl>

    -c. 

    The remaining command parameters should be self explanatory. 

2. Why did you write wintee?

    For the past number of years, I've been developing exclusively in Linux for embedded devices. During this time, I became very dependent on the tee command for aiding the debugging of applications, shell scripts and make files. Since I've come to work for Point2 Technologies, all of my development work has been on the Windows platform. As anyone who has ever used the Windows command console for executing command scripts can attest to, the screen buffer can easily be filled prior to the end of a script's execution. Unless a person is redirecting output to a file or other stream, any important messages in the beginning of the script's execution can be lost and can lead to some very difficult to debug issues. The GNU tee application solves this problem by copying standard input messages to both standard output and an arbitrary number of other streams. Unfortunately Windows does not ship with a tee type command, so I decided that I could write one in a very short time. The end result is wintee. 

3. What platforms can I use wintee on?

    I have only run wintee under the command console for Windows XP Home and Professional, but it should run under any 32 bit version of Windows. I haven't tried running wintee on a 64 bit version of Windows, but I'd like to hear from anyone who does so I can update this wiki page with the results. 

    I used Borland C++ 5.02 to develop wintee as a console application. That being said, I haven't tried wintee on a true DOS platform, so again, if anyone wants to see if the application will run under a true DOS distribution, I'd like to hear what your results are so I can update this wiki page with the results. 

4. I've found a bug, how do I report it?

    If you find a bug in this application, please report it on the issues page for this project. The issue page can be found here.
    http://code.google.com/p/wintee/issues/list

5. I'd really like to have more features/functionality. How do I request that these be added to wintee?

    If there is a feature you feel that wintee is missing, please report it using the issues page for the wintee project. The issue page can be found here. 
    http://code.google.com/p/wintee/issues/list