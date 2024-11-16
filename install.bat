@echo off

SET path1=hubert_base.pt
SET path2=rmvpe.pt

if EXIST %path1% (
	echo hubert_base.pt - OK
) else (
	call curl -L -O https://huggingface.co/lj1995/VoiceConversionWebUI/resolve/main/hubert_base.pt
	echo hubert_base.pt - OK
)
if EXIST %path2% (
	echo rmvpe.pt - OK
) else (
	call curl -L -O https://huggingface.co/lj1995/VoiceConversionWebUI/resolve/main/rmvpe.pt
	echo rmvpe.pt - OK
)
if EXIST venv\Script\activate.bat (
	echo venv - OK
) else (
	call py -3.10 -m venv venv
	echo venv - OK
)
call venv\Scripts\activate
:test
call pip --version || findstr /I "pip 21.3.1" > nul
if %errorlevel% == 0 (
	echo pip - OK
	goto go
) else (
	call python -m pip install -U pip==21.3.1
	goto test
)
:go

:cudatest
if "%CUDA_VERSION%" == "cpu" (
	echo Skipping torch -> cpu
	goto cudaSkip
)
SET /P cudaCont=Do you want to install CUDA? (y/n):
if %cudaCont% == n (
	goto cudaSkip
)
echo Download Microsoft Build Tools before continue: "https://visualstudio.microsoft.com/ru/thank-you-downloading-visual-studio/?sku=BuildTools&rel=16"
pause
echo Download cuda before continue: "https://developer.nvidia.com/cuda-12-4-0-download-archive?target_os=Windows&target_arch=x86_64&target_version=11"
pause
call pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
echo CUDA loaded.
:cudaSkip
:ollamatest
SET /P ollamaCont=Do you want to install ollama model? (y/n):
if %ollamaCont% == n (
	goto :ollamaSkip
)
echo Download Ollama client before load model: "https://ollama.com/download"
pause
start ollama_installation.bat
echo Ollama installed.
pause
:ollamaSkip
pip install -r requirements.txt
SET /P configUPD=Need config update? / WARN: This action will delete your json data / default=y / (y/n):
if %configUPD% == n (
	goto configSkip
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
:configSkip
SET /P startCont=Start FairyVA? (y/n):
if %startCont% == y (
	start start.bat
	exit
) else (
	echo Success
)
pause
exit