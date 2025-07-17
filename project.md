### Project Setup Instructions
Since you specified wireless mode only and already have UV installed, we'll proceed with that. Remember, for wireless ADB:
- Ensure ADB Platform-Tools is installed and in your PATH (download from https://developer.android.com/tools/releases/platform-tools if not).
- On your Pixel 4a 5G, enable Wireless Debugging (as in your reference: Developer Options > Wireless debugging > Pair device with pairing code).
- Manually pair once: Run `adb pair <IP>:<port>` in your terminal and enter the pairing code from your phone.
- Then connect: `adb connect <IP>:<port>`. This starts the ADB server and enables wireless access. You only need to pair once per session or if the code changes; connect can be repeated.
- The script will use the provided `--host` (e.g., `<IP>:<port>`) to connect if not already connected.

We'll use the `adbutils` library (more actively maintained as of 2025, supports Python 3.8+, including 3.10.2, and handles wireless connections via `adb.connect(host:port)`).

Run these commands in your terminal to set up the project:

1. Create and navigate to the project directory:
   ```
   mkdir adb_file_transfer
   cd adb_file_transfer
   ```

2. Initialize the project with UV, pinning Python 3.10.2 (UV will download and install this version if not already on your system):
   ```
   uv init --python 3.10.2
   ```
   This creates `pyproject.toml`, a virtual environment (`.venv`), and a basic package structure under `src/adb_file_transfer/`.

3. Add the dependency:
   ```
   uv add adbutils
   ```
   This installs `adbutils` into the project's environment and updates `pyproject.toml` and the lockfile.

4. Create the main script file: Inside the project directory, create `src/adb_file_transfer/transfer.py` (or use your editor to make it) and paste the following code into it:

```python
import argparse

from adbutils import adb as adb_client

def main():
    parser = argparse.ArgumentParser(description="Easy ADB file transfer over wireless.")
    parser.add_argument("--action", choices=["push", "pull"], required=True,
                        help="Action: 'push' (computer to phone) or 'pull' (phone to computer)")
    parser.add_argument("--local", required=True,
                        help="Local file path on computer (for push: source; for pull: destination)")
    parser.add_argument("--remote", required=True,
                        help="Remote file path on phone (e.g., /storage/emulated/0/Pictures/myfile.jpg)")
    parser.add_argument("--host", required=True,
                        help="Device host:port (e.g., 192.168.1.100:5555)")

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

    if args.action == "push":
        device.push(args.local, args.remote)
        print(f"Pushed {args.local} to {args.remote} on device.")
    elif args.action == "pull":
        device.pull(args.remote, args.local)
        print(f"Pulled {args.remote} from device to {args.local}.")

if __name__ == "__main__":
    main()
```

5. To run the script: Use `uv run` to execute it in the project's environment (no need to activate the venv manually). Examples:
   - Push a file: `uv run python -m adb_file_transfer.transfer --action push --local /path/to/myphoto.jpg --remote /storage/emulated/0/Pictures/Backups/myphoto.jpg --host 192.168.1.100:5555`
   - Pull a file: `uv run python -m adb_file_transfer.transfer --action pull --local /path/to/save/myphoto.jpg --remote /storage/emulated/0/Pictures/Backups/myphoto.jpg --host 192.168.1.100:5555`

   Replace paths and host as needed. Note: This handles single files only. For directories, you'd need recursive logic (we can add that later if desired). Ensure file paths exist and you have permissions on the phone (e.g., no root needed for /storage/emulated/0/ paths).

6. Troubleshooting:
   - If the ADB server isn't running, start it with `adb start-server`.
   - Run `adb devices` to verify your device shows up after connecting.
   - Errors like "device offline"? Re-pair and reconnect.
   - UV sync: If dependencies change, run `uv sync`.

This should give you a working, isolated project for wireless file transfers. Let me know if you run into issues or want enhancements!