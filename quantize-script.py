#!/usr/bin/env python3
"""
quantize_model.py
Windows-specific script to quantize GGUF model to Q4_K_M format.
"""

import os
import sys
import logging
import subprocess
import argparse
from colorama import init, Fore
from pathlib import Path
import time

# Initialize colorama
init()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('quantization.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

def quantize_model(input_model, output_model):
    """
    Quantize the model to Q4_K_M format.
    
    Args:
        input_model (str): Path to input GGUF model
        output_model (str): Path for output quantized model
    """
    try:
        print(f"{Fore.CYAN}Starting quantization to Q4_K_M format...{Fore.RESET}")
        start_time = time.time()
        
        # Path to llama-quantize executable
        quantize_exe = Path("llama.cpp") / "build" / "bin" / "llama-quantize.exe"
        
        if not quantize_exe.exists():
            raise FileNotFoundError(f"Quantize executable not found at: {quantize_exe}")
            
        # Build the quantization command
        command = [
            str(quantize_exe),
            input_model,
            output_model,
            "q4_k_m"
        ]
        
        print(f"{Fore.YELLOW}Running command: {' '.join(command)}{Fore.RESET}")
        
        # Run quantization with full error capture
        process = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        
        # Print both stdout and stderr
        if process.stdout:
            print(process.stdout)
        
        if process.stderr:
            print(f"{Fore.RED}{process.stderr}{Fore.RESET}")
        
        process.check_returncode()
        
        # Calculate time taken and file size
        time_taken = time.time() - start_time
        if os.path.exists(output_model):
            file_size = os.path.getsize(output_model) / (1024 * 1024 * 1024)  # Size in GB
            print(f"{Fore.GREEN}Quantization completed successfully!{Fore.RESET}")
            print(f"Time taken: {time_taken:.2f} seconds")
            print(f"Output size: {file_size:.2f} GB")
            logging.info(f"Model quantized to: {output_model}")
            logging.info(f"Time: {time_taken:.2f}s, Size: {file_size:.2f}GB")
        else:
            raise FileNotFoundError(f"Output file {output_model} not found")
            
    except subprocess.CalledProcessError as e:
        print(f"{Fore.RED}Quantization command failed with return code {e.returncode}{Fore.RESET}")
        if e.stdout:
            print("STDOUT:")
            print(e.stdout)
        if e.stderr:
            print("STDERR:")
            print(e.stderr)
        logging.error(f"Quantization failed: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"{Fore.RED}Error during quantization: {str(e)}{Fore.RESET}")
        logging.error(f"Quantization failed: {str(e)}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Quantize GGUF model to Q4_K_M")
    parser.add_argument("--input_model", type=str, 
                       default="./models/qwen-7b-f16.gguf",
                       help="Input GGUF model path")
    parser.add_argument("--output_model", type=str, 
                       default="./models/qwen-7b-q4_k_m.gguf",
                       help="Output quantized model path")
    
    args = parser.parse_args()
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(args.output_model), exist_ok=True)
    
    print(f"{Fore.YELLOW}Starting quantization process...{Fore.RESET}")
    print(f"Input size: {os.path.getsize(args.input_model) / (1024 * 1024 * 1024):.2f} GB")
    quantize_model(args.input_model, args.output_model)

if __name__ == "__main__":
    main()