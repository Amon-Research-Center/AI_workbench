# Enhanced script that includes attribute camouflage

enhanced_stegovault_script = """
#!/bin/bash

#===============================================================================
# StegoVault - Hide LUKS Encrypted Container in Image (with Camouflage)
# Description: Appends encrypted container to a JPG image and mimics file attributes
#===============================================================================

set -euo pipefail

todo
# READ $IMAGE
# READ $MNT_PT

# Configuration
IMG_SOURCE="$IMAGE"                   # Your base image
VAULT_IMG="$IMG_VLT"                # Resulting image+container file
CONTAINER_SIZE_MB=20                         # Size of the encrypted container
MAPPER_NAME="secure_container"
MOUNT_POINT="$MNT_PT/secure_data"
TEMP_CONTAINER="temp_container.bin"

# Logging function
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $*"
}

# Step 1: Create Encrypted Container
create_vault() {
    log "Creating ${CONTAINER_SIZE_MB}MB LUKS container..."
    dd if=/dev/zero of="$TEMP_CONTAINER" bs=1M count="$CONTAINER_SIZE_MB"
    cryptsetup luksFormat "$TEMP_CONTAINER"
    log "Appending container to image..."
    cp "$IMG_SOURCE" "$VAULT_IMG"
    cat "$TEMP_CONTAINER" >> "$VAULT_IMG"
    rm "$TEMP_CONTAINER"

    # Mimic attributes
    log "Copying file timestamps and permissions from $IMG_SOURCE..."
    touch -r "$IMG_SOURCE" "$VAULT_IMG"
    chmod --reference="$IMG_SOURCE" "$VAULT_IMG"
    chown --reference="$IMG_SOURCE" "$VAULT_IMG"

    # Optional: make immutable
    # sudo chattr +i "$VAULT_IMG"

    log "Vault created and hidden in $VAULT_IMG"
}

# Step 2: Mount Vault
mount_vault() {
    mkdir -p "$MOUNT_POINT"
    log "Opening encrypted container from $VAULT_IMG..."
    sudo cryptsetup open "$VAULT_IMG" "$MAPPER_NAME"
    sudo mount "/dev/mapper/$MAPPER_NAME" "$MOUNT_POINT"
    log "Vault mounted at $MOUNT_POINT"
}

# Step 3: Unmount Vault
unmount_vault() {
    log "Unmounting and closing vault..."
    sudo umount "$MOUNT_POINT"
    sudo cryptsetup close "$MAPPER_NAME"
    log "Vault unmounted and closed."
}

# Help Message
usage() {
    echo "Usage: $0 [create|mount|unmount]"
    exit 1
}

# Command Parser
case "${1:-}" in
    create) create_vault ;;
    mount) mount_vault ;;
    unmount) unmount_vault ;;
    *) usage ;;
esac
"""

# Write the enhanced script to a file
enhanced_script_path = Path("/mnt/data/stegovault_camouflage.sh")
enhanced_script_path.write_text(enhanced_stegovault_script)

enhanced_script_path.name
