"""
VAMS - Violence Analysis & Monitoring System
Clean Web Interface
"""

import streamlit as st
import tempfile
import os
import cv2
from pathlib import Path
from processing.video_processor import VideoProcessor
import config

# Page configuration
st.set_page_config(
    page_title="VAMS - Violence Detection",
    page_icon="🎥",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .main {padding: 1rem;}

    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        padding: 0.75rem;
        border-radius: 12px;
        border: none;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }

    [data-testid="stFileUploader"] {
        padding: 2rem;
        border: 2px dashed #667eea;
        border-radius: 16px;
        background: rgba(102, 126, 234, 0.05);
    }

    .stProgress > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }

    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        color: #667eea;
    }

    @media (max-width: 768px) {
        .main {padding: 0.5rem;}
        .stButton>button {font-size: 0.9rem; padding: 0.6rem;}
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("<h1 style='text-align: center; color: #667eea;'>🎥 VAMS</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666; margin-bottom: 2rem;'>Violence Detection System</p>", unsafe_allow_html=True)

# File uploader
uploaded_file = st.file_uploader(
    "Drop video here",
    type=['mp4', 'avi', 'mov', 'mkv', 'webm'],
    label_visibility="collapsed"
)

if uploaded_file is not None:
    # Compact file info
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("File", uploaded_file.name[:12] + "...")
    with col2:
        st.metric("Size", f"{uploaded_file.size / (1024*1024):.1f}MB")
    with col3:
        st.metric("Type", Path(uploaded_file.name).suffix.upper())

    st.markdown("<br>", unsafe_allow_html=True)

    # Optional settings
    with st.expander("⚙️ Settings"):
        sensitivity = st.slider(
            "Detection Sensitivity",
            0.1, 0.5, config.CONF_THRESHOLD, 0.05,
            help="Lower = more sensitive"
        )
        config.CONF_THRESHOLD = sensitivity

    # Analyze button
    if st.button("🚀 Analyze Video"):
        progress_bar = st.progress(0)
        status_text = st.empty()
        preview_placeholder = st.empty()

        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                # Save file
                input_path = os.path.join(temp_dir, uploaded_file.name)
                with open(input_path, 'wb') as f:
                    f.write(uploaded_file.getbuffer())

                output_filename = f"analyzed_{uploaded_file.name}"
                output_path = os.path.join(temp_dir, output_filename)

                # Get total frames
                temp_cap = cv2.VideoCapture(input_path)
                total_frames = int(temp_cap.get(cv2.CAP_PROP_FRAME_COUNT))
                temp_cap.release()

                # Progress callback
                def progress_callback(frame, stats):
                    progress = min(stats['current_frame'] / total_frames, 1.0)
                    progress_bar.progress(progress)
                    status_text.text(f"⚡ {stats['current_frame']}/{total_frames} | Fights: {stats['fight_frames']}")
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    preview_placeholder.image(frame_rgb, use_container_width=True)

                # Process
                processor = VideoProcessor(
                    video_paths=[input_path],
                    output_path=output_path,
                    progress_callback=progress_callback,
                    headless=True
                )

                stats = processor.process()
                progress_bar.progress(1.0)
                status_text.empty()
                preview_placeholder.empty()

                # Read result
                with open(output_path, 'rb') as f:
                    processed_video = f.read()

                st.session_state['processed_video'] = processed_video
                st.session_state['output_filename'] = output_filename
                st.session_state['stats'] = stats

            st.success("✅ Complete!")
            st.rerun()

        except Exception as e:
            st.error(f"❌ {str(e)}")

# Results
if 'processed_video' in st.session_state:
    st.markdown("---")
    stats = st.session_state['stats']

    # Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Frames", stats['total_frames'])
    with col2:
        st.metric("Fights", stats['fight_frames'])
    with col3:
        fight_pct = (stats['fight_frames'] / stats['total_frames'] * 100) if stats['total_frames'] > 0 else 0
        st.metric("Rate", f"{fight_pct:.1f}%")

    st.markdown("<br>", unsafe_allow_html=True)

    # # Video player
    # st.video(st.session_state['processed_video'])

    # Buttons
    st.download_button(
        "⬇️ Download",
        st.session_state['processed_video'],
        st.session_state['output_filename'],
        "video/mp4",
        use_container_width=True
    )

    if st.button("🔄 New Analysis", use_container_width=True):
        for key in ['processed_video', 'output_filename', 'stats']:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()

else:
    if uploaded_file is None:
        st.info("👆 Upload a video to start", icon="ℹ️")
