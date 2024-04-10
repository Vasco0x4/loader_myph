#!/bin/bash

# Step 1: Download the repository
echo "Downloading myph from GitHub..."
git clone https://github.com/matro7sh/myph

cd myph

# Step 2: Compilation
# Check if 'make' is installed and use it if available; otherwise, use 'go build'.
if command -v make &> /dev/null
then
    echo "Compiling myph with make..."
    make
else
    echo "Compiling myph with go build..."
    go build -o myph .
fi

# Step 3: Moving the Executable
echo "Moving the myph executable to /usr/local/bin..."
sudo mv myph /usr/local/bin/myph

# Step 4: Verification in $PATH
if command -v myph &> /dev/null
then
    echo "[+] The myph loader has been successfully installed."
else
    echo "Error: myph could not be installed correctly."
fi
