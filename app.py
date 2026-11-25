
import streamlit as st
import img2pdf
import fitz
import io
import zipfile

from PIL import Image, ImageOps


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="JPG to PDF Converter & Resizer – Free Online Tool",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Manrope:wght@500;600;700;800&display=swap');

:root {
    --ink: #172554;
    --muted: #64748b;
    --blue: #2563eb;
    --blue-dark: #1d4ed8;
    --violet: #7c3aed;
    --cyan: #06b6d4;
    --surface: #ffffff;
    --line: #e2e8f0;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background:
        radial-gradient(ellipse at 8% 0%, rgba(59,130,246,.12), transparent 34%),
        radial-gradient(ellipse at 95% 8%, rgba(124,58,237,.10), transparent 30%),
        #f4f7fc;
    color: var(--ink);
}

.block-container {
    max-width: 1380px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

.main-title {
    font-family: 'Manrope', sans-serif;
    font-size: clamp(2rem, 3.4vw, 2.8rem);
    line-height: 1.12;
    letter-spacing: -1.5px;
    font-weight: 800;
    color: #172554;
    margin: 0 0 8px 0;
}

.tagline {
    font-size: 1.02rem;
    color: #64748b;
    margin: 0 0 20px 0;
    line-height: 1.65;
}

.hero-shell {
    position: relative;
    overflow: hidden;
    padding: 30px 34px 26px;
    margin: 4px 0 25px;
    border: 1px solid rgba(255,255,255,.75);
    border-radius: 24px;
    background: linear-gradient(120deg, #ffffff 0%, #eef5ff 58%, #f4efff 100%);
    box-shadow: 0 16px 45px rgba(30, 64, 175, .09);
}

.hero-shell:after {
    content: "";
    position: absolute;
    width: 230px;
    height: 230px;
    border-radius: 50%;
    right: -55px;
    top: -100px;
    background: linear-gradient(135deg, rgba(37,99,235,.17), rgba(124,58,237,.13));
    filter: blur(2px);
}

.hero-kicker {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    padding: 6px 11px;
    border-radius: 999px;
    background: #e7efff;
    color: #2453b8;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1.2px;
    margin-bottom: 13px;
}

.hero-copy {
    position: relative;
    z-index: 1;
    max-width: 760px;
}

.hero-pills {
    display: flex;
    flex-wrap: wrap;
    gap: 9px;
    margin-top: 18px;
}

.hero-pill {
    border: 1px solid #dbe6fb;
    background: rgba(255,255,255,.78);
    color: #405477;
    padding: 7px 12px;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 600;
}

.section-title {
    color: #172554;
    font-family: 'Manrope', sans-serif;
    font-size: 1.55rem;
    font-weight: 800;
    letter-spacing: -.5px;
    margin: 3px 0 4px;
}

h1, h2, h3 {
    color: #172554;
    font-family: 'Manrope', sans-serif;
    letter-spacing: -.35px;
}

h2, [data-testid="stSubheader"] {
    font-weight: 750 !important;
}

p, label, .stMarkdown {
    color: #334155;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #101d43 0%, #172554 55%, #25245c 100%);
    border-right: 1px solid rgba(255,255,255,.08);
}

[data-testid="stSidebar"] * {
    color: #eaf0ff !important;
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h2 {
    font-family: 'Manrope', sans-serif;
    font-size: 1.35rem;
    letter-spacing: -.4px;
}

[data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
    color: #aebde0 !important;
}

[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,.15);
}

[data-testid="stTabs"] [data-baseweb="tab-list"] {
    gap: 9px;
    padding: 8px;
    border: 1px solid #e3eaf6;
    border-radius: 16px;
    background: rgba(255,255,255,.78);
    box-shadow: 0 8px 24px rgba(15,23,42,.045);
}

[data-testid="stTabs"] button[role="tab"] {
    border-radius: 11px;
    padding: 11px 17px;
    color: #64748b;
    font-weight: 700;
    border: 1px solid transparent;
    transition: all .18s ease;
}

[data-testid="stTabs"] button[role="tab"]:hover {
    color: #1d4ed8;
    background: #eff6ff;
}

[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
    color: #ffffff !important;
    background: linear-gradient(105deg, #2563eb, #6d4ce8);
    border-color: transparent;
    box-shadow: 0 5px 14px rgba(37,99,235,.23);
}

[data-testid="stTabs"] button[role="tab"][aria-selected="true"] p {
    color: #ffffff !important;
}

div.stButton > button, div.stDownloadButton > button {
    background: linear-gradient(105deg, #2563eb, #6848df);
    color: #ffffff !important;
    border: 0;
    border-radius: 12px;
    min-height: 46px;
    padding:  .55rem 1.1rem;
    font-weight: 750;
    box-shadow: 0 7px 16px rgba(37,99,235,.18);
    transition: transform .18s ease, box-shadow .18s ease, filter .18s ease;
}

div.stButton > button:hover, div.stDownloadButton > button:hover {
    color: #ffffff !important;
    filter: brightness(1.06);
    transform: translateY(-2px);
    box-shadow: 0 11px 22px rgba(37,99,235,.25);
    border: 0;
}

div.stButton > button:focus, div.stDownloadButton > button:focus {
    color: #ffffff !important;
    box-shadow: 0 0 0 3px rgba(96,165,250,.28);
}

[data-testid="stFileUploader"] {
    border: 1.5px dashed #9bb8ef;
    border-radius: 17px;
    padding: 12px;
    background: linear-gradient(135deg, #f8fbff, #f4f1ff);
    transition: border-color .2s ease, background .2s ease;
}

[data-testid="stFileUploader"]:hover {
    border-color: #6366f1;
    background: #f0f5ff;
}

[data-testid="stFileUploader"] section {
    border: 0 !important;
}

[data-testid="stFileUploader"] button {
    border-radius: 9px !important;
    border: 1px solid #c7d7f5 !important;
    color: #1d4ed8 !important;
    background: white !important;
    font-weight: 700 !important;
}

[data-testid="stAlert"] {
    border-radius: 13px;
    border: 1px solid rgba(148,163,184,.22);
}

[data-testid="stMetric"] {
    background: linear-gradient(145deg, #ffffff, #f5f8ff);
    border: 1px solid #e2eaf8;
    border-radius: 15px;
    padding: 15px 17px;
    box-shadow: 0 5px 18px rgba(15,23,42,.04);
}

[data-testid="stMetricLabel"] {
    color: #64748b !important;
    font-weight: 650;
}

[data-testid="stMetricValue"] {
    color: #1e40af !important;
    font-weight: 800;
}

[data-testid="stExpander"] {
    border: 1px solid #e1e8f4;
    border-radius: 13px;
    background: rgba(255,255,255,.78);
    overflow: hidden;
}

[data-testid="stExpander"] summary {
    font-weight: 700;
    color: #243b68;
}

[data-baseweb="select"] > div,
[data-baseweb="input"] > div,
[data-baseweb="textarea"] > div {
    border-radius: 10px;
    border-color: #d5deed;
    background: #ffffff;
}

[data-baseweb="select"] > div:focus-within,
[data-baseweb="input"] > div:focus-within {
    border-color: #6489ef;
    box-shadow: 0 0 0 2px rgba(37,99,235,.12);
}

[data-testid="stRadio"] > div {
    gap: 10px;
}

[data-testid="stRadio"] label {
    background: #ffffff;
    border: 1px solid #e0e8f5;
    border-radius: 10px;
    padding: 8px 12px;
}

[data-testid="stSlider"] [role="slider"] {
    background: #2563eb;
}

[data-testid="stImage"] img {
    border-radius: 13px;
}

hr {
    border-color: #e2e8f0;
    opacity: .9;
}

#MainMenu, footer {
    visibility: hidden;
}

@media (max-width: 768px) {
    .block-container {
        padding: 1rem 1rem 2rem;
    }
    .hero-shell {
        padding: 22px 20px;
        border-radius: 18px;
    }
    [data-testid="stTabs"] [data-baseweb="tab-list"] {
        gap: 4px;
        padding: 5px;
    }
    [data-testid="stTabs"] button[role="tab"] {
        padding: 9px 10px;
        font-size: 12px;
    }
}

/* ===== Readability + typography refinement ===== */
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Manrope:wght@500;600;700;800&display=swap');

html, body, [class*="css"], .stApp {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 16px;
}

p, li, label, [data-testid="stMarkdownContainer"],
[data-testid="stWidgetLabel"], [data-testid="stCaptionContainer"],
[data-testid="stFileUploader"] small {
    font-size: 15.5px !important;
    line-height: 1.65 !important;
}

[data-testid="stCaptionContainer"] {
    color: #52627b !important;
}

[data-testid="stWidgetLabel"] p,
[data-testid="stWidgetLabel"] label {
    color: #263858 !important;
    font-weight: 650 !important;
    font-size: 15px !important;
}

[data-testid="stTabs"] button[role="tab"] {
    font-size: 14.5px !important;
    font-weight: 750 !important;
}

[data-testid="stTabs"] button[role="tab"] p {
    font-size: 14.5px !important;
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] li,
[data-testid="stSidebar"] label {
    font-size: 15px !important;
    line-height: 1.7 !important;
}

[data-testid="stAlert"] {
    border-radius: 14px !important;
    padding: 14px 17px !important;
}

[data-testid="stAlert"][kind="info"],
div[data-testid="stAlert"]:has(svg[data-testid="stIconInfo"]) {
    background: #e8f1ff !important;
    border: 1px solid #b9d2ff !important;
    color: #173f83 !important;
}

[data-testid="stAlert"][kind="info"] *,
div[data-testid="stAlert"]:has(svg[data-testid="stIconInfo"]) * {
    color: #173f83 !important;
    font-size: 15.5px !important;
    font-weight: 600 !important;
}

[data-testid="stAlert"][kind="success"],
div[data-testid="stAlert"]:has(svg[data-testid="stIconSuccess"]) {
    background: #e9f8ef !important;
    border: 1px solid #b8e7c8 !important;
    color: #17633b !important;
}

[data-testid="stAlert"][kind="success"] *,
div[data-testid="stAlert"]:has(svg[data-testid="stIconSuccess"]) * {
    color: #17633b !important;
    font-size: 15.5px !important;
    font-weight: 600 !important;
}

div.stButton > button,
div.stDownloadButton > button {
    color: #ffffff !important;
    font-size: 15px !important;
    font-weight: 750 !important;
    letter-spacing: .1px;
}

div.stButton > button *,
div.stDownloadButton > button * {
    color: #ffffff !important;
}

[data-testid="stFileUploader"] *,
[data-testid="stFileUploader"] section,
[data-testid="stFileUploader"] small {
    font-size: 14.5px !important;
}

[data-testid="stMetricLabel"] *,
[data-testid="stMetricValue"] {
    font-family: 'Manrope', sans-serif !important;
}

[data-testid="stExpander"] summary,
[data-testid="stExpander"] summary p {
    font-size: 15px !important;
    font-weight: 700 !important;
}

[data-baseweb="select"] *,
[data-baseweb="input"] *,
[data-baseweb="textarea"] * {
    font-size: 15px !important;
}

@media (max-width: 768px) {
    p, li, label, [data-testid="stMarkdownContainer"] {
        font-size: 15px !important;
    }
    [data-testid="stTabs"] button[role="tab"],
    [data-testid="stTabs"] button[role="tab"] p {
        font-size: 13px !important;
    }
}

/* ===== Larger text + richer but balanced colours ===== */
html, body, [class*="css"], .stApp {
    font-size: 17px !important;
}

p, li, label,
[data-testid="stMarkdownContainer"],
[data-testid="stWidgetLabel"],
[data-testid="stCaptionContainer"] {
    font-size: 17px !important;
    line-height: 1.7 !important;
}

.main-title {
    font-size: clamp(2.35rem, 4vw, 3.15rem) !important;
    color: #163b80 !important;
}

.tagline {
    font-size: 1.15rem !important;
    color: #425a7d !important;
}

h1, h2, h3,
[data-testid="stSubheader"] {
    color: #244da0 !important;
}

.section-title {
    font-size: 1.75rem !important;
    color: #244da0 !important;
}

.hero-kicker {
    background: linear-gradient(100deg, #dbeafe, #ede9fe) !important;
    color: #4338a8 !important;
    font-size: 13px !important;
}

.hero-pill {
    background: linear-gradient(110deg, #ffffff, #f0f5ff) !important;
    border-color: #c8d8fa !important;
    color: #294c86 !important;
    font-size: 13.5px !important;
}

[data-testid="stTabs"] button[role="tab"],
[data-testid="stTabs"] button[role="tab"] p {
    font-size: 16px !important;
}

[data-testid="stWidgetLabel"] p,
[data-testid="stWidgetLabel"] label {
    font-size: 16.5px !important;
    color: #244477 !important;
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] li,
[data-testid="stSidebar"] label {
    font-size: 16px !important;
}

div.stButton > button,
div.stDownloadButton > button {
    font-size: 16px !important;
}

[data-testid="stFileUploader"] *,
[data-testid="stFileUploader"] section,
[data-testid="stFileUploader"] small {
    font-size: 15.5px !important;
}

[data-testid="stMetric"] {
    background: linear-gradient(135deg, #eef6ff 0%, #f3efff 100%) !important;
    border: 1px solid #cbdaf8 !important;
}

[data-testid="stMetricLabel"] {
    color: #405b88 !important;
    font-size: 15px !important;
}

[data-testid="stMetricValue"] {
    color: #2854b8 !important;
}

[data-testid="stExpander"] {
    border-color: #cbd9f3 !important;
    background: linear-gradient(120deg, #ffffff, #f6f8ff) !important;
}

[data-testid="stExpander"] summary,
[data-testid="stExpander"] summary p {
    color: #3155a0 !important;
    font-size: 16px !important;
}

[data-testid="stRadio"] label {
    background: linear-gradient(120deg, #ffffff, #f1f6ff) !important;
    border-color: #cbdaf4 !important;
}

[data-testid="stFileUploader"] {
    background: linear-gradient(135deg, #edf6ff 0%, #f4efff 100%) !important;
    border-color: #8eabed !important;
}

@media (max-width: 768px) {
    p, li, label, [data-testid="stMarkdownContainer"] {
        font-size: 15.5px !important;
    }
    .main-title {
        font-size: 2.15rem !important;
    }
    .tagline {
        font-size: 1rem !important;
    }
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# COMMON HELPER FUNCTIONS
# ==========================================

def convert_jpg_to_pdf(uploaded_images):

    image_bytes_list = []

    for uploaded_file in uploaded_images:

        image = Image.open(
            io.BytesIO(uploaded_file.getvalue())
        )

        image = ImageOps.exif_transpose(image)
        image = image.convert("RGB")

        image_buffer = io.BytesIO()

        image.save(
            image_buffer,
            format="JPEG",
            quality=95,
            optimize=True
        )

        image_bytes_list.append(
            image_buffer.getvalue()
        )

    return img2pdf.convert(image_bytes_list)


def convert_pdf_to_jpg(uploaded_pdf, dpi, quality):

    pdf_document = fitz.open(
        stream=uploaded_pdf.getvalue(),
        filetype="pdf"
    )

    if pdf_document.needs_pass:
        pdf_document.close()
        raise ValueError("Password-protected PDF is not supported.")

    if len(pdf_document) == 0:
        pdf_document.close()
        raise ValueError("PDF contains no pages.")

    jpg_files = []

    for page_number, page in enumerate(pdf_document):

        pix = page.get_pixmap(
            dpi=dpi,
            colorspace=fitz.csRGB,
            alpha=False
        )

        image = Image.frombytes(
            "RGB",
            [pix.width, pix.height],
            pix.samples
        )

        image_buffer = io.BytesIO()

        image.save(
            image_buffer,
            format="JPEG",
            quality=quality,
            optimize=True
        )

        jpg_files.append((
            f"page_{page_number + 1:03d}.jpg",
            image_buffer.getvalue()
        ))

    pdf_document.close()

    return jpg_files


def create_zip(files):

    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(
        zip_buffer,
        "w",
        compression=zipfile.ZIP_DEFLATED
    ) as zip_file:

        for filename, file_bytes in files:

            zip_file.writestr(
                filename,
                file_bytes
            )

    return zip_buffer.getvalue()


def size_mb(file_bytes):

    return len(file_bytes) / (1024 * 1024)


def format_file_size(file_bytes, unit="MB"):

    """Format a byte count in the unit selected by the user."""

    if unit == "KB":
        return f"{len(file_bytes) / 1024:.2f} KB"

    return f"{len(file_bytes) / (1024 * 1024):.2f} MB"


def format_size_delta(original_bytes, output_bytes, unit="MB"):

    divisor = 1024 if unit == "KB" else 1024 * 1024
    difference = (output_bytes - original_bytes) / divisor

    return f"{difference:.2f} {unit}"


# ==========================================
# JPG COMPRESSION ENGINE
# ==========================================


def compress_jpg(uploaded_file, target_mb):

    original_bytes = uploaded_file.getvalue()
    target_bytes = int(target_mb * 1024 * 1024)

    if len(original_bytes) <= target_bytes:
        return original_bytes, (
            "Original file is already smaller than "
            "the requested target."
        )

    image = Image.open(io.BytesIO(original_bytes))
    image = ImageOps.exif_transpose(image)
    image = image.convert("RGB")

    best_under_target = None
    smallest_candidate = None

    # Reduce quality only. Dimensions remain unchanged.
    for quality in range(95, 4, -1):

        buffer = io.BytesIO()

        image.save(
            buffer,
            format="JPEG",
            quality=quality,
            optimize=True,
            progressive=True
        )

        candidate = buffer.getvalue()

        if (
            smallest_candidate is None
            or len(candidate) < len(smallest_candidate)
        ):
            smallest_candidate = candidate

        if len(candidate) <= target_bytes:

            best_under_target = candidate
            break

    image.close()

    if best_under_target is not None:

        actual_kb = len(best_under_target) / 1024

        return best_under_target, (
            f"Target achieved: {actual_kb:.1f} KB. "
            "Original dimensions preserved."
        )

    actual_kb = len(smallest_candidate) / 1024

    return smallest_candidate, (
        f"Target could not be achieved using quality "
        f"reduction alone. Smallest output: {actual_kb:.1f} KB. "
        "Original dimensions preserved."
    )



# ==========================================
# PDF BALANCED COMPRESSION
# ==========================================

def compress_pdf_balanced(uploaded_pdf):

    pdf_document = fitz.open(
        stream=uploaded_pdf.getvalue(),
        filetype="pdf"
    )

    if pdf_document.needs_pass:
        pdf_document.close()
        raise ValueError("Password-protected PDF is not supported.")

    if len(pdf_document) == 0:
        pdf_document.close()
        raise ValueError("PDF contains no pages.")

    # Lossless optimization only. Do not rasterize pages or recompress
    # embedded images at a lower JPEG quality.
    output = pdf_document.tobytes(
        garbage=4,
        deflate=True,
        deflate_images=True,
        deflate_fonts=True
    )

    pdf_document.close()

    # If optimization makes the file larger, keep the original bytes.
    original = uploaded_pdf.getvalue()

    if len(output) >= len(original):
        return original

    return output


# ==========================================
# PDF MAXIMUM COMPRESSION
# ==========================================

def compress_pdf_maximum(uploaded_pdf, target_mb):

    original = uploaded_pdf.getvalue()
    target_bytes = target_mb * 1024 * 1024

    source_pdf = fitz.open(
        stream=original,
        filetype="pdf"
    )

    if source_pdf.needs_pass:
        source_pdf.close()
        raise ValueError("Password-protected PDF is not supported.")

    if len(source_pdf) == 0:
        source_pdf.close()
        raise ValueError("PDF contains no pages.")

    best_under_target = None
    smallest_candidate = None

    # Test resolution and quality combinations.
    dpi_values = [150, 120, 96, 72]
    quality_values = [85, 70, 55, 40]

    for dpi in dpi_values:

        for quality in quality_values:

            output_pdf = fitz.open()

            for page in source_pdf:

                pix = page.get_pixmap(
                    dpi=dpi,
                    colorspace=fitz.csRGB,
                    alpha=False
                )

                image = Image.frombytes(
                    "RGB",
                    [pix.width, pix.height],
                    pix.samples
                )

                image_buffer = io.BytesIO()

                image.save(
                    image_buffer,
                    format="JPEG",
                    quality=quality,
                    optimize=True
                )

                page_size = page.rect

                new_page = output_pdf.new_page(
                    width=page_size.width,
                    height=page_size.height
                )

                new_page.insert_image(
                    new_page.rect,
                    stream=image_buffer.getvalue()
                )

            candidate = output_pdf.tobytes(
                garbage=4,
                deflate=True
            )

            output_pdf.close()

            if (
                smallest_candidate is None
                or len(candidate) < len(smallest_candidate)
            ):
                smallest_candidate = candidate

            if len(candidate) <= target_bytes:

                if (
                    best_under_target is None
                    or len(candidate) > len(best_under_target)
                ):
                    best_under_target = candidate

    source_pdf.close()

    if best_under_target is not None:
        return best_under_target, (
            "Target achieved using maximum compression."
        )

    return smallest_candidate, (
        "Requested target could not be achieved with "
        "the tested settings. Smallest tested PDF provided."
    )


# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.markdown("## 📄 JPG to PDF Converter & Resizer")
    st.caption("Convert. Compress. Resize.")

    st.divider()

    st.markdown("### Navigation")

    st.markdown("""
    - 🔄 JPG / PDF Converter
    - 📦 File Compressor
    - 🪪 Passport Photo & Signature Resizer
    """)

    st.divider()

    st.caption("Version 1.0")
    st.caption("Python + Streamlit")


# ==========================================
# HEADER
# ==========================================

st.markdown("""
<div class="hero-shell">
  <div class="hero-copy">
    <div class="hero-kicker">✦ SMART FILE TOOLKIT</div>
    <div class="main-title">JPG to PDF Converter &amp; Resizer</div>
    <div class="tagline">Everything you need to convert, compress and resize files — in one simple workspace.</div>
    <div class="hero-pills">
      <span class="hero-pill">↔ JPG / PDF Conversion</span>
      <span class="hero-pill">✦ Smart Compression</span>
      <span class="hero-pill">▣ Photo &amp; Signature Resizing</span>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)


# ==========================================
# MAIN TABS
# ==========================================

tab1, tab2, tab3 = st.tabs([
    "🔄 JPG / PDF Converter",
    "📦 JPG & PDF Compressor",
    "🪪 Passport Photo & Signature Resizer"
])


# ==========================================
# FEATURE 1: JPG / PDF CONVERTER
# ==========================================

with tab1:

    st.markdown(
        '<div class="section-title">Image & PDF Converter</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Convert JPG images into PDF or PDF pages into JPG images."
    )

    conversion_type = st.radio(
        "Select Conversion Type",
        ["JPG to PDF", "PDF to JPG"],
        horizontal=True,
        key="conversion_type"
    )

    st.divider()

    if conversion_type == "JPG to PDF":

        st.subheader("🖼️ JPG to PDF Converter")

        uploaded_images = st.file_uploader(
            "Upload JPG Images",
            type=["jpg", "jpeg"],
            accept_multiple_files=True,
            key="jpg_to_pdf"
        )

        if uploaded_images:

            st.success(
                f"{len(uploaded_images)} image(s) uploaded."
            )

            with st.expander("Preview Images"):

                preview_columns = st.columns(3)

                for index, uploaded_file in enumerate(uploaded_images):

                    image = Image.open(
                        io.BytesIO(uploaded_file.getvalue())
                    )

                    with preview_columns[index % 3]:

                        st.image(
                            image,
                            caption=uploaded_file.name,
                            use_container_width=True
                        )

            if st.button("🔄 Convert JPG to PDF"):

                try:

                    with st.spinner("Creating PDF..."):

                        pdf_output = convert_jpg_to_pdf(
                            uploaded_images
                        )

                    st.success("PDF created successfully!")

                    st.metric(
                        "Output PDF Size",
                        f"{size_mb(pdf_output):.2f} MB"
                    )

                    st.download_button(
                        "⬇️ Download PDF",
                        data=pdf_output,
                        file_name="converted_images.pdf",
                        mime="application/pdf"
                    )

                except Exception as error:
                    st.error(f"Conversion failed: {error}")

        else:

            st.info("Upload one or multiple JPG images.")

    else:

        st.subheader("📄 PDF to JPG Converter")

        uploaded_pdf = st.file_uploader(
            "Upload PDF File",
            type=["pdf"],
            key="pdf_to_jpg"
        )

        dpi = st.selectbox(
            "Image Resolution (DPI)",
            [72, 100, 150, 200, 300],
            index=2
        )

        quality = st.slider(
            "JPG Image Quality",
            40, 100, 90, 5
        )

        if uploaded_pdf:

            if st.button("🔄 Convert PDF to JPG"):

                try:

                    with st.spinner("Converting PDF pages..."):

                        jpg_files = convert_pdf_to_jpg(
                            uploaded_pdf,
                            dpi,
                            quality
                        )

                    st.success(
                        f"{len(jpg_files)} page(s) converted."
                    )

                    preview_columns = st.columns(2)

                    for index, (filename, image_bytes) in enumerate(jpg_files):

                        with preview_columns[index % 2]:

                            st.image(
                                image_bytes,
                                caption=filename,
                                use_container_width=True
                            )

                    if len(jpg_files) == 1:

                        st.download_button(
                            "⬇️ Download JPG",
                            data=jpg_files[0][1],
                            file_name=jpg_files[0][0],
                            mime="image/jpeg"
                        )

                    else:

                        zip_output = create_zip(jpg_files)

                        st.download_button(
                            "⬇️ Download All JPG Images (ZIP)",
                            data=zip_output,
                            file_name="converted_pdf_pages.zip",
                            mime="application/zip"
                        )

                except Exception as error:
                    st.error(f"Conversion failed: {error}")

        else:

            st.info("Upload a PDF file to get started.")


# ==========================================
# FEATURE 2: JPG & PDF COMPRESSOR
# ==========================================

with tab2:

    st.markdown(
        '<div class="section-title">File Compressor</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Compress JPG images and PDF files to your desired size."
    )

    compression_type = st.radio(
        "Select File Type",
        ["JPG Compressor", "PDF Compressor"],
        horizontal=True,
        key="compression_type"
    )

    st.divider()

    # --------------------------------------
    # JPG COMPRESSOR
    # --------------------------------------

    if compression_type == "JPG Compressor":

        st.subheader("🖼️ JPG Image Compressor")

        uploaded_jpg = st.file_uploader(
            "Upload JPG Images",
            type=["jpg", "jpeg"],
            accept_multiple_files=True,
            key="jpg_compress"
        )

        jpg_target_unit = st.selectbox(
            "Target Size Unit",
            ["KB", "MB"],
            index=1,
            key="jpg_target_unit"
        )

        if jpg_target_unit == "KB":
            target_jpg_value = st.number_input(
                "Target Size per Image (KB)",
                min_value=1.0,
                max_value=512000.0,
                value=1024.0,
                step=100.0,
                key="target_jpg_kb"
            )
            target_jpg = target_jpg_value / 1024
        else:
            target_jpg_value = st.number_input(
                "Target Size per Image (MB)",
                min_value=0.01,
                max_value=500.0,
                value=1.0,
                step=0.1,
                key="target_jpg_mb"
            )
            target_jpg = target_jpg_value

        st.caption(
            "The target applies separately to each uploaded image."
        )

        if uploaded_jpg:

            st.success(
                f"{len(uploaded_jpg)} image(s) uploaded."
            )

            if st.button("📦 Compress JPG Images"):

                compressed_files = []

                with st.spinner("Compressing JPG images..."):

                    for uploaded_file in uploaded_jpg:

                        try:

                            compressed, message = compress_jpg(
                                uploaded_file,
                                target_jpg
                            )

                            compressed_files.append((
                                uploaded_file.name.rsplit(".", 1)[0]
                                + "_compressed.jpg",
                                compressed
                            ))

                        except Exception as error:

                            st.error(
                                f"{uploaded_file.name}: {error}"
                            )

                if compressed_files:

                    st.success("JPG compression completed!")

                    for filename, compressed in compressed_files:

                        original_name = filename.replace(
                            "_compressed.jpg", ".jpg"
                        )

                        original_file = next(
                            (
                                item for item in uploaded_jpg
                                if item.name == original_name
                            ),
                            None
                        )

                        original_size = (
                            size_mb(original_file.getvalue())
                            if original_file else 0
                        )

                        output_size = size_mb(compressed)

                        col1, col2 = st.columns(2)

                        original_bytes_for_metric = (
                            original_file.getvalue() if original_file else b""
                        )

                        col1.metric(
                            f"{filename} - Original",
                            format_file_size(original_bytes_for_metric, jpg_target_unit)
                        )

                        col2.metric(
                            "Compressed Size",
                            format_file_size(compressed, jpg_target_unit),
                            delta=format_size_delta(
                                len(original_bytes_for_metric),
                                len(compressed),
                                jpg_target_unit
                            )
                        )

                    if len(compressed_files) == 1:

                        st.download_button(
                            "⬇️ Download Compressed JPG",
                            data=compressed_files[0][1],
                            file_name=compressed_files[0][0],
                            mime="image/jpeg"
                        )

                    else:

                        compressed_zip = create_zip(
                            compressed_files
                        )

                        st.download_button(
                            "⬇️ Download All Compressed JPGs (ZIP)",
                            data=compressed_zip,
                            file_name="compressed_images.zip",
                            mime="application/zip"
                        )


    # --------------------------------------
    # PDF COMPRESSOR
    # --------------------------------------

    else:

        st.subheader("📄 PDF File Compressor")

        uploaded_pdf_compress = st.file_uploader(
            "Upload PDF File",
            type=["pdf"],
            key="pdf_compress"
        )

        compression_mode = st.radio(
            "Select Compression Mode",
            ["Balanced Compression", "Maximum Compression"],
            help=(
                "Balanced preserves document content. "
                "Maximum converts pages into JPEG images."
            )
        )

        pdf_target_unit = st.selectbox(
            "Target Size Unit",
            ["KB", "MB"],
            index=1,
            key="pdf_target_unit"
        )

        if pdf_target_unit == "KB":
            target_pdf_value = st.number_input(
                "Desired Output Size (KB)",
                min_value=1.0,
                max_value=512000.0,
                value=5120.0,
                step=100.0,
                key="target_pdf_kb"
            )
            target_pdf = target_pdf_value / 1024
        else:
            target_pdf_value = st.number_input(
                "Desired Output Size (MB)",
                min_value=0.01,
                max_value=500.0,
                value=5.0,
                step=0.5,
                key="target_pdf_mb"
            )
            target_pdf = target_pdf_value

        if compression_mode == "Balanced Compression":

            st.info(
                "Uses lossless PDF cleanup and stream compression only. "
                "Pages and embedded images are not intentionally "
                "rasterized or recompressed at a lower image quality. "
                "The selected target size is used only in Maximum "
                "Compression mode."
            )

        else:

            st.warning(
                "Maximum Compression rasterizes PDF pages. "
                "Selectable text, links, forms, bookmarks and "
                "other interactive document features may be lost. "
                "The original page count and visual page content "
                "are retained."
            )

        if uploaded_pdf_compress:

            original_pdf_bytes = uploaded_pdf_compress.getvalue()

            st.metric(
                "Original PDF Size",
                format_file_size(original_pdf_bytes, pdf_target_unit)
            )

            if st.button("📦 Compress PDF"):

                try:

                    with st.spinner(
                        "Compressing PDF. Please wait..."
                    ):

                        if compression_mode == "Balanced Compression":

                            compressed_pdf = compress_pdf_balanced(
                                uploaded_pdf_compress
                            )

                            message = (
                                "Lossless optimization completed. "
                                "Pages and embedded images were not "
                                "intentionally rasterized or reduced "
                                "in visual quality. If no size reduction "
                                "was possible, the original PDF was kept."
                            )

                        else:

                            compressed_pdf, message = compress_pdf_maximum(
                                uploaded_pdf_compress,
                                target_pdf
                            )

                    st.success("PDF processing completed!")

                    original_size = size_mb(original_pdf_bytes)
                    output_size = size_mb(compressed_pdf)

                    col1, col2 = st.columns(2)

                    col1.metric(
                        "Original Size",
                        format_file_size(original_pdf_bytes, pdf_target_unit)
                    )

                    col2.metric(
                        "Output Size",
                        format_file_size(compressed_pdf, pdf_target_unit),
                        delta=format_size_delta(
                            len(original_pdf_bytes),
                            len(compressed_pdf),
                            pdf_target_unit
                        )
                    )

                    if output_size < original_size:

                        reduction = (
                            (original_size - output_size)
                            / original_size
                        ) * 100

                        st.success(
                            f"File size reduced by {reduction:.1f}%"
                        )

                    elif output_size > original_size:

                        st.warning(
                            "The optimized PDF is larger than "
                            "the original. Consider keeping the original."
                        )

                    else:

                        st.info("No change in file size.")

                    if (
                        compression_mode == "Maximum Compression"
                        and output_size > target_pdf
                    ):

                        st.warning(
                            f"Requested target of {target_pdf_value:.2f} "
                            f"{pdf_target_unit} could not be achieved. "
                            "The smallest tested output has been provided."
                        )

                    st.info(message)

                    st.download_button(
                        "⬇️ Download Compressed PDF",
                        data=compressed_pdf,
                        file_name="compressed_document.pdf",
                        mime="application/pdf"
                    )

                except Exception as error:

                    st.error(
                        f"PDF compression failed: {error}"
                    )

        else:

            st.info("Upload a PDF file to start compression.")




# ==========================================
# FEATURE 3: PASSPORT PHOTO RESIZER
# ==========================================

with tab3:

    st.markdown(
        '<div class="section-title">Passport Photo &amp; Signature Resizer</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Create a standard passport-size photo or resize "
        "your photograph to custom pixel dimensions."
    )

    st.divider()

    # UPLOAD PHOTOGRAPH

    uploaded_photo = st.file_uploader(
        "Upload Your Photograph",
        type=["jpg", "jpeg", "png"],
        key="passport_photo"
    )

    if uploaded_photo:

        try:

            original_image = Image.open(
                io.BytesIO(uploaded_photo.getvalue())
            )

            original_image = ImageOps.exif_transpose(
                original_image
            )

            st.success("Photograph uploaded successfully!")

            # ORIGINAL PHOTO PREVIEW

            with st.expander("Preview Original Photograph"):

                st.image(
                    original_image,
                    caption="Original Photograph",
                    width=180
                )

                st.caption(
                    f"Original Dimensions: "
                    f"{original_image.width} × "
                    f"{original_image.height} pixels"
                )

            st.divider()

            # SELECT RESIZING MODE

            st.subheader("Select Photo Size")

            resize_mode = st.radio(
                "Choose your preferred option:",
                [
                    "Passport Size Photo",
                    "Custom Dimensions (Pixels)"
                ],
                horizontal=True,
                key="passport_resize_mode"
            )

            # PASSPORT SIZE OPTION

            if resize_mode == "Passport Size Photo":

                st.info(
                    "Standard Passport Photo: "
                    "35 × 45 mm "
                    "(413 × 531 pixels at 300 DPI)"
                )

                width = 413
                height = 531

                st.caption(
                    "The photograph will be centre-cropped "
                    "to the standard 35 × 45 mm aspect ratio."
                )

                # PASSPORT SIZE PREVIEW

                passport_preview = ImageOps.fit(
                    original_image,
                    (206, 266),
                    method=Image.Resampling.LANCZOS,
                    centering=(0.5, 0.5)
                )

                st.image(
                    passport_preview,
                    caption="Passport Size Preview",
                    width=150
                )

                passport_preview.close()

            # CUSTOM DIMENSIONS OPTION

            else:

                st.subheader("Enter Custom Dimensions")

                col1, col2 = st.columns([1, 1.2])

                with col1:

                    width = st.number_input(
                        "Width (Pixels)",
                        min_value=1,
                        max_value=10000,
                        value=100,
                        step=1,
                        key="passport_width"
                    )

                    height = st.number_input(
                        "Height (Pixels)",
                        min_value=1,
                        max_value=10000,
                        value=200,
                        step=1,
                        key="passport_height"
                    )

                    st.info(
                        f"Selected Dimensions: "
                        f"{int(width)} × "
                        f"{int(height)} pixels"
                    )

                with col2:

                    st.markdown("**Live Crop Preview**")

                    # PREVIEW SIZE LIMIT
                    # Maximum preview area: 320 x 320 pixels

                    scale = min(
                        320 / int(width),
                        320 / int(height)
                    )

                    preview_width = max(
                        1,
                        int(int(width) * scale)
                    )

                    preview_height = max(
                        1,
                        int(int(height) * scale)
                    )

                    # LIVE CROP PREVIEW

                    live_preview = ImageOps.fit(
                        original_image,
                        (preview_width, preview_height),
                        method=Image.Resampling.LANCZOS,
                        centering=(0.5, 0.5)
                    )

                    st.image(
                        live_preview,
                        caption=(
                            f"Preview: {int(width)} × "
                            f"{int(height)} px"
                        ),
                        width=preview_width
                    )

                    live_preview.close()

                st.caption(
                    "Change width or height to see "
                    "the crop update automatically."
                )

            st.divider()

            # OUTPUT SETTINGS

            st.subheader("Output Settings")

            output_format = st.selectbox(
                "Select Output Format",
                ["JPG", "PNG"],
                key="passport_output_format"
            )

            if output_format == "JPG":

                jpg_quality = st.slider(
                    "JPG Quality",
                    min_value=50,
                    max_value=100,
                    value=95,
                    step=5,
                    key="passport_jpg_quality"
                )

            else:

                jpg_quality = 95

            st.caption(
                "Crop Position: Centre | "
                "Output dimensions will be exact."
            )

            st.divider()

            # CHECK WHETHER SETTINGS HAVE CHANGED

            current_config = (
                uploaded_photo.name,
                uploaded_photo.size,
                resize_mode,
                int(width),
                int(height),
                output_format,
                jpg_quality
            )

            if (
                st.session_state.get("passport_output_config")
                != current_config
            ):

                st.session_state.pop(
                    "passport_output", None
                )

                st.session_state.pop(
                    "passport_filename", None
                )

                st.session_state.pop(
                    "passport_mime", None
                )

                st.session_state.pop(
                    "passport_width_result", None
                )

                st.session_state.pop(
                    "passport_height_result", None
                )

                st.session_state.pop(
                    "passport_size_result", None
                )

                st.session_state.pop(
                    "passport_output_config", None
                )

            # RESIZE BUTTON

            if st.button(
                "✂️ Resize Photograph",
                use_container_width=True
            ):

                try:

                    with st.spinner("Resizing photograph..."):

                        # APPLY EXACT CROP AND DIMENSIONS

                        resized_image = ImageOps.fit(
                            original_image,
                            (int(width), int(height)),
                            method=Image.Resampling.LANCZOS,
                            centering=(0.5, 0.5)
                        )

                        output_buffer = io.BytesIO()

                        # JPG OUTPUT

                        if output_format == "JPG":

                            # White background for transparent images

                            rgba_image = resized_image.convert("RGBA")

                            background = Image.new(
                                "RGB",
                                rgba_image.size,
                                (255, 255, 255)
                            )

                            background.paste(
                                rgba_image,
                                mask=rgba_image.getchannel("A")
                            )

                            background.save(
                                output_buffer,
                                format="JPEG",
                                quality=jpg_quality,
                                optimize=True
                            )

                            background.close()
                            rgba_image.close()

                            file_extension = "jpg"
                            mime_type = "image/jpeg"

                        # PNG OUTPUT

                        else:

                            resized_image.save(
                                output_buffer,
                                format="PNG",
                                optimize=True
                            )

                            file_extension = "png"
                            mime_type = "image/png"

                        # GET OUTPUT DATA

                        output_bytes = output_buffer.getvalue()

                        original_name = uploaded_photo.name.rsplit(
                            ".", 1
                        )[0]

                        # SAVE OUTPUT IN SESSION STATE

                        st.session_state["passport_output"] = (
                            output_bytes
                        )

                        st.session_state["passport_filename"] = (
                            f"{original_name}_resized."
                            f"{file_extension}"
                        )

                        st.session_state["passport_mime"] = (
                            mime_type
                        )

                        st.session_state["passport_width_result"] = (
                            int(width)
                        )

                        st.session_state["passport_height_result"] = (
                            int(height)
                        )

                        st.session_state["passport_size_result"] = (
                            len(output_bytes) / 1024
                        )

                        st.session_state["passport_output_config"] = (
                            current_config
                        )

                        resized_image.close()
                        output_buffer.close()

                    st.success(
                        "Photograph resized successfully!"
                    )

                except Exception as error:

                    st.error(
                        f"Photo resizing failed: {error}"
                    )

            # DISPLAY GENERATED PHOTO

            if "passport_output" in st.session_state:

                st.divider()

                st.subheader("Resized Photograph")

                st.image(
                    st.session_state["passport_output"],
                    caption="Final Resized Photograph",
                    width=180
                )

                col1, col2 = st.columns(2)

                with col1:

                    st.metric(
                        "Output Width",
                        f"{st.session_state['passport_width_result']} px"
                    )

                with col2:

                    st.metric(
                        "Output Height",
                        f"{st.session_state['passport_height_result']} px"
                    )

                st.metric(
                    "Output File Size",
                    f"{st.session_state['passport_size_result']:.2f} KB"
                )

                # DOWNLOAD BUTTON

                st.download_button(
                    label="⬇️ Download Resized Photograph",
                    data=st.session_state["passport_output"],
                    file_name=st.session_state["passport_filename"],
                    mime=st.session_state["passport_mime"],
                    use_container_width=True
                )

        except Exception as error:

            st.error(
                f"Photo processing failed: {error}"
            )

    else:

        st.info(
            "Please upload a JPG, JPEG or PNG photograph "
            "to get started."
        )


