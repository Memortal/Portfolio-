#!/usr/bin/env python3
"""Import approved non-AMP media from a Wix catalog into small, locally hosted assets.

This is a PUBLIC repository import. Do not expand importApproved to private files.
No 3rd-party image search or guessed URLs; the manifest holds exact Wix Media API URLs.
"""
import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
import time
import unicodedata
import urllib.error
import urllib.request
from pathlib import Path

from PIL import Image, ImageOps, UnidentifiedImageError

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data/media-manifest.json"
ASSET = ROOT / "assets"
MAX_DOWNLOAD = 350 * 1024 * 1024
MAX_VIDEO_OUTPUT = 38 * 1024 * 1024
MAX_IMAGE_OUTPUT = 12 * 1024 * 1024
Image.MAX_IMAGE_PIXELS = 250_000_000


def slug(value):
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    value = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return value[:55] or "image"


def download(url, dest):
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (compatible; MEMOPortfolio/1.0)",
        "Accept": "*/*",
    })
    with urllib.request.urlopen(req, timeout=100) as response, open(dest, "wb") as fp:
        size = 0
        while True:
            chunk = response.read(1024 * 1024)
            if not chunk:
                break
            fp.write(chunk)
            size += len(chunk)
            if size > MAX_DOWNLOAD:
                raise ValueError("source file exceeds 350 MiB safety threshold")
    return size


def save_image(src, dst):
    with Image.open(src) as source:
        is_animated = bool(getattr(source, "is_animated", False))
        if is_animated:
            source.seek(0)
        im = ImageOps.exif_transpose(source)
        im.thumbnail((2400, 2400), Image.Resampling.LANCZOS)
        if im.mode not in ("RGB", "RGBA"):
            im = im.convert("RGBA" if "A" in im.getbands() else "RGB")
        dst.parent.mkdir(parents=True, exist_ok=True)
        im.save(dst, "WEBP", quality=83, method=5)
        if dst.stat().st_size > MAX_IMAGE_OUTPUT:
            im.thumbnail((1600, 1600), Image.Resampling.LANCZOS)
            im.save(dst, "WEBP", quality=76, method=4)
        return {"width": im.width, "height": im.height,
                "note": "Animated GIF converted to a single preview frame" if is_animated else None}


def save_video(src, dst):
    if not shutil.which("ffmpeg"):
        raise RuntimeError("ffmpeg is not available on this runner")
    dst.parent.mkdir(parents=True, exist_ok=True)
    specs = [
        ("1280:-2:force_original_aspect_ratio=decrease", "32"),
        ("960:-2:force_original_aspect_ratio=decrease", "37"),
        ("720:-2:force_original_aspect_ratio=decrease", "40"),
    ]
    for scale, crf in specs:
        cmd = [
            "ffmpeg", "-hide_banner", "-loglevel", "error", "-nostdin", "-y",
            "-i", str(src), "-map", "0:v:0", "-map", "0:a:0?",
            "-vf", f"scale={scale}", "-c:v", "libx264", "-preset", "veryfast",
            "-crf", crf, "-c:a", "aac", "-b:a", "80k", "-movflags", "+faststart",
            str(dst),
        ]
        run = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             timeout=480)
        if run.returncode != 0:
            raise RuntimeError(run.stderr.decode(errors="replace")[-450:])
        if dst.stat().st_size <= MAX_VIDEO_OUTPUT:
            return
    raise ValueError("video still exceeds 38 MiB after three compression settings")


def main():
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    entries = data["files"]
    done = 0
    errors = 0
    skipped = 0
    for i, item in enumerate(entries, 1):
        if not item.get("importApproved", False):
            item["importStatus"] = "linked-only"
            skipped += 1
            continue
        if item.get("localPath") and (ROOT / item["localPath"]).exists():
            item["importStatus"] = "complete"
            done += 1
            continue
        source = item.get("sourceUrl", "")
        if not source.startswith(("https://static.wixstatic.com/", "https://video.wixstatic.com/")):
            item["importStatus"] = "invalid-source"
            errors += 1
            continue
        media_type = item["mediaType"]
        group = "portfolio"
        safe_name = slug(item["name"])
        ident = hashlib.sha256(source.encode("utf-8")).hexdigest()[:12]
        folder = "videos" if media_type == "VIDEO" else "images"
        suffix = ".mp4" if media_type == "VIDEO" else ".webp"
        output = ASSET / folder / group / f"{safe_name}-{ident}{suffix}"
        relative = output.relative_to(ROOT).as_posix()
        if output.exists():
            item["localPath"] = relative
            item["importStatus"] = "complete"
            done += 1
            continue
        print(f"[{i}/{len(entries)}] {media_type}: {item['name']}", flush=True)
        try:
            with tempfile.TemporaryDirectory(prefix="wixport-") as tmp:
                original = Path(tmp) / "original"
                download(source, original)
                if media_type == "IMAGE":
                    meta = save_image(original, output)
                    item["optimizedWidth"] = meta["width"]
                    item["optimizedHeight"] = meta["height"]
                    if meta["note"]:
                        item["note"] = meta["note"]
                elif media_type == "VIDEO":
                    save_video(original, output)
                else:
                    raise ValueError("Only IMAGE and VIDEO are supported for public import")
            item["localPath"] = relative
            item["importStatus"] = "complete"
            item["optimizedBytes"] = output.stat().st_size
            done += 1
        except Exception as exc:
            item["importStatus"] = "error"
            item["importError"] = str(exc)[:240]
            errors += 1
            try:
                output.unlink(missing_ok=True)
            except Exception:
                pass
            print(f"  Unable to import: {exc}", flush=True)
        # Partial progress survives job cancellation; committing is managed by the workflow.
        if i % 25 == 0:
            MANIFEST.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    data["importSummary"] = {"importedFiles": done, "linkedOnly": skipped,
                             "errors": errors, "lastRun": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    MANIFEST.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"FINISHED: imported={done}, linked-only={skipped}, errors={errors}", flush=True)


if __name__ == "__main__":
    main()
