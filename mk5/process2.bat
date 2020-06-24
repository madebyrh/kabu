@echo off

setlocal enabledelayedexpansion

set base=C:\Users\ficti\Desktop\stock_analyze\mk5\tmp2_data\japan-all-stock-data_

for %%f in (%1\*) do (
    REM echo %%~nxf
    
    REM echo %%f
    set x=%%f
    move %%f .\price_data\
    move !base!!x:~-12! .\financial_data\
    REM echo !base!!x:~-12!
    python mcad_2.py
    timeout /t 2 > nul
    python sell_2.py
    timeout /t 2 > nul
    python buy.py
    timeout /t 2 > nul
    python ma.py
    timeout /t 5 > nul
    python reserve.py
    timeout /t 2 > nul
)

pause
