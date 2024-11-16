@echo off
call ollama list || findstr /I "GB" > nul
if %errorlevel% == 0 (
	echo Ollama model already installed
	goto skipInstall
)
SET /P model=Enter ollama model what you want download (defaulf = llama3.1:8b) OR if you want default model enter - none:
if %model% == none (
	call ollama run llama3.1:8b
) else (
	echo Press Ctrl+C to stop proccess
	call ollama run %model%
)
call /exit
:skipInstall
exit