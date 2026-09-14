#!/usr/bin/env python3
"""Self-checking RootMC development bootstrap."""
from __future__ import annotations

import hashlib
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / ".runtime"
LOG_DIR = RUNTIME / "logs"
LOG_FILE = LOG_DIR / "boot.log"


def log(message: str) -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    line = f"[RootRecord RootMC] {message}"
    print(line, flush=True)
    with LOG_FILE.open("a", encoding="utf-8") as handle:
        handle.write(line + "\n")


def run(command: list[str]) -> None:
    log("RUN " + " ".join(command))
    subprocess.run(command, cwd=ROOT, check=True)


def fingerprint(*paths: Path) -> str:
    digest = hashlib.sha256()
    for path in paths:
        if path.is_file():
            digest.update(str(path.relative_to(ROOT)).encode())
            digest.update(path.read_bytes())
    return digest.hexdigest()


def ensure_dependencies() -> None:
    for command in ("git",):
        if not shutil.which(command):
            log(f"WARNING missing dependency: {command}")
    package = ROOT / "package.json"
    lock = ROOT / "package-lock.json"
    if package.is_file() and shutil.which("npm"):
        marker = RUNTIME / "node-dependencies.sha256"
        current = fingerprint(package, lock)
        needs_install = not marker.exists() or marker.read_text().strip() != current
        if needs_install:
            run(["npm", "ci" if lock.is_file() else "install"])
            marker.write_text(current, encoding="utf-8")


def main() -> int:
    log("BOOT_START")
    for directory in (RUNTIME, RUNTIME / "data", RUNTIME / "config", RUNTIME / "logs", ROOT / "media"):
        directory.mkdir(parents=True, exist_ok=True)
        log(f"READY {directory.relative_to(ROOT)}")
    ensure_dependencies()
    log("BOOT_COMPLETE")
    log(f"Log file: {LOG_FILE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
