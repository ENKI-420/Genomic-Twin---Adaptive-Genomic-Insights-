#!/usr/bin/env python3

import os
import sys
import re
import shutil

def fix_escape_sequence():
    """Fix the invalid escape sequence in the Powerline config file."""
    file_path = "/usr/lib/python3/dist-packages/powerline/bindings/config.py"
    
    # Check if file exists
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} not found.")
        return False
    
    # Create a backup
    backup_path = file_path + ".bak"
    shutil.copy2(file_path, backup_path)
    print(f"Created backup at {backup_path}")
    
    # Read the file
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    # Find the line with the invalid escape sequence
    pattern = re.compile(r"TMUX_VAR_RE = re\.compile\('\\\\\\$\(_POWERLINE_\\\\w\+\)'\)")
    found = False
    
    for i, line in enumerate(lines):
        if pattern.search(line):
            # Replace the line with the proper raw string notation
            lines[i] = line.replace("re.compile('\\$", "re.compile(r'\\$")
            found = True
            print(f"Fixed line {i+1}: {line.strip()} -> {lines[i].strip()}")
    
    if not found:
        # Alternative approach - if regex fails, look for line 179
        if len(lines) >= 179:
            line_num = 178  # 0-indexed for 179th line
            if "TMUX_VAR_RE" in lines[line_num] and "\\$" in lines[line_num]:
                lines[line_num] = lines[line_num].replace("re.compile('\\$", "re.compile(r'\\$")
                found = True
                print(f"Fixed line 179: {lines[line_num].strip()}")
    
    if not found:
        print("Could not find the line with the invalid escape sequence.")
        return False
    
    # Write the modified content back to the file
    try:
        with open(file_path, 'w') as f:
            f.writelines(lines)
        print(f"Successfully updated {file_path}")
        return True
    except Exception as e:
        print(f"Error writing to file: {e}")
        print(f"Original file was backed up to {backup_path}")
        return False

if __name__ == "__main__":
    print("Starting fix for invalid escape sequence...")
    
    # Check if running as root
    if os.geteuid() != 0:
        print("This script needs to be run with sudo privileges.")
        print("Please run 'sudo python3 fix_config_simple.py'")
        sys.exit(1)
    
    if fix_escape_sequence():
        print("Fix completed successfully!")
    else:
        print("Failed to apply the fix.")

