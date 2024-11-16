@echo off
call git pull
SET /P appl=Do you want to copy configs? (y/n):
if %appl% == n (
	goto skipcopy
)
echo Copy config files..
SET application=configs\default\application.json
SET library=configs\default\library.json
SET llama=configs\default\llama.json
SET settings=configs\default\settings.json
if EXIST configs\application.json (
	ERASE configs\application.json /q
)
if EXIST configs\library.json (
	ERASE configs\library.json /q
)
if EXIST configs\llama.json (
	ERASE configs\llama.json /q
)
if EXIST configs\settings.json (
	ERASE configs\settings.json /q
)
xcopy %application% configs
xcopy %library% configs
xcopy %llama% configs
xcopy %settings% configs
echo Success
:skipcopy
pause