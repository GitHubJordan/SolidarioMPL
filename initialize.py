import os
import platform
import subprocess

def main():
    # Detect the operating system
    system = platform.system()
    print(f"Detected OS: {system}")

    # Determine the correct script to run based on the OS
    if system == "Windows":
        command = "initialize.bat"
    else:
        command = "./initialize.sh"

    # Run the initialization script
    subprocess.run(command, shell=True)

if __name__ == "__main__":
    main()
