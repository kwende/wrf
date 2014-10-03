import urllib2
import urllib
import re
import shutil
import os
import sys
import subprocess

def replace_wrfNamelist(namelistContent, key, value):
	startIndex = namelistContent.index(key)
	endIndex = namelistContent.index(',', startIndex)
	return namelistContent.replace(namelistContent[startIndex:endIndex], key + ' = ' + value)

def find_second_last(text, pattern):
	return text.rfind(pattern, 0, text.rfind(pattern))

oDirName = '/home/brush/Downloads/weather/DATA'
baseUrl = 'http://www.ftp.ncep.noaa.gov/data/nccf/com/gfs/prod/'
wpsDir = '/home/brush/Downloads/weather/WPS'
wrfDir = '/home/brush/Downloads/weather/WRFV3/test/em_real'
namelistWRFPath = '/home/brush/Downloads/weather/WPS/namelist.wps'
namelistInputPath = '/home/brush/Downloads/weather/WRFV3/test/em_real/namelist.input'
emRealDir = '/home/brush/Downloads/weather/WRFV3/test/em_real/'
ncargRoot = '/usr/local'
nclFilePath = '/home/brush/Downloads/weather/code/wrf_Precip3.ncl'
tempNclFilePath = '/home/brush/Downloads/weather/code/tempGraph.ncl'
nclTempFilePath = '/home/brush/Downloads/weather/code/wrf_Surface1.ncl'

os.environ["NCARG_ROOT"] = ncargRoot

os.chdir(emRealDir)

wrfFiles = os.listdir(wrfDir)
wrfFileForProcessing = ''
for wrfFile in wrfFiles:
	if wrfFile.startswith('wrfout'):
		wrfFileForProcessing = wrfFile

#subprocess.call(['/usr/local/bin/ncl',nclFilePath,'netcdfFile=\"' + wrfFileForProcessing + '"'])
subprocess.call(['/usr/local/bin/ncl',nclTempFilePath,'netcdfFile=\"' + wrfFileForProcessing + '"'])
#subprocess.call(['/usr/local/bin/ncl',tempNclFilePath,'netcdfFile=\"' + wrfFileForProcessing + '"'])
#ffmpeg -r 4 -i plt_Precip.000%03d.png -c:v libx264 -r 30 -pix_fmt yuv420p out.mp4
#subprocess.call(['/usr/local/bin/ffmpeg', '-r', '4', '-i', 'plt_Precip3.000%03d.png', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', 'out.mp4'])
subprocess.call(['/usr/local/bin/ffmpeg', '-r', '4', '-i', 'plt_Surface1.000%03d.png', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', 'temp.mp4'])
