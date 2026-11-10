# Agency Composition Patterns (`L1 Behind` & `L3 Front`)

## 1. Split Hero Hook (`hook-behind.html` + `hook-front.html`)

When opening a vertical ad with a two-part question (e.g., `¿TU NEGOCIO` / `NO FACTURA?`):
- **Line 1 (`¿TU NEGOCIO`)** goes in **`L1 Behind`** at `top: 150px; font-size: 176px;` so the top of the speaker's hair slightly overlaps the bottom of the letters, creating immediate 3D depth.
- **Line 2 (`NO FACTURA?`)** goes in **`L3 Front`** at `top: 722px; font-size: 162px; color: #ff3b5c;` across the speaker's upper chest (well below the chin at `y ~ 480px`), directly above the glassmorphic revenue crash card (`top: 904px`).
- **Why**: Placing Line 2 in `L1 Behind` at `top: 325px` hides the middle letters behind the speaker's sunglasses/face.

---

## 2. Alternating Left/Right Service Medallions (`servicios.html` in `L1 Behind`)

When enumerating 3 to 4 services while the speaker talks in the center:
- Alternate sides (`L` at `left: 5px`, `R` at `left: 775px`) with `300x300` circular dark plates (`top: 360px`) so the speaker's head (`x: 340..740`) stays 100% clear.
- Place a progress rail (`01 / 04` + 4 progress segments) in the top crown zone (`top: 190px`).
- **Curtain Reveal Padding Rule**: When revealing multi-line `Anton` labels inside `.sv-ln { overflow: hidden }`, always use generous bottom padding (`padding: 28px 6px 26px; margin-top: -24px;`) so descending strokes or diacritics (`CAMPAÑAS ESTRATÉGICAS`) never clip by 2px at the bottom.
- **Card Exit Timing Rule**: Ensure card $N$'s exit (`c.out + 0.34`) completes **before** card $N+1$'s entrance (`c_next.t0`) so no ghost card lingers on the opposite side.

---

## 3. Barbell / Physical Metaphor Behind Shoulders (`peso-operativo.html` in `L1 Behind`)

- Place the barbell bar at `y: 590px` across the canvas (`x: 60..1020`) in `L1 Behind`. Because `L2` (`person` matte) composites on top of `L1`, the bar naturally passes **behind the speaker's neck and shoulders**, while the neon weight plates (`x: 60..240` and `x: 840..1020`) flank both arms.
- Place the circular load gauge (`CARGA 100%` -> `LIBRE 0%`) at `top: 205px` (crown zone above the head).
- **Counter Transition Rule**: When crossfading `#pw-t100` (`100%`) to `#pw-t0` (`0%`), explicitly tween `#pw-t100` to `opacity: 0, scale: 0.6` while tweening `#pw-t0` from `opacity: 0, scale: 1.5` to `opacity: 1, scale: 1` so both numbers never remain co-visible.

---

## 4. Client Tug-of-War Arches (`competencia.html` in `L1 Behind`)

- Place `TU NEGOCIO` hub at `(165, 320)` and `RIVAL` hub at `(915, 320)` with top pills (`#cp-chip1`, `#cp-chip2`) at `top: 148px; font: 900 29px/1 'Montserrat'`.
- Animate customer avatars along a quadratic Bezier arch (`controlPoint = [540, 70 + 30 * (i % 3)]`) so they fly **over the speaker's head** from left to right (turning red) and then snap back to `TU NEGOCIO` (turning cyan) when the shockwave fires.

---

## 5. Interactive DM Closing Card (`cta-crecer-front.html` in `L3 Front`)

- Place the glassmorphic DM card at `left: 60px; width: 960px; top: 880px` in `L3 Front`.
- Sequence:
  1. Input field types `CRECER` character-by-character with keyboard SFX cues.
  2. Cursor clicks the send button (`scale: 0.88` -> `1.08` + ripple).
  3. Instant automated reply bubble slides in (`TE ENVIAMOS LA SOLUCIÓN EXACTA`).
- **Caption Cutoff Rule**: Suppress bottom captions (`captions.html`) starting `0.15s` before the DM reply bubble animates so there is zero duplicate text at the bottom of the screen.

---

## 6. HyperFrames Lint Zero-Warning Rules

1. **No `clip-path: polygon(...)` or `radial-gradient` pseudo-elements in high-count tracks (`captions.html`)**:
   - Use inline `<svg viewBox="0 0 24 24"><path d="M12 0 L15 9 L24 12 L15 15 L12 24 L9 15 L0 12 L9 9 Z" fill="#67e8f9"/></svg>` for sparkles and `text-shadow` for glow.
2. **No `svg_round_cap_hidden_dash`**:
   - Any `<path>` or `<line>` with `stroke-linecap="round"` that starts hidden must use `pathLength="100"` with `stroke-dasharray: 100 120; stroke-dashoffset: 110; opacity: 0`, setting `opacity: 1` only when the draw tween begins.
3. **No `overlapping_gsap_tweens`**:
   - Never schedule two tweens on the same target and property (e.g., `filter` or `opacity`) with overlapping `[start, start + duration]` intervals; use a single `keyframes: [...]` tween or non-overlapping start times.
4. **Deterministic Randomness**:
   - Always use a seeded LCG (`seed = (seed * 1664525 + 1013904223) >>> 0; return seed / 4294967296;`) instead of `Math.random()`.
