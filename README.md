# Miko!! Generative-Voice Assistant

Hello! My name is Miko!! your voice assistant!!
I was created to simplify quick tasks on the PC, now you can use your voice to find out information about the world, or do simple actions on the PC!
My program uses llama3.1 8b to generate answers to difficult questions and search for information

This GitHub project is used for the basis: [RVC-tts-webui](https://github.com/litagin02/rvc-tts-webui)

0.6 test v.
## Install

Requirements: Tested for Python 3.10 and pip 21.3.1 on Windows 11. So please use Python 3.10

Please check Troubleshooting on this page before install and make sure that everything is done
Maybe fairseq needs Microsoft C++ Build Tools.
[Download installer](https://visualstudio.microsoft.com/ja/thank-you-downloading-visual-studio/?sku=BuildTools&rel=16) and install it.

```bash
git clone ####################### GITHUBLINK
cd rvc-tts-webui

# Download models in root directory
curl -L -O https://huggingface.co/lj1995/VoiceConversionWebUI/resolve/main/hubert_base.pt
curl -L -O https://huggingface.co/lj1995/VoiceConversionWebUI/resolve/main/rmvpe.pt

# Make virtual environment
python -m venv env
# Activate venv (for Windows)
env\Scripts\activate

# python -m pip install -U pip==21.3.1

# Install PyTorch manually if you want to use NVIDIA GPU (Windows)
#   But you need to install CUDA before install PyTorch
#   CUDA https://developer.nvidia.com/cuda-12-4-0-download-archive?target_os=Windows&target_arch=x86_64
# See https://pytorch.org/get-started/locally/ for more details
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124

# Install requirements
pip install -r requirements.txt
```

## Locate RVC models

Place your RVC models in `weights/` directory as follows:

```bash
weights
├── model1
│   ├── my_model1.pth
│   └── my_index_file_for_model1.index
└── model2
    ├── my_model2.pth
    └── my_index_file_for_model2.index
```

Each model directory should contain exactly one `.pth` file and at most one `.index` file. Directory names are used as model names.

It seems that non-ASCII characters in path names gave faiss errors (like `weights/モデル1/index.index`), so please avoid them.

## Launch

```bash
# Activate venv (for Windows)
env\Scripts\activate
```

## Usage

By default, the generation of responses and voices is disabled, you can enable it after launching the application.


## Troubleshooting

### Microsoft C++ BuildTools
You need download Microsoft C++ Build Tools from Download installer on Install page if you have this trouble
```
error: Microsoft Visual C++ 14.0 or greater is required. Get it with "Microsoft C++ Build Tools": https://visualstudio.microsoft.com/visual-cpp-build-tools/
      [end of output]

  note: This error originates from a subprocess, and is likely not a problem with pip.
  ERROR: Failed building wheel for fairseq
Failed to build fairseq
ERROR: Could not build wheels for fairseq, which is required to install pyproject.toml-based projects
```

### assist ERROR
You will probably see the inscription when you output it `assist ERROR` it doesn't affect the task execution, so just ignore it. xD
But, if there is anything else after the `ERROR`, then it should not be ignored.

### PyYAML or another trouble in installation process
Most likely you don't have the correct version of python and pip, check it:
```bash
# If env not active
env\Scripts\activate

pip --version
# There should be Python==3.10 and pip==21.3.1

# If your pip version is different, run:

python -m pip install pip==21.3.1
```