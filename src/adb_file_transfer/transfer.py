import argparse
import os
import glob
from pathlib import Path

from adbutils import adb as adb_client

def bulk_push(device, local_folder, remote_folder, pattern):
    """Push multiple files matching pattern from local folder to remote folder."""
    local_path = Path(local_folder)
    
    if not local_path.exists():
        raise FileNotFoundError(f"Local folder not found: {local_folder}")
    
    if not local_path.is_dir():
        raise ValueError(f"Local path must be a directory for bulk operations: {local_folder}")
    
    # Find all files matching the pattern
    files_to_transfer = list(local_path.glob(pattern))
    
    if not files_to_transfer:
        print(f"No files found matching pattern '{pattern}' in {local_folder}")
        return
    
    print(f"Found {len(files_to_transfer)} files to transfer...")
    
    # Ensure remote folder ends with /
    if not remote_folder.endswith('/'):
        remote_folder += '/'
    
    success_count = 0
    for i, file_path in enumerate(files_to_transfer, 1):
        try:
            remote_file_path = remote_folder + file_path.name
            device.push(str(file_path), remote_file_path)
            print(f"[{i}/{len(files_to_transfer)}] Pushed {file_path.name} to {remote_file_path}")
            success_count += 1
        except Exception as e:
            print(f"[{i}/{len(files_to_transfer)}] Failed to push {file_path.name}: {e}")
    
    print(f"\nTransfer complete: {success_count}/{len(files_to_transfer)} files successfully pushed.")

def bulk_pull(device, remote_folder, local_folder, pattern):
    """Pull multiple files matching pattern from remote folder to local folder."""
    local_path = Path(local_folder)
    
    # Create local folder if it doesn't exist
    local_path.mkdir(parents=True, exist_ok=True)
    
    if not local_path.is_dir():
        raise ValueError(f"Local path must be a directory for bulk operations: {local_folder}")
    
    # For pull operations, we need to list files on the device first
    # This is a simplified approach - in practice, you might need more sophisticated remote file listing
    try:
        # Get list of files from device using shell command
        result = device.shell(f"find {remote_folder} -name '{pattern}' -type f")
        remote_files = [f.strip() for f in result.strip().split('\n') if f.strip()]
        
        if not remote_files:
            print(f"No files found matching pattern '{pattern}' in {remote_folder}")
            return
        
        print(f"Found {len(remote_files)} files to transfer...")
        
        success_count = 0
        for i, remote_file in enumerate(remote_files, 1):
            try:
                filename = Path(remote_file).name
                local_file_path = local_path / filename
                device.pull(remote_file, str(local_file_path))
                print(f"[{i}/{len(remote_files)}] Pulled {filename} to {local_file_path}")
                success_count += 1
            except Exception as e:
                print(f"[{i}/{len(remote_files)}] Failed to pull {Path(remote_file).name}: {e}")
        
        print(f"\nTransfer complete: {success_count}/{len(remote_files)} files successfully pulled.")
        
    except Exception as e:
        print(f"Error listing files on device: {e}")
        print("Make sure the remote folder exists and is accessible.")

def main():
    parser = argparse.ArgumentParser(description="Easy ADB file transfer over wireless.")
    parser.add_argument("--action", choices=["push", "pull"], required=True,
                        help="Action: 'push' (computer to phone) or 'pull' (phone to computer)")
    parser.add_argument("--local", required=True,
                        help="Local file/folder path on computer (for push: source; for pull: destination)")
    parser.add_argument("--remote", required=True,
                        help="Remote file/folder path on phone (e.g., /storage/emulated/0/Pictures/)")
    parser.add_argument("--host", required=True,
                        help="Device host:port (e.g., 192.168.1.100:5555)")
    parser.add_argument("--bulk", action="store_true",
                        help="Enable bulk transfer mode for multiple files")
    parser.add_argument("--pattern", default="*.jpg",
                        help="File pattern for bulk mode (default: *.jpg)")

    args = parser.parse_args()

    # Split host into IP and port
    if ':' not in args.host:
        raise ValueError("Host must be in format IP:port (e.g., 192.168.1.100:5555)")

    host, port_str = args.host.split(':')
    port = int(port_str)

    # Connect to ADB server and device (if not already connected)
    adb_client.connect(f"{host}:{port}")

    # Get device handle
    device = adb_client.device(f"{host}:{port}")

    if args.bulk:
        # Bulk transfer mode
        if args.action == "push":
            bulk_push(device, args.local, args.remote, args.pattern)
        elif args.action == "pull":
            bulk_pull(device, args.remote, args.local, args.pattern)
    else:
        # Single file transfer mode
        if args.action == "push":
            device.push(args.local, args.remote)
            print(f"Pushed {args.local} to {args.remote} on device.")
        elif args.action == "pull":
            device.pull(args.remote, args.local)
            print(f"Pulled {args.remote} from device to {args.local}.")

if __name__ == "__main__":
    main()