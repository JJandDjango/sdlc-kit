@echo off
rem The declared test command: runs every tests\test_*.bat, or the one file
rem named as the first argument. A test file exits 0 when its check holds.
setlocal
if "%~1"=="" goto all
set ONE=%~1
set ONE=%ONE:/=\%
call "%ONE%"
if errorlevel 1 goto onefail
echo PASS %ONE%
exit /b 0
:onefail
echo FAIL %ONE%
exit /b 1
:all
set FAILED=0
set COUNT=0
for %%T in (tests\test_*.bat) do call :run "%%T"
echo %COUNT% tests, %FAILED% failed
if not "%FAILED%"=="0" exit /b 1
exit /b 0
:run
set /a COUNT+=1
call %1
if errorlevel 1 goto runfail
echo PASS %~1
exit /b 0
:runfail
set /a FAILED+=1
echo FAIL %~1
exit /b 0
