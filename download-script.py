"""
download_model.py
Downloads Qwen2.5-7B-Instruct model from Hugging Face.
"""

import os
import sys
import logging
from huggingface_hub import snapshot_download, hf_hub_download
from tqdm import tqdm
import hashlib
import argparse
from colorama import init, Fore

# Initialize colorama for cross-platform colored output
init()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('download.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

def calculate_checksum(file_path):
    """Calculate SHA256 checksum of a file."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def download_model(output_dir="./models", repo_id="Qwen/Qwen2.5-7B-Instruct"):
    """
    Download the model from Hugging Face.
    
    Args:
        output_dir (str): Directory to save the model
        repo_id (str): Hugging Face repository ID
    """
    try:
        print(f"{Fore.CYAN}Starting download of {repo_id}...{Fore.RESET}")
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Download the model with progress tracking
        print(f"{Fore.YELLOW}This may take a while depending on your internet connection...{Fore.RESET}")
        local_dir = snapshot_download(
            repo_id=repo_id,
            local_dir=output_dir,
            local_dir_use_symlinks=False,
            resume_download=True,
            token=os.getenv("HF_TOKEN")  # In case the model requires authentication
        )
        
        print(f"{Fore.GREEN}Download completed successfully!{Fore.RESET}")
        logging.info(f"Model downloaded to: {local_dir}")
        
        # Verify the download
        print(f"{Fore.CYAN}Verifying downloaded files...{Fore.RESET}")
        config_path = os.path.join(local_dir, "config.json")
        if os.path.exists(config_path):
            checksum = calculate_checksum(config_path)
            logging.info(f"Config file checksum: {checksum}")
            print(f"{Fore.GREEN}Verification completed!{Fore.RESET}")
        else:
            print(f"{Fore.YELLOW}Warning: config.json not found in downloaded files{Fore.RESET}")
        
        return local_dir
        
    except Exception as e:
        print(f"{Fore.RED}Error during download: {str(e)}{Fore.RESET}")
        logging.error(f"Download failed: {str(e)}")
        
        if "401" in str(e):
            print(f"{Fore.YELLOW}This model might require authentication. Try setting the HF_TOKEN environment variable with your Hugging Face token.{Fore.RESET}")
        elif "404" in str(e):
            print(f"{Fore.RED}Model not found. Please check the repository ID.{Fore.RESET}")
        
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Download Qwen2.5-7B-Instruct model")
    parser.add_argument("--output_dir", type=str, default="./models",
                        help="Directory to save the model")
    parser.add_argument("--repo_id", type=str, default="Qwen/Qwen2.5-7B-Instruct",
                        help="Hugging Face repository ID")
    
    args = parser.parse_args()
    
    print(f"{Fore.YELLOW}Starting model download process...{Fore.RESET}")
    model_path = download_model(args.output_dir, args.repo_id)
    print(f"{Fore.GREEN}Model downloaded successfully to: {model_path}{Fore.RESET}")

if __name__ == "__main__":
    main()