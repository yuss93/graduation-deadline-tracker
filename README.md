# Engineering the Future: Graduation Deadline Tracker (CCNY)

A high-performance, interactive T-minus countdown HUD and milestone command center built for the **Handshake AI Skills Studio Challenge**.

## Target Milestone
- **Target:** May 22, 2027 (B.E. in Computer Engineering, CCNY Commencement)

## Core Architecture & Features
- **Interactive Glassmorphic HUD (`index.html`):** Real-time second-by-second countdown clock, neon glowing card shadows, and smooth hover elevation effects.
- **Dynamic CRUD Task Manager:** Add custom milestones with automatic T-minus calculation, mark items complete (with strikethrough and green completion badges), or delete tasks.
- **Client-Side Persistence:** Fully saves tasks and checklist states using browser `localStorage`.
- **Python Automation & Wallpaper Generation:** Includes scripts for generating high-resolution vertical lock screen wallpapers (`1170x2532`).

## Tech Stack
- **Frontend:** HTML5, CSS3 (Glassmorphism, Flexbox, Custom Variables), Vanilla JavaScript (ES6+)
- **Automation / Export:** Python 3, Pillow, Playwright (Chromium Headless)
- **Version Control:** Git & GitHub

## Quick Start
```bash
# Open the interactive web dashboard locally
open index.html

# Run the Python wallpaper generator script
python3 countdown_lockscreen.py
