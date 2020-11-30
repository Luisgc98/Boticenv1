@echo off
REM Configures the machine as bot where this script is executed.
REM Executed steps:
REM 1.- Register the machine as bot
REM 2.- Restart needed processes

setlocal EnableDelayedExpansion

:: declares variables
set defaultLocalPortal=http://localhost:5000

REM this variables are dinamically updated from portal
set providedPortal=__PORTAL__
set userSecret=[__USER_SECRET__]

if -%providedPortal%-==-- (
	echo "No Portal URL provied, using default %defaultLocalPortal%"
	call :configurePortal %defaultLocalPortal%
)else (	
	echo "To update Portal with URL: %providedPortal%"
	call :configurePortal %providedPortal%
)

REM configures or updates the portal configuration
:configurePortal
echo "To update portal URL with %~1"
if not exist "%AUTOMAGICA_PORTAL_URL%" (
	echo "Portal already configured, with value %AUTOMAGICA_PORTAL_URL%, updating the value to %~1"
)else (
	echo "Portal not configured, to configure with value to " %~1
)
setx AUTOMAGICA_PORTAL_URL %~1
set AUTOMAGICA_PORTAL_URL=%~1
REM setx is not available in XP, Windows Vista and above
goto :setupAsBot

REM sets up the machine as bot
:setupAsBot
echo "entering setupAsBot"
if -%userSecret%-==-- (
	echo "No user secret information provided, the process can not continue"
	goto :end
)else (
	
	REM authenticate and register with the portal
	python -m automagica --connect %userSecret%
	
	:: restart python process
	taskkill /F /IM Python & taskkill /F /IM python & start python -m automagica --bot

	goto :end
	
)
endlocal

:end
echo "Configure portal ended"
exit /b