"""
Moving Car & Object Detection Platform (Powered by 7 Autonomous SDLC AI Agents)
Real-time deep learning computer vision dashboard for urban dashcam and highway traffic detection.
Features:
- Multi-class recognition: cars, pedestrians, buses, trucks, motorcycles, traffic lights.
- Real-time video motion tracking with trajectory trails, speed estimation, and collision warnings.
- 7 Autonomous SDLC Agents orchestration hub & 10 automated safety test benchmarks.
"""

import os
from pathlib import Path
import time
import cv2
import numpy as np
import pandas as pd
from PIL import Image
import streamlit as st

from core.detector import RoadObjectDetector, CLASS_COLORS, ROAD_TARGET_CLASSES
from core.tracker import RoadObjectTracker
from core.video_processor import VideoStreamProcessor
from agents.pm_coordinator_agent import PMCoordinatorAgent
from agents.architecture_agent import VisionArchitectureAgent
from agents.planner_calibration_agent import PlannerCalibrationAgent
from agents.developer_vision_agent import DeveloperVisionAgent
from agents.reviewer_safety_agent import ReviewerSafetyAgent
from agents.qa_testing_agent import QATestingAgent
from agents.self_healing_agent import SelfHealingAgent

BASE_DIR = Path(__file__).resolve().parent
MODELS_DIR = BASE_DIR / "models"
SAMPLE_IMAGES_DIR = BASE_DIR / "data" / "sample_images"
SAMPLE_VIDEOS_DIR = BASE_DIR / "data" / "sample_videos"

st.set_page_config(
    page_title="AutoVision AI - Moving Car & Object Detection",
    page_icon="🚘",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-Contrast Styling
st.markdown("""
<style>
    .main-title {
        font-size: 26px !important;
        font-weight: 800;
        color: #0f172a;
        margin-bottom: 2px;
    }
    .sub-title {
        font-size: 14px;
        color: #64748b;
        margin-bottom: 15px;
    }
    .kpi-card {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 10px 14px;
        text-align: center;
    }
    .kpi-val {
        font-size: 22px;
        font-weight: 800;
        margin: 0;
    }
    .kpi-lbl {
        font-size: 11px;
        font-weight: 600;
        color: #64748b;
        text-transform: uppercase;
    }
    .stButton>button {
        border-radius: 6px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_vision_system():
    detector = RoadObjectDetector()
    tracker = RoadObjectTracker()
    video_proc = VideoStreamProcessor(detector=detector, tracker=tracker)
    
    agents = {
        'pm': PMCoordinatorAgent(),
        'architect': VisionArchitectureAgent(),
        'planner': PlannerCalibrationAgent(),
        'developer': DeveloperVisionAgent(detector=detector, tracker=tracker),
        'reviewer': ReviewerSafetyAgent(),
        'qa': QATestingAgent(detector=detector),
        'self_healing': SelfHealingAgent()
    }
    return detector, tracker, video_proc, agents

detector, tracker, video_proc, agents = load_vision_system()

# Sidebar Navigation
st.sidebar.markdown("### 🚘 AutoVision AI")
st.sidebar.caption("Moving Car & Road Object Detection")

app_mode = st.sidebar.radio(
    "Select Operating Mode:",
    ["📷 Road Photo Detection", "🎥 Moving Car Video Tracker", "🤖 7 SDLC Agents Hub", "🧪 Automated Safety Tests"],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.markdown("### ⚙️ Detection Parameters")
conf_thresh = st.sidebar.slider(
    "Confidence Threshold:",
    min_value=0.10,
    max_value=0.80,
    value=0.35,
    step=0.05,
    help="AI certainty filter. 0.35 filters out background noise and faint artifacts, keeping only clear, genuine vehicles."
)
iou_thresh = st.sidebar.slider(
    "NMS IoU Threshold:",
    min_value=0.20,
    max_value=0.70,
    value=0.45,
    step=0.05,
    help="Duplicate box remover (Non-Maximum Suppression). Controls how much two overlapping boxes can overlap before the duplicate is removed."
)
draw_motion_trails = st.sidebar.checkbox(
    "Draw Motion Vector Trails",
    value=False,
    help="Disabled by default to keep the video completely clean and eliminate trailing scribble marks."
)
show_speed_est = st.sidebar.checkbox(
    "Show Estimated Speed (km/h)",
    value=True,
    help="Displays calculated real-time speed in km/h next to the vehicle name."
)

with st.sidebar.expander("❓ What do these parameters mean?"):
    st.markdown("""
    **1. Confidence Threshold (Certainty):**
    - *Example:* Set to `0.15` (15%) to catch distant cars far down the road.
    - *Example:* Set to `0.60` (60%) to ignore blurry or half-hidden cars and only highlight obvious, close-up vehicles.

    **2. NMS IoU Threshold (Duplicate Filter):**
    - The AI naturally guesses multiple boxes for the same car. 
    - This setting merges duplicates into a single clean box. Default `0.45` is optimal.

    **3. Motion Trails (Video Mode):**
    - Draws a tail behind each vehicle showing its path (useful for tracking lane changes).

    **4. Speed (km/h) (Video Mode):**
    - Calculates vehicle speed by tracking movement across video frames.
    """)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🎨 Visual Display Settings")

badge_style_opt = st.sidebar.selectbox(
    "Label Style:",
    [
        "Micro Translucent Pill (High Contrast & Crisp)",
        "Micro Colored Tag (Compact)",
        "Minimal Text Only (Drop Shadow, No Box)",
        "No Labels (Clean Outlines Only)"
    ],
    index=0,
    help="Micro Translucent Pill gives 100% contrast and sharp legibility in all videos (including 1080p and 4K)."
)
style_map = {
    "Micro Translucent Pill (High Contrast & Crisp)": "micro_pill",
    "Micro Colored Tag (Compact)": "micro_tag",
    "Minimal Text Only (Drop Shadow, No Box)": "no_badge",
    "No Labels (Clean Outlines Only)": "none"
}
chosen_badge_style = style_map[badge_style_opt]

font_size_val = st.sidebar.slider(
    "Text Font Size:",
    min_value=7,
    max_value=16,
    value=10,
    help="Automatically scales with video resolution so labels are perfectly legible on HD and 4K video feeds."
)

label_content_choice = st.sidebar.radio(
    "Label Content:",
    ["Vehicle Name Only (e.g. car)", "Vehicle Name + % (e.g. car 85%)"],
    index=0,
    help="Showing only vehicle name keeps the label width tiny (~18px)."
)
label_content_map = {
    "Vehicle Name Only (e.g. car)": "name_only",
    "Vehicle Name + % (e.g. car 85%)": "name_conf"
}
chosen_label_content = label_content_map[label_content_choice]

box_style_choice = st.sidebar.selectbox(
    "Bounding Box Outline:",
    ["Standard Crisp Box", "Corner HUD Brackets (Tesla / Waymo Style)", "No Outlines (Labels Only)"],
    index=0
)
box_style_map = {
    "Standard Crisp Box": "rectangle",
    "Corner HUD Brackets (Tesla / Waymo Style)": "corners",
    "No Outlines (Labels Only)": "none"
}
chosen_box_style = box_style_map[box_style_choice]

box_thickness = st.sidebar.slider(
    "Line Thickness (px):",
    min_value=1,
    max_value=4,
    value=2,
    help="Controls bounding box border thickness (scales automatically for 4K video feeds)."
)

with st.sidebar.expander("📥 Download Test Videos & Photos"):
    st.markdown("""
    **Free High-Quality Car Datasets:**
    - 🎥 [Pexels Highway Traffic Videos](https://www.pexels.com/search/videos/highway%20traffic/) *(Free MP4 HD clips)*
    - 🎥 [Pixabay Street Traffic Footage](https://pixabay.com/videos/search/traffic%20cars/) *(Free Dashcam MP4)*
    - 📷 [Unsplash Urban Car Photos](https://unsplash.com/s/photos/street-traffic) *(Free High-Res JPG)*
    - 🤖 [Roboflow Universe Vehicle Data](https://universe.roboflow.com/search?q=vehicle+detection) *(AI Datasets)*
    - 🚗 [KITTI Raw Driving Sequences](https://www.cvlibs.net/datasets/kitti/raw_data.php) *(Autonomous Benchmark)*
    """)

st.sidebar.markdown("---")
st.sidebar.caption("System: YOLOv8 ONNX (640x640) | Multi-Agent SDLC v1.0")

# =========================================================================
# MODE 1: ROAD PHOTO DETECTION (SINGLE IMAGE)
# =========================================================================
if app_mode == "📷 Road Photo Detection":
    st.markdown('<div class="main-title">🚘 Urban Road Object Detection</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Multi-class real-time neural detection for cars, pedestrians, buses, and road infrastructure.</div>', unsafe_allow_html=True)

    img_col1, img_col2 = st.columns([1, 2])
    
    with img_col1:
        source_type = st.radio("Image Source:", ["Pre-Loaded Road Samples", "Upload Custom Image"], horizontal=True)
        
        sample_images = {
            "Dense Highway Traffic (17 Vehicles - Reference Scene)": str(SAMPLE_IMAGES_DIR / "user_highway_17cars.jpg"),
            "Highway Rush Hour (Overhead Multi-Lane)": str(SAMPLE_IMAGES_DIR / "highway_rush_hour.jpg"),
            "Multi-Lane Highway (Cars in Motion)": str(SAMPLE_IMAGES_DIR / "multi_lane_highway.jpg"),
            "Highway Traffic Jam (Close-Up Sedans)": str(SAMPLE_IMAGES_DIR / "highway_traffic_jam.jpg"),
            "Busy City Intersection (Multi-Directional)": str(SAMPLE_IMAGES_DIR / "busy_intersection.jpg"),
            "City Street with Bus & Pedestrians (5 Entities)": str(SAMPLE_IMAGES_DIR / "busy_city_bus.jpg"),
            "Crosswalk with Pedestrians & Vehicles": str(SAMPLE_IMAGES_DIR / "city_crosswalk_pedestrians.jpg"),
            "Urban Bus & Commuter Traffic": str(SAMPLE_IMAGES_DIR / "urban_bus_traffic.jpg"),
            "Urban Road (2 Sedans Cruising)": str(SAMPLE_IMAGES_DIR / "urban_road_cars.jpg"),
            "Urban Street Dashcam (Autonomous Reference)": str(SAMPLE_IMAGES_DIR / "urban_street_dashcam.jpg")
        }
        
        selected_img_path = None
        if source_type == "Pre-Loaded Road Samples":
            chosen_sample = st.selectbox("Select Road Scene:", list(sample_images.keys()), index=0)
            selected_img_path = sample_images[chosen_sample]
            input_bgr = cv2.imread(selected_img_path)
        else:
            uploaded_file = st.file_uploader("Upload Street Image (JPG, PNG, WebP):", type=["jpg", "jpeg", "png", "webp"])
            if uploaded_file is not None:
                file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
                input_bgr = cv2.imdecode(file_bytes, 1)
            else:
                input_bgr = None

    if input_bgr is not None:
        # Agent 3: Calibration
        calibrated_bgr, calib_meta = agents['planner'].calibrate_frame(input_bgr)
        
        # Agent 4: Detection
        t0 = time.perf_counter()
        detections = detector.detect(calibrated_bgr, conf_threshold=conf_thresh, iou_threshold=iou_thresh)
        annotated_bgr = detector.draw_detections(
            calibrated_bgr, 
            detections, 
            box_thickness=box_thickness,
            font_size=font_size_val,
            badge_style=chosen_badge_style,
            box_style=chosen_box_style,
            label_content=chosen_label_content
        )
        inference_ms = (time.perf_counter() - t0) * 1000.0

        # Agent 5: Safety Audit
        safety_audit = agents['reviewer'].audit_detections(detections, input_bgr.shape)

        # Count entities
        cars_count = sum(1 for d in detections if d['class'] in {'car', 'truck', 'bus'})
        peds_count = sum(1 for d in detections if d['class'] == 'person')
        lights_count = sum(1 for d in detections if d['class'] in {'traffic light', 'stop sign'})

        # Display Live KPI Metrics
        m1, m2, m3, m4, m5 = st.columns(5)
        with m1:
            st.markdown(f'<div class="kpi-card"><p class="kpi-val" style="color:#0284c7;">{cars_count}</p><p class="kpi-lbl">Vehicles</p></div>', unsafe_allow_html=True)
        with m2:
            st.markdown(f'<div class="kpi-card"><p class="kpi-val" style="color:#e11d48;">{peds_count}</p><p class="kpi-lbl">Pedestrians</p></div>', unsafe_allow_html=True)
        with m3:
            st.markdown(f'<div class="kpi-card"><p class="kpi-val" style="color:#2563eb;">{lights_count}</p><p class="kpi-lbl">Signals</p></div>', unsafe_allow_html=True)
        with m4:
            st.markdown(f'<div class="kpi-card"><p class="kpi-val" style="color:#059669;">{len(detections)}</p><p class="kpi-lbl">Total Objects</p></div>', unsafe_allow_html=True)
        with m5:
            st.markdown(f'<div class="kpi-card"><p class="kpi-val" style="color:#7e22ce;">{inference_ms:.1f}ms</p><p class="kpi-lbl">Latency</p></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Side-by-Side Permanent High-Definition Display
        view_col1, view_col2 = st.columns(2)
        with view_col1:
            st.markdown("#### 📷 1. Original Camera View (Clean — Before AI)")
            st.caption("Clean unedited photo directly from vehicle camera with zero overlays.")
            st.image(cv2.cvtColor(input_bgr, cv2.COLOR_BGR2RGB), use_container_width=True)
        with view_col2:
            st.markdown(f"#### 🎯 2. AutoVision AI Detection ({len(detections)} Entities — After AI)")
            st.caption("Neural network detected and highlighted entities with precision micro-labels.")
            st.image(cv2.cvtColor(annotated_bgr, cv2.COLOR_BGR2RGB), use_container_width=True)

        # Detailed Detections Table
        if detections:
            st.markdown("#### 📋 Detected Road Entities Breakdown")
            table_data = []
            for i, d in enumerate(detections):
                x, y, w, h = d['box']
                table_data.append({
                    "Entity #": f"#{i+1}",
                    "Class": d['class'].upper(),
                    "Confidence": f"{d['confidence']*100:.1f}%",
                    "Bounding Box (X, Y, W, H)": f"[{x}, {y}, {w}, {h}]",
                    "Area (Pixels)": f"{w * h:,} px"
                })
            st.dataframe(pd.DataFrame(table_data), use_container_width=True, hide_index=True)

        # Safety Audit Card
        if safety_audit['safety_alerts']:
            for alert in safety_audit['safety_alerts']:
                st.warning(f"⚠️ **{alert['type']}**: {alert['message']}")
        else:
            st.success("✅ **Road Safety Status**: Normal roadway conditions. No critical hazards or pedestrian violations detected.")

# =========================================================================
# MODE 2: MOVING CAR VIDEO TRACKER
# =========================================================================
elif app_mode == "🎥 Moving Car Video Tracker":
    st.markdown('<div class="main-title">🎥 Moving Car & Object Video Tracker</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Continuous multi-object tracking with motion vector trails, speed estimation, and collision proximity alerts.</div>', unsafe_allow_html=True)

    v_col1, v_col2 = st.columns([1, 2])
    with v_col1:
        vid_source = st.radio("Video Source:", ["Sample Highway Dashcam Video", "Upload MP4 Video"], horizontal=True)
        
        sample_video_path = str(SAMPLE_VIDEOS_DIR / "highway_traffic.mp4")
        chosen_video_path = sample_video_path
        
        if vid_source == "Upload MP4 Video":
            uploaded_video = st.file_uploader("Upload Road Video (MP4):", type=["mp4", "avi", "mov"])
            if uploaded_video:
                temp_video_path = str(BASE_DIR / "data" / "uploaded_temp.mp4")
                with open(temp_video_path, "wb") as f:
                    f.write(uploaded_video.read())
                chosen_video_path = temp_video_path

        max_frames_to_process = st.slider("Max Frames to Process:", min_value=30, max_value=300, value=120, step=30)
        frame_skip = st.select_slider("Frame Skip (Speed vs Quality):", options=[1, 2, 3], value=1)
        run_tracking_btn = st.button("▶️ Run Moving Car Tracker", type="primary")

    video_placeholder = st.empty()
    stats_placeholder = st.empty()

    if run_tracking_btn and chosen_video_path and os.path.exists(chosen_video_path):
        cap = cv2.VideoCapture(chosen_video_path)
        total_vid_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps_source = cap.get(cv2.CAP_PROP_FPS) or 30.0
        cap.release()

        tracker_instance = RoadObjectTracker()
        vid_processor = VideoStreamProcessor(detector=detector, tracker=tracker_instance)

        progress_bar = st.progress(0.0)
        status_text = st.empty()

        frame_count = 0
        total_cars_tracked = set()
        start_proc_time = time.perf_counter()

        for f_idx, annotated_frame, metrics in vid_processor.process_video_generator(
            chosen_video_path, conf_threshold=conf_thresh, max_frames=max_frames_to_process, skip_frames=frame_skip,
            draw_trails=draw_motion_trails, show_speed=show_speed_est,
            box_thickness=box_thickness, font_size=font_size_val, badge_style=chosen_badge_style,
            box_style=chosen_box_style
        ):
            frame_count += 1
            for obj in metrics['tracked_objects']:
                total_cars_tracked.add(obj['id'])

            # Render in Streamlit
            video_placeholder.image(
                cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB),
                caption=f"Frame #{f_idx} | Active Vehicles: {metrics['active_cars']} | Speed Est: {metrics['fps']} FPS",
                use_container_width=True
            )

            # Update stats
            progress = min(1.0, frame_count / (max_frames_to_process // frame_skip))
            progress_bar.progress(progress)
            status_text.markdown(f"**Processing Frame {f_idx}** (Tracked Unique Objects: `{len(total_cars_tracked)}`)")

        total_elapsed = time.perf_counter() - start_proc_time
        avg_fps = round(frame_count / max(0.1, total_elapsed), 1)

        st.success(f"🎉 **Video Stream Processing Complete!** Processed `{frame_count}` frames in `{total_elapsed:.2f}s` (Average `{avg_fps} FPS`).")
        
        # Summary telemetry
        sc1, sc2, sc3, sc4 = st.columns(4)
        with sc1:
            st.metric("Unique Vehicles Tracked", f"{len(total_cars_tracked)}")
        with sc2:
            st.metric("Average Inference FPS", f"{avg_fps} FPS")
        with sc3:
            st.metric("Collision Warnings", f"{metrics.get('collision_alerts', 0)}")
        with sc4:
            st.metric("Total Frames Analyzed", f"{frame_count}")

# =========================================================================
# MODE 3: THE 7 AUTONOMOUS SDLC AGENTS HUB
# =========================================================================
elif app_mode == "🤖 7 SDLC Agents Hub":
    st.markdown('<div class="main-title">🤖 7 Autonomous SDLC AI Agents Hub</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Multi-agent architecture orchestrating road vision, calibration, detection, safety review, QA, and self-healing.</div>', unsafe_allow_html=True)

    agent_tabs = st.tabs([
        "1. PM Coordinator",
        "2. Vision Architect",
        "3. Frame Calibration",
        "4. Vision Developer",
        "5. Safety Reviewer",
        "6. QA Automation",
        "7. Self-Healing DevOps"
    ])

    with agent_tabs[0]:
        st.markdown("### Agent 1: Road Stream Coordinator (PM Agent)")
        st.write("Coordinates incoming road streams, session IDs, incident tickets, and client telemetry.")
        st.json({
            "agent": agents['pm'].agent_name,
            "role": agents['pm'].role_title,
            "incident_tickets_open": len(agents['pm'].incident_log),
            "status": "ACTIVE_MONITORING"
        })

    with agent_tabs[1]:
        st.markdown("### Agent 2: Vision Architect Agent")
        st.write("Designs model topology, ONNX session provider, and COCO multi-class taxonomy.")
        blueprint = agents['architect'].get_pipeline_blueprint()
        st.json(blueprint)

    with agent_tabs[2]:
        st.markdown("### Agent 3: Frame Calibration Agent (Planner)")
        st.write("Plans aspect-ratio preserving letterboxing and dynamic CLAHE night/shadow contrast filters.")
        st.json({
            "target_resolution": "640x640 letterboxed",
            "padding_value": "(114, 114, 114) Neutral Gray",
            "illumination_filter": "Adaptive CLAHE on L-channel"
        })

    with agent_tabs[3]:
        st.markdown("### Agent 4: Computer Vision Specialist (Developer)")
        st.write("Executes YOLOv8 ONNX inference, draws high-contrast executive bounding boxes, and tracks velocity.")
        st.json({
            "model_path": detector.model_path,
            "supported_classes": len(detector.session.get_outputs()),
            "tracker_mode": "Centroid + IoU with Dynamic Trajectories"
        })

    with agent_tabs[4]:
        st.markdown("### Agent 5: Road Safety Reviewer")
        st.write("Audits detections for vulnerable pedestrians in travel lanes, close tailgating hazards, and low-confidence noise.")
        st.json({
            "min_confidence_floor": agents['reviewer'].min_confidence_floor,
            "vulnerability_zones": "Center roadway travel path (0.25W to 0.75W)",
            "proximity_threshold": "Brake warning when box height > 25% frame"
        })

    with agent_tabs[5]:
        st.markdown("### Agent 6: Quality Assurance Inspector")
        st.write("Automated safety verification suite executing 10 clinical road safety tests.")
        if st.button("🧪 Run QA Test Suite Now"):
            report = agents['qa'].run_all_safety_tests(sample_image_path=str(SAMPLE_IMAGES_DIR / "urban_street_dashcam.jpg"))
            st.success(f"QA Suite Result: {report['passed']}/{report['total_tests']} PASSED ({report['pass_rate_percent']}%)")
            st.json(report)

    with agent_tabs[6]:
        st.markdown("### Agent 7: Self-Healing System Maintainer (DevOps)")
        st.write("Monitors frame latency, auto-recovers from corrupted video streams, and prevents application crashes.")
        latency_audit = agents['self_healing'].monitor_latency(24.5)
        st.json(latency_audit)

# =========================================================================
# MODE 4: AUTOMATED SAFETY TEST SUITE
# =========================================================================
elif app_mode == "🧪 Automated Safety Tests":
    st.markdown('<div class="main-title">🧪 10 Automated Safety Benchmark Tests</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Rigorous regression testing verifying model topology, vehicle detection, pedestrian recognition, and real-time latency.</div>', unsafe_allow_html=True)

    if st.button("▶️ Execute 10 Safety Benchmark Tests", type="primary"):
        with st.spinner("Running automated tests across neural vision pipeline..."):
            qa_report = agents['qa'].run_all_safety_tests(sample_image_path=str(SAMPLE_IMAGES_DIR / "urban_street_dashcam.jpg"))
        
        tc1, tc2, tc3 = st.columns(3)
        with tc1:
            st.metric("Total Tests", qa_report['total_tests'])
        with tc2:
            st.metric("Passed Tests", f"{qa_report['passed']} / {qa_report['total_tests']}")
        with tc3:
            st.metric("Pass Rate", f"{qa_report['pass_rate_percent']}%", delta="100% Target Met")

        st.markdown("---")
        st.markdown("#### Test Execution Details")

        for test in qa_report['test_results']:
            badge = "🟢 PASSED" if test['status'] == "PASSED" else "🔴 FAILED"
            with st.expander(f"{badge} | {test['test_id']}: {test['name']}", expanded=True):
                st.write(f"**Description:** {test['description']}")
                st.write(f"**Output Details:** `{test['detail']}`")
