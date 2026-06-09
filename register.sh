#!/bin/bash

# Define the output file name
OUTPUT_FILE="generated_config.json"

# Generate cryptographically secure random hex values using openssl
# 4 bytes = 8 hex characters
SENDER_ID=$(openssl rand -hex 4)
RECIPIENT_ID=$(openssl rand -hex 4)

# 32 bytes = 64 hex characters (Standard length for AES-256 / OSCORE Master Secret)
SECRET_KEY=$(openssl rand -hex 32)

# Write the beautifully formatted JSON to the file
cat << EOF > "$OUTPUT_FILE"
{
  "sender-id_hex": "$SENDER_ID",
  "recipient-id_hex": "$RECIPIENT_ID",
  "secret_hex": "$SECRET_KEY"
}
EOF

# Provide feedback to the user
echo "Unique OSCORE configuration JSON generated successfully!"
echo "Saved to: $(pwd)/$OUTPUT_FILE"
echo "------------------------------------------------------------"
cat "$OUTPUT_FILE"
echo "------------------------------------------------------------"

