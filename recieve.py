import argparse
import os
import socket
from pathlib import Path


def is_allowed_filename(filename: str) -> bool:
    lower_name = filename.lower()
    return lower_name.endswith(".mp4") or lower_name.endswith(".txt")


def main() -> None:
    parser = argparse.ArgumentParser(description="UDP file receiver for .mp4 and .txt files")
    parser.add_argument(
        "--output",
        default="downloads",
        help="Directory where received files will be saved",
    )
    args = parser.parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", 12345))
    print("Listening for UDP packets on port 12345...")
    print(f"Saving allowed files to: {output_dir.resolve()}")

    while True:
        data, addr = sock.recvfrom(65535)
        separator_index = data.find(b"\n")
        if separator_index == -1:
            print(f"Invalid packet from {addr}: missing filename header")
            continue

        header_line = data[:separator_index].decode("utf-8", errors="replace").strip()
        payload = data[separator_index + 1 :]

        if not header_line.startswith("FILENAME:"):
            print(f"Invalid header from {addr}: {header_line}")
            continue

        filename = os.path.basename(header_line.split("FILENAME:", 1)[1].strip())
        if not filename:
            print(f"Empty filename from {addr}")
            continue

        if not is_allowed_filename(filename):
            print(f"Ignoring unsupported file type: {filename}")
            continue

        target_path = output_dir / filename
        try:
            with target_path.open("ab") as f:
                f.write(payload)
            print(f"Received {len(payload)} bytes for {filename} from {addr}")
        except OSError as exc:
            print(f"Failed to save {filename}: {exc}")


if __name__ == "__main__":
    main()
