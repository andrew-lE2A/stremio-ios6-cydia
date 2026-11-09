#!/usr/bin/env python3
"""Generate a simple static Cydia APT repository from the newest .deb in debs/."""
import gzip
import hashlib
import io
import os
import re
import sys
import tarfile

ROOT = os.path.dirname(os.path.abspath(__file__))
DEBS = os.path.join(ROOT, "debs")


def read_control_from_deb(path):
    data = open(path, "rb").read()
    if not data.startswith(b"!<arch>\n"):
        raise ValueError("not a Debian ar archive: " + path)
    cursor = 8
    while cursor + 60 <= len(data):
        header = data[cursor:cursor + 60]
        name = header[:16].decode("ascii").strip().rstrip("/")
        size = int(header[48:58].decode("ascii").strip())
        body = data[cursor + 60:cursor + 60 + size]
        cursor += 60 + size + (size & 1)
        if name.startswith("control.tar"):
            mode = "r:gz" if name.endswith(".gz") else "r:xz" if name.endswith(".xz") else "r:"
            with tarfile.open(fileobj=io.BytesIO(body), mode=mode) as archive:
                for member in archive.getmembers():
                    if member.name.lstrip("./") == "control":
                        return archive.extractfile(member).read().decode("utf-8")
    raise ValueError("deb has no control archive")


def parse_control(text):
    fields = {}
    key = None
    for line in text.splitlines():
        if line.startswith((" ", "\t")) and key:
            fields[key] += "\n" + line
        elif ":" in line:
            key, value = line.split(":", 1)
            fields[key] = value.strip()
    return fields


def main():
    debs = sorted(name for name in os.listdir(DEBS) if name.endswith(".deb"))
    if not debs:
        sys.exit("Put a .deb in CydiaRepo/debs/ first")
    # Keep just the newest package in the published index; older files may remain archived locally.
    candidates = []
    for name in debs:
        fields = parse_control(read_control_from_deb(os.path.join(DEBS, name)))
        candidates.append((tuple(int(part) if part.isdigit() else part for part in re.split(r"([0-9]+)", fields.get("Version", "0"))), name, fields))
    _, name, fields = max(candidates, key=lambda row: row[0])
    deb_path = os.path.join(DEBS, name)
    blob = open(deb_path, "rb").read()
    fields.update({
        "Filename": "debs/" + name,
        "Size": str(len(blob)),
        "MD5sum": hashlib.md5(blob).hexdigest(),
        "SHA256": hashlib.sha256(blob).hexdigest(),
    })
    index = "".join("%s: %s\n" % (key, value) for key, value in fields.items()) + "\n"
    open(os.path.join(ROOT, "Packages"), "wb").write(index.encode("utf-8"))
    with open(os.path.join(ROOT, "Packages.gz"), "wb") as output:
        with gzip.GzipFile(fileobj=output, mode="wb", mtime=0) as compressed:
            compressed.write(index.encode("utf-8"))
    release = """Origin: Stremio iOS 6
Label: Stremio iOS 6
Suite: stable
Version: 1.0
Codename: ios6
Architectures: iphoneos-arm
Components: main
Description: Stremio iOS 6 jailbreak packages
"""
    open(os.path.join(ROOT, "Release"), "w", encoding="utf-8").write(release)
    print("Indexed %s version %s (%s bytes)" % (fields.get("Package"), fields.get("Version"), len(blob)))


if __name__ == "__main__":
    main()
