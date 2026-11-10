# 365 Collaboration Viral SFX Catalog & Audio Engineering Rules

## Default SFX Library Location

```text
C:\Users\infon\Desktop\editor de video - romotions\my-video\public\click.mp3\
```

Contains **105 curated viral sound effects** (`.mp3` and `.wav`) organized by psychological retention function.

---

## Psychological SFX Mapping by Scene Beat

Use 2 to 5 layered SFX cues per scene in `scenes.json`. Never exceed `volume: 0.35` on individual SFX so the master voiceover remains dominant.

| Narrative Beat / Visual Action | Recommended Files in Library | Gain (`volume`) | Purpose |
| :--- | :--- | :--- | :--- |
| **Hook Impact (0.0s - 0.5s)** | `riser-hit-sfc.mp3`, `cinematic-impact-climax-intro.mp3`, `bass-drop.mp3` | `0.26 - 0.32` | Stops the scroll in the first 300ms |
| **Glitch / Tech Reveal** | `glitch-1.mp3`, `glitch-2.mp3`, `digital-beep.mp3`, `hacker-data.mp3` | `0.20 - 0.25` | Signals chromatic aberration or HUD appearance |
| **Card / Badge Entrance** | `whoosh-1.mp3`, `swoosh-fast.mp3`, `air-woosh.mp3`, `pop-up.mp3` | `0.20 - 0.26` | Gives physical weight to cards entering L1/L3 |
| **Money / ROI / Revenue Up** | `cash-register.mp3`, `coin-drop.mp3`, `ding-correct.mp3`, `level-up.mp3` | `0.24 - 0.30` | Dopamine reinforcement on positive numbers (`X2`, `+$`) |
| **Money Loss / Crash / Rival** | `glass-shatter.mp3`, `error-buzz.mp3`, `downfall-riser.mp3`, `thud-heavy.mp3` | `0.22 - 0.28` | Visceral tension when showing revenue drop or competition |
| **Urgency / Time Running Out** | `clock-ticking.mp3`, `stopwatch-tick.mp3`, `heartbeat-low.mp3` | `0.18 - 0.22` | Subconscious urgency under "sobrevivir" / "competencia" |
| **Heavy Weight / Barbell Release** | `metal-clang.mp3`, `heavy-drop.mp3`, `shatter-release.mp3` | `0.25 - 0.30` | Anchors physical metaphor in `peso-operativo` |
| **Engine / Tachometer Rev** | `riser-cyber.mp3`, `power-up-synth.mp3`, `electric-hum.mp3` | `0.22 - 0.28` | Drives tachometer needle sweep in `motor-tech` |
| **CTA / Typing / DM Send** | `keyboard-typing.mp3`, `mouse-click.mp3`, `notification-bell.mp3`, `pop-clean.mp3` | `0.24 - 0.30` | Triggers action on `COMENTA "CRECER"` |

---

## Automatic Category Fallback Table

If a scene JSON references a descriptive cue name that differs slightly from a filename on disk, `reel_pipeline.py build-audio` automatically resolves it by substring/category matching against the 105 files in `click.mp3/`:

- **`whoosh` / `swoosh` / `swipe`** -> matches `*whoosh*`, `*swoosh*`, `*swish*`
- **`riser` / `build`** -> matches `*riser*`, `*rise*`, `*swell*`
- **`boom` / `hit` / `impact` / `slam`** -> matches `*impact*`, `*boom*`, `*hit*`, `*cinematic*`
- **`click` / `tap` / `button`** -> matches `*click*`, `*tap*`, `*switch*`
- **`pop` / `bubble`** -> matches `*pop*`, `*bubble*`
- **`cash` / `coin` / `money`** -> matches `*cash*`, `*coin*`, `*cha-ching*`
- **`ding` / `bell` / `notify`** -> matches `*ding*`, `*bell*`, `*notif*`, `*correct*`
- **`glitch` / `digital` / `tech`** -> matches `*glitch*`, `*digital*`, `*cyber*`, `*beep*`
- **`tick` / `clock`** -> matches `*tick*`, `*clock*`, `*watch*`
- **`type` / `key`** -> matches `*key*`, `*type*`, `*typing*`

---

## Master Mix Chain Specification (`-14 LUFS`)

1. **Master Voiceover (`master_voice.wav`)**:
   - `highpass=f=80,equalizer=f=220:t=q:w=1.2:g=-2.5,equalizer=f=3200:t=q:w=1.0:g=2.5,acompressor=threshold=-18dB:ratio=3:attack=8:release=120:makeup=3dB`
2. **Musical Bed (`pad.wav` + `drumloop.wav`)**:
   - Warm A-minor9 stereo pad (`220 Hz`, `329.6 Hz`, `392 Hz`, `493.9 Hz`, `587.3 Hz`) + `85 BPM` soft kick/hat pulse.
   - Mixed at low bed level (`0.12 - 0.16`) and ducked whenever voice energy is present.
3. **Final Loudness Normalization**:
   - `loudnorm=I=-14:TP=-1.2:LRA=9` exported at `48000 Hz` stereo WAV (`work/mix_v2.wav`), then encoded to `AAC 192 kbps` in the final MP4.
