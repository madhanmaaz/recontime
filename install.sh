#!/bin/bash

# Colors for output
RESET="\033[0m"
RED="\033[31m"
GREEN="\033[32m"
CYAN="\033[36m"

# Ensure script is NOT run as root
if [[ $EUID -eq 0 ]]; then
    echo -e "${RED}Please do not run this script as root. Use a non-root user with sudo.${RESET}"
    exit 1
fi

# Platform Check
echo -e "> ${CYAN}Current platform${GREEN}[${RESET}$(uname)${GREEN}]${RESET}"
if [[ "$OSTYPE" == "win32" ]]; then
    echo -e "${RED}::ERR platform error.${RESET}"
    exit 1
fi

# Adding recontime to PATH and creating alias
echo "Configuring recontime command..."
RECONTIME_PATH="$PWD/recontime.py"
if [[ -f "$RECONTIME_PATH" ]]; then
    PROFILE="$HOME/.profile"
    if ! grep -q "alias recontime=" "$PROFILE"; then
        echo -e "\n# Alias for recontime\nalias recontime='python3 $RECONTIME_PATH'" >> "$PROFILE"
        echo "Alias for recontime added to $PROFILE"
    else
        echo "Alias for recontime already exists in $PROFILE"
    fi
    source "$PROFILE"
else
    echo "recontime.py not found at $RECONTIME_PATH. Please run the script at the tool location."
    exit 1
fi

# Function to install Go
installGo() {
    URL="https://go.dev/dl/go1.23.4.linux-amd64.tar.gz"
    TAR_FILE="go1.23.4.linux-amd64.tar.gz"
    INSTALL_PATH="/usr/local"
    GO_PATH="/usr/local/go"
    GO_BIN_PATH="${GO_PATH}/bin"
    PKG_BIN_PATH="$HOME/go/bin"

    echo "Downloading Go..."
    if ! curl "$URL" -L -o "$TAR_FILE"; then
        echo -e "${RED}Error downloading Go. Exiting.${RESET}"
        exit 1
    fi

    if [[ -d "$GO_PATH" ]]; then
        echo "Removing existing Go installation..."
        sudo rm -rf "$GO_PATH"
    fi

    echo "Extracting Go tarball..."
    sudo tar -C "$INSTALL_PATH" -xzf "$TAR_FILE"

    echo "Configuring environment variables..."
    PROFILE="$HOME/.profile"
    if ! grep -q "export PATH=\"${GO_BIN_PATH}:\$PATH\"" "$PROFILE"; then
        echo -e "\n# Go environment setup\nexport PATH=\"${GO_BIN_PATH}:\$PATH\"" >> "$PROFILE"
    fi

    if ! grep -q "export PATH=\"${PKG_BIN_PATH}:\$PATH\"" "$PROFILE"; then
        echo -e "\n# Add local Go binaries\nexport PATH=\"${PKG_BIN_PATH}:\$PATH\"" >> "$PROFILE"
    fi
    source "$PROFILE"

    echo "Verifying Go installation..."
    go version || { echo -e "${RED}Go installation failed.${RESET}"; exit 1; }

    echo "Go installation completed successfully!"
    rm -f "$TAR_FILE"
}

# Dependencies to install
declare -A POST_DEPS=( 
    ["pip3"]="sudo apt install -y python3-pip"
    ["assetfinder"]="sudo apt install -y assetfinder"
    ["subfinder"]="GO111MODULE=on go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest"
    ["hakrawler"]="go install -v github.com/hakluke/hakrawler@latest"
    ["whois"]="sudo apt install -y whois"
    ["httpx"]="GO111MODULE=on go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest"
    ["gau"]="GO111MODULE=on go install github.com/lc/gau/v2/cmd/gau@latest"
)

# Function to check and install dependencies
checkDep() {
    for KEY in "${!POST_DEPS[@]}"; do
        if ! command -v "$KEY" &> /dev/null; then
            echo -e "> ${CYAN}Installing${GREEN}[${RESET}${KEY}${GREEN}]${RESET}"
            eval "${POST_DEPS[$KEY]}"
        else
            echo -e "> ${CYAN}Found${GREEN}[${RESET}${KEY}${GREEN}]${RESET}"
        fi
    done
}

# Main Script Execution
if [[ "$1" == "--force" ]]; then
    installGo
elif ! command -v go &> /dev/null; then
    installGo
fi

if [[ -f requirements.txt ]]; then
    pip3 install -r requirements.txt --break-system-packages
else
    echo -e "${RED}requirements.txt not found. Skipping Python dependency installation.${RESET}"
fi

echo -e "${GREEN}+=== Installation success ===+${RESET}"
