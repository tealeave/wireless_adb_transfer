# Wireless ADB File Transfer

Easy wireless file transfer between PC and Android devices using ADB.

## Prerequisites

- **ADB Platform-Tools** installed and in your PATH
  - Download from: https://developer.android.com/tools/releases/platform-tools
- **Android device** with Developer Options enabled
- **UV** package manager installed

## Setup

1. **Enable Wireless Debugging on your Android device:**
   - Go to Settings > Developer Options > Wireless debugging
   - Enable "Wireless debugging"
   - Tap "Pair device with pairing code"

2. **Pair your device (one-time setup):**
   ```bash
   adb pair <IP>:<port>
   ```
   Enter the pairing code shown on your phone.

3. **Connect to your device:**
   ```bash
   adb connect <IP>:<port>
   ```

4. **Verify connection:**
   ```bash
   adb devices
   ```

## Finding Your Phone's IP Address

You'll need your phone's IP address and port for wireless transfers. Here are several ways to find it:

### Method 1: Through Wireless Debugging (Recommended)
1. Go to **Settings > Developer Options > Wireless debugging**
2. Enable "Wireless debugging"
3. Tap **"Pair device with pairing code"**
4. The IP address and port will be displayed (e.g., `192.168.1.100:5555`)

### Method 2: Through WiFi Settings
1. Go to **Settings > WiFi**
2. Tap on your connected network name
3. Look for "IP address" in the network details
4. Use port `5555` (default ADB port)

### Method 3: Using ADB Command (if connected via USB first)
```bash
adb shell ip route | grep wlan
```

**Note:** The IP address shown in the pairing screen is what you'll use for the `--host` parameter.

## Quick Start

Ready to transfer files? Here are the most common commands:

### Transfer All Photos from PC to Phone
```bash
cd /home/tealeave/projects/wireless_adb_transfer
PYTHONPATH=src uv run python -m adb_file_transfer.transfer --action push --local /path/to/your/photos/ --remote /storage/emulated/0/Pictures/ --host YOUR_IP:5555 --bulk
```

### Transfer All Photos from Phone to PC
```bash
cd /home/tealeave/projects/wireless_adb_transfer
PYTHONPATH=src uv run python -m adb_file_transfer.transfer --action pull --local /path/to/save/photos/ --remote /storage/emulated/0/Pictures/ --host YOUR_IP:5555 --bulk
```

### Transfer Single File
```bash
cd /home/tealeave/projects/wireless_adb_transfer
PYTHONPATH=src uv run python -m adb_file_transfer.transfer --action push --local /path/to/file.jpg --remote /storage/emulated/0/Pictures/file.jpg --host YOUR_IP:5555
```

**Replace `YOUR_IP:5555` with your actual phone's IP address from the previous section.**

## Usage

### Single File Transfer

#### Push a file from PC to phone:
```bash
cd /home/tealeave/projects/wireless_adb_transfer
PYTHONPATH=src uv run python -m adb_file_transfer.transfer --action push --local /path/to/local/file.jpg --remote /storage/emulated/0/Pictures/file.jpg --host 192.168.1.100:5555
```

#### Pull a file from phone to PC:
```bash
cd /home/tealeave/projects/wireless_adb_transfer
PYTHONPATH=src uv run python -m adb_file_transfer.transfer --action pull --local /path/to/save/file.jpg --remote /storage/emulated/0/Pictures/file.jpg --host 192.168.1.100:5555
```

### Bulk Transfer (Multiple Files)

#### Push all JPG files from PC folder to phone folder:
```bash
cd /home/tealeave/projects/wireless_adb_transfer
PYTHONPATH=src uv run python -m adb_file_transfer.transfer --action push --local /path/to/local/photos/ --remote /storage/emulated/0/Pictures/ --host 192.168.1.100:5555 --bulk
```

#### Push all PNG files from PC folder to phone folder:
```bash
cd /home/tealeave/projects/wireless_adb_transfer
PYTHONPATH=src uv run python -m adb_file_transfer.transfer --action push --local /path/to/local/photos/ --remote /storage/emulated/0/Pictures/ --host 192.168.1.100:5555 --bulk --pattern "*.png"
```

#### Push all documents (PDF, DOC, TXT) to phone:
```bash
cd /home/tealeave/projects/wireless_adb_transfer
PYTHONPATH=src uv run python -m adb_file_transfer.transfer --action push --local /path/to/documents/ --remote /storage/emulated/0/Documents/ --host 192.168.1.100:5555 --bulk --pattern "*.{pdf,doc,docx,txt}"
```

#### Pull all JPG files from phone folder to PC:
```bash
cd /home/tealeave/projects/wireless_adb_transfer
PYTHONPATH=src uv run python -m adb_file_transfer.transfer --action pull --local /path/to/save/photos/ --remote /storage/emulated/0/Pictures/ --host 192.168.1.100:5555 --bulk
```

**Expected Output Example:**
```
Found 15 files to transfer...
[1/15] Pushed photo001.jpg to /storage/emulated/0/Pictures/photo001.jpg
[2/15] Pushed photo002.jpg to /storage/emulated/0/Pictures/photo002.jpg
[3/15] Pushed photo003.jpg to /storage/emulated/0/Pictures/photo003.jpg
...
[15/15] Pushed photo015.jpg to /storage/emulated/0/Pictures/photo015.jpg

Transfer complete: 15/15 files successfully pushed.
```

### Parameters:
- `--action`: Either "push" (PC to phone) or "pull" (phone to PC)
- `--local`: Local file/folder path on your computer
- `--remote`: Remote file/folder path on your phone (e.g., /storage/emulated/0/Pictures/)
- `--host`: Device host:port (e.g., 192.168.1.100:5555)
- `--bulk`: Enable bulk transfer mode for multiple files
- `--pattern`: File pattern for bulk mode (default: "*.jpg")

## Advanced Usage

### Complex Pattern Matching

#### Transfer multiple image formats:
```bash
PYTHONPATH=src uv run python -m adb_file_transfer.transfer --action push --local /photos/ --remote /storage/emulated/0/Pictures/ --host 192.168.1.100:5555 --bulk --pattern "*.{jpg,jpeg,png,gif,bmp}"
```

#### Transfer files with specific naming patterns:
```bash
# Transfer all files starting with "IMG_"
--pattern "IMG_*"

# Transfer all files containing "vacation"
--pattern "*vacation*"

# Transfer all files ending with specific numbers
--pattern "*_2024.*"
```

### Common Use Cases

#### Backup all photos from Camera to PC:
```bash
cd /home/tealeave/projects/wireless_adb_transfer
PYTHONPATH=src uv run python -m adb_file_transfer.transfer --action pull --local ~/phone_backup/photos/ --remote /storage/emulated/0/DCIM/Camera/ --host 192.168.1.100:5555 --bulk --pattern "*.{jpg,jpeg}"
```

#### Transfer screenshots to PC:
```bash
cd /home/tealeave/projects/wireless_adb_transfer
PYTHONPATH=src uv run python -m adb_file_transfer.transfer --action pull --local ~/phone_backup/screenshots/ --remote /storage/emulated/0/Pictures/Screenshots/ --host 192.168.1.100:5555 --bulk
```

#### Batch upload documents to phone:
```bash
cd /home/tealeave/projects/wireless_adb_transfer
PYTHONPATH=src uv run python -m adb_file_transfer.transfer --action push --local ~/Documents/work/ --remote /storage/emulated/0/Documents/work/ --host 192.168.1.100:5555 --bulk --pattern "*.{pdf,docx,xlsx}"
```

### Performance Tips

- **Large transfers**: For 100+ files, transfers happen one at a time with progress updates
- **Network speed**: Transfer speed depends on your WiFi connection quality
- **File size**: Larger files take longer; the tool shows individual file progress
- **Error handling**: Failed individual files don't stop the entire transfer

## Common Android Paths

- Pictures: `/storage/emulated/0/Pictures/`
- Downloads: `/storage/emulated/0/Download/`
- Documents: `/storage/emulated/0/Documents/`
- DCIM (Camera): `/storage/emulated/0/DCIM/`

## Troubleshooting

### General Issues
- **Device offline**: Re-pair and reconnect using the steps above
- **ADB server not running**: Run `adb start-server`
- **Connection issues**: Ensure both devices are on the same network
- **Permission denied**: Make sure wireless debugging is enabled and paired correctly

### Module Import Issues
- **"No module named 'adb_file_transfer'"**: 
  - Always run from the project directory: `cd /home/tealeave/projects/wireless_adb_transfer`
  - Always include `PYTHONPATH=src` before the command
  - Full command: `PYTHONPATH=src uv run python -m adb_file_transfer.transfer ...`

### Bulk Transfer Issues
- **No files found**: Check that the source folder contains files matching your pattern
- **Path errors**: Ensure folder paths exist and end with `/` for remote Android paths
- **Partial transfers**: Some files may fail individually; check the summary for success count
- **Remote folder listing**: For pull operations, ensure the remote folder is accessible
- **Timeout errors**: Large bulk transfers may take time; this is normal for 50+ files

### Performance Issues
- **Slow transfers**: 
  - Check WiFi signal strength on both devices
  - Close other network-intensive apps
  - Transfer during off-peak network hours
- **Large file transfers**: 
  - Consider splitting very large batches into smaller chunks
  - Monitor available storage space on target device
- **Connection drops**: 
  - Keep devices close to WiFi router
  - Disable WiFi sleep mode on Android device
  - Re-run the same command to resume from where it left off

### Common Error Messages
- **"device not found"**: Device not connected to ADB - re-pair and connect
- **"permission denied"**: Check file permissions and Android folder access
- **"no space left"**: Target device storage is full
- **"connection refused"**: Wrong IP address or port number
