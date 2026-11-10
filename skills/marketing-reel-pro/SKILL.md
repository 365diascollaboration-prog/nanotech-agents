---
name: marketing-reel-pro
description: >-
  End-to-end agency-grade ($300k look) vertical marketing reel and ad production
  (1080x1920 @ 60 fps) using HyperFrames, GSAP, FFmpeg, and AI silhouette matting.
  Supports Dual Input Modes: (A) Master audio + multi-shot scene clips (word-level
  lip-sync matching + 60 fps MCI optical flow interpolation with zero frozen frames)
  or (B) Single continuous video with audio. Builds a real 4-layer depth composite
  (L0 Base 60fps -> L1 Behind Motion Graphics -> L2 AI Subject Matte -> L3 Front
  Cards & Kinetic Captions), sidechain-ducked music bed + 50-60 viral SFX cues
  normalized to -14 LUFS, and sequential low-memory rendering safe for 7-8 GB RAM.
---

# Marketing Reel Pro ($300k Agency Vertical Ad Pipeline)

## Overview

`marketing-reel-pro` turns raw vertical footage into a high-retention, agency-grade vertical commercial (`1080x1920` at `60 fps`, H.264 `CRF 17` + AAC `192k` at `-14 LUFS`). Built from real production workflows by **Nanoboy (365 Collaboration)**, it solves the three biggest problems in AI-assisted vertical video editing:

1. **Multi-Shot Lip-Sync Without Frozen Frames (Mode A)** or **Single-Clip Mastering (Mode B)**: Aligns spoken phrases between a master voiceover and separate scene takes, filling duration gaps with motion-compensated interpolation (`minterpolate=fps=60:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1`) and slow-motion on non-speaking walking shots so lips never desync or freeze.
2. **True 4-Layer Depth Compositing (`L0` -> `L1` -> `L2` -> `L3`)**: Extracts a frame-accurate 60 fps human alpha matte (`rembg` `u2netp` + temporal smoothing) so giant hero typography, gauges, barbells, and radial bursts render **behind the speaker's shoulders and head (`L1`)**, while data cards, badges, and kinetic captions sit cleanly **in front (`L3`)**.
3. **Neurological Retention Audio + Low-Memory Safety**: Mixes master voiceover (high-pass + presence EQ + compression), a sidechain-ducked musical chord pad + 85 BPM pulse, and 50-60 frame-accurate viral SFX cues from `scenes.json`, while enforcing a strict single-worker `--low-memory-mode` render pipeline that never freezes machines with 7-8 GB RAM.

---

## Dependencies

When executing this workflow, coordinate with the following installed skills (do not reimplement their core primitives):

- **`hyperframes`** & **`hyperframes-cli`**: Core HTML-to-video rendering engine (`npx hyperframes lint --verbose`, `npx hyperframes snapshot --at`, `npx hyperframes render --low-memory-mode`).
- **`motion-graphics`** & **`hyperframes-animation`**: Deterministic GSAP timeline authoring (`window.__timelines["<id>"] = tl`, seeded PRNG instead of `Math.random()`).
- **`talking-head-recut`** & **`embedded-captions`**: Word-level Whisper transcription conventions and safe-zone hierarchy between lower-third kinetic captions and full-scene graphic overlays.

System requirements:
- `ffmpeg` and `ffprobe` on `PATH`
- `npx hyperframes` (v0.9+)
- Python 3.10+ with `rembg` (optional for `extract-matte`; falls back to existing matte or `npx hyperframes remove-background`)

---

## Quick Start

Run the deterministic pipeline CLI (`scripts/reel_pipeline.py`) for every programmatic step. All subcommands write structured JSON reports and media artifacts to disk rather than dumping large payloads to stdout.

### Mode A: Master Audio + Multi-Shot Scene Clips

```bash
python skills/marketing-reel-pro/scripts/reel_pipeline.py prepare-base \
  --mode multi-shot \
  --audio "C:/Users/infon/Downloads/audio-anuncio.mp4" \
  --clips-dir "C:/Users/infon/Downloads/scenes_unzipped" \
  --work-dir "C:/Users/infon/Downloads/mi-anuncio-proyecto/work" \
  --output "C:/Users/infon/Downloads/mi-anuncio-proyecto/work/base_report.json"
```

### Mode B: Single Continuous Video With Audio

```bash
python skills/marketing-reel-pro/scripts/reel_pipeline.py prepare-base \
  --mode single-video \
  --video "C:/Users/infon/Downloads/video-corrido.mp4" \
  --work-dir "C:/Users/infon/Downloads/mi-anuncio-proyecto/work" \
  --output "C:/Users/infon/Downloads/mi-anuncio-proyecto/work/base_report.json"
```

### Extract 60fps Silhouette Matte, Build Layers, Mix Audio & Composite

```bash
# 1. Generate 60fps grayscale alpha matte + 540p preview proxies
python skills/marketing-reel-pro/scripts/reel_pipeline.py extract-matte \
  --base-video "work/base/base60.mp4" \
  --work-dir "work" \
  --output "work/matte_report.json"

# 2. Generate performance-safe kinetic captions (y: 1120-1330, inline SVG stars)
python skills/marketing-reel-pro/scripts/reel_pipeline.py gen-captions \
  --transcript "work/audio_master_words.json" \
  --cta-cutoff 52.40 \
  --html-out "compositions/captions.html" \
  --output "work/captions_report.json"

# 3. Merge scenes.d/*.json and build isolated L1 (behind) & L3 (front) projects
python skills/marketing-reel-pro/scripts/reel_pipeline.py setup-layers \
  --project-dir "." \
  --output "work/layers_report.json"

# 4. Build -14 LUFS master audio mix (voice + ducked pad/loop + 60 viral SFX cues)
python skills/marketing-reel-pro/scripts/reel_pipeline.py build-audio \
  --project-dir "." \
  --sfx-dir "C:/Users/infon/Desktop/editor de video - romotions/my-video/public/click.mp3" \
  --wav-out "work/mix_v2.wav" \
  --output "work/audio_report.json"

# 5. Render L1 & L3 sequentially (--low-memory-mode) and composite 4 layers to MP4
python skills/marketing-reel-pro/scripts/reel_pipeline.py composite \
  --project-dir "." \
  --final-mp4 "C:/Users/infon/Downloads/anuncio-final-v2.mp4" \
  --output "work/composite_report.json"
```

---

## Utility Scripts

The CLI script [`scripts/reel_pipeline.py`](scripts/reel_pipeline.py) implements 6 subcommands. Every subcommand requires `--output <path.json>` and writes a JSON summary with `status`, `elapsed_seconds`, and output file paths.

### 1. `prepare-base`
Builds `work/base/base60.mp4` (`1080x1920 @ 60 fps`, graded with `eq=contrast=1.06:saturation=1.12:brightness=0.01,unsharp=5:5:0.75:5:5:0.0,vignette=PI/7`) and extracts `work/master_voice.wav` (`48 kHz` stereo).
- `--mode`: `multi-shot` (Mode A) or `single-video` (Mode B). Required.
- `--audio`: Path to master audio/video containing the reference voiceover (Mode A).
- `--clips-dir`: Directory of scene clips or `.mp4` takes (Mode A).
- `--segments-json`: Optional JSON mapping each clip's `ss`, `to`, and `target_dur` to match the master voiceover phrase-by-phrase.
- `--video`: Path to single continuous source video (Mode B).
- `--work-dir`: Working directory path. Required.
- `--output`: Path to JSON status report. Required.

### 2. `extract-matte`
Generates `work/matte/matte60.mp4` (grayscale alpha mask aligned frame-for-frame with `base60.mp4`) plus lightweight `work/backdrop_540.mp4` and `work/matte_preview_540.webm` proxies for fast `hyperframes snapshot` checks.
- `--base-video`: Path to `work/base/base60.mp4`. Required.
- `--work-dir`: Working directory path. Required.
- `--model`: `u2netp` (default, fast CPU) or `u2net_human_seg`.
- `--output`: Path to JSON status report. Required.

### 3. `gen-captions`
Compiles word-level timestamps into `compositions/captions.html` using 2-4 word groups in the safe lower zone (`top: 1120px` to `1330px`), highlighting brand keywords in cyan (`#06b6d4`) and impact keywords in purple (`#7c3aed`) with inline `<svg>` stars (avoiding `clip-path: polygon(...)` so HyperFrames never triggers `composition_heavy_overlay_count_high`).
- `--transcript`: Word-level JSON (`[{"word": "...", "start": 0.0, "end": 0.3}, ...]`). Required.
- `--cta-cutoff`: Timestamp in seconds after which bottom captions stop so the final CTA DM card (`L3`) has zero text overlap. Required.
- `--html-out`: Output path for `compositions/captions.html`. Required.
- `--output`: Path to JSON status report. Required.

### 4. `setup-layers`
Merges `scenes.d/*.json` into root `scenes.json`, splits scenes by `"layer": "behind"` (`L1`) vs `"layer": "front"` (`L3`), creates standalone HyperFrames projects in `work/render-behind/` and `work/render-front/` with `background: transparent`, and updates root `index.html` for unified visual snapshots.
- `--project-dir`: Root project directory. Required.
- `--output`: Path to JSON status report. Required.

### 5. `build-audio`
Synthesizes the full agency audio mix (`work/mix_v2.wav`):
1. Master voiceover with high-pass (`80 Hz`), presence boost (`3.2 kHz`), and `acompressor`.
2. Musical chord pad (`A2/E3/G3/B3/D4` warm stereo detuned saw/sine) + `85 BPM` kick/hat groove, automatically sidechain-ducked under the voiceover.
3. Base transition/impact SFX + every scene's `"sfx"` array from `scenes.json` resolved against your 105-sound library (`C:\Users\infon\Desktop\editor de video - romotions\my-video\public\click.mp3\`), with automatic category fallback if a filename varies.
4. EBU R128 loudness normalization (`loudnorm=I=-14:TP=-1.2:LRA=9`).

### 6. `composite`
Executes the low-memory sequential render and 4-layer FFmpeg composite:
1. Renders `work/render-behind` -> `layers/behind.mov` (`ProRes 4444` RGBA @ 60 fps, `--low-memory-mode`).
2. Renders `work/render-front` -> `layers/front.mov` (`ProRes 4444` RGBA @ 60 fps, `--low-memory-mode`).
3. Composites `L0` (`base60.mp4`) + `L1` (`behind.mov`) + `L2` (`[base60][matte60]alphamerge`) + `L3` (`front.mov`) + `mix_v2.wav` -> final `.mp4` (`CRF 17`, `faststart`).
4. Extracts a 12-frame `final_contact_sheet.jpg` and runs `ffprobe` validation.

---

## Workflow

Follow these 7 steps in order whenever creating or editing a vertical marketing reel:

### Step 1: Probe Inputs & Select Mode (A or B)
1. Inspect the user's files with `ffprobe`.
2. If the user provides **separate scene clips + a master audio file** -> use **Mode A (`multi-shot`)**. Transcribe both the master audio and each scene clip to align spoken clauses, then run `reel_pipeline.py prepare-base --mode multi-shot`.
3. If the user provides **a single continuous video with audio** -> use **Mode B (`single-video`)**. Run `reel_pipeline.py prepare-base --mode single-video` to normalize to `1080x1920 @ 60 fps` and extract `work/master_voice.wav`.

### Step 2: Generate the 60fps AI Subject Matte
Run `reel_pipeline.py extract-matte` to create `work/matte/matte60.mp4` and the 540p preview proxies (`work/backdrop_540.mp4`, `work/matte_preview_540.webm`).

### Step 3: Design the 4-Layer Scene Plan (`scenes.json`)
Plan 10 to 16 visual scenes across the reel's duration (a visual change every 2.5 to 4.0 seconds) and assign each sub-composition to the right depth layer:
- **`"layer": "behind"` (`L1`)**: Giant hero typography (`top: 140px–220px`), radial vortexes, 365 sun rays, rising sales charts, workflow node networks, barbell plates behind shoulders (`peso-operativo`), and arch trajectories (`competencia`).
- **`"layer": "front"` (`L3`)**: Chest-level punchlines (`top: 720px`) over dark shirts, glassmorphic data cards (`top: 904px`), lower badges, and the final interactive DM card (`COMENTA "CRECER"`).
- Consult [`references/brand-presets.md`](references/brand-presets.md) and [`references/composition-patterns.md`](references/composition-patterns.md) for exact pixel coordinates and GSAP patterns.

### Step 4: Author Sub-Compositions & Kinetic Captions
1. Write each scene's `<template>` HTML in `compositions/<scene-id>.html`.
2. Generate `compositions/captions.html` via `reel_pipeline.py gen-captions`, setting `--cta-cutoff` to the exact timestamp where the final CTA DM card starts typing its response so captions never collide with the closing card.
3. Run `reel_pipeline.py setup-layers` to sync `scenes.json`, `work/render-behind/`, `work/render-front/`, and root `index.html`.

### Step 5: Lint & Visual QA via Contact Sheet (Mandatory Gate)
Before running any full 60 fps render:
1. Run `npx hyperframes lint --verbose` on `work/render-behind` and `work/render-front`. Fix all errors and eliminate heavy overlay warnings.
2. Run `npx hyperframes snapshot --at "<key_timestamps>"` on the root project and inspect the generated `contact-sheet.jpg`:
   - Verify **zero text is obscured by the speaker's face/sunglasses** (if a `behind` word is unreadable behind the head in a close-up, move it to `front` on the chest at `top: 720px` or above the head at `top: 145px`).
   - Verify **zero clipping** inside `overflow: hidden` text curtains (`.sv-ln` needs sufficient bottom padding, e.g., `padding: 28px 6px 26px`).
   - Verify **zero ghost cards** from overlapping card exits/entrances.

### Step 6: Build the -14 LUFS Viral Audio Mix
Run `reel_pipeline.py build-audio` using [`references/sfx-catalog-365.md`](references/sfx-catalog-365.md) so every visual entrance, counter tick, cash ding, warning buzz, and DM button click has a frame-accurate sound effect.

### Step 7: Sequential Low-Memory Render & 4-Layer Composite
Run `reel_pipeline.py composite` (or invoke the 3 commands sequentially, **never in parallel**). Inspect `work/final_v2_contact_sheet.jpg` and verify `ffprobe` reports `1080x1920`, `60/1` fps, `h264`, and `aac` before presenting the final MP4 link to the user.

---

## Rate Limiting & Hardware Guardrails

This pipeline runs 100% locally (FFmpeg + local Whisper + local `rembg` + local Headless Chromium via HyperFrames) and does not call external rate-limited REST APIs. Instead, it enforces **strict hardware and memory rate-limiting** for 7-8 GB RAM machines:

1. **Single Heavy Process Lock**: Never run two `hyperframes render` or heavy `ffmpeg` processes concurrently. `reel_pipeline.py` executes `behind.mov`, `front.mov`, and the final FFmpeg composite strictly sequentially.
2. **Mandatory `--low-memory-mode`**: Always pass `--low-memory-mode` to `npx hyperframes render` (pins to 1 worker and screenshot capture mode, preventing Chromium OOM crashes).
3. **No Dev/Preview Servers**: Never start `npm run dev`, `npx hyperframes preview`, or background HTTP servers unless explicitly requested by the user.

---

## Common Mistakes

1. **Placing secondary headline text behind the face in close-ups**:
   - *Problem*: Putting a two-line title both in `behind` (`L1`) at `top: 150px` and `top: 325px` causes the second line (`top: 325px`) to sit directly behind the speaker's eyes/sunglasses (`NO [face] URA?`), making short words unreadable.
   - *Fix*: Keep line 1 (`¿TU NEGOCIO`) in `behind` at `top: 150px` (above the head) and place line 2 (`NO FACTURA?`) in `front` (`L3`) at `top: 722px` over the speaker's chest, right above the `top: 904px` data card.
2. **Triggering `composition_heavy_overlay_count_high` in `captions.html`**:
   - *Problem*: Using `clip-path: polygon(...)` and `radial-gradient` pseudo-elements on 80+ word spans causes Chromium capture stalls or black frames during long 60 fps renders.
   - *Fix*: Always use inline `<svg>` for sparkle stars and `text-shadow` for word glow (built into `reel_pipeline.py gen-captions`).
3. **Hidden SVG round caps (`svg_round_cap_hidden_dash`)**:
   - *Problem*: Setting `stroke-linecap="round"` with `stroke-dasharray: 100; stroke-dashoffset: 100` leaves a visible dot at `offset = 100` before the line draws.
   - *Fix*: Use `pathLength="100"` with `stroke-dasharray: 100 120; stroke-dashoffset: 110; opacity: 0` and animate `opacity: 1` at the exact draw start time.
4. **Duplicate captions colliding with the final CTA DM card**:
   - *Problem*: Leaving bottom captions active during the last 3 seconds while the interactive DM card types out the same words.
   - *Fix*: Pass `--cta-cutoff 52.40` (or the start of the DM card's bottom message) to `gen-captions` so the lower third stays 100% clean for the CTA.
