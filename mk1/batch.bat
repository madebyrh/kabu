@echo off
setlocal enabledelayedexpansion
for %%f in (%1\*) do (
    REM echo %%~nxf
    echo %%f
    set x=%%f

    echo !x:~-12!
)
