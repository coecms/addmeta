netcdf test-2049 {
dimensions:
        x = 15 ;
        y = 10 ;
        Times = 4;
variables:
        double Times(Times) ;
                Times:standard_name = "time" ;
                Times:units = "days since 2040-01-01 12:00:00" ;
                Times:calendar = "standard" ;
        float temp(Times, y, x) ;
                temp:units = "degC" ;
                temp:_FillValue = 1.e+20f ;
                temp:missing_value = 1.e+20f ;
                temp:long_name = "Temperature" ;

// global attributes:
                :unlikelytobeoverwritten = "total rubbish" ;
                :Publisher = "Will be overwritten" ;
}
 
