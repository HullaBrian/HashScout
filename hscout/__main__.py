import argparse
import csv
import hashlib
import os
import subprocess
from zipfile import ZipFile

import py7zr


def _get_hash(file: str, algorithm: str) -> str:
    """Calculates the hash of a given file."""
    hasher = hashlib.new(algorithm)
    with open(file, "rb") as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()


def _unzip(path: str, password: str = "") -> str:
    """Unzips a given zip file into the same directory as the zip file. Returns the path of the unzipped directory"""
    uncompressed_path: str = "".join(args.input.split(".")[:-1])
    print(f"\nAttempting to unzip {uncompressed_path}...\nTrying to unzip normally...", end="")

    with ZipFile(path, mode="r") as zip_f:
        try:
            zip_f.extractall(path=uncompressed_path, pwd=password.encode("utf-8"))
            print("SUCCESS!\n")
            return uncompressed_path
        except RuntimeError:
            print("FAILED\nTrying py7zr library...", end="")

    try:
        with py7zr.SevenZipFile(path, "r", password=password) as archive:
            archive.extractall(uncompressed_path)
        print("SUCCESS!\n")
        return uncompressed_path
    except py7zr.exceptions.Bad7zFile:
        print("FAILED\nTrying system 7zip binary...", end="")

    # .\7z.exe e D:\dev\HashScout\testing\Brutus.zip -phacktheblue -oD:\dev\HashScout\testing\Brutus\
    sz_path: str = os.path.join("C:", "Program Files", "7-Zip", "7z.exe")
    try:
        subprocess.call(
            [sz_path, "e", path, f"-p{password}", f"-o{uncompressed_path}", "-aos"],  # skip existing files
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        print("SUCCESS!\n")
    except subprocess.CalledProcessError:
        print("FAILED\nNO OTHER ALTERNATIVES EXIST - EXITING...")
        return ""

    return uncompressed_path


parser = argparse.ArgumentParser(
    prog="HashScout",
    description="A tool to get hashes of all files in a directory or .zip",
    epilog="Project repository: https://github.com/HullaBrian/HashScout",
)
parser.add_argument(
    "input",
    help="input zip file or directory",
)
parser.add_argument(
    "-a",
    "--algorithm",
    help="hashing algorithm to use [SHA256|MD5]",
    required=False,
    default="SHA256",
)
parser.add_argument(
    "-p",
    "--password",
    help="password to use for unlocking a zip",
    required=False,
    default=""
)
args = parser.parse_args()

hashes: list[tuple[str, str]] = []  # Map file name to hash value
if os.path.isfile(args.input):  # Check if it's a .zip
    print(f"{args.input} is a file. Extracting...")
    hashes.append((args.input, _get_hash(args.input, args.algorithm)))
    directory = _unzip(args.input, args.password)
else:  # It's a directory
    print(f"{args.input} is a directory...")
    directory = args.input

print("Traversing directory...")
for root, dirs, files in os.walk(directory):  # Traverse directory structure
    for file in files:
        file_path = str(os.path.join(root, file))
        file_hash = _get_hash(file_path, args.algorithm)
        print(f"Found {file_path}")
        hashes.append((file_path, file_hash,))

print("\nCollected hashes:")
output_path: str = os.path.join(os.sep.join(directory.split(os.sep)[:-1]), "output.csv")
with open(output_path, "w", newline="") as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=["File Path", "Hash"])
    csv_writer.writeheader()

    for file_path, hash in hashes:
        print(f"{file_path}: {hash}")
        csv_writer.writerow({"File Path": file_path, "Hash": hash})
