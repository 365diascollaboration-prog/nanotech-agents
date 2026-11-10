# NANOTECH AGENTS — AI Operator Instructions (`AGENTS.md` / `CLAUDE.md`)

When any AI coding assistant (Google Antigravity, Claude Code, OpenAI Codex, Hermes Agent, Gemini CLI, OpenCode, Cursor) operates inside or uses tools from this repository, follow these rules unconditionally:

## 1. Selecting the Right Video Production Tool

- **Vertical 9:16 Commercials, Reels, TikToks & Shorts (`1080x1920 @ 60 fps`)**:
  - Read [`skills/marketing-reel-pro/SKILL.md`](skills/marketing-reel-pro/SKILL.md) and [`agents/marketing-reel-pro.md`](agents/marketing-reel-pro.md) FIRST.
  - Use the deterministic Python CLI [`skills/marketing-reel-pro/scripts/reel_pipeline.py`](skills/marketing-reel-pro/scripts/reel_pipeline.py) (`prepare-base`, `extract-matte`, `gen-captions`, `setup-layers`, `build-audio`, `composite`).
  - Supports **Mode A (`multi-shot`)** (master voiceover + separate scene clips with word-level lip-sync & MCI 60 fps optical flow) and **Mode B (`single-video`)** (single continuous talking-head clip).
  - Enforces **4-layer depth compositing (`L0 Base` -> `L1 Behind` -> `L2 AI Subject Matte` -> `L3 Front + Kinetic Captions`)** and `-14 LUFS` sidechain-ducked audio with 50-60 viral SFX cues.
- **Horizontal 16:9 YouTube Episodes (`1920x1080` 3-Column or `1280x720` Overlay)**:
  - Read [`agents/video-producer-latam.md`](agents/video-producer-latam.md).

## 2. Non-Negotiable Hardware & Quality Rules

1. **Low-Memory Hardware Protection (7-8 GB RAM Safe)**:
   - Never start preview/dev servers (`npm run dev`, `npx hyperframes preview`).
   - Run strictly **ONE** heavy render or FFmpeg process at a time.
   - Always pass `--low-memory-mode` to `npx hyperframes render`.
2. **Zero Face-Collision Rule (`1080x1920`)**:
   - The speaker's face/sunglasses occupy `y: 250px – 520px`. Never cover the eyes with front text (`L3`) or place short unreadable words directly behind the head in `L1`.
   - Split two-part hooks: Line 1 in `L1 Behind` (`top: 150px` above the head) and Line 2 in `L3 Front` (`top: 722px` across the chest, right above the `top: 904px` data card).
   - Keep kinetic captions in `y: 1120px – 1330px` and cut them off (`--cta-cutoff`) before the final interactive DM card animates.
3. **Zero HyperFrames Lint Warnings**:
   - Use inline `<svg>` stars instead of `clip-path: polygon(...)` on caption words.
   - Use `pathLength="100"`, `stroke-dasharray: 100 120; stroke-dashoffset: 110; opacity: 0` on hidden `stroke-linecap="round"` SVG paths.
   - Use seeded deterministic PRNGs instead of `Math.random()`.
   - Zero em-dashes (`—`) or en-dashes (`–`) in visible on-screen text.
