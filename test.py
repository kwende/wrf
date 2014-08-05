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
nclFilePath = '/home/brush/Downloads/weather/code/wrf_Precip.ncl'

if len(sys.argv) > 1:
	if os.path.exists(oDirName):
		shutil.rmtree(oDirName)

	os.makedirs(oDirName)
	
	topLevelResponse = urllib2.urlopen(baseUrl, timeout=60).read()

	lastGfsIndex = find_second_last(topLevelResponse, '>gfs.')+1
	endOfLastGfsIndex = topLevelResponse.index('/', lastGfsIndex)
	directoryName = topLevelResponse[lastGfsIndex:endOfLastGfsIndex]

	print directoryName

	fullDirectoryUrl = baseUrl + directoryName + '/'
	dirLevelResponse = urllib2.urlopen(fullDirectoryUrl, timeout=60).read()

	m = re.findall('>gfs\\.t[0-9].z\\.pgrbf[0-9].\\.grib2<', dirLevelResponse)

	for f in range(0, len(m)):
		fileName = m[f][1:len(m[f])-1]
		fullFileUrl = fullDirectoryUrl + fileName
		print 'Downloading ' + fullFileUrl
		urllib.urlretrieve(fullFileUrl, os.path.join(oDirName, fileName))

wpsDirFiles = os.listdir(wpsDir)

for wpsDirFile in wpsDirFiles:
	if wpsDirFile.startswith('FILE:'):
		os.remove(os.path.join(wpsDir,wpsDirFile))
	elif wpsDirFile.startswith('PFILE:'):
		os.remove(os.path.join(wpsDir,wpsDirFile))
	elif wpsDirFile.startswith('GRIBFILE'):
		os.remove(os.path.join(wpsDir,wpsDirFile))
	elif wpsDirFile.startswith('met_em'):
		os.remove(os.path.join(wpsDir,wpsDirFile))

wrfFiles = os.listdir(wrfDir)

for wrfFile in wrfFiles:
	if wrfFile.startswith('met_em'):
		os.remove(os.path.join(wrfDir, wrfFile))
	elif wrfFile.startswith('wrfout'):
		os.remove(os.path.join(wrfDir, wrfFile))

grib2Files = os.listdir(oDirName)
firstGribFile = ''
lastGribFile = ''
numberOfGribFiles = len(grib2Files)
firstGribFileNameValue = 'pgrbf00'
lastGribFileNameValue = 'pgrbf' + str((numberOfGribFiles-1)*3)

for grib2File in grib2Files:
	if not grib2File.find(firstGribFileNameValue) == -1:
		firstGribFile = os.path.join(oDirName,grib2File)
	elif not grib2File.find(lastGribFileNameValue) == -1:
		lastGribFile = os.path.join(oDirName,grib2File)

print firstGribFile

output = subprocess.check_output('wgrib2 -start_ft ' + firstGribFile, stderr=subprocess.STDOUT,shell=True)
output = output.split('\n',1)[0]
output = output[output.index('=')+1:]

startInWPSFormat = output[:4] + '-' + output[4:6] + '-' + output[6:8] + '_' + output[8:] + ':00:00'
startInWPSFormat = 'start_date = \'' + startInWPSFormat + '\''
print startInWPSFormat

startYear = int(output[:4])
startMonth = int(output[5:6])
startDay = int(output[7:8])
startHour = int(output[8:])

output = subprocess.check_output('wgrib2 -start_ft ' + lastGribFile, stderr=subprocess.STDOUT,shell=True)
output = output.split('\n',1)[0]
output = output[output.index('=')+1:]

endInWPSFormat = output[:4] + '-' + output[4:6] + '-' + output[6:8] + '_' + output[8:] + ':00:00'
endInWPSFormat = 'end_date = \'' + endInWPSFormat + '\''
print endInWPSFormat 

endYear = int(output[:4])
endMonth = int(output[5:6])
endDay = int(output[7:8])
endHour = int(output[8:])

numberOfFiles = len(grib2Files)

file = open(namelistWRFPath,'r+')
namelistContent = file.read()

startDateIndex = namelistContent.index('start_date')
endStartDateIndex = namelistContent.index(',', startDateIndex)
oldStartDate = namelistContent[startDateIndex:endStartDateIndex]

endDateIndex = namelistContent.index('end_date')
endEndDateIndex = namelistContent.index(',', endDateIndex)
oldEndDate = namelistContent[endDateIndex:endEndDateIndex]

print 'startDateIndex - ' + str(startDateIndex)
print 'endStartDateIndex - ' + str(endStartDateIndex)
print oldStartDate
print oldEndDate

namelistContent = namelistContent.replace(oldStartDate, startInWPSFormat)
namelistContent = namelistContent.replace(oldEndDate, endInWPSFormat)

file.seek(0)
file.write(namelistContent)
file.truncate()
file.close()

file = open(namelistInputPath, 'r+')
namelistInputContent = file.read()
namelistInputContent = replace_wrfNamelist(namelistInputContent, 'start_year', str(startYear))
namelistInputContent = replace_wrfNamelist(namelistInputContent, 'start_month', str(startMonth))
namelistInputContent = replace_wrfNamelist(namelistInputContent, 'start_day', str(startDay))
namelistInputContent = replace_wrfNamelist(namelistInputContent, 'start_hour', str(startHour))
namelistInputContent = replace_wrfNamelist(namelistInputContent, 'end_year', str(endYear))
namelistInputContent = replace_wrfNamelist(namelistInputContent, 'end_month', str(endMonth))
namelistInputContent = replace_wrfNamelist(namelistInputContent, 'end_day', str(endDay))
namelistInputContent = replace_wrfNamelist(namelistInputContent, 'end_hour', str(endHour))

file.seek(0)
file.write(namelistInputContent)
file.truncate()
file.close()

os.chdir(wpsDir)
print os.getcwd()
subprocess.call(['./geogrid.exe'], shell=True)
subprocess.call(['./link_grib.csh ../DATA/'], shell=True)
subprocess.call(['./ungrib.exe'], shell=True)
subprocess.call(['./metgrid.exe'], shell=True)

os.chdir(emRealDir)
files = os.listdir(wpsDir)
for file in files:
	if file.startswith('met_em'):
		os.symlink(os.path.join(wpsDir,file),os.path.join(emRealDir,file))

subprocess.call(['mpirun','-np','1','real.exe'])
subprocess.call(['mpirun','-np','8','wrf.exe'])
os.environ["NCARG_ROOT"] = ncargRoot
#subprocess.call(['ncl','wrfOutPath=' + nclFilePath,'
