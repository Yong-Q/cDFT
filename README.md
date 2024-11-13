###Author
YongQiu :kingqy@foxmail.com

###The part of the code that changes

##Source directory

GPU-accelerated-cDFT-main/src/CPU_Yu_Liu/

##
1.Error regarding conversion of const char* to char*
2.Error in second call of destructor
3.cal ck() function partial pointer memory unfreed error
4.The delete[] or free function does not point to NULL


###
Added Input conversion file from .cif：data_cdftinput.py

###Usage
g++ -std=c++11 -g  {file.cpp} -o my -lfftw3

###cite  
Qiu Y, Chen L, Zhang X, Ping D,
Tian Y, Zhou Z. A universal machine learning framework to
automatically identify high-performance covalent organic
framework membranes for CH4/H2 separation. AIChE J. 2024;
e18575. doi:10.1002/aic.18575
