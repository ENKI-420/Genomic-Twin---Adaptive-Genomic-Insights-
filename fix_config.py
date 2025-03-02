#!/usr/bin/env python3

import re
import sys
import os
import shutil

def fix_config_file():
    file_path = "/usr/lib/python3/dist-packages/powerline/bindings/config.py"
    
    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} does not exist")
        return 1
    
    # Create a backup of the original file
    backup_path = f"{file_path}.bak"
    try:
        shutil.copy2(file_path, backup_path)
        print(f"Created backup at {backup_path}")
    except PermissionError:
        print("Error: Need sudo permissions to create a backup")
        print(f"Try running: sudo python3 {__file__}")
        return 1
    
    # Read the file content
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
    except PermissionError:
        print("Error: Need sudo permissions to read the file")
        print(f"Try running: sudo python3 {__file__}")
        return 1
    
    # Make the replacement on line 179 (index 178)
    if len(lines) < 179:
        print(f"Error: File has fewer than 179 lines")
        return 1
    
    line_index = 178  # 0-based indexing
    original_line = lines[line_index]
    
    # Check if the line contains the pattern we're looking for
    if "TMUX_VAR_RE = re.compile" not in original_line or "\\$(_POWERLINE_\\w+)" not in original_line:
        print(f"Error: Line 179 doesn't match the expected pattern")
        print(f"Found: {original_line.strip()}")
        return 1
    
    # Add 'r' prefix to the regex
    new_line = re.sub(r"re\.compile\('\\\\\\$\(_POWERLINE_\\w\+\)'\)", 
                      r"re.compile(r'\\$(_POWERLINE_\\w+)')", 
                      original_line)
    
    lines[line_index] = new_line
    
    # Write the modified content back to the file
    try:
        with open(file_path, 'w') as f:
            f.writelines(lines)
        print(f"Successfully updated {file_path}")
        print(f"Changed line 179 from: {original_line.strip()}")
        print(f"                    to: {new_line.strip()}")
    except PermissionError:
        print("Error: Need sudo permissions to write to the file")
        print(f"Try running: sudo python3 {__file__}")
        return 1
    
    return 0

if __name__ == "__main__":
    print("Fixing invalid escape sequence in powerline config.py...")
    exit_code = fix_config_file()
    if exit_code == 0:
        print("Fix completed successfully!")
    sys.exit(exit_code)

