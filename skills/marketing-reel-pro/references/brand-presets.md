# 365 Collaboration Brand Presets & 1080x1920 Safe-Zone Coordinates

## 1. Brand Color Palette (`365 Collaboration`)

| Token | Hex | RGB / RGBA | Usage |
| :--- | :--- | :--- | :--- |
| `--brand-cyan` | `#06b6d4` | `rgb(6, 182, 212)` | Primary brand accent, positive metrics, active keywords |
| `--brand-cyan-hi` | `#67e8f9` | `rgb(103, 232, 249)` | High-energy rim light, SVG glow strokes, sparkle stars |
| `--brand-purple` | `#7c3aed` | `rgb(124, 58, 237)` | Power keywords (`DOMINARLO`, `AUTOMATIZACIONES`, `MULTIPLICADO`) |
| `--brand-purple-hi` | `#a78bfa` | `rgb(167, 139, 250)` | Secondary gradient stops and halo blooms |
| `--danger-red` | `#ff3b5c` | `rgb(255, 59, 92)` | Pain points (`NO FACTURA?`, `100% CARGA`, `RIVAL`, revenue drop) |
| `--emerald-win` | `#10b981` | `rgb(16, 185, 129)` | Freedom / solution state (`LIBRE 0%`, ROI checkmarks) |
| `--obsidian-bg` | `#07071a` | `rgba(10, 10, 32, 0.90)` | Glassmorphic card plates (isolates text from busy backgrounds) |
| `--snow-white` | `#f1f5f9` | `rgb(241, 245, 249)` | Base kinetic caption text and primary headlines |

---

## 2. Typography System

- **Display / Hero / Kinetic Captions**: `Anton` (`assets/fonts/Anton-Regular.ttf`), uppercase, tight line-height (`0.98 - 1.04`).
- **UI Labels / Badges / Data Cards / DM Chat**: `Montserrat` (`700`, `800`, `900`), uppercase for chips (`letter-spacing: 0.08em - 0.20em`), sentence/uppercase for chat bubbles.
- **Hard Rule**: Never use em-dashes (`—`) or en-dashes (`–`) in visible on-screen text.

---

## 3. Vertical 9:16 (`1080x1920`) Spatial Architecture & Face Protection

```text
+---------------------------------------------------+ y = 0
|                 TOP UI MARGIN                     |
|  y: 140 - 250   TOP CROWN ZONE (L1 Behind / L3)   |
|                 - Giant Hero Line 1 (¿TU NEGOCIO) |
|                 - Top Progress Rails (01/04)      |
|                 - Overhead Gauges (CARGA 100%)    |
+---------------------------------------------------+ y = 250
|                                                   |
|  y: 250 - 520   SPEAKER HEAD & GLASSES ZONE       |
|                 - NEVER place front text here!    |
|                 - Side hubs/medallions stay       |
|                   at x < 310 or x > 770           |
|                                                   |
+---------------------------------------------------+ y = 520
|  y: 520 - 710   SHOULDERS & UPPER TORSO (L1)      |
|                 - Barbell shaft behind shoulders  |
|                 - Left/Right service medallions   |
+---------------------------------------------------+ y = 710
|  y: 710 - 1115  CHEST & CARD ZONE (L3 Front)      |
|                 - y: 720  Secondary Punchline     |
|                           (e.g. NO FACTURA?)      |
|                 - y: 904  Data Cards (INGRESOS)   |
+---------------------------------------------------+ y = 1115
|  y: 1120 - 1330 KINETIC CAPTIONS RAIL (L3 Front)  |
|                 - 2 to 4 words per screen         |
|                 - Never touches chin (y < 520)    |
|                 - Auto-suppressed during final    |
|                   CTA DM card response            |
+---------------------------------------------------+ y = 1350
|  y: 1350 - 1920 PLATFORM UI SAFE ZONE             |
|                 (Reels / TikTok buttons & description) |
+---------------------------------------------------+ y = 1920
```

---

## 4. Base Footage Color Grade & 60 fps Optical Flow Preset

Apply this exact FFmpeg filter chain when building `work/base/base60.mp4`:

```text
scale=1080:1920:flags=lanczos,
minterpolate=fps=60:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1,
eq=contrast=1.06:saturation=1.12:brightness=0.01,
unsharp=5:5:0.75:5:5:0.0,
vignette=PI/7,
format=yuv420p
```
