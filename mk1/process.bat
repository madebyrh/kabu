@echo off
 
for %%f in (%1\*) do (
    REM echo %%~nxf
    echo %%f
    move %%f .\price_data\
    python mcad_2.py
    timeout /t 5 > nul
    python sell_2.py
    timeout /t 5 > nul
    python buy.py
    timeout /t 5 > nul
    python ma.py
    timeout /t 10 > nul
    python reserve.py
    timeout /t 5 > nul
)

pause

