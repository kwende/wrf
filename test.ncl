begin
	cdf = addfile("/home/brush/Downloads/weather/WRFV3/test/em_real/wrfout_d01_2014-08-12_18:00:00", "r+")
	print(cdf->T)

end
