
"""
convert_to_gguf.py
Windows-specific version for Qwen2.5-7B-Instruct model conversion to GGUF format.
"""

import os
import sys
import logging
import subprocess
import argparse
from colorama import init, Fore
from pathlib import Path

# Initialize colorama
init()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('conversion.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

def convert_to_gguf(input_dir, output_file):
    """
    Convert the model to GGUF format using Windows paths.
    
    Args:
        input_dir (str): Path to the input model directory
        output_file (str): Path for the output GGUF file
    """
    try:
        print(f"{Fore.CYAN}Starting conversion to GGUF format...{Fore.RESET}")
        
        # Ensure paths are Windows-compatible
        llamacpp_path = Path("llama.cpp")
        convert_script = llamacpp_path / "convert_hf_to_gguf.py"
        
        if not convert_script.exists():
            raise FileNotFoundError(f"Convert script not found at: {convert_script}")
            
        # Build the conversion command
        command = [
            sys.executable,
            str(convert_script),
            "./models",  # Changed to models directory where the files are
            "--outfile",
            output_file,
            "--outtype",
            "f16"
        ]
        
        print(f"{Fore.YELLOW}Running command: {' '.join(command)}{Fore.RESET}")
        
        # Run conversion with full error capture
        process = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        
        # Print both stdout and stderr
        if process.stdout:
            print("STDOUT:")
            print(process.stdout)
        
        if process.stderr:
            print(f"{Fore.RED}STDERR:{Fore.RESET}")
            print(process.stderr)
        
        process.check_returncode()  # This will raise CalledProcessError if return code is non-zero
        
        print(f"{Fore.GREEN}Conversion completed successfully!{Fore.RESET}")
        logging.info(f"Model converted to: {output_file}")
        
        # Verify the output file
        if not os.path.exists(output_file):
            raise FileNotFoundError(f"Output file {output_file} not found")
        
        file_size = os.path.getsize(output_file) / (1024 * 1024 * 1024)  # Size in GB
        print(f"{Fore.CYAN}Output file size: {file_size:.2f} GB{Fore.RESET}")
        
    except subprocess.CalledProcessError as e:
        print(f"{Fore.RED}Conversion command failed with return code {e.returncode}{Fore.RESET}")
        if e.stdout:
            print("STDOUT:")
            print(e.stdout)
        if e.stderr:
            print("STDERR:")
            print(e.stderr)
        logging.error(f"Conversion failed: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"{Fore.RED}Error during conversion: {str(e)}{Fore.RESET}")
        logging.error(f"Conversion failed: {str(e)}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Convert model to GGUF format")
    parser.add_argument("--input_dir", type=str, default="./models",  # Changed to models directory
                        help="Input model directory")
    parser.add_argument("--output_file", type=str, default="./models/qwen-7b-f16.gguf",
                        help="Output GGUF file path")
    
    args = parser.parse_args()
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(args.output_file), exist_ok=True)
    
    print(f"{Fore.YELLOW}Starting GGUF conversion process...{Fore.RESET}")
    convert_to_gguf(args.input_dir, args.output_file)

if __name__ == "__main__":
    main()