# AI Property Studio (Python starter)

A local Python app prototype for generating a property promo video from photos, then applying visual adjustments and exporting MP4.

## Requirements
- Windows 10/11
- Python 3.11–3.13 (Python 3.13 is intended to work; if a dependency install fails, use Python 3.12)
- Internet for the first dependency installation

## Quick start (Windows)
1. Extract this folder.
2. Double-click `run_windows.bat`.
3. Wait while dependencies install.
4. Your browser should open the local Streamlit app. If not, open the local URL shown in the terminal (usually `http://localhost:8501`).
5. Enter sample property details, upload JPG/PNG/WEBP photos and click **Generate my first video**.

## Manual setup
```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m streamlit run app.py
```

## What currently works
- Property detail form and photo upload
- Theme/aspect-ratio/resolution choices
- Brightness, contrast, saturation, sharpness and color filters
- Scene title cards and scene timing
- MP4 rendering using MoviePy + FFmpeg
- Built-in original ambient music generated locally, upload-your-own music option (MP3/WAV/M4A/AAC), music volume slider, and soundtrack looping/trimming
- Optional offline text-to-speech narration with an editable suggested property script (requires a working system voice)
- Five promo templates, color styles, scene fade/cut transition, and landscape/vertical/square/4:5 exports for social platforms
- MP4 download and project JSON export

## Honest scope note
This is the first runnable milestone, not yet a full CapCut/Premiere replacement. This is a local prototype. Narration uses the computer’s installed text-to-speech voices, not a cloud AI voice service; available voices and languages depend on Windows configuration. A true drag-and-drop multi-track timeline, per-scene editing, subtitles, and undo/redo remain future upgrades. The current scene planner uses templates and only supplied property facts.

## Troubleshooting
- If `py -3.13` is not found, install Python 3.13 or change the version in `run_windows.bat` to an installed Python version.
- If PowerShell blocks activation, use `run_windows.bat` instead.
- If MP4 rendering fails, copy the full error shown in the app/terminal and use it to troubleshoot.
- Test with a few small sample photos first; high-resolution images and longer videos take more time.
- Do not put API keys or real customer personal data in the project.


## Latest creative workflow additions

- **Listing Copywriter:** creates editable headline, property description, social caption/hashtags and WhatsApp enquiry text from the property details entered by the user. This local template-based tool does not use an external AI API; verify property claims before publishing.
- **Scene title editing:** edit the overlay title for each uploaded photo before rendering the video.
- **Social export presets:** quick format choices for Instagram Reels/Stories, YouTube Shorts, square/portrait feed posts, landscape video and lightweight 720p export.
- Existing local music generation/upload, voice-over, filters, animations, transitions, Property Finder and dark UI are retained in the source.

The source has been syntax-checked. Video rendering and browser interactions should still be tested on the target Windows machine.
