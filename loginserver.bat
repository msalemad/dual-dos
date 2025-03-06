@echo off
echo Starting LoginServer...
:loop
echo LoginServer running...
timeout /t 5 >nul
goto loop
````

### /c:/Users/usuario/Proyectos/dual-dos/gameserver.bat

Create a batch file to simulate the execution of a GameServer with a keep-alive loop.

<file>
````batch
:: filepath: /c:/Users/usuario/Proyectos/dual-dos/gameserver.bat
@echo off
echo Starting GameServer...
:loop
echo GameServer running...
timeout /t 5 >nul
goto loop
