---
name: Tactical Logbook
colors:
  surface: '#101418'
  surface-dim: '#101418'
  surface-bright: '#36393e'
  surface-container-lowest: '#0b0f13'
  surface-container-low: '#181c20'
  surface-container: '#1c2024'
  surface-container-high: '#272a2f'
  surface-container-highest: '#31353a'
  on-surface: '#e0e2e9'
  on-surface-variant: '#bacbb9'
  inverse-surface: '#e0e2e9'
  inverse-on-surface: '#2d3136'
  outline: '#869486'
  outline-variant: '#3d4a3e'
  surface-tint: '#54e083'
  primary: '#ffffff'
  on-primary: '#003918'
  primary-container: '#73fd9c'
  on-primary-container: '#007438'
  inverse-primary: '#006d35'
  secondary: '#65d4f9'
  on-secondary: '#003543'
  secondary-container: '#159dc0'
  on-secondary-container: '#002e3b'
  tertiary: '#ffffff'
  on-tertiary: '#432c00'
  tertiary-container: '#ffdeac'
  on-tertiary-container: '#865c00'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#73fd9c'
  primary-fixed-dim: '#54e083'
  on-primary-fixed: '#00210c'
  on-primary-fixed-variant: '#005226'
  secondary-fixed: '#b7eaff'
  secondary-fixed-dim: '#65d4f9'
  on-secondary-fixed: '#001f28'
  on-secondary-fixed-variant: '#004e61'
  tertiary-fixed: '#ffdeac'
  tertiary-fixed-dim: '#ffba38'
  on-tertiary-fixed: '#281900'
  on-tertiary-fixed-variant: '#604100'
  background: '#101418'
  on-background: '#e0e2e9'
  surface-variant: '#31353a'
  surface-panel: '#101418'
  surface-well: '#000000'
  border-subtle: '#0f1622'
  border-active: '#203653'
  status-red: '#ef4444'
  label-muted: '#5d6b87'
typography:
  display-frequency:
    fontFamily: JetBrains Mono
    fontSize: 22px
    fontWeight: '900'
    letterSpacing: 0.1em
  headline-lg:
    fontFamily: JetBrains Mono
    fontSize: 26px
    fontWeight: '900'
    lineHeight: '1.2'
  headline-md:
    fontFamily: JetBrains Mono
    fontSize: 14px
    fontWeight: '900'
    letterSpacing: 0.2em
  body-md:
    fontFamily: JetBrains Mono
    fontSize: 12px
    fontWeight: '500'
    lineHeight: '1.5'
  label-caps:
    fontFamily: JetBrains Mono
    fontSize: 10px
    fontWeight: '800'
    letterSpacing: 0.12em
  label-micro:
    fontFamily: JetBrains Mono
    fontSize: 8px
    fontWeight: '700'
    letterSpacing: 0.05em
  telemetry:
    fontFamily: JetBrains Mono
    fontSize: 10px
    fontWeight: '900'
    letterSpacing: 0.1em
spacing:
  panel-pad: 0.75rem
  header-h: 48px
  footer-h: 32px
  sidebar-w: 480px
  gutter: 1px
---

## Brand & Style
The brand is defined by a "Tactical Hardware" aesthetic, evoking the feeling of specialized radio equipment, military-grade interfaces, or high-end developer instrumentation. It targets technical power users who require high-density information display and rapid data processing.

The design style is a hybrid of **Brutalism** and **Tactile Hardware**. It utilizes raw, high-contrast borders and monospaced typography characteristic of terminal interfaces, combined with "Hardware Grade Wells" (recessed, inset-shadow containers) that mimic physical panels. The emotional response is one of precision, reliability, and "mission-critical" authority. Glow effects are used sparingly as tactical indicators for active states or critical telemetry.

## Colors
The palette is rooted in a deep "void" black (`#05080c`) and obsidian surface tones. The primary interaction color is a high-vibrancy Emerald Green, used for success states and primary branding. Secondary Cyan and Tertiary Amber are reserved for data categorization and highlights.

A critical component of the color system is the "Glow" utility:
- **Emerald Glow:** `rgba(117, 255, 158, 0.6)` for primary actions.
- **Cyan Glow:** `rgba(108, 218, 255, 0.6)` for frequencies and navigation.
- **Amber Glow:** `rgba(255, 186, 56, 0.6)` for alerts and branding.

Neutral colors are used to create structural hierarchy, with `label-muted` providing low-priority metadata and `on-surface-variant` used for tactile button labels.

## Typography
The system exclusively uses **JetBrains Mono** to reinforce the technical, developer-centric feel. Typography is highly structured, using uppercase transformations and heavy letter spacing to create a "printed plate" look found on physical hardware.

- **Frequencies:** Use `display-frequency` with a Cyan glow.
- **Section Headers:** Use `headline-md` in all-caps with generous tracking.
- **Hardware Labels:** Use `label-caps` for all interactive triggers and button text.
- **Metadata:** Use `label-micro` for secondary data points and "recessed" info.

## Layout & Spacing
The layout uses a **Grid Gutter** philosophy where components are separated by 1px "gutters" (background-colored gaps) rather than traditional padding, creating a modular, tiled interface.

- **Fixed Rails:** The Header (48px) and Footer (32px) are fixed anchors.
- **Main Workspace:** A fluid grid system for central content.
- **Detailed Sidebar:** A fixed-width (480px) inspection panel for deep-dive data.
- **Information Density:** High density is achieved by using 1px gaps and `recessed-well` containers to group related technical fields without adding excessive vertical height.

## Elevation & Depth
Depth is created through **Hardware Grade Wells** and **Structural Outlines** rather than soft shadows:
- **Recessed Wells:** Uses `background: #000000` with an inset shadow `0 2px 4px rgba(0,0,0,0.8)` and a dark blue-grey border. This makes the element appear "milled" into the panel.
- **Raised Panels:** The `surface-panel` acts as the base plate.
- **Indicator Rails:** 3px thick solid color left-borders on wells indicate the "mode" or "category" (e.g., CW, Digital, RTTY).
- **Tactile Indicators:** Pulse animations and drop-shadows on small circular "LEDs" provide a sense of live telemetry.

## Shapes
The shape language is strictly **Sharp (0px)** or **Minimal (2px)**. 
- **Containers:** 0px rounding to maintain the rigid grid structure.
- **Hardware Buttons:** 2px rounding to provide a slight tactile feel without breaking the industrial aesthetic.
- **Status LEDs:** Circular (full rounding) to represent physical bulbs.
- **Input Fields:** Recessed rectangles with 0px rounding.

## Components
### Buttons (Hardware Grade)
Buttons are 32px tall, featuring a subtle vertical gradient (`#12161b` to `#080a0d`) and a 1px solid border. Hover states should transition the border and text color to the primary or themed color with a subtle outer glow.

### Recessed Inputs
Search and select inputs must be placed inside a `recessed-well`. They use no background or border themselves, inheriting the "carved" look of the well. Typography within is strictly `label-caps`.

### Technical Plates
Data is displayed on "Technical Plates"—recessed grids that combine a `label-micro` title with a bold value. Use `grid-gutters` within these plates to maintain the modular look.

### Mode Rails
Standardized color-coding for radio modes:
- **CW:** Primary Emerald (`#75ff9e`)
- **Digital:** Secondary Cyan (`#6cdaff`)
- **RTTY:** Tertiary Amber (`#ffba38`)
- **Alert/Live:** Red (`#ef4444`)

### Telemetry Footer
A 32px fixed bar at the bottom. It contains monochromatic labels and pulse-animated LEDs for "system ready" indicators.