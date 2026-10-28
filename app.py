import os
import json
import math
import tempfile
import wave
from urllib.parse import quote_plus
from pathlib import Path
import streamlit as st
from PIL import Image, ImageEnhance, ImageFilter, ImageOps, ImageDraw, ImageFont
import numpy as np

APP_DIR = Path(__file__).parent
OUTPUT_DIR = APP_DIR / "outputs"
PROJECT_DIR = APP_DIR / "projects"
OUTPUT_DIR.mkdir(exist_ok=True)
PROJECT_DIR.mkdir(exist_ok=True)

st.set_page_config(page_title="AI Property Studio", page_icon="🏡", layout="wide")

CUSTOM_CSS = """
<style>
:root {
  --bg:#080d12; --panel:#111923; --panel2:#151f2a; --ink:#edf3fa;
  --muted:#93a4b7; --line:#263545; --green:#36d6a0; --green2:#14b884;
  --gold:#e9c878; --blue:#6ea8ff;
}
.stApp { background: radial-gradient(ellipse at 85% -5%, #173b3a 0%, #0b121a 38%, #080d12 78%); color:var(--ink); }
[data-testid="stAppViewContainer"] > .main { background:transparent; }
[data-testid="stMainBlockContainer"] { max-width:1540px; padding-top:1.5rem; padding-bottom:3rem; }
[data-testid="stHeader"] { background:rgba(8,13,18,.92); }
[data-testid="stToolbar"] { right:1rem; }
[data-testid="stSidebar"] { background:linear-gradient(180deg,#0d171f 0%,#101e28 58%,#0b151d 100%); border-right:1px solid #253542; }
[data-testid="stSidebar"] * { color:#eaf2f8; }
[data-testid="stSidebar"] [data-testid="stRadio"] label { background:#14232d; border:1px solid #263c49; border-radius:12px; padding:9px 12px; margin:4px 0; transition:all .18s ease; }
[data-testid="stSidebar"] [data-testid="stRadio"] label:hover { background:#1a3438; border-color:#36d6a0; }
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h2 { font-size:1.4rem; letter-spacing:-.03em; color:#fff; }
.hero { position:relative; overflow:hidden; padding:32px 36px 34px; border-radius:24px; background:linear-gradient(115deg,#14242d 0%,#173c3a 56%,#155a49 100%); border:1px solid #31564f; margin:0 0 26px 0; box-shadow:0 20px 55px rgba(0,0,0,.28); }
.hero:after { content:""; position:absolute; width:260px; height:260px; border:1px solid rgba(75,230,174,.22); border-radius:50%; right:-65px; top:-130px; box-shadow:0 0 0 28px rgba(75,230,174,.045),0 0 0 58px rgba(75,230,174,.025); pointer-events:none; }
.hero .eyebrow { display:inline-block; text-transform:uppercase; letter-spacing:.16em; color:#75edc0; font-weight:800; font-size:.72rem; margin-bottom:10px; }
.hero h1 { margin:0; font-size:clamp(2rem,3.4vw,3rem); line-height:1.2; color:#fff; letter-spacing:-.05em; }
.hero p { max-width:850px; color:#d0e5df; margin:12px 0 0; font-size:1.02rem; line-height:1.65; }
.small-muted { color:var(--muted); font-size:.9rem; }
/* Dark cards and work areas */
[data-testid="stVerticalBlockBorderWrapper"] { border:1px solid #273846 !important; border-radius:18px !important; background:linear-gradient(145deg,rgba(20,31,42,.96),rgba(14,23,32,.96)); box-shadow:0 12px 30px rgba(0,0,0,.13); }
[data-testid="stMetric"] { background:#121e28; padding:16px 18px; border-radius:16px; border:1px solid #293b49; box-shadow:0 8px 22px rgba(0,0,0,.13); }
[data-testid="stMetricLabel"], [data-testid="stCaptionContainer"] { color:var(--muted) !important; }
[data-testid="stMetricValue"] { color:#f5fbff !important; }
[data-testid="stForm"], [data-testid="stExpander"] { border-radius:15px; border-color:#2b3c4b; background:#101923; }
[data-testid="stExpander"] summary { color:#edf3fa !important; }
.stButton>button, .stDownloadButton>button, .stLinkButton>a { border-radius:12px; min-height:2.7rem; padding:.55rem 1rem; font-weight:700; letter-spacing:.005em; border:1px solid #344958; background:#1a2935; color:#edf7fb; transition:all .18s ease; box-shadow:0 4px 12px rgba(0,0,0,.12); }
.stButton>button:hover, .stDownloadButton>button:hover, .stLinkButton>a:hover { transform:translateY(-2px); background:#223a43; border-color:#36d6a0; color:#fff; box-shadow:0 8px 20px rgba(20,184,132,.14); }
.stButton>button[kind="primary"], .stDownloadButton>button[kind="primary"] { background:linear-gradient(105deg,#14b884,#36d6a0); border:1px solid #49e4b1; color:#06150f; box-shadow:0 8px 24px rgba(20,184,132,.22); }
.stButton>button[kind="primary"] p { color:#06150f !important; font-weight:800; }
.stButton>button[kind="primary"]:hover { background:linear-gradient(105deg,#36d6a0,#70edc2); color:#06150f; box-shadow:0 10px 28px rgba(20,184,132,.3); }
[data-testid="stTextInput"] input, [data-testid="stNumberInput"] input, [data-testid="stTextArea"] textarea { border-radius:11px; border:1px solid #2c4050; background:#0d151e; color:#f2f7fc; }
[data-testid="stSelectbox"] div[data-baseweb="select"] > div, [data-testid="stMultiSelect"] div[data-baseweb="select"] > div { border-radius:11px; border:1px solid #2c4050; background:#0d151e; color:#f2f7fc; }
[data-testid="stSelectbox"] div[data-baseweb="select"] *, [data-testid="stMultiSelect"] div[data-baseweb="select"] * { color:#f2f7fc; }
[data-testid="stFileUploader"] section { background:linear-gradient(145deg,#121f29,#0d171f); border:1.5px dashed #3a6b65; border-radius:16px; padding:13px; }
[data-testid="stFileUploader"] section:hover { border-color:#36d6a0; background:#14252b; }
[data-testid="stFileUploader"] button { border-radius:10px !important; border:1px solid #42625f !important; background:#183a35 !important; color:#eafff6 !important; font-weight:700 !important; }
[data-testid="stRadio"] [role="radiogroup"] { gap:8px; }
[data-testid="stRadio"] [role="radiogroup"] label { background:#121e28; border:1px solid #2a3d4b; border-radius:11px; padding:7px 12px; }
[data-testid="stCheckbox"] label { color:#eaf2f8; }
[data-testid="stImage"] img { border-radius:13px; border:1px solid #2b3d4b; }
[data-testid="stMarkdownContainer"] p, [data-testid="stMarkdownContainer"] li { color:#d8e2ec; }
h1,h2,h3,h4 { color:#f4f8fc; letter-spacing:-.035em; }
h2 { font-size:1.6rem !important; margin-top:.45rem; }
h3 { font-size:1.22rem !important; }
label, [data-testid="stWidgetLabel"] p { color:#dce7f0 !important; }
hr { border-color:#263744; }
div[data-testid="stAlert"] { border-radius:13px; border-width:1px; }
[data-testid="stProgressBar"] > div > div { background:linear-gradient(90deg,#14b884,#6be8bd); }
[data-testid="stSlider"] [role="slider"] { background:#36d6a0; }
@media (max-width: 850px) { .hero { padding:24px 22px; border-radius:19px; } [data-testid="stMainBlockContainer"] { padding-top:1rem; } }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

if "project" not in st.session_state:
    st.session_state.project = {
        "name": "Sunrise Luxury Apartment",
        "location": "Mohali, Punjab",
        "price": "₹85 lakh",
        "property_type": "Apartment",
        "bedrooms": 3,
        "bathrooms": 2,
        "area": "1450 sq. ft.",
        "features": "Modular kitchen, balcony, parking, 24/7 security",
        "contact": "+91 98765 43210",
        "cta": "Book your site visit today",
        "theme": "Luxury Gold",
        "duration": 4,
        "resolution": "1080p",
        "aspect": "16:9",
        "brightness": 1.0,
        "contrast": 1.0,
        "saturation": 1.0,
        "sharpness": 1.0,
        "filter": "Original",
        "transition": "Fade",
        "voiceover": False,
        "voice_script": "",
        "template": "Luxury Showcase",
        "animation": "None",
        "music": "Built-in free music",
        "music_volume": 0.22,
    }

st.markdown("""
<div class="hero">
  <div class="eyebrow">Your real-estate creative workspace</div>
  <h1>🏡 AI Property Studio</h1>
  <p>Turn property photos into polished promos, explore nearby projects, and build your next listing campaign.</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## Studio")
    page = st.radio("Workspace", ["Create Video", "Listing Copywriter", "Property Finder", "Visual Editor", "Project & Export", "How to use"])
    st.markdown("---")
    st.markdown("**Build status**")
    st.caption("Creative tools • property discovery • video export")

p = st.session_state.project

def get_font(size):
    candidates = [
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/Library/Fonts/Arial.ttf"
    ]
    for f in candidates:
        if os.path.exists(f):
            try:
                return ImageFont.truetype(f, size=size)
            except Exception:
                pass
    return ImageFont.load_default()

def fit_cover(img, size):
    return ImageOps.fit(img.convert("RGB"), size, method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))

def apply_adjustments(img, brightness, contrast, saturation, sharpness, filter_name):
    img = img.convert("RGB")
    img = ImageEnhance.Brightness(img).enhance(brightness)
    img = ImageEnhance.Contrast(img).enhance(contrast)
    img = ImageEnhance.Color(img).enhance(saturation)
    img = ImageEnhance.Sharpness(img).enhance(sharpness)
    if filter_name == "Warm":
        overlay = Image.new("RGB", img.size, (255, 180, 90))
        img = Image.blend(img, overlay, 0.10)
    elif filter_name == "Cool":
        overlay = Image.new("RGB", img.size, (90, 150, 255))
        img = Image.blend(img, overlay, 0.08)
    elif filter_name == "Luxury Gold":
        img = ImageEnhance.Contrast(img).enhance(1.08)
        overlay = Image.new("RGB", img.size, (245, 190, 105))
        img = Image.blend(img, overlay, 0.07)
    elif filter_name == "Matte":
        img = ImageEnhance.Contrast(img).enhance(0.82)
        img = ImageEnhance.Brightness(img).enhance(1.04)
    elif filter_name == "Black & White":
        img = ImageOps.grayscale(img).convert("RGB")
    elif filter_name == "Soft":
        img = img.filter(ImageFilter.GaussianBlur(radius=0.35))
    return img

def draw_wrapped(draw, text, font, max_width):
    words = text.split()
    lines, line = [], ""
    for word in words:
        test = (line + " " + word).strip()
        if draw.textbbox((0,0), test, font=font)[2] <= max_width:
            line = test
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines

def render_scene(image, title, subtitle, p, size, idx, total):
    img = fit_cover(image, size)
    img = apply_adjustments(img, p["brightness"], p["contrast"], p["saturation"], p["sharpness"], p["filter"])

    # Dark translucent bottom gradient keeps the text readable.
    overlay = Image.new("RGBA", size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    band_h = int(size[1] * 0.38)
    for y in range(size[1] - band_h, size[1]):
        alpha = int(190 * ((y - (size[1] - band_h)) / max(1, band_h)))
        od.line((0, y, size[0], y), fill=(5, 10, 18, alpha))
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    d = ImageDraw.Draw(img)

    margin = int(size[0] * 0.055)
    title_font = get_font(max(22, int(size[0] * 0.042)))
    sub_font = get_font(max(14, int(size[0] * 0.022)))
    tag_font = get_font(max(12, int(size[0] * 0.018)))

    d.rounded_rectangle(
        (margin, margin, margin + int(size[0] * 0.25), margin + int(size[1] * 0.055)),
        radius=12, fill=(18, 28, 42)
    )
    d.text((margin + 12, margin + 7), f"PROPERTY  •  {idx+1:02d}/{total:02d}",
           font=tag_font, fill=(245, 196, 111))

    max_text_width = size[0] - 2 * margin
    title_lines = draw_wrapped(d, title, title_font, max_text_width)[:2]
    subtitle_lines = draw_wrapped(d, subtitle, sub_font, max_text_width)[:2] if subtitle else []

    # Calculate real font heights instead of using fixed increments. This prevents
    # title/subtitle lines from touching or overlapping at 1080p and vertical sizes.
    title_gap = max(6, int(size[1] * 0.012))
    subtitle_gap = max(4, int(size[1] * 0.006))
    title_heights = [max(1, d.textbbox((0, 0), line, font=title_font)[3] -
                         d.textbbox((0, 0), line, font=title_font)[1]) for line in title_lines]
    subtitle_heights = [max(1, d.textbbox((0, 0), line, font=sub_font)[3] -
                            d.textbbox((0, 0), line, font=sub_font)[1]) for line in subtitle_lines]

    title_block = sum(title_heights) + title_gap * max(0, len(title_lines) - 1)
    subtitle_block = sum(subtitle_heights) + subtitle_gap * max(0, len(subtitle_lines) - 1)
    section_gap = max(8, int(size[1] * 0.018)) if subtitle_lines else 0
    total_block = title_block + section_gap + subtitle_block
    y = size[1] - margin - total_block

    for line, line_height in zip(title_lines, title_heights):
        d.text((margin, y), line, font=title_font, fill="white",
               stroke_width=1, stroke_fill=(0, 0, 0))
        y += line_height + title_gap

    if subtitle_lines:
        y += section_gap - title_gap
        for line, line_height in zip(subtitle_lines, subtitle_heights):
            d.text((margin, y), line, font=sub_font, fill=(239, 242, 247))
            y += line_height + subtitle_gap

    return img

def create_free_music(output_path, duration, sample_rate=22050):
    """Create an original, royalty-free ambient instrumental locally (no download/API)."""
    import numpy as np
    total = max(1, int(duration * sample_rate))
    audio = np.zeros(total, dtype=np.float32)
    # Gentle major-key chord progression, with soft plucked notes and no samples.
    chords = [(261.63, 329.63, 392.00), (220.00, 261.63, 329.63),
              (174.61, 220.00, 261.63), (196.00, 246.94, 293.66)]
    beat = 60.0 / 88.0
    for chord_idx, start in enumerate(np.arange(0, duration, beat * 4)):
        chord = chords[chord_idx % len(chords)]
        for note_idx, freq in enumerate(chord):
            t0 = start + note_idx * 0.035
            n0 = int(t0 * sample_rate)
            n = min(int(1.65 * sample_rate), total - n0)
            if n <= 0:
                continue
            t = np.arange(n, dtype=np.float32) / sample_rate
            env = np.exp(-2.5 * t) * np.minimum(1.0, t * 35)
            tone = (np.sin(2*np.pi*freq*t) + 0.25*np.sin(2*np.pi*freq*2*t)) * env
            audio[n0:n0+n] += tone * 0.11
        # quiet warm bass pulse on each chord
        n0 = int(start * sample_rate)
        n = min(int(2.0 * sample_rate), total - n0)
        if n > 0:
            t = np.arange(n, dtype=np.float32) / sample_rate
            audio[n0:n0+n] += 0.10 * np.sin(2*np.pi*(chord[0]/2)*t) * np.exp(-2.0*t)
    # Soft fade in/out and normalize safely.
    fade = min(int(1.2 * sample_rate), total // 2)
    if fade:
        audio[:fade] *= np.linspace(0, 1, fade, dtype=np.float32)
        audio[-fade:] *= np.linspace(1, 0, fade, dtype=np.float32)
    peak = float(np.max(np.abs(audio))) if total else 0
    if peak > 0:
        audio = audio / max(1.0, peak * 1.4)
    pcm = (np.clip(audio, -1, 1) * 32767).astype(np.int16)
    with wave.open(str(output_path), 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(pcm.tobytes())

def create_video(images, scene_titles, p, output_path, fps=24, music_path=None, music_volume=0.22, voice_path=None):
    try:
        from moviepy import ImageClip, concatenate_videoclips, vfx, AudioFileClip, concatenate_audioclips, CompositeAudioClip
    except Exception:
        from moviepy.editor import ImageClip, concatenate_videoclips, vfx, AudioFileClip, concatenate_audioclips, CompositeAudioClip
    if p["aspect"] == "9:16":
        size = (720, 1280)
    elif p["aspect"] == "1:1":
        size = (1080, 1080)
    elif p["aspect"] == "4:5":
        size = (864, 1080)
    else:
        size = (1920, 1080) if p["resolution"] == "1080p" else (1280, 720)

    clips = []
    total = len(images)
    for i, image in enumerate(images):
        title = scene_titles[i] if i < len(scene_titles) else p["name"]
        subtitle = p["price"] if i == 0 else (p["location"] if i == total-1 else p["features"])
        frame = render_scene(image, title, subtitle, p, size, i, total)
        frame_path = OUTPUT_DIR / f"scene_{i+1:02d}.jpg"
        frame.save(frame_path, quality=94)
        clip = ImageClip(np.array(frame)).with_duration(float(p["duration"]))
        # Optional per-scene animation. Keep every output frame at the original size.
        animation = p.get("animation", "None")
        if animation in ("Slow Zoom In", "Slow Zoom Out"):
            try:
                from PIL import Image as PILImage
                base_frame = np.array(frame)
                base_h, base_w = base_frame.shape[:2]
                def zoom_frame(get_frame, t, _anim=animation, _duration=float(p["duration"]), _w=base_w, _h=base_h):
                    raw = get_frame(t)
                    progress = min(1.0, max(0.0, t / max(0.01, _duration)))
                    scale = (1.0 + 0.10 * progress) if _anim == "Slow Zoom In" else (1.10 - 0.10 * progress)
                    new_w, new_h = max(_w, int(_w * scale)), max(_h, int(_h * scale))
                    pil = PILImage.fromarray(raw).resize((new_w, new_h), PILImage.Resampling.LANCZOS)
                    left = (new_w - _w) // 2
                    top = (new_h - _h) // 2
                    return np.array(pil.crop((left, top, left + _w, top + _h)))
                clip = clip.transform(zoom_frame)
            except Exception:
                pass
        if p["transition"] == "Fade":
            try:
                clip = clip.with_effects([vfx.FadeIn(0.35), vfx.FadeOut(0.25)])
            except Exception:
                pass
        clips.append(clip)
    final = concatenate_videoclips(clips, method="compose")
    audio_track = None
    voice_track = None
    audio_mix = None
    audio_parts = []
    try:
        if music_path:
            audio_track = AudioFileClip(str(music_path))
            # Loop short music files to cover the full video; trim longer files.
            if audio_track.duration < final.duration:
                repeats = int(math.ceil(final.duration / max(0.1, audio_track.duration)))
                audio_parts = [AudioFileClip(str(music_path)) for _ in range(repeats)]
                audio_track = concatenate_audioclips(audio_parts).subclipped(0, final.duration)
            else:
                audio_track = audio_track.subclipped(0, final.duration)
            try:
                audio_track = audio_track.with_volume_scaled(float(music_volume))
            except Exception:
                audio_track = audio_track.volumex(float(music_volume))
            # Music is mixed with narration below when both are enabled.
        audio_layers = []
        if audio_track is not None:
            audio_layers.append(audio_track)
        if voice_path:
            voice_track = AudioFileClip(str(voice_path))
            voice_track = voice_track.subclipped(0, min(voice_track.duration, final.duration))
            audio_layers.append(voice_track)
        if audio_layers:
            audio_mix = CompositeAudioClip(audio_layers).with_duration(final.duration)
            final = final.with_audio(audio_mix)
        final.write_videofile(
            str(output_path), fps=fps, codec="libx264", audio=bool(audio_layers),
            audio_codec="aac", preset="medium", logger=None,
            ffmpeg_params=["-pix_fmt", "yuv420p"]
        )
    finally:
        try: final.close()
        except Exception: pass
        if audio_mix:
            try: audio_mix.close()
            except Exception: pass
        if audio_track:
            try: audio_track.close()
            except Exception: pass
        if voice_track:
            try: voice_track.close()
            except Exception: pass
        for c in audio_parts:
            try: c.close()
            except Exception: pass
        for c in clips:
            try: c.close()
            except Exception: pass

def get_uploaded_images(uploaded):
    images = []
    for f in uploaded or []:
        try:
            im = Image.open(f).convert("RGB")
            images.append(im)
        except Exception:
            continue
    return images

def build_listing_copy(project, language="English", tone="Luxury / premium"):
    """Create editable listing copy locally from user-provided property facts (no external AI/API)."""
    name = str(project.get("name", "Property")).strip() or "Property"
    location = str(project.get("location", "your preferred location")).strip()
    price = str(project.get("price", "Price on request")).strip()
    ptype = str(project.get("property_type", "property")).strip().lower()
    area = str(project.get("area", "Area on request")).strip()
    beds = int(project.get("bedrooms", 0) or 0)
    baths = int(project.get("bathrooms", 0) or 0)
    features = str(project.get("features", "")).strip().strip("., ")
    contact = str(project.get("contact", "")).strip()
    cta = str(project.get("cta", "Contact us for details")).strip()
    if language == "Hinglish":
        headline = f"{name} — aapke next home ki talaash yahin se shuru"
        description = f"{location} mein {name} ke baare mein jaaniye. Yeh {ptype} {area} area ke saath listed hai, price {price}. Ismein {beds} bedroom aur {baths} bathroom hain."
        if features:
            description += f" Features (provided details ke mutabik): {features}."
        description += f" {cta}. Details aur availability seller se verify karein."
        caption = f"Dream home search kar rahe ho? {name}, {location} 📍\n{price} | {beds} bedrooms | {area}\n{cta}."
        whatsapp = f"Hi! {name} ke liye details chahiye. Location: {location}; Price: {price}; Area: {area}; Bedrooms: {beds}; Bathrooms: {baths}. Please share verified availability and site-visit details."
    elif language == "Hindi":
        headline = f"{name} — aapke naye ghar ka ek vikalp"
        description = f"{location} mein sthit {name} ek {ptype} listing hai. Area: {area}; listed price: {price}; bedrooms: {beds}; bathrooms: {baths}."
        if features:
            description += f" Di gayi jaankari ke mutabik suvidhayein: {features}."
        description += f" {cta}. Kripya price, suvidhayein aur availability seller se verify karein."
        caption = f"{name} | {location}\nPrice: {price} · Area: {area}\n{cta}."
        whatsapp = f"Namaste, mujhe {name} ke baare mein verified details chahiye. Location: {location}; Price: {price}; Area: {area}; Bedrooms: {beds}; Bathrooms: {baths}. Kripya availability aur site visit details share karein."
    else:
        if tone == "Friendly / welcoming":
            headline = f"Find your next place to call home at {name}"
            opening = f"Explore {name}, a {ptype} listing in {location}."
        elif tone == "Investor focused":
            headline = f"Explore the property details: {name}"
            opening = f"Review the available details for {name}, a {ptype} listing in {location}."
        else:
            headline = f"Discover {name} — refined property living"
            opening = f"Discover {name}, a {ptype} listing located in {location}."
        description = f"{opening} The listed price is {price}, with an area of {area}, {beds} bedrooms and {baths} bathrooms."
        if features:
            description += f" Listed features: {features}."
        description += f" {cta}. Contact the seller to confirm current pricing, availability and all property details."
        caption = f"{name} 📍 {location}\n{price} | {area} | {beds} bedrooms · {baths} bathrooms\n{cta}.\n#RealEstate #PropertyListing #{''.join(ch for ch in location.title() if ch.isalnum())}"
        whatsapp = f"Hello, I’m interested in {name}. Could you please share the latest verified details and availability?\nLocation: {location}\nListed price: {price}\nArea: {area}\nBedrooms/Bathrooms: {beds}/{baths}\nContact: {contact or 'Please share contact details'}"
    hashtags = "#RealEstate #Property #PropertyForSale #HomeSearch #PropertyTour"
    return {"headline": headline, "description": description, "caption": caption, "whatsapp": whatsapp, "hashtags": hashtags}


if page == "Create Video":
    st.markdown("""
    <div style="display:flex;gap:10px;flex-wrap:wrap;margin:-4px 0 20px;">
      <span style="background:#e4f4eb;color:#17634e;padding:7px 12px;border-radius:999px;font-size:.82rem;font-weight:700;">✦ AI video creator</span>
      <span style="background:#fff;color:#56736a;border:1px solid #dce9e1;padding:7px 12px;border-radius:999px;font-size:.82rem;">01 · Property details</span>
      <span style="background:#fff;color:#56736a;border:1px solid #dce9e1;padding:7px 12px;border-radius:999px;font-size:.82rem;">02 · Photos & audio</span>
      <span style="background:#fff;color:#56736a;border:1px solid #dce9e1;padding:7px 12px;border-radius:999px;font-size:.82rem;">03 · Style & export</span>
    </div>
    """, unsafe_allow_html=True)
    with st.container(border=True):
        st.subheader("01  ·  Property details")
        c1, c2, c3 = st.columns(3)
        with c1:
            p["name"] = st.text_input("Property name", p["name"])
            p["location"] = st.text_input("Location", p["location"])
            p["price"] = st.text_input("Price", p["price"])
        with c2:
            p["property_type"] = st.selectbox("Property type", ["Apartment","Villa","Independent House","Plot","Commercial","Other"], index=["Apartment","Villa","Independent House","Plot","Commercial","Other"].index(p["property_type"]))
            p["bedrooms"] = st.number_input("Bedrooms", 0, 30, int(p["bedrooms"]))
            p["bathrooms"] = st.number_input("Bathrooms", 0, 30, int(p["bathrooms"]))
        with c3:
            p["area"] = st.text_input("Area", p["area"])
            p["contact"] = st.text_input("Contact", p["contact"])
            p["cta"] = st.text_input("Call to action", p["cta"])
        p["features"] = st.text_area("Key features (use only verified facts)", p["features"], height=85)

    with st.container(border=True):
        st.subheader("02  ·  Upload property photos")
        uploaded = st.file_uploader("Upload 4–8 property images (JPG/PNG/WEBP)", type=["jpg","jpeg","png","webp"], accept_multiple_files=True)
        if uploaded:
            st.caption(f"{len(uploaded)} image(s) uploaded. You can continue with fewer for testing.")
            cols = st.columns(min(4, len(uploaded)))
            for i, f in enumerate(uploaded):
                with cols[i % len(cols)]:
                    st.image(f, caption=f.name, use_container_width=True)
    with st.container(border=True):
        st.subheader("03  ·  Background music")
        music_mode = st.radio(
            "Choose music source",
            ["Built-in free music", "Upload my own music", "No music"],
            index=["Built-in free music", "Upload my own music", "No music"].index(p.get("music", "Built-in free music")),
            horizontal=True,
            help="Built-in music is generated locally by this app. You can also upload audio you have rights to use."
        )
        p["music"] = music_mode
        uploaded_music = None
        if music_mode == "Built-in free music":
            st.caption("A simple original ambient instrumental is generated on your computer. No music download or API key is needed.")
        elif music_mode == "Upload my own music":
            uploaded_music = st.file_uploader("Upload your music (MP3, WAV, M4A, AAC)", type=["mp3", "wav", "m4a", "aac"], accept_multiple_files=False)
            st.caption("Only upload audio you own or are allowed to use.")
        if music_mode != "No music":
            p["music_volume"] = st.slider("Music volume", 0.0, 1.0, float(p.get("music_volume", 0.22)), 0.05, help="Lower values keep the music soft under the property visuals.")

    with st.container(border=True):
        st.subheader("04  ·  Voice-over narration")
        p["voiceover"] = st.checkbox("Add spoken narration to my video (offline text-to-speech)", value=bool(p.get("voiceover", False)))
        auto_script = f"Welcome to {p['name']}, located in {p['location']}. This {p['property_type'].lower()} is priced at {p['price']}. It offers {p['bedrooms']} bedrooms, {p['bathrooms']} bathrooms, and an area of {p['area']}. Key features include {p['features']}. {p['cta']}. For details, contact {p['contact']}."
        if not p.get("voice_script"):
            p["voice_script"] = auto_script
        if p["voiceover"]:
            voice_script = st.text_area("Narration script (edit as you like)", value=p.get("voice_script", auto_script), height=110,
                                        help="A suggested script is created from your property details. Review it before rendering.")
            p["voice_script"] = voice_script
            st.caption("Narration is generated locally using your computer's installed text-to-speech voice. Voice/language availability depends on Windows settings.")

    with st.container(border=True):
        st.subheader("05  ·  Video style & format")
        export_presets = {
            "Custom": None,
            "Instagram Reels / Stories (9:16)": ("9:16", "1080p"),
            "YouTube Shorts (9:16)": ("9:16", "1080p"),
            "Instagram Feed Square (1:1)": ("1:1", "1080p"),
            "Instagram Feed Portrait (4:5)": ("4:5", "1080p"),
            "YouTube / Facebook Landscape (16:9)": ("16:9", "1080p"),
            "Lightweight Landscape (720p)": ("16:9", "720p"),
        }
        p.setdefault("export_preset", "Custom")
        selected_preset = st.selectbox("Quick export preset", list(export_presets.keys()),
                                       index=list(export_presets.keys()).index(p["export_preset"] if p["export_preset"] in export_presets else "Custom"),
                                       help="Choose a social platform preset or use Custom to set format manually.")
        p["export_preset"] = selected_preset
        if export_presets[selected_preset] is not None:
            p["aspect"], p["resolution"] = export_presets[selected_preset]
        st.caption("Presets set the frame shape and resolution. Always preview the final video before posting.")
        a,b,c,d = st.columns(4)
        with a:
            p["template"] = st.selectbox("Promo template", ["Luxury Showcase", "Quick Listing", "Family Home", "Investor Focus", "Minimal Cinematic"], index=["Luxury Showcase", "Quick Listing", "Family Home", "Investor Focus", "Minimal Cinematic"].index(p.get("template", "Luxury Showcase")))
            p["theme"] = st.selectbox("Color style", ["Luxury Gold","Clean & Bright","Cinematic Blue","Elegant Neutral","Minimal"])
        with b:
            p["aspect"] = st.selectbox("Aspect ratio", ["16:9","9:16","1:1","4:5"])
        with c:
            p["resolution"] = st.selectbox("Resolution", ["720p","1080p"])
        with d:
            p["duration"] = st.slider("Seconds per scene", 2, 8, int(p["duration"]))
        # Filter and animation are independent controls; choosing a theme won't overwrite the filter.
        p["filter"] = st.selectbox(
            "Photo filter",
            ["Original", "Luxury Gold", "Warm", "Cool", "Matte", "Black & White", "Soft"],
            index=["Original", "Luxury Gold", "Warm", "Cool", "Matte", "Black & White", "Soft"].index(p.get("filter") if p.get("filter") in ["Original", "Luxury Gold", "Warm", "Cool", "Matte", "Black & White", "Soft"] else "Original")
        )
        p["animation"] = st.selectbox(
            "Photo animation",
            ["None", "Slow Zoom In", "Slow Zoom Out"],
            index=["None", "Slow Zoom In", "Slow Zoom Out"].index(p.get("animation") if p.get("animation") in ["None", "Slow Zoom In", "Slow Zoom Out"] else "None")
        )
        p["transition"] = st.selectbox("Scene transition", ["Fade", "Cut"], index=["Fade", "Cut"].index(p.get("transition") if p.get("transition") in ["Fade", "Cut"] else "Fade"))
        if uploaded:
            scene_count = len(uploaded)
            scene_title_templates = {
                "Luxury Showcase": ["Discover " + p["name"], "Luxury in every detail", "Designed for your lifestyle", "A place to call home", p["cta"]],
                "Quick Listing": [p["name"], p["price"] + " | " + p["area"], f"{p['bedrooms']} bedrooms • {p['bathrooms']} bathrooms", p["location"], p["cta"]],
                "Family Home": ["Welcome to " + p["name"], "Room for every moment", "Comfort for the whole family", p["location"], p["cta"]],
                "Investor Focus": [p["name"] + " investment opportunity", "Property type: " + p["property_type"], "Area: " + p["area"], "Location: " + p["location"], "Ask us for details"],
                "Minimal Cinematic": [p["name"], p["location"], p["price"], p["area"], p["cta"]]
            }
            default_scene_titles = list(scene_title_templates.get(p["template"], scene_title_templates["Luxury Showcase"]))
            while len(default_scene_titles) < scene_count:
                default_scene_titles.append("Discover more features")
            with st.expander("✏️ Edit titles for each scene", expanded=False):
                st.caption("These titles appear over each photo. Edit them before generating the video.")
                for scene_idx, photo_file in enumerate(uploaded):
                    st.text_input(f"Scene {scene_idx + 1} · {photo_file.name}", value=default_scene_titles[scene_idx],
                                  key=f"scene_title_{p['template']}_{scene_idx}")
        if st.button("✨ Generate my first video", type="primary", use_container_width=True):
            images = get_uploaded_images(uploaded)
            if not images:
                st.error("Please upload at least one valid property photo before generating the video.")
            elif not p["name"].strip() or not p["location"].strip():
                st.error("Please enter at least a property name and location.")
            else:
                template_titles = {
                    "Luxury Showcase": ["Discover " + p["name"], "Luxury in every detail", "Designed for your lifestyle", "A place to call home", p["cta"]],
                    "Quick Listing": [p["name"], p["price"] + " | " + p["area"], p["bedrooms"] .__str__() + " bedrooms • " + p["bathrooms"].__str__() + " bathrooms", p["location"], p["cta"]],
                    "Family Home": ["Welcome to " + p["name"], "Room for every moment", "Comfort for the whole family", p["location"], p["cta"]],
                    "Investor Focus": [p["name"] + " investment opportunity", "Property type: " + p["property_type"], "Area: " + p["area"], "Location: " + p["location"], "Ask us for details"],
                    "Minimal Cinematic": [p["name"], p["location"], p["price"], p["area"], p["cta"]]
                }
                titles = template_titles.get(p.get("template", "Luxury Showcase"), template_titles["Luxury Showcase"])[:len(images)]
                if len(titles) < len(images):
                    titles += ["Discover more features" for _ in range(len(images)-len(titles))]
                titles = [st.session_state.get(f"scene_title_{p['template']}_{i}", titles[i]).strip() or titles[i]
                          for i in range(len(titles))]
                out = OUTPUT_DIR / "property_video.mp4"
                music_path = None
                voice_path = None
                with st.spinner("Building scenes, preparing audio and rendering MP4… this may take a few minutes."):
                    try:
                        total_duration = len(images) * float(p["duration"])
                        if music_mode == "Built-in free music":
                            music_path = OUTPUT_DIR / "built_in_free_music.wav"
                            create_free_music(music_path, total_duration)
                        elif music_mode == "Upload my own music":
                            if uploaded_music is None:
                                st.error("Please upload a music file or choose another music option.")
                                st.stop()
                            suffix = Path(uploaded_music.name).suffix.lower() or ".mp3"
                            music_path = OUTPUT_DIR / f"uploaded_music{suffix}"
                            music_path.write_bytes(uploaded_music.getvalue())
                        if p.get("voiceover"):
                            if not p.get("voice_script", "").strip():
                                st.error("Please enter a narration script or turn off voice-over.")
                                st.stop()
                            try:
                                import pyttsx3
                                voice_path = OUTPUT_DIR / "property_voiceover.wav"
                                engine = pyttsx3.init()
                                engine.setProperty("rate", 165)
                                engine.setProperty("volume", 0.95)
                                engine.save_to_file(p["voice_script"].strip(), str(voice_path))
                                engine.runAndWait()
                                engine.stop()
                                if not voice_path.exists() or voice_path.stat().st_size < 1000:
                                    raise RuntimeError("The local speech engine did not create an audio file. Check installed Windows voices.")
                            except Exception as voice_error:
                                raise RuntimeError("Could not generate narration. Install the app requirements and check Windows text-to-speech voices. Details: " + str(voice_error))
                        create_video(images, titles, p, out, music_path=music_path,
                                     music_volume=float(p.get("music_volume", 0.22)), voice_path=voice_path)
                        st.session_state.last_video = str(out)
                        st.session_state.last_project = {
                            "property": {k:v for k,v in p.items()},
                            "scene_titles": titles,
                            "image_names": [f.name for f in uploaded],
                            "generated_file": str(out)
                        }
                        with open(PROJECT_DIR / "last_project.json", "w", encoding="utf-8") as fp:
                            json.dump(st.session_state.last_project, fp, indent=2, ensure_ascii=False)
                        st.success("Your first video is ready! Open Project & Export to preview and download it.")
                    except Exception as e:
                        st.error("Video rendering failed. Check the setup instructions and error details below.")
                        st.exception(e)

elif page == "Listing Copywriter":
    st.markdown("## ✍️ Property Listing Copywriter")
    st.write("Create editable property descriptions, social captions and WhatsApp enquiry messages from the facts you entered in Create Video.")
    st.info("This version generates copy locally from your form details; it does not call an external AI service. Verify all facts before publishing.")
    lang = st.selectbox("Output language", ["English", "Hinglish", "Hindi"])
    tone = st.selectbox("Writing style", ["Luxury / premium", "Friendly / welcoming", "Investor focused"])
    if st.button("✨ Generate listing content", type="primary", use_container_width=True):
        st.session_state.listing_copy = build_listing_copy(p, lang, tone)
        st.session_state.listing_copy_language = lang
    copy = st.session_state.get("listing_copy")
    if copy:
        st.markdown("### Preview and edit")
        copy["headline"] = st.text_input("Headline", value=copy["headline"])
        copy["description"] = st.text_area("Property description", value=copy["description"], height=150)
        copy["caption"] = st.text_area("Social media caption", value=copy["caption"], height=130)
        copy["hashtags"] = st.text_input("Hashtags", value=copy["hashtags"])
        copy["whatsapp"] = st.text_area("WhatsApp enquiry message", value=copy["whatsapp"], height=130)
        all_copy = ("HEADLINE\n" + copy["headline"] + "\n\nDESCRIPTION\n" + copy["description"] +
                    "\n\nSOCIAL CAPTION\n" + copy["caption"] + "\n\nHASHTAGS\n" + copy["hashtags"] +
                    "\n\nWHATSAPP MESSAGE\n" + copy["whatsapp"])
        st.download_button("⬇️ Download all listing copy (.txt)", data=all_copy.encode("utf-8"),
                           file_name="property_listing_copy.txt", mime="text/plain", type="primary", use_container_width=True)
        st.caption("Tip: update the property details in Create Video, then generate the copy again to refresh it.")
    else:
        st.markdown("#### Your generated content will appear here")
        st.write(f"Current property: **{p.get('name', 'Property')}** · {p.get('location', '')} · {p.get('price', '')}")
        st.button("Generate a draft", on_click=lambda: st.session_state.update({"listing_copy": build_listing_copy(p, lang, tone)}), type="secondary")

elif page == "Property Finder":
    st.markdown("## 🔎 Discover a property & nearby alternatives")
    st.write("Enter a flat/apartment project name and its area. This page creates targeted search links for current listings, map locations and property photos.")
    st.info("This starter version opens live searches in your browser; it does not claim to verify availability, prices, or listings inside the app. Always confirm details with the seller or official project website.")
    f1, f2 = st.columns(2)
    with f1:
        project_query = st.text_input("Flat / apartment / society name", value=p.get("name", ""), placeholder="e.g. Sunny Enclave Apartments")
        area_query = st.text_input("Locality / city", value=p.get("location", "Mohali, Punjab"), placeholder="e.g. Sector 117, Mohali")
    with f2:
        finder_type = st.selectbox("What are you looking for?", ["Flats for sale", "Flats for rent", "New projects", "Resale flats", "Luxury apartments", "Affordable apartments"])
        budget_query = st.text_input("Budget (optional)", placeholder="e.g. 50–70 lakh")
    query_base = " ".join(x.strip() for x in [project_query, area_query] if x and x.strip())
    nearby_query = " ".join(x.strip() for x in [finder_type, area_query, budget_query] if x and x.strip())
    if project_query.strip() or area_query.strip():
        st.markdown("### Search shortcuts")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("#### 📍 Project location")
            st.caption("Look for the project pin, address and nearby landmarks.")
            st.link_button("Open Google Maps", "https://www.google.com/maps/search/?api=1&query=" + quote_plus(query_base or area_query))
        with c2:
            st.markdown("#### 🖼️ Property photos")
            st.caption("See exterior, interiors and gallery photos matching the project name.")
            st.link_button("View Google Images", "https://www.google.com/search?tbm=isch&q=" + quote_plus(query_base + " apartment photos"))
        with c3:
            st.markdown("#### 🏢 Similar properties")
            st.caption("Search for other projects in the same area and budget.")
            st.link_button("Find nearby options", "https://www.google.com/search?q=" + quote_plus(nearby_query + " apartments"))
        st.markdown("### Property portal searches")
        q = quote_plus(nearby_query)
        pc1, pc2, pc3 = st.columns(3)
        with pc1:
            st.markdown("**99acres**")
            st.link_button("Search listings", "https://www.google.com/search?q=site%3A99acres.com+" + q)
        with pc2:
            st.markdown("**Magicbricks**")
            st.link_button("Search listings", "https://www.google.com/search?q=site%3Amagicbricks.com+" + q)
        with pc3:
            st.markdown("**Housing.com**")
            st.link_button("Search listings", "https://www.google.com/search?q=site%3Ahousing.com+" + q)
        st.markdown("### Suggested searches")
        suggestions = [
            f"{finder_type} near {area_query}",
            f"Ready-to-move apartments in {area_query}",
            f"New residential projects near {area_query}",
            f"{project_query} reviews, amenities and possession date" if project_query.strip() else f"Best residential societies in {area_query}",
        ]
        for suggestion in suggestions:
            st.markdown(f"- [{suggestion}](https://www.google.com/search?q={quote_plus(suggestion)})")
    else:
        st.warning("Enter a project name or locality to create search links.")
    st.markdown("---")
    st.markdown("### How to make this a true in-app property recommender")
    st.write("To show verified live listings, prices and photos directly inside this app, we would need a permitted property-data/API provider or a licensed listing feed. Without that connection, this page safely opens searches rather than inventing listings or photos.")

elif page == "Visual Editor":
    st.subheader("Visual editor")
    st.write("Adjust the look of your generated scenes, then regenerate the MP4 to apply the settings.")
    st.info("In this starter version, adjustments are applied when you generate the video. The full multi-track timeline and direct prompt-based editing are planned next upgrades.")
    p["brightness"] = st.slider("Brightness", 0.4, 1.8, float(p["brightness"]), 0.05)
    p["contrast"] = st.slider("Contrast", 0.4, 1.8, float(p["contrast"]), 0.05)
    p["saturation"] = st.slider("Saturation", 0.0, 2.0, float(p["saturation"]), 0.05)
    p["sharpness"] = st.slider("Sharpness", 0.0, 3.0, float(p["sharpness"]), 0.1)
    p["filter"] = st.selectbox("Color filter", ["Original","Luxury Gold","Warm","Cool","Matte","Black & White","Soft"], index=["Original","Luxury Gold","Warm","Cool","Matte","Black & White","Soft"].index(p.get("filter", "Original")))
    p["animation"] = st.selectbox("Photo animation", ["None", "Slow Zoom In", "Slow Zoom Out"], index=["None", "Slow Zoom In", "Slow Zoom Out"].index(p.get("animation") if p.get("animation") in ["None", "Slow Zoom In", "Slow Zoom Out"] else "None"))
    p["transition"] = st.selectbox("Transition style", ["Fade","Cut"], index=["Fade","Cut"].index(p.get("transition", "Fade")))
    st.caption("Tip: after changing controls, go to Create Video and click Generate my first video again to apply the settings.")

elif page == "Project & Export":
    st.subheader("Project preview & export")
    video_path = st.session_state.get("last_video")
    if not video_path and (OUTPUT_DIR / "property_video.mp4").exists():
        video_path = str(OUTPUT_DIR / "property_video.mp4")
    if video_path and Path(video_path).exists():
        st.video(video_path)
        with open(video_path, "rb") as f:
            st.download_button("⬇️ Download MP4", data=f, file_name="property_promo.mp4", mime="video/mp4", type="primary")
        st.success(f"Video file ready: {Path(video_path).stat().st_size / (1024*1024):.1f} MB")
    else:
        st.info("Generate a video first from the Create Video page. Your MP4 will appear here.")
    st.markdown("### Project information")
    project_file = PROJECT_DIR / "last_project.json"
    if project_file.exists():
        st.json(json.loads(project_file.read_text(encoding="utf-8")))
        st.download_button("Download project JSON", data=project_file.read_bytes(), file_name="property_project.json", mime="application/json")
    else:
        st.caption("Project JSON will be created after the first successful render.")

elif page == "How to use":
    st.subheader("Getting started")
    st.markdown("""
1. Open **Create Video** and enter verified property details.
2. Upload one or more JPG, PNG or WEBP property photos.
3. Select a promo template, color style, aspect ratio, resolution and scene duration.
4. Choose a photo filter, animation, scene transition, and optionally music and narration.
5. Click **Generate my first video** and wait for MP4 rendering.
6. Open **Visual Editor** to fine-tune brightness, contrast, saturation, sharpness, filters, animation and transitions.
7. Return to **Create Video** and regenerate to apply your latest adjustments.
8. Open **Project & Export** to preview and download the MP4 and project JSON.

### Current starter scope
- Working property form and image upload.
- Rule-based scene titles using supplied facts.
- Image adjustments and several color filters, selectable independently from the visual theme.
- Fade/cut scene transitions and slow zoom-in/zoom-out photo animations.
- MP4 slideshow rendering through MoviePy/FFmpeg.
- Project JSON and MP4 download.

### Planned next upgrades
- True drag-and-drop multi-track timeline.
- Per-scene editing and regenerate-one-scene workflow.
- AI script generation through a configurable model/API.
- Local text-to-speech narration, background music mixing, promo templates and social aspect ratios are implemented. Subtitles and a true multi-track timeline remain future upgrades.
- Undo/redo history, autosave and project reopening.
- Better scene transitions, animation and export presets.
""")

st.markdown("---")
st.markdown('<p class="small-muted">AI Property Studio  ·  Your real-estate creative workspace  ·  Local prototype</p>', unsafe_allow_html=True)
