#!/bin/bash

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Define a custom TLD for your local development (e.g., .test)
CUSTOM_TLD=".dev.io"

# Check if Homebrew is installed and install it if not
if ! command -v brew &>/dev/null; then
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
fi

# Stop dnsmasq if it's already running
if brew services list | grep -q "dnsmasq"; then
  sudo brew services stop dnsmasq
fi

# Uninstall mkcert if it's already installed
if brew list | grep -q "mkcert"; then
  brew uninstall mkcert
fi

# Create the 'certs' directory if it doesn't exist
CERTS_DIR="$SCRIPT_DIR/certs"
mkdir -p "$CERTS_DIR"

# Remove existing certificate files if they exist
rm -f "$CERTS_DIR/api$CUSTOM_TLD.crt" "$CERTS_DIR/api$CUSTOM_TLD.key" "$CERTS_DIR/ui$CUSTOM_TLD.crt" "$CERTS_DIR/ui$CUSTOM_TLD.key"

# Install dnsmasq
brew install dnsmasq

# Configure dnsmasq for local domains
echo "address=/$CUSTOM_TLD/127.0.0.1" > /usr/local/etc/dnsmasq.conf

# Start dnsmasq and configure it to start at boot
sudo brew services start dnsmasq

# Install mkcert
brew install mkcert

# Generate SSL certificates for local domains (replace with your domain names)
mkcert -install
mkcert -cert-file "$CERTS_DIR/api$CUSTOM_TLD.crt" -key-file "$CERTS_DIR/api$CUSTOM_TLD.key" "api$CUSTOM_TLD"
mkcert -cert-file "$CERTS_DIR/ui$CUSTOM_TLD.crt" -key-file "$CERTS_DIR/ui$CUSTOM_TLD.key" "ui$CUSTOM_TLD"

# Update /etc/hosts file
echo "127.0.0.1 api$CUSTOM_TLD ui$CUSTOM_TLD" | sudo tee -a /etc/hosts

# Restart dnsmasq to apply changes
sudo brew services restart dnsmasq

# Configure your API server (replace with your server setup)
# Example: Node.js with Express
# Your Express app setup here...

# Configure your UI server (replace with your server setup)
# Example: Nginx
# Your Nginx configuration here...

echo "Local domains api$CUSTOM_TLD and ui$CUSTOM_TLD are set up with SSL certificates."
echo "You can access your API at https://api$CUSTOM_TLD and your UI at https://ui$CUSTOM_TLD."
