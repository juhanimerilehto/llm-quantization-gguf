
"""
test_model.py
Windows-specific script to test the quantized Qwen model with improved prompting.
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

def format_prompt(prompt):
    """Format prompt to encourage direct responses."""
    return f"""<|im_start|>user
{prompt}<|im_end|>
<|im_start|>assistant
Let me write that story for you directly:

"""

def test_model(model_path, prompt, max_tokens=2048):
    """
    Test the model with a given prompt.
    """
    try:
        # Path to cli executable
        cli_exe = Path("llama.cpp") / "build" / "bin" / "llama-cli.exe"
        
        if not cli_exe.exists():
            raise FileNotFoundError(f"CLI executable not found at: {cli_exe}")
            
        formatted_prompt = format_prompt(prompt)
            
        # Build the command
        command = [
            str(cli_exe),
            "-m", model_path,
            "-ngl", "35",          # Use GPU for 35 layers
            "-c", "4096",          # Increased context window
            "-n", str(max_tokens), # Max tokens to generate
            "-t", "8",             # Thread count
            "--temp", "0.7",       # Temperature
            "--top-p", "0.9",      # Top-p sampling
            "--prompt", formatted_prompt
        ]
        
        print(f"{Fore.CYAN}Running inference...{Fore.RESET}")
        print(f"{Fore.YELLOW}Prompt: {prompt}{Fore.RESET}\n")
        
        # Run inference
        process = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        
        if process.returncode == 0:
            print(f"{Fore.GREEN}Model output:{Fore.RESET}")
            print(process.stdout)
        else:
            print(f"{Fore.RED}Error during inference:{Fore.RESET}")
            print(process.stderr)
            
    except Exception as e:
        print(f"{Fore.RED}Error: {str(e)}{Fore.RESET}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Test quantized GGUF model")
    parser.add_argument("--model", type=str, 
                       default="./models/qwen-7b-q4_k_m.gguf",
                       help="Path to quantized model")
    parser.add_argument("--prompt", type=str,
                       default="Write a short story about a programmer who discovers an AI.",
                       help="Prompt for the model")
    parser.add_argument("--max-tokens", type=int,
                       default=2048,
                       help="Maximum number of tokens to generate")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.model):
        print(f"{Fore.RED}Error: Model file not found at {args.model}{Fore.RESET}")
        sys.exit(1)
    
    test_model(args.model, args.prompt, args.max_tokens)

if __name__ == "__main__":
    main()