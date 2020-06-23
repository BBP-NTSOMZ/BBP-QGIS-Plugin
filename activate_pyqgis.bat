@
@echo OFF
REM Make parent of this script location our current directory,
REM converting UNC path to drive letter if needed
@SET OSGEO4W_ROOT="C:\Program Files\QGIS 3.10"
echo %OSGEO4W_ROOT%\bin\o4w_env.bat

call %OSGEO4W_ROOT%\bin\o4w_env.bat
path %PATH%;%OSGEO4W_ROOT%\bin
path %PATH%;%OSGEO4W_ROOT%\apps\qgis\bin
path %PATH%;%OSGEO4W_ROOT%\apps\grass\grass78\lib
path %PATH%;%OSGEO4W_ROOT%\apps\Qt5\bin
path %PATH%;%OSGEO4W_ROOT%\apps\Python37\Scripts

set PYTHONPATH=%PYTHONPATH%;%OSGEO4W_ROOT%\apps\qgis\python
set PYTHONHOME=%OSGEO4W_ROOT%\apps\Python37

