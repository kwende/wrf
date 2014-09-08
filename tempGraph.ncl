load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/wrf/WRFUserARW.ncl"

a = addfile(netcdfPath,"r")

times = wrf_user_getvar(a,"times",-1)
ntimes = dimsizes(times)

x = new(ntimes,float)
y = new(ntimes,float)

do it = 0,ntimes-1,1
	tc2 = wrf_user_getvar(a,"T2",it)     ; T2 in Kelvin
	tc2 = tc2-273.16                  ; T2 in C
	tf2 = 1.8*tc2+32.

	y(it) = tf2(34,36)
	x(it) = it * 3
end do

wks = gsn_open_wks("png","tempGraph")
plot = gsn_xy(wks,x,y,False)
