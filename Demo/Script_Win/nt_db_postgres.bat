@echo off
setlocal

set IMAGE_NAME=nutn-my-postgres
set SCRIPT_DIR=%~dp0%

set command=%1

docker images | findstr /c:"%IMAGE_NAME%" > nul
if %errorlevel% neq 0 (
    echo Docker image %IMAGE_NAME% not found. Building...
    docker build -f %SCRIPT_DIR%\..\Docker\Postgres\Dockerfile -t %IMAGE_NAME% .
)

call :check_container_exists
if errorlevel 1 (
    docker run --name nutn-my-postgres-container -p 5432:5432 -d %IMAGE_NAME%
)


if "%command%"=="start" (
    echo "start postgres services"
    docker start nutn-my-postgres-container
) else (
    if "%command%"=="stop" (
        echo "stop postgres services"
        docker stop nutn-my-postgres-container
    ) else (
        if "%command%"=="init" (
            call %SCRIPT_DIR%\nt_db_postgres.bat stop
            docker rm nutn-my-postgres-container
            docker rmi nutn-my-postgres
            call %SCRIPT_DIR%\nt_db_postgres.bat start
        ) else (
            echo "command not found"
        )
    )
)

:end
endlocal

:check_container_exists
for /f "tokens=*" %%a in ('docker ps -a --format "{{.Names}}"') do (
    if "%%a"=="nutn-my-postgres-container" (
        exit /b 0
    )
)
exit /b 1