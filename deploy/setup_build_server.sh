#!/bin/bash

# Configuration
VM_NAME="KivyBuildServer_2004"
ISO_PATH="$HOME/Downloads/ubuntu-20.04.6-desktop-amd64.iso" # Adjust if your path is different
VM_USER="unknown"
VM_PASS="password123" # Change this to your preference
PROJECT_DIR="/home/unknown/omnicommander_elite/deploy"

echo "[*] Creating VM: $VM_NAME"
VBoxManage createvm --name "$VM_NAME" --ostype "Ubuntu_64" --register

echo "[*] Configuring Hardware (4GB RAM, 2 CPUs)"
VBoxManage modifyvm "$VM_NAME" --memory 4096 --cpus 2 --vram 128 --graphicscontroller vmsvga --nic1 nat

echo "[*] Creating 30GB Hard Drive"
VBoxManage createmedium disk --filename "$HOME/VirtualBox VMs/$VM_NAME/$VM_NAME.vdi" --size 30720

echo "[*] Setting up Storage Controllers"
VBoxManage storagectl "$VM_NAME" --name "SATA Controller" --add sata --bootable on
VBoxManage storageattach "$VM_NAME" --storagectl "SATA Controller" --port 0 --device 0 --type hdd --medium "$HOME/VirtualBox VMs/$VM_NAME/$VM_NAME.vdi"

echo "[*] Mapping Shared Project Folder"
VBoxManage sharedfolder add "$VM_NAME" --name "deploy" --hostpath "$PROJECT_DIR" --automount

echo "[*] Starting Unattended Installation..."
VBoxManage unattended install "$VM_NAME" \
    --iso="$ISO_PATH" \
    --user="$VM_USER" \
    --password="$VM_PASS" \
    --full-user-name="Build Agent" \
    --install-additions \
    --time-zone="UTC"

echo "[+] Setup Complete. Launching VM now..."
VBoxManage startvm "$VM_NAME"
