@ECHO OFF

ECHO HELLO! This program will add FFMPEG to your system variables.
ECHO You can manually install FFMPEG. Visit : https://www.ffmpeg.org/download.html

SET /p input=Continue? Y/N.

if %input% == Y setx /m PATH "%~dp0/FFMPEG/;%PATH%" 
if %input% == N ECHO Terminated...

PAUSE