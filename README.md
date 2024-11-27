# Qwen2.5-7B-Instruct Quantization Tool

**Version 1.0**
### Creator: Juhani Merilehto - @juhanimerilehto - Jyväskylä University of Applied Sciences (JAMK), Likes institute

![JAMK Likes Logo](./assets/likes_str_logo.png)

## Overview

A comprehensive Windows-optimized tool for downloading, converting, and quantizing the Qwen2.5-7B-Instruct model to GGUF format. This project provides a structured approach to model quantization with separate scripts for each phase of the process, specifically designed for Windows environments.

## Features

- **Phased Approach**: Separate scripts for download, conversion, quantization, and inference testing
- **Progress Tracking**: Detailed progress bars and status updates
- **Error Handling**: Robust error handling and validation at each step
- **Flexible Quantization**: Support for multiple quantization formats (Q4_K_M, Q4_K_S, Q4_0)
- **Resource Management**: Optimized for consumer hardware (tested on RTX 4070 12GB)
- **Windows Support**: Full Windows compatibility with proper path handling
- **Inference Testing**: Built-in testing capabilities with the quantized model

## Hardware Requirements

- **GPU:** NVIDIA GPU with at least 12GB VRAM (tested on RTX 4070)
- **RAM:** 32GB recommended
- **Storage:** 50GB free space for model files and intermediate formats
- **CUDA:** CUDA 11.7 or higher
- **OS:** Windows 10/11 with Visual Studio 2022 Build Tools

## Project Structure

```plaintext
llm-quantization-gguf/
├── assets/
│   └── likes_str_logo.png
├── llama.cpp/           # llama.cpp repository and builds
├── models/             # Model storage directory
├── build.ps1           # Build script for llama.cpp
├── convert-script.py   # GGUF conversion script
├── download-script.py  # Model download script
├── quantize-script.py  # Quantization script
├── test-model.py      # Inference testing script
├── requirements.txt
└── README.md
```

## Installation

### 1. Clone the repository:
```powershell
git clone [your-repo-url]
cd llm-quantization-gguf
```

### 2. Create a virtual environment:
```powershell
python -m venv llm-env
.\llm-env\Scripts\activate
```

### 3. Install dependencies:
```powershell
pip install -r requirements.txt
```

### 4. Install required tools:
```powershell
# Install Visual Studio 2022 Build Tools with C++ support
winget install Microsoft.VisualStudio.2022.BuildTools --override "--add Microsoft.VisualStudio.Workload.VCTools --includeRecommended"

# Install CMake
winget install Kitware.CMake

# Install NVIDIA CUDA Toolkit
winget install Nvidia.CUDA

# Alternative manual installation:
# 1. Visit: https://developer.nvidia.com/cuda-downloads
# 2. Select: Windows > x86_64 > 11.7 or higher
# 3. Select your preferred installer type (network or local)
# 4. Follow the installation wizard
# 5. Restart your computer after installation

# Verify CUDA installation
nvcc --version

```

## Usage

### 1. Build llama.cpp:
```powershell
.\build.ps1
```

### 2. Download the model:
```powershell
python download-script.py
```

### 3. Convert to GGUF:
```powershell
python convert-script.py
```

### 4. Quantize:
```powershell
python quantize-script.py
```

### 5. Test the model:
```powershell
python test-model.py --prompt "Write a creative story about an AI."
```

## Supported Quantization Formats

- Q4_K_M: High quality, ~4.4GB (recommended)
- Q4_K_S: Balanced quality and size, ~3.8GB
- Q4_0: Smallest size, ~3.5GB

## Actual Processing Times (RTX 4070)

- Download: ~10-15 minutes (internet speed dependent)
- Conversion to GGUF: ~10 minutes
- Quantization (Q4_K_M): ~3 minutes
- Model Sizes:
  - Original F16: 14.19 GB
  - Q4_K_M: 4.36 GB

## Performance Notes

- GPU Utilization: Uses 35 layers on GPU for optimal performance
- Context Window: 4096 tokens supported
- Thread Count: Automatically optimized for your CPU
- Temperature: 0.7 default for balanced creativity
- Top-p: 0.9 for diverse but focused responses

## Credits

- **Juhani Merilehto (@juhanimerilehto)** – Specialist, Data and Statistics
- **JAMK Likes** – Organization sponsor

## License

This project is licensed for free use under the condition that proper credit is given to Juhani Merilehto (@juhanimerilehto) and JAMK Likes institute.
