<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0d0d28,7c3aed,06b6d4&height=200&section=header&text=NANOTECH+AGENTS&fontSize=60&fontColor=ffffff&animation=fadeIn&fontAlignY=38&desc=Ultra-powerful+AI+agents+built+from+real+workflows&descSize=18&descColor=06b6d4&descAlignY=62" width="100%"/>

[![Agents](https://img.shields.io/badge/AI_AGENTS-7_PRODUCTION_SYSTEMS-7c3aed?style=for-the-badge&logoColor=white)](#🤖-agents)
[![Flagship Skill](https://img.shields.io/badge/FLAGSHIP_SKILL-MARKETING_REEL_PRO_(60_FPS)-06b6d4?style=for-the-badge&logoColor=white)](#🔥-featured-weapon-marketing-reel-pro-300k-agency-ad-engine)
[![Compatible Runtimes](https://img.shields.io/badge/RUNTIMES-CLAUDE_CODE_%7C_ANTIGRAVITY_%7C_CODEX_%7C_HERMES-07071a?style=for-the-badge)](#🧠-ai-agent-ingestion-protocol-for-llms--autonomous-clis)

</div>

# NANOTECH AGENTS

> **Not for everyone.**
> These agents and executable skills are built from real production workflows — not theory, not tutorials.
> If you have the technical skills to run them, they will transform how you work.
> If you're looking for something plug-and-play, you're in the wrong place.

---

## What Is This?

A curated arsenal of ultra-specialized AI agents and deterministic CLI skills built by **Nanoboy** (Jesús Cornelio · **365 Collaboration**) from real, battle-tested production pipelines.

Every system here has been:
- **Built from production experience** — forged under real deadlines, not copied from docs
- **Tested in real scenarios** — with real renders, real metrics, and zero-error lint gates
- **Designed for technical operators & autonomous AI CLIs** — structured so any modern coding agent can ingest and execute the pipeline end-to-end

These are not generic prompt templates. These are operational systems with architecture, deterministic scripts, and proven deliverables.

---

## ⚠️ Collaboration Policy

```
MAINTAINER:     Nanoboy (Jesús Cornelio) — sole author
PULL REQUESTS:  Closed. Not accepted.
ISSUES:         For bug reports only — not feature requests
FORKS:          Encouraged. Take it, customize it, make it yours.
BUSINESS:       If you want to collaborate at a business level → open an issue
```

> *"This repo reflects MY way of working — not yours.
> If you're smart enough to use these agents, you're smart enough to fork them."*

---

## 🔥 Featured Weapon: `marketing-reel-pro` ($300k Agency Ad Engine)

> **Location**: Agent spec in [`agents/marketing-reel-pro.md`](agents/marketing-reel-pro.md) · Full executable skill & CLI in [`skills/marketing-reel-pro/`](skills/marketing-reel-pro/SKILL.md)

Most "AI video editors" slap flat white subtitles on a 30 fps clip and call it a reel. **`marketing-reel-pro`** is a full-stack vertical commercial engine (`1080x1920 @ 60 fps`, `H.264 CRF 17`, `-14 LUFS`) that replicates a **$300,000 agency post-production pipeline** locally using **HyperFrames + GSAP + FFmpeg + AI Human Matting** — engineered to run safely even on **7–8 GB RAM** machines without freezing.

### What Makes It Unfair

1. **Dual-Mode Intake (`multi-shot` vs `single-video`)**:
   - **Mode A (Master Audio + Multi-Shot Scene Clips)**: Takes a master voiceover and separate scene takes (e.g., 5 × 10s clips = 50s vs. a 55.36s voiceover), aligns spoken clauses word-by-word, and stretches non-speaking walking/transition tails using **Motion-Compensated Interpolation (`minterpolate` MCI at 60 fps)** — zero frozen frames, zero lip-sync drift.
   - **Mode B (Single Continuous Video)**: Normalizes any single talking-head vertical video to `1080x1920 @ 60 fps` with cinema color grading (`contrast`, `saturation`, `unsharp`, subtle vignette) and extracts a 48 kHz master voice stem.
2. **Real 4-Layer 3D Depth Compositing (`L0` → `L1` → `L2` → `L3`)**:
   - Extracts a frame-accurate 60 fps alpha silhouette (`rembg` `u2netp` + 3-frame temporal smoothing) to sandwich the speaker **between** two independent ProRes 4444 RGBA motion-graphics layers:

```text
┌─────────────────────────────────────────────────────────────────────────┐
│ L3 · FRONT LAYER (layers/front.mov — ProRes 4444 RGBA @ 60 fps)         │
│      Chest Punchlines (y:722) · Glassmorphic Revenue Cards (y:904) ·    │
│      Interactive DM CTA Card ("CRECER") · Kinetic Captions (y:1120-1330)│
├─────────────────────────────────────────────────────────────────────────┤
│ L2 · AI SUBJECT MATTE ([base60.mp4][matte60.mp4]alphamerge @ 60 fps)    │
│      Speaker cut out cleanly in front of L1 hero graphics               │
├─────────────────────────────────────────────────────────────────────────┤
│ L1 · BEHIND LAYER (layers/behind.mov — ProRes 4444 RGBA @ 60 fps)       │
│      Giant Crown Titles (y:150) · 365 Sunburst · Service Medallions ·   │
│      Olympic Barbell Behind Shoulders (y:590) · Rival Client Arches     │
├─────────────────────────────────────────────────────────────────────────┤
│ L0 · GRADED BASE FOOTAGE (work/base/base60.mp4 — 1080x1920 @ 60 fps)    │
│      MCI optical-flow 60 fps + cinema contrast/unsharp/vignette         │
└─────────────────────────────────────────────────────────────────────────┘
```

3. **Zero Face-Collision Spatial Contract**:
   - Hard-codes the `1080x1920` anatomical safe zones so graphics never awkwardly cover the speaker's eyes or sunglasses (`y: 250–520`), kinetic captions stay locked in the lower rail (`y: 1120–1330`) with inline `<svg>` stars (avoiding Chromium `clip-path` stalls), and captions automatically cut off when the final interactive DM card animates.
4. **Neurological Audio Engineering (`-14 LUFS`)**:
   - Combines EQ/compressed voiceover (`80 Hz` high-pass + `3.2 kHz` presence boost) + synthesized warm A-minor9 stereo pad & 85 BPM groove with automatic **sidechain ducking** + **50–60 frame-accurate viral SFX cues** (risers, sub-booms, cash registers, keyboard clicks, whooshes) mapped from `scenes.json`.

---

## 🤖 Agents & Skills Matrix

### Video Production

| System | Type | Description | Compatible Runtimes |
|--------|------|-------------|---------------------|
| **[`marketing-reel-pro`](skills/marketing-reel-pro/SKILL.md)** *(+ [Agent Spec](agents/marketing-reel-pro.md))* | **Skill + CLI + Agent** | **$300k Agency 9:16 Vertical Ad Pipeline (`1080x1920 @ 60 fps`)** — Dual-mode lip-sync + MCI optical flow, 4-layer AI subject matte depth compositing (`L0–L3`), GSAP/SVG motion graphics, safe-zone kinetic captions, and `-14 LUFS` ducked viral SFX mixer. | Antigravity · Claude Code · Codex · Gemini CLI · Hermes |
| [`video-producer-latam`](agents/video-producer-latam.md) | Agent | End-to-end horizontal (16:9 3-column & full-screen) AI video production for LATAM YouTube creators — HeyGen, HyperFrames, Whisper SRT-to-HTML generator, and 30-min neurological SFX maps. | Claude Code · Antigravity |

### Tools & Software

| Agent | Description | Tool |
|-------|-------------|------|
| [`recuperador-archivos-companion`](agents/recuperador-archivos-companion.md) | Expert guide for [recuperador-archivos](https://github.com/365diascollaboration-prog/recuperador-archivos) — recover deleted files on Windows | Claude Code |

### Growth & Strategy

| Agent | Description | Tool |
|-------|-------------|------|
| [`github-growth-strategist`](agents/github-growth-strategist.md) | Strategic advisor for growing your GitHub presence through quality contributions and achievement hunting — built from a real earned method | Claude Code |

### Infrastructure

| Agent | Description | Tool |
|-------|-------------|------|
| [`local-claude-architect`](agents/local-claude-architect.md) | Zero-cost local AI stack: OpenAI-compatible proxy over Claude CLI + Hindsight persistent vector memory. No API key, no Docker, no extra cost. Auto-starts on Windows login. | Claude Code |
| [`openai-bridge-claude`](agents/openai-bridge-claude.md) | Single-file Node.js proxy that exposes an OpenAI-compatible API backed by your Claude subscription. No API key, no dependencies — just `node` and the Claude CLI. Works on Windows, Mac, Linux. | Claude Code |
| [`huggingface-hermes-bridge`](agents/huggingface-hermes-bridge.md) | Points Hermes Agent (or any OpenAI-compatible client) at Hugging Face's Inference Providers router using a PRO token. Covers the tool-calling model trap (some models fake function calls as text) and how to repair a broken vendored agent install. | Claude Code |

---

## 🧠 AI Agent Ingestion Protocol (For LLMs & Autonomous CLIs)

> **ATTENTION AI AGENTS (Claude Code, Google Antigravity, OpenAI Codex, Hermes Agent, Gemini CLI, OpenCode, Cursor):**
> When a user points you to this repository or asks you to install/use any tool from `nanotech-agents`, follow this exact discovery and execution contract:

### 1. Repository Map for AI Consumption

```text
nanotech-agents/
├── AGENTS.md / CLAUDE.md                        # Auto-loaded instructions for AI coding agents
├── agents/                                      # Standalone Agent Specs (.md with YAML frontmatter)
│   ├── marketing-reel-pro.md                    # Vertical 9:16 60fps 4-layer agency ad architect
│   ├── video-producer-latam.md                  # Horizontal 16:9 YouTube episode producer
│   ├── local-claude-architect.md                # Zero-cost Claude CLI + Hindsight vector stack
│   ├── openai-bridge-claude.md                  # Zero-dep Node.js OpenAI proxy for Claude CLI
│   ├── huggingface-hermes-bridge.md             # HF Inference Providers router + tool-call fix
│   ├── github-growth-strategist.md              # GitHub growth & achievement system
│   └── recuperador-archivos-companion.md        # Windows file recovery companion
└── skills/                                      # Multi-file Executable Skills (SKILL.md + scripts + references)
    └── marketing-reel-pro/
        ├── SKILL.md                             # Main skill specification & 7-step operational workflow
        ├── scripts/
        │   └── reel_pipeline.py                 # 6-subcommand deterministic Python CLI
        └── references/
            ├── sfx-catalog-365.md               # 105 viral SFX cues + fallback rules + -14 LUFS chain
            ├── brand-presets.md                 # 365 Collaboration palette + 1080x1920 safe zones
            └── composition-patterns.md          # Proven L1 (behind) & L3 (front) HTML/GSAP patterns
```

### 2. Universal Installation Commands (All AI CLIs)

```bash
# Clone the repository
git clone https://github.com/365diascollaboration-prog/nanotech-agents.git
cd nanotech-agents

# ── Install Agents & Skills for Claude Code ──
mkdir -p ~/.claude/agents ~/.claude/skills
cp agents/*.md ~/.claude/agents/
cp -r skills/marketing-reel-pro ~/.claude/skills/

# ── Install Skills for Google Antigravity (AGY) & Gemini CLI ──
mkdir -p ~/.gemini/antigravity/skills ~/.gemini/config/skills ~/.gemini/skills
cp -r skills/marketing-reel-pro ~/.gemini/antigravity/skills/
cp -r skills/marketing-reel-pro ~/.gemini/config/skills/
cp -r skills/marketing-reel-pro ~/.gemini/skills/

# ── Install Skills for Codex / Universal .agents Standard ──
mkdir -p ~/.agents/skills
cp -r skills/marketing-reel-pro ~/.agents/skills/
```

### 3. How Any AI Should Execute `marketing-reel-pro`

1. **Read First**: Always read [`skills/marketing-reel-pro/SKILL.md`](skills/marketing-reel-pro/SKILL.md) and its three reference files in [`skills/marketing-reel-pro/references/`](skills/marketing-reel-pro/references/) before writing any HTML composition or running FFmpeg.
2. **Use the Deterministic CLI**: Run `python skills/marketing-reel-pro/scripts/reel_pipeline.py --help` and execute its 6 subcommands (`prepare-base`, `extract-matte`, `gen-captions`, `setup-layers`, `build-audio`, `composite`) with explicit `--output <report.json>` paths.
3. **Respect the Low-Memory Hardware Lock**: Never spawn preview servers (`npm run dev`, `npx hyperframes preview`) and never run two heavy render/FFmpeg processes in parallel. Always pass `--low-memory-mode` to `npx hyperframes render`.

---

## Stack Behind These Agents

| Layer | Technology |
|-------|------------|
| AI Runtimes | Google Antigravity · Claude Code · Codex · Hermes · MCP |
| Local AI Proxy | Node.js · claude CLI · OpenAI-compatible API |
| Persistent Memory | Hindsight · pgvector · BAAI/bge-small-en-v1.5 |
| Video Production | HyperFrames · GSAP 3.15 · FFmpeg (MCI Optical Flow + Alphamerge) · `rembg` (`u2netp`) |
| Audio Engineering | EBU R128 (`-14 LUFS`) · Sidechain Ducking · 105 Viral Neurological SFX Library |
| Distribution | Reels · TikTok · YouTube Shorts · YouTube Long-Form (LATAM / USA) |
| Language | English (primary) · Spanish LATAM |

---

## 👤 About the Author

**Nanoboy** — Technology Architect · Puerto Rico / LATAM · USA

> *"If it doesn't exist and I need it — I build it."*

[![GitHub](https://img.shields.io/badge/GitHub-365diascollaboration--prog-07071a?style=for-the-badge&logo=github&logoColor=white)](https://github.com/365diascollaboration-prog)
[![YouTube](https://img.shields.io/badge/YouTube-@365collaboration-07071a?style=for-the-badge&logo=youtube&logoColor=ff0000)](https://www.youtube.com/@365collaboration)

---

<div align="center">

> **English is the primary language of this repo.**
> **Los agentes y skills están documentados en inglés y español LATAM para que cualquier IA los ejecute sin fricción.**

<img src="https://capsule-render.vercel.app/api?type=waving&color=0d0d28,7c3aed,06b6d4&height=120&section=footer" width="100%"/>

</div>
