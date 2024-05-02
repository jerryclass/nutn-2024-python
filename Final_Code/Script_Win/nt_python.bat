@echo off

set IMAGE_NAME=nutn-my-python
set SCRIPT_DIR=%~dp0%

docker images | findstr /c:"nutn-my-python" > nul

if not %errorlevel% == 0 (
    docker build -t %IMAGE_NAME% %SCRIPT_DIR%\..\Docker\Python
)

set execute_file=%1
IF NOT EXIST "%execute_file%" (
    echo Error: %execute_file% does not exist or is not a regular file.
    exit /b 1
)

docker run -it --rm -v "%cd%:/app" %IMAGE_NAME% python /app/%execute_file%