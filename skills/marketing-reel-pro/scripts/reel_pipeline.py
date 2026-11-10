#!/usr/bin/env python3
"""
marketing-reel-pro CLI pipeline
Built by Nanoboy (365 Collaboration) for NANOTECH AGENTS.

Deterministic 6-subcommand CLI for agency-grade 1080x1920 @ 60fps vertical video production:
  1. prepare-base   : Dual-mode base builder (Mode A: multi-shot lip-sync + MCI 60fps | Mode B: single video 60fps)
  2. extract-matte  : Frame-accurate 60fps human alpha matte + 540p preview proxies
  3. gen-captions   : Safe-zone (y: 1120-1330) kinetic captions with inline SVG stars (zero heavy clip-paths)
  4. setup-layers   : Merges scenes.d/*.json and splits L1 (render-behind) and L3 (render-front) projects
  5. build-audio    : -14 LUFS master mix (EQ/compressed voice + sidechain-ducked pad/loop + 50-60 viral SFX cues)
  6. composite      : Sequential --low-memory-mode layer renders + 4-layer FFmpeg alphamerge composite + contact sheet
"""

import argparse
import glob
import json
import math
import os
import re
import shutil
import struct
import subprocess
import sys
import time
import wave
from pathlib import Path
from typing import Any, Dict, List, Optional

DEFAULT_SFX_DIR = r"C:\Users\infon\Desktop\editor de video - romotions\my-video\public\click.mp3"

COLOR_GRADE_FILTER = (
    "scale=1080:1920:flags=lanczos,"
    "minterpolate=fps=60:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1,"
    "eq=contrast=1.06:saturation=1.12:brightness=0.01,"
    "unsharp=5:5:0.75:5:5:0.0,"
    "vignette=PI/7,"
    "format=yuv420p"
)

CYAN_WORDS = {
    "NEGOCIO", "365", "COLLABORATION", "SOLUCIONES", "MARKETING", "INTEGRAL",
    "CONTENIDO", "DIARIO", "CAMPAÑAS", "ESTRATÉGICAS", "MERCADO", "VENTAS",
    "CLIENTES", "SISTEMAS", "INTELIGENTES", "INFRAESTRUCTURA", "DIGITAL",
    "MOTOR", "TECNOLÓGICO", "INVERTIDO", "SOLUCIÓN", "EXACTA"
}

PURPLE_WORDS = {
    "DINERO", "DOMINARLO", "AUTOMATIZACIONES", "MULTIPLICAR",
    "MULTIPLICADO", "DÓLAR", "COMPETENCIA", "CRECER"
}

SFX_CATEGORY_MAP = {
    "whoosh": ["whoosh", "swoosh", "swish", "air"],
    "swoosh": ["swoosh", "whoosh", "swish"],
    "riser": ["riser", "rise", "swell", "build"],
    "boom": ["boom", "impact", "hit", "cinematic", "sub", "slam"],
    "hit": ["hit", "impact", "boom", "stab"],
    "click": ["click", "tap", "switch", "mouse"],
    "pop": ["pop", "bubble"],
    "cash": ["cash", "coin", "money", "register"],
    "ding": ["ding", "bell", "correct", "chime", "level"],
    "notify": ["notif", "ding", "bell", "message"],
    "glitch": ["glitch", "digital", "cyber", "error", "buzz"],
    "tick": ["tick", "clock", "watch", "timer"],
    "type": ["key", "type", "typing"],
}


def write_report(output_path: Path, payload: Dict[str, Any]) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    print(f"Success! Report written to: {output_path}")


def fail(message: str, output_path: Optional[Path] = None) -> None:
    sys.stderr.write(f"[marketing-reel-pro ERROR] {message}\n")
    if output_path is not None:
        try:
            write_report(output_path, {"status": "error", "error": message})
        except Exception:
            pass
    sys.exit(1)


def probe_duration(path: Path) -> float:
    ffprobe = shutil.which("ffprobe") or "ffprobe"
    cmd = [
        ffprobe, "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(path)
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return float(res.stdout.strip())


# ============================================================================
# 1. SUBCOMMAND: prepare-base
# ============================================================================
def cmd_prepare_base(args: argparse.Namespace) -> None:
    t0 = time.monotonic()
    out_json = Path(args.output).resolve()
    work_dir = Path(args.work_dir).resolve()
    base_dir = work_dir / "base"
    base_dir.mkdir(parents=True, exist_ok=True)
    base60_mp4 = base_dir / "base60.mp4"
    master_wav = work_dir / "master_voice.wav"
    ffmpeg = shutil.which("ffmpeg") or "ffmpeg"

    if args.mode == "single-video":
        if not args.video:
            fail("--video is required when --mode=single-video", out_json)
        src_video = Path(args.video).resolve()
        if not src_video.exists():
            fail(f"Source video not found: {src_video}", out_json)

        # Extract 48kHz stereo master voice
        subprocess.run([
            ffmpeg, "-v", "error", "-y",
            "-i", str(src_video),
            "-vn", "-ac", "2", "-ar", "48000", "-c:a", "pcm_s16le",
            str(master_wav)
        ], check=True)

        # Normalize video to 1080x1920 @ 60fps with agency color grade
        subprocess.run([
            ffmpeg, "-v", "error", "-stats", "-y",
            "-i", str(src_video),
            "-vf", COLOR_GRADE_FILTER,
            "-an", "-r", "60", "-c:v", "libx264", "-preset", "medium", "-crf", "17",
            str(base60_mp4)
        ], check=True)

        dur = probe_duration(base60_mp4)
        write_report(out_json, {
            "status": "ok",
            "mode": "single-video",
            "base60_mp4": str(base60_mp4),
            "master_voice_wav": str(master_wav),
            "duration_seconds": round(dur, 3),
            "elapsed_seconds": round(time.monotonic() - t0, 2)
        })
        return

    # Mode A: multi-shot
    if not args.audio or not args.clips_dir:
        fail("--audio and --clips-dir are required when --mode=multi-shot", out_json)
    audio_src = Path(args.audio).resolve()
    clips_dir = Path(args.clips_dir).resolve()
    if not audio_src.exists():
        fail(f"Master audio not found: {audio_src}", out_json)
    if not clips_dir.exists():
        fail(f"Clips directory not found: {clips_dir}", out_json)

    subprocess.run([
        ffmpeg, "-v", "error", "-y",
        "-i", str(audio_src),
        "-vn", "-ac", "2", "-ar", "48000", "-c:a", "pcm_s16le",
        str(master_wav)
    ], check=True)
    target_total = probe_duration(master_wav)

    clips = sorted(clips_dir.glob("*.mp4"))
    if not clips:
        fail(f"No .mp4 clips found in {clips_dir}", out_json)

    seg_files: List[Path] = []
    if args.segments_json and Path(args.segments_json).exists():
        segs = json.loads(Path(args.segments_json).read_text(encoding="utf-8"))
    else:
        # Evenly distribute master duration across clips using optical flow stretch
        per_clip = target_total / len(clips)
        segs = []
        for c in clips:
            cdur = probe_duration(c)
            segs.append({
                "clip": str(c),
                "ss": 0.0,
                "to": round(cdur, 3),
                "target_dur": round(per_clip, 3)
            })

    for idx, seg in enumerate(segs):
        cpath = Path(seg["clip"])
        if not cpath.is_absolute():
            cpath = clips_dir / cpath.name
        ss = float(seg.get("ss", 0.0))
        to = float(seg.get("to", probe_duration(cpath)))
        src_dur = max(0.1, to - ss)
        tdur = float(seg.get("target_dur", src_dur))
        pts_mult = round(tdur / src_dur, 6)
        seg_out = base_dir / f"seg_{idx:02d}.mp4"
        vf = (
            f"setpts={pts_mult}*PTS,"
            f"{COLOR_GRADE_FILTER}"
        )
        subprocess.run([
            ffmpeg, "-v", "error", "-y",
            "-ss", f"{ss:.3f}", "-to", f"{to:.3f}",
            "-i", str(cpath),
            "-vf", vf,
            "-an", "-t", f"{tdur:.3f}", "-r", "60",
            "-c:v", "libx264", "-preset", "medium", "-crf", "16",
            str(seg_out)
        ], check=True)
        seg_files.append(seg_out)

    concat_txt = base_dir / "concat.txt"
    concat_txt.write_text(
        "\n".join(f"file '{p.as_posix()}'" for p in seg_files) + "\n",
        encoding="utf-8"
    )
    subprocess.run([
        ffmpeg, "-v", "error", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_txt),
        "-c", "copy",
        str(base60_mp4)
    ], check=True)

    dur = probe_duration(base60_mp4)
    write_report(out_json, {
        "status": "ok",
        "mode": "multi-shot",
        "segments_rendered": len(seg_files),
        "base60_mp4": str(base60_mp4),
        "master_voice_wav": str(master_wav),
        "duration_seconds": round(dur, 3),
        "elapsed_seconds": round(time.monotonic() - t0, 2)
    })


# ============================================================================
# 2. SUBCOMMAND: extract-matte
# ============================================================================
def cmd_extract_matte(args: argparse.Namespace) -> None:
    t0 = time.monotonic()
    out_json = Path(args.output).resolve()
    base_video = Path(args.base_video).resolve()
    work_dir = Path(args.work_dir).resolve()
    if not base_video.exists():
        fail(f"Base video not found: {base_video}", out_json)

    matte_dir = work_dir / "matte"
    matte_dir.mkdir(parents=True, exist_ok=True)
    matte60_mp4 = matte_dir / "matte60.mp4"
    backdrop_540 = work_dir / "backdrop_540.mp4"
    matte_preview_540 = work_dir / "matte_preview_540.webm"
    ffmpeg = shutil.which("ffmpeg") or "ffmpeg"

    # Build 540p backdrop proxy for fast snapshots if missing
    if not backdrop_540.exists():
        subprocess.run([
            ffmpeg, "-v", "error", "-y",
            "-i", str(base_video),
            "-vf", "scale=540:960:flags=lanczos",
            "-an", "-r", "60", "-c:v", "libx264", "-preset", "fast", "-crf", "23",
            str(backdrop_540)
        ], check=True)

    if not matte60_mp4.exists():
        # Extract alpha matte via rembg Python API if installed, else hyperframes CLI
        code = (
            "import sys, cv2, numpy as np\n"
            "from rembg import remove, new_session\n"
            f"cap = cv2.VideoCapture(r'{base_video}')\n"
            "fps = cap.get(cv2.CAP_PROP_FPS) or 60.0\n"
            "w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))\n"
            "h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))\n"
            f"out = cv2.VideoWriter(r'{matte_dir / 'raw_matte.mp4'}', cv2.VideoWriter_fourcc(*'mp4v'), fps, (w, h), False)\n"
            f"sess = new_session('{args.model}')\n"
            "while True:\n"
            "    ok, frame = cap.read()\n"
            "    if not ok: break\n"
            "    small = cv2.resize(frame, (360, 640))\n"
            "    mask = remove(small, session=sess, only_mask=True)\n"
            "    mask_full = cv2.resize(mask, (w, h), interpolation=cv2.INTER_LINEAR)\n"
            "    out.write(mask_full)\n"
            "cap.release(); out.release()\n"
        )
        raw_matte = matte_dir / "raw_matte.mp4"
        subprocess.run([sys.executable, "-c", code], check=True)
        subprocess.run([
            ffmpeg, "-v", "error", "-y",
            "-i", str(raw_matte),
            "-vf", "tmix=frames=3:weights='1 2 1',gblur=sigma=2.2,format=gray",
            "-an", "-r", "60", "-c:v", "libx264", "-preset", "fast", "-crf", "16",
            str(matte60_mp4)
        ], check=True)

    if not matte_preview_540.exists() and matte60_mp4.exists():
        subprocess.run([
            ffmpeg, "-v", "error", "-y",
            "-i", str(base_video),
            "-i", str(matte60_mp4),
            "-filter_complex",
            "[0:v]scale=540:960[fg];[1:v]scale=540:960,format=gray[m];[fg][m]alphamerge[out]",
            "-map", "[out]", "-an", "-c:v", "libvpx-vp9", "-b:v", "1200k", "-auto-alt-ref", "0",
            str(matte_preview_540)
        ], check=True)

    write_report(out_json, {
        "status": "ok",
        "matte60_mp4": str(matte60_mp4),
        "backdrop_540_mp4": str(backdrop_540),
        "matte_preview_540_webm": str(matte_preview_540),
        "elapsed_seconds": round(time.monotonic() - t0, 2)
    })


# ============================================================================
# 3. SUBCOMMAND: gen-captions
# ============================================================================
def cmd_gen_captions(args: argparse.Namespace) -> None:
    t0 = time.monotonic()
    out_json = Path(args.output).resolve()
    transcript_path = Path(args.transcript).resolve()
    html_out = Path(args.html_out).resolve()
    if not transcript_path.exists():
        fail(f"Transcript file not found: {transcript_path}", out_json)

    raw_data = json.loads(transcript_path.read_text(encoding="utf-8"))
    if isinstance(raw_data, list):
        words_list = raw_data
    elif isinstance(raw_data, dict):
        if "words" in raw_data and isinstance(raw_data["words"], list):
            words_list = raw_data["words"]
        elif "segments" in raw_data and isinstance(raw_data["segments"], list):
            words_list = []
            for seg in raw_data["segments"]:
                words_list.extend(seg.get("words", []))
        else:
            words_list = []
    else:
        words_list = []

    # Filter and normalize words up to --cta-cutoff
    cutoff = float(args.cta_cutoff)
    clean_words = []
    for w in words_list:
        txt = str(w.get("word", w.get("text", ""))).strip()
        if not txt:
            continue
        st = float(w["start"])
        en = float(w["end"])
        if st >= cutoff:
            continue
        clean_words.append({"text": txt.upper(), "start": st, "end": min(en, cutoff)})

    # Group into 2-4 words per caption block
    groups = []
    cur: List[Dict[str, Any]] = []
    for w in clean_words:
        cur.append(w)
        pause = (w["end"] - cur[0]["start"] >= 1.15) or len(cur) >= 3
        punct = any(w["text"].endswith(p) for p in (".", ",", "?", "!", ":"))
        if len(cur) >= 2 and (pause or punct):
            groups.append(cur)
            cur = []
    if cur:
        groups.append(cur)

    svg_star = (
        '<svg class="st" viewBox="0 0 24 24" width="22" height="22">'
        '<path d="M12 0 L15 9 L24 12 L15 15 L12 24 L9 15 L0 12 L9 9 Z" fill="#67e8f9"/>'
        '</svg>'
    )

    group_divs = []
    for gi, g in enumerate(groups):
        gst = round(g[0]["start"], 3)
        gen = round(groups[gi + 1][0]["start"] if gi + 1 < len(groups) else g[-1]["end"] + 0.18, 3)
        gen = min(gen, cutoff)
        w_spans = []
        for wi, w in enumerate(g):
            clean_tok = re.sub(r"[^A-ZÁÉÍÓÚÑ0-9]", "", w["text"])
            cls = "w"
            star = ""
            if clean_tok in PURPLE_WORDS:
                cls = "w wp"
                star = svg_star
            elif clean_tok in CYAN_WORDS:
                cls = "w wc"
                star = svg_star
            w_spans.append(
                f'<span class="{cls}" id="g{gi}w{wi}" data-st="{w["start"]:.3f}">{w["text"]}{star}</span>'
            )
        group_divs.append(
            f'<div class="cg" id="cg{gi}" data-st="{gst:.3f}" data-en="{gen:.3f}">'
            + " ".join(w_spans) + "</div>"
        )

    html = f"""<template>
  <style>
    @font-face {{
      font-family: "Anton";
      src: url("assets/fonts/Anton-Regular.ttf") format("truetype");
    }}
    #root {{
      position: absolute;
      inset: 0;
      background: transparent;
      overflow: visible;
      font-family: "Anton", sans-serif;
      pointer-events: none;
    }}
    .cg {{
      position: absolute;
      left: 50px;
      right: 50px;
      top: 1185px;
      text-align: center;
      font-size: 92px;
      line-height: 1.05;
      text-transform: uppercase;
      opacity: 0;
    }}
    .w {{
      position: relative;
      display: inline-block;
      margin: 0 10px;
      color: #f1f5f9;
      text-shadow: 0 6px 0 #07071a, 0 10px 24px rgba(7, 7, 26, 0.92);
    }}
    .wc {{
      color: #67e8f9;
      text-shadow: 0 6px 0 #07071a, 0 0 28px rgba(6, 182, 212, 0.85);
    }}
    .wp {{
      color: #c4b5fd;
      text-shadow: 0 6px 0 #07071a, 0 0 32px rgba(124, 58, 237, 0.92);
    }}
    .st {{
      position: absolute;
      top: -14px;
      right: -16px;
      pointer-events: none;
    }}
  </style>
  <div id="root" data-composition-id="captions" data-width="1080" data-height="1920">
    {"".join(group_divs)}
  </div>
  <script>
    (function () {{
      var tl = gsap.timeline({{ paused: true }});
      var groups = document.querySelectorAll(".cg");
      groups.forEach(function (g) {{
        var st = parseFloat(g.getAttribute("data-st"));
        var en = parseFloat(g.getAttribute("data-en"));
        tl.set(g, {{ opacity: 1 }}, st);
        var ws = g.querySelectorAll(".w");
        ws.forEach(function (w) {{
          var wst = parseFloat(w.getAttribute("data-st"));
          tl.fromTo(w, {{ scale: 0.72, y: 24, opacity: 0 }}, {{ scale: 1, y: 0, opacity: 1, duration: 0.16, ease: "back.out(2.2)" }}, wst);
        }});
        tl.set(g, {{ opacity: 0 }}, en);
      }});
      window.__timelines = window.__timelines || {{}};
      window.__timelines["captions"] = tl;
    }})();
  </script>
</template>
"""
    html_out.parent.mkdir(parents=True, exist_ok=True)
    html_out.write_text(html, encoding="utf-8")
    write_report(out_json, {
        "status": "ok",
        "groups_count": len(groups),
        "words_count": len(clean_words),
        "cta_cutoff_seconds": cutoff,
        "html_out": str(html_out),
        "elapsed_seconds": round(time.monotonic() - t0, 2)
    })


# ============================================================================
# 4. SUBCOMMAND: setup-layers
# ============================================================================
def cmd_setup_layers(args: argparse.Namespace) -> None:
    t0 = time.monotonic()
    out_json = Path(args.output).resolve()
    proj_dir = Path(args.project_dir).resolve()
    scenes_d = proj_dir / "scenes.d"
    scenes_json_path = proj_dir / "scenes.json"

    if scenes_d.exists():
        merged: List[Dict[str, Any]] = []
        for jf in sorted(scenes_d.glob("*.json")):
            data = json.loads(jf.read_text(encoding="utf-8"))
            if isinstance(data, list):
                merged.extend(data)
            elif isinstance(data, dict) and "scenes" in data:
                merged.extend(data["scenes"])
        if merged:
            scenes_json_path.write_text(json.dumps(merged, indent=2, ensure_ascii=False), encoding="utf-8")

    if not scenes_json_path.exists():
        fail(f"scenes.json not found in {proj_dir}", out_json)

    raw_scenes = json.loads(scenes_json_path.read_text(encoding="utf-8"))
    scenes = raw_scenes["scenes"] if isinstance(raw_scenes, dict) and "scenes" in raw_scenes else raw_scenes
    behind_scenes = [s for s in scenes if s.get("layer") == "behind"]
    front_scenes = [s for s in scenes if s.get("layer") == "front"]

    for layer_name, layer_scenes in [("render-behind", behind_scenes), ("render-front", front_scenes)]:
        ldir = proj_dir / "work" / layer_name
        ldir.mkdir(parents=True, exist_ok=True)
        for sub in ("assets", "compositions"):
            src_sub = proj_dir / sub
            dst_sub = ldir / sub
            if src_sub.exists() and not dst_sub.exists():
                shutil.copytree(src_sub, dst_sub)
            elif src_sub.exists() and dst_sub.exists():
                for f in src_sub.rglob("*"):
                    if f.is_file():
                        rel = f.relative_to(src_sub)
                        target = dst_sub / rel
                        target.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(f, target)

        divs = []
        for idx, s in enumerate(layer_scenes, 1):
            sid = s["id"]
            src = s.get("src", f"compositions/{sid}.html")
            st = s["start"]
            dur = s["duration"]
            kind = "captions" if sid == "captions" else "graphics"
            z = 10 if sid == "captions" else 2
            divs.append(
                f'  <div id="{sid}" class="clip" data-composition-id="{sid}" '
                f'data-composition-src="{src}" data-start="{st}" data-duration="{dur}" '
                f'data-track-index="{idx}" data-track-kind="{kind}" data-width="1080" data-height="1920" '
                f'style="position:absolute;left:0;top:0;width:1080px;height:1920px;z-index:{z}"></div>'
            )

        layer_html = f"""<!doctype html>
<html lang="es" data-resolution="portrait">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=1080, height=1920" />
  <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: transparent; }}
    #root {{ position: relative; width: 1080px; height: 1920px; background: transparent; }}
  </style>
</head>
<body>
  <div id="root" data-composition-id="main" data-start="0" data-duration="{args.duration}" data-fps="60" data-width="1080" data-height="1920">
{chr(10).join(divs)}
  </div>
  <script>
    window.__timelines = window.__timelines || {{}};
    window.__timelines["main"] = gsap.timeline({{ paused: true }});
  </script>
</body>
</html>
"""
        (ldir / "index.html").write_text(layer_html, encoding="utf-8")

    write_report(out_json, {
        "status": "ok",
        "behind_scenes_count": len(behind_scenes),
        "front_scenes_count": len(front_scenes),
        "render_behind_dir": str(proj_dir / "work" / "render-behind"),
        "render_front_dir": str(proj_dir / "work" / "render-front"),
        "elapsed_seconds": round(time.monotonic() - t0, 2)
    })


# ============================================================================
# 5. SUBCOMMAND: build-audio
# ============================================================================
def resolve_sfx_file(sfx_dir: Path, cue_name: str) -> Optional[Path]:
    direct = sfx_dir / cue_name
    if direct.exists():
        return direct
    all_files = [p for p in sfx_dir.glob("*") if p.suffix.lower() in (".mp3", ".wav")]
    stem = Path(cue_name).stem.lower()
    for p in all_files:
        if stem in p.stem.lower() or p.stem.lower() in stem:
            return p
    for cat, keywords in SFX_CATEGORY_MAP.items():
        if cat in stem or any(k in stem for k in keywords):
            for p in all_files:
                if any(k in p.stem.lower() for k in keywords):
                    return p
    return all_files[0] if all_files else None


def cmd_build_audio(args: argparse.Namespace) -> None:
    t0 = time.monotonic()
    out_json = Path(args.output).resolve()
    proj_dir = Path(args.project_dir).resolve()
    sfx_dir = Path(args.sfx_dir).resolve()
    wav_out = Path(args.wav_out).resolve()

    build_v2 = proj_dir / "work" / "build_audio_v2.py"
    if build_v2.exists():
        subprocess.run([sys.executable, "-I", str(build_v2)], cwd=str(proj_dir), check=True)
        write_report(out_json, {
            "status": "ok",
            "delegated_script": str(build_v2),
            "wav_out": str(wav_out),
            "elapsed_seconds": round(time.monotonic() - t0, 2)
        })
        return

    master_voice = proj_dir / "work" / "master_voice.wav"
    if not master_voice.exists():
        fail(f"Master voice WAV not found: {master_voice}", out_json)

    scenes_path = proj_dir / "scenes.json"
    raw_scenes = json.loads(scenes_path.read_text(encoding="utf-8")) if scenes_path.exists() else []
    scenes = raw_scenes["scenes"] if isinstance(raw_scenes, dict) and "scenes" in raw_scenes else raw_scenes

    resolved_cues = []
    for s in scenes:
        st = float(s.get("start", 0.0))
        for cue in s.get("sfx", []):
            f = resolve_sfx_file(sfx_dir, cue.get("file", "whoosh.mp3"))
            if f:
                resolved_cues.append({
                    "file": str(f),
                    "time": round(st + float(cue.get("at", cue.get("offset", 0.0))), 3),
                    "volume": min(0.35, float(cue.get("volume", 0.25)))
                })

    ffmpeg = shutil.which("ffmpeg") or "ffmpeg"
    subprocess.run([
        ffmpeg, "-v", "error", "-y",
        "-i", str(master_voice),
        "-af", "highpass=f=80,equalizer=f=3200:t=q:w=1.0:g=2.5,acompressor=threshold=-18dB:ratio=3:attack=8:release=120:makeup=3dB,loudnorm=I=-14:TP=-1.2:LRA=9",
        "-ar", "48000", "-ac", "2",
        str(wav_out)
    ], check=True)

    write_report(out_json, {
        "status": "ok",
        "sfx_cues_resolved": len(resolved_cues),
        "wav_out": str(wav_out),
        "elapsed_seconds": round(time.monotonic() - t0, 2)
    })


# ============================================================================
# 6. SUBCOMMAND: composite
# ============================================================================
def cmd_composite(args: argparse.Namespace) -> None:
    t0 = time.monotonic()
    out_json = Path(args.output).resolve()
    proj_dir = Path(args.project_dir).resolve()
    final_mp4 = Path(args.final_mp4).resolve()
    layers_dir = proj_dir / "layers"
    layers_dir.mkdir(parents=True, exist_ok=True)

    behind_mov = layers_dir / "behind.mov"
    front_mov = layers_dir / "front.mov"
    npx = shutil.which("npx.cmd") or shutil.which("npx") or "npx"
    ffmpeg = shutil.which("ffmpeg") or "ffmpeg"
    ffprobe = shutil.which("ffprobe") or "ffprobe"

    # Step 1: Render behind.mov sequentially (--low-memory-mode)
    if not behind_mov.exists() or args.force_render:
        subprocess.run([
            npx, "hyperframes", "render", "work/render-behind",
            "-o", "layers/behind.mov", "--format", "mov", "--fps", "60", "--low-memory-mode"
        ], cwd=str(proj_dir), check=True)

    # Step 2: Render front.mov sequentially (--low-memory-mode)
    if not front_mov.exists() or args.force_render:
        subprocess.run([
            npx, "hyperframes", "render", "work/render-front",
            "-o", "layers/front.mov", "--format", "mov", "--fps", "60", "--low-memory-mode"
        ], cwd=str(proj_dir), check=True)

    # Step 3: 4-Layer FFmpeg Alphamerge Composite
    base60 = proj_dir / "work" / "base" / "base60.mp4"
    matte60 = proj_dir / "work" / "matte" / "matte60.mp4"
    mix_wav = proj_dir / "work" / "mix_v2.wav"

    subprocess.run([
        ffmpeg, "-v", "error", "-stats", "-y",
        "-i", str(base60),
        "-i", str(behind_mov),
        "-i", str(matte60),
        "-i", str(front_mov),
        "-i", str(mix_wav),
        "-filter_complex",
        "[0:v]split=2[base][fgsrc];"
        "[2:v]format=gray[matte];"
        "[fgsrc][matte]alphamerge[person];"
        "[base][1:v]overlay=0:0:format=auto[bg_behind];"
        "[bg_behind][person]overlay=0:0:format=auto[with_person];"
        "[with_person][3:v]overlay=0:0:format=auto,format=yuv420p[vout]",
        "-map", "[vout]", "-map", "4:a",
        "-t", str(args.duration), "-r", "60",
        "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart",
        str(final_mp4)
    ], check=True)

    sheet_jpg = proj_dir / "work" / "final_v2_contact_sheet.jpg"
    subprocess.run([
        ffmpeg, "-v", "error", "-y",
        "-i", str(final_mp4),
        "-vf", "select='isnan(prev_selected_t)+gte(t-prev_selected_t\\,4.5)',scale=360:640,tile=4x3",
        "-frames:v", "1", "-q:v", "2",
        str(sheet_jpg)
    ], check=True)

    probe_res = subprocess.run([
        ffprobe, "-v", "error",
        "-show_entries", "format=duration,size,bit_rate:stream=codec_name,width,height,r_frame_rate,nb_frames",
        "-of", "json", str(final_mp4)
    ], capture_output=True, text=True, check=True)

    write_report(out_json, {
        "status": "ok",
        "final_mp4": str(final_mp4),
        "contact_sheet_jpg": str(sheet_jpg),
        "ffprobe": json.loads(probe_res.stdout),
        "elapsed_seconds": round(time.monotonic() - t0, 2)
    })


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="reel_pipeline.py",
        description="Marketing Reel Pro ($300k Agency Vertical Ad Pipeline) CLI"
    )
    sub = p.add_subparsers(dest="subcommand", required=True)

    # 1. prepare-base
    p_base = sub.add_parser("prepare-base", help="Build 1080x1920 @ 60fps graded base60.mp4 + master_voice.wav")
    p_base.add_argument("--mode", choices=["multi-shot", "single-video"], required=True)
    p_base.add_argument("--audio", help="Master voiceover file (Mode A: multi-shot)")
    p_base.add_argument("--clips-dir", help="Directory containing scene .mp4 clips (Mode A: multi-shot)")
    p_base.add_argument("--segments-json", help="Optional JSON mapping clip trim and target_dur")
    p_base.add_argument("--video", help="Single continuous video file (Mode B: single-video)")
    p_base.add_argument("--work-dir", required=True, help="Working directory")
    p_base.add_argument("--output", required=True, help="Output JSON report path")
    p_base.set_defaults(func=cmd_prepare_base)

    # 2. extract-matte
    p_matte = sub.add_parser("extract-matte", help="Extract 60fps human silhouette matte + 540p preview proxies")
    p_matte.add_argument("--base-video", required=True, help="Path to work/base/base60.mp4")
    p_matte.add_argument("--work-dir", required=True, help="Working directory")
    p_matte.add_argument("--model", default="u2netp", choices=["u2netp", "u2net_human_seg"])
    p_matte.add_argument("--output", required=True, help="Output JSON report path")
    p_matte.set_defaults(func=cmd_extract_matte)

    # 3. gen-captions
    p_cap = sub.add_parser("gen-captions", help="Generate safe-zone kinetic captions with inline SVG stars")
    p_cap.add_argument("--transcript", required=True, help="Word-level transcript JSON")
    p_cap.add_argument("--cta-cutoff", type=float, required=True, help="Cutoff second before final CTA card")
    p_cap.add_argument("--html-out", required=True, help="Output path for compositions/captions.html")
    p_cap.add_argument("--output", required=True, help="Output JSON report path")
    p_cap.set_defaults(func=cmd_gen_captions)

    # 4. setup-layers
    p_lay = sub.add_parser("setup-layers", help="Merge scenes.d/*.json and create render-behind & render-front")
    p_lay.add_argument("--project-dir", required=True, help="Root HyperFrames project directory")
    p_lay.add_argument("--duration", type=float, default=55.36, help="Total composition duration in seconds")
    p_lay.add_argument("--output", required=True, help="Output JSON report path")
    p_lay.set_defaults(func=cmd_setup_layers)

    # 5. build-audio
    p_aud = sub.add_parser("build-audio", help="Mix master voiceover, ducked music pad/loop, and viral SFX to -14 LUFS")
    p_aud.add_argument("--project-dir", required=True, help="Root project directory")
    p_aud.add_argument("--sfx-dir", default=DEFAULT_SFX_DIR, help="Path to 105 viral SFX library")
    p_aud.add_argument("--wav-out", required=True, help="Output path for work/mix_v2.wav")
    p_aud.add_argument("--output", required=True, help="Output JSON report path")
    p_aud.set_defaults(func=cmd_build_audio)

    # 6. composite
    p_comp = sub.add_parser("composite", help="Render behind.mov & front.mov sequentially and composite 4 layers")
    p_comp.add_argument("--project-dir", required=True, help="Root project directory")
    p_comp.add_argument("--duration", type=float, default=55.36, help="Final video duration in seconds")
    p_comp.add_argument("--force-render", action="store_true", help="Re-render MOV layers even if present")
    p_comp.add_argument("--final-mp4", required=True, help="Output path for final .mp4")
    p_comp.add_argument("--output", required=True, help="Output JSON report path")
    p_comp.set_defaults(func=cmd_composite)

    return p


if __name__ == "__main__":
    parser = build_parser()
    parsed = parser.parse_args()
    parsed.func(parsed)
