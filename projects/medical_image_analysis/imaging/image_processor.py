"""
Enterprise Clinical Multimodal Medical Image Synthesis & DICOM Processing Engine
Supports X-Rays, MRIs, and CT Scans with Subtle Pattern & Anomaly Highlighting.
Designed to demonstrate how AI assists doctors in catching hard-to-notice pathologies.
"""
import os
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageStat, ImageEnhance

class MedicalImageProcessor:
    """Multimodal Medical Imaging Engine for X-Ray, MRI, and CT Scans."""

    @staticmethod
    def generate_synthetic_scan(scan_type: str, output_path: str, overlay: bool = True) -> str:
        """
        Generates realistic clinical scans across three core modalities:
        - X-RAY: 'XRAY_PNEUMONIA', 'XRAY_CARDIOMEGALY', 'XRAY_PNEUMOTHORAX', 'XRAY_NORMAL'
        - MRI: 'MRI_TUMOR' (Glioblastoma), 'MRI_MS_PLAQUES' (Subtle MS Demyelinating Plaques)
        - CT: 'CT_STROKE' (Acute Ischemic Stroke on Head CT), 'CT_NODULE' (Chest CT Sub-cm Nodule)
        """
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        st_upper = scan_type.upper()
        width, height = 512, 512

        # =========================================================================
        # 1. CT SCANS (Computed Tomography)
        # =========================================================================
        if "CT" in st_upper:
            img = Image.new("RGB", (width, height), color=(8, 10, 14))
            draw = ImageDraw.Draw(img)

            if "STROKE" in st_upper or "HEAD" in st_upper:
                # Axial Non-Contrast Head CT Slice (Stroke Protocol)
                # Calvarium (Dense White Cortical Bone: ~1000 HU)
                draw.ellipse([80, 55, 432, 455], fill=(240, 242, 245), outline=(255, 255, 255), width=7)
                # Diploe / Inner Table Bone
                draw.ellipse([92, 67, 420, 443], fill=(18, 22, 28))
                # Brain Parenchyma (Soft Tissue: ~30-40 HU)
                draw.ellipse([100, 75, 412, 435], fill=(70, 75, 82))

                # Falx Cerebri (Midline Dura)
                draw.line([(256, 78), (256, 430)], fill=(45, 50, 58), width=3)

                # Bilateral Frontal Horns of Lateral Ventricles (CSF: ~0-10 HU)
                draw.ellipse([218, 205, 248, 280], fill=(22, 25, 30))
                draw.ellipse([264, 205, 294, 280], fill=(22, 25, 30))
                # Third ventricle
                draw.rectangle([252, 275, 260, 310], fill=(22, 25, 30))

                # Normal subtle sulci (Left hemisphere)
                for angle in range(190, 350, 20):
                    rad = math.radians(angle)
                    x1 = int(256 + 135 * math.cos(rad))
                    y1 = int(255 + 155 * math.sin(rad))
                    x2 = int(256 + 115 * math.cos(rad))
                    y2 = int(255 + 135 * math.sin(rad))
                    draw.line([(x1, y1), (x2, y2)], fill=(50, 55, 62), width=2)

                # SUBTLE PATHOLOGY: Early Acute Ischemic Stroke (Right MCA Territory)
                # Very subtle hypodensity (loss of gray-white matter differentiation & insular ribbon)
                # Naked eye struggles to distinguish this 28 HU region from normal 36 HU brain!
                draw.ellipse([125, 170, 215, 295], fill=(58, 62, 70))
                draw.ellipse([135, 185, 200, 275], fill=(52, 56, 64))

                if overlay:
                    # AI ATTENTION HEATMAP: Dynamic Colorized HU Attenuation Disparity Map
                    # Shows ischemic core in translucent crimson/magenta and penumbra in cyan
                    draw.ellipse([120, 165, 220, 300], outline=(236, 72, 153), width=3)
                    draw.ellipse([130, 180, 205, 280], outline=(239, 68, 68), width=2)
                    
                    # Attention gradient lines
                    draw.arc([115, 160, 225, 305], start=45, end=270, fill=(245, 158, 11), width=2)
                    
                    # Crosshair measurement & HU readout
                    draw.line([(170, 150), (170, 315)], fill=(236, 72, 153), width=1)
                    draw.line([(105, 235), (235, 235)], fill=(236, 72, 153), width=1)
                    draw.text((120, 145), "HU DISPARITY: -8.4 HU", fill=(253, 230, 138))

                    # AI Detection Alert Box
                    draw.rectangle([15, 460, 497, 498], fill=(112, 26, 117), outline=(236, 72, 153), width=2)
                    draw.text((25, 468), "AI ATTENTION: Early Right MCA Acute Ischemic Stroke (Loss of Insular Ribbon)", fill=(253, 242, 248))

                # CT PACS HUD
                draw.text((20, 15), "NON-CONTRAST HEAD CT (AXIAL) - STROKE CODE PROTOCOL", fill=(56, 189, 248))
                draw.text((430, 15), "W: 80 L: 40", fill=(148, 163, 184))
                draw.text((430, 30), "Slice: 5.0mm", fill=(148, 163, 184))
                draw.text((20, 30), "PATIENT: MARCUS A. REID (59M) | CT-STROKE-7721", fill=(148, 163, 184))
                draw.text((470, 240), "R", fill=(56, 189, 248))
                draw.text((30, 240), "L", fill=(56, 189, 248))

            else:
                # Axial Chest CT (Pulmonary Window W:1500 L:-600)
                # Outer Thoracic Wall
                draw.ellipse([60, 70, 452, 440], fill=(20, 24, 32), outline=(180, 185, 195), width=4)
                # Spine / Vertebral Body
                draw.rectangle([236, 360, 276, 420], fill=(220, 225, 230))
                # Mediastinum & Cardiac Outline (Soft tissue)
                draw.ellipse([180, 200, 332, 380], fill=(65, 72, 82))
                # Trachea / Bronchi bifurcation
                draw.ellipse([246, 215, 266, 235], fill=(8, 10, 14))

                # Right & Left Lung Fields (Very dark air density: ~ -800 HU)
                draw.chord([85, 95, 235, 410], start=30, end=330, fill=(18, 22, 28))
                draw.chord([277, 95, 427, 410], start=210, end=150, fill=(18, 22, 28))

                # Pulmonary Vascular Branching (Subtle white arborizing vessels)
                for i in range(5):
                    draw.line([(180, 250), (120 + i*15, 200 + i*30)], fill=(75, 82, 92), width=2)
                    draw.line([(330, 250), (390 - i*15, 200 + i*30)], fill=(75, 82, 92), width=2)

                # SUBTLE PATHOLOGY: 6.4mm Sub-Centimeter Solitary Ground-Glass Nodule (Left Posterior)
                # Faint density (-350 HU) that blends into normal pulmonary vasculature
                draw.ellipse([345, 320, 368, 343], fill=(130, 138, 150))
                draw.ellipse([350, 325, 363, 338], fill=(175, 182, 195))

                if overlay:
                    # AI 3D Volumetric Contour & Target Reticle
                    draw.ellipse([335, 310, 378, 353], outline=(245, 158, 11), width=2)
                    draw.line([(356, 300), (356, 363)], fill=(245, 158, 11), width=1)
                    draw.line([(325, 331), (388, 331)], fill=(245, 158, 11), width=1)
                    draw.text((285, 295), "6.4mm GROUND-GLASS NODULE", fill=(245, 158, 11))

                    draw.rectangle([15, 460, 497, 498], fill=(120, 53, 15), outline=(245, 158, 11), width=2)
                    draw.text((25, 468), "AI DETECTION: High-Resolution Chest CT 6.4mm Sub-Centimeter Nodule", fill=(254, 243, 199))

                draw.text((20, 15), "CHEST HIGH-RESOLUTION CT (LUNG WINDOW: W:1500 L:-600)", fill=(56, 189, 248))
                draw.text((430, 15), "120 kVp", fill=(148, 163, 184))
                draw.text((430, 30), "Slice: 1.25mm", fill=(148, 163, 184))
                draw.text((20, 30), "PATIENT: ARTHUR PENDRICK (54M) | CT-CHEST-9932", fill=(148, 163, 184))
                draw.text((470, 240), "R", fill=(56, 189, 248))
                draw.text((30, 240), "L", fill=(56, 189, 248))

            img.save(output_path, "PNG")
            return output_path

        # =========================================================================
        # 2. MRI SCANS (Magnetic Resonance Imaging)
        # =========================================================================
        if "MRI" in st_upper or "TUMOR" in st_upper or "PLAQUE" in st_upper:
            img = Image.new("RGB", (width, height), color=(10, 14, 20))
            draw = ImageDraw.Draw(img)

            # Skull Outer Contour
            draw.ellipse([80, 50, 432, 450], fill=(22, 28, 38), outline=(130, 140, 155), width=4)
            # Subdural space / CSF
            draw.ellipse([92, 62, 420, 438], fill=(30, 36, 48), outline=(60, 70, 85), width=2)
            # Cerebral Hemispheres
            draw.ellipse([100, 70, 412, 430], fill=(75, 82, 95))

            # Interhemispheric Fissure
            draw.line([(256, 75), (256, 425)], fill=(35, 42, 55), width=3)

            # Lateral Ventricles
            draw.ellipse([215, 200, 248, 290], fill=(25, 30, 40))
            draw.ellipse([264, 200, 297, 290], fill=(25, 30, 40))
            draw.ellipse([228, 230, 245, 275], fill=(15, 20, 28))
            draw.ellipse([267, 230, 284, 275], fill=(15, 20, 28))

            # Gyri cortical patterns
            for angle in range(0, 360, 18):
                rad = math.radians(angle)
                x1 = int(256 + 140 * math.cos(rad))
                y1 = int(250 + 160 * math.sin(rad))
                x2 = int(256 + 110 * math.cos(rad))
                y2 = int(250 + 130 * math.sin(rad))
                draw.line([(x1, y1), (x2, y2)], fill=(55, 62, 75), width=2)

            if "PLAQUE" in st_upper or "MS" in st_upper:
                # MULTIPLE SCLEROSIS: Subtle Periventricular Demyelinating Micro-Plaques
                # Small 3-5mm hyperintense spots radiating perpendicular to ventricles (Dawson's fingers)
                plaque_locs = [(200, 195), (205, 270), (305, 210), (312, 265)]
                for px, py in plaque_locs:
                    draw.ellipse([px, py, px + 12, py + 12], fill=(195, 205, 220))
                    draw.ellipse([px + 2, py + 2, px + 10, py + 10], fill=(230, 238, 250))

                if overlay:
                    # AI Multi-Target Highlight Reticles
                    for i, (px, py) in enumerate(plaque_locs):
                        draw.ellipse([px - 6, py - 6, px + 18, py + 18], outline=(168, 85, 247), width=2)
                        draw.line([(px + 6, py - 12), (px + 6, py + 24)], fill=(168, 85, 247), width=1)
                        draw.line([(px - 12, py + 6), (px + 24, py + 6)], fill=(168, 85, 247), width=1)
                        draw.text((px + 14, py - 10), f"Plaque #{i+1}", fill=(216, 180, 254))

                    draw.rectangle([15, 460, 497, 498], fill=(88, 28, 135), outline=(168, 85, 247), width=2)
                    draw.text((25, 468), "AI DETECTION: 4 Periventricular Demyelinating Micro-Plaques (Multiple Sclerosis)", fill=(243, 232, 255))

                draw.text((20, 15), "BRAIN MRI (AXIAL T2/FLAIR) - DEMYELINATING PROTOCOL", fill=(56, 189, 248))
                draw.text((430, 15), "TR: 9200ms", fill=(148, 163, 184))
                draw.text((430, 30), "TE: 125ms", fill=(148, 163, 184))
                draw.text((20, 30), "PATIENT: CLAIRE TEMPLE (38F) | MRN-44812-MS", fill=(148, 163, 184))

            else:
                # BRAIN TUMOR (Glioblastoma / Neoplasm)
                # Surrounding Vasogenic Edema
                draw.ellipse([135, 125, 235, 225], fill=(60, 68, 80))
                # Contrast-enhancing active tumor rim
                draw.ellipse([150, 140, 218, 208], fill=(235, 240, 250))
                # Central Necrotic Core
                draw.ellipse([170, 160, 198, 188], fill=(140, 145, 160))

                if overlay:
                    # AI Neoplasm Segmentation Mask & Calipers
                    draw.ellipse([145, 135, 223, 213], outline=(239, 68, 68), width=3)
                    draw.rectangle([130, 120, 240, 230], outline=(245, 158, 11), width=1)
                    draw.line([(184, 110), (184, 240)], fill=(245, 158, 11), width=1)
                    draw.line([(120, 174), (250, 174)], fill=(245, 158, 11), width=1)

                    draw.rectangle([15, 460, 497, 498], fill=(127, 29, 29), outline=(239, 68, 68), width=2)
                    draw.text((25, 468), "AI DETECTION: Right Frontal Lobe Mass (28.4mm Hyperdense Neoplasm)", fill=(254, 202, 202))

                draw.text((20, 15), "BRAIN MRI (AXIAL T2/FLAIR) - CONTRAST ENHANCED", fill=(56, 189, 248))
                draw.text((430, 15), "TR: 9000ms", fill=(148, 163, 184))
                draw.text((430, 30), "TE: 110ms", fill=(148, 163, 184))
                draw.text((20, 30), "PATIENT: ELEANOR VANCE (62F) | MRN-90281-V", fill=(148, 163, 184))

            draw.text((470, 240), "R", fill=(56, 189, 248))
            draw.text((30, 240), "L", fill=(56, 189, 248))

            img.save(output_path, "PNG")
            return output_path

        # =========================================================================
        # 3. X-RAY SCANS (Chest Radiography CXR)
        # =========================================================================
        img = Image.new("RGB", (width, height), color=(12, 16, 24))
        draw = ImageDraw.Draw(img)

        # Bilateral Hemithorax / Lung Cavities
        draw.ellipse([65, 80, 225, 430], fill=(38, 44, 52))
        draw.ellipse([287, 80, 447, 430], fill=(38, 44, 52))

        # Thoracic Spine & Mediastinum
        draw.rectangle([235, 60, 277, 455], fill=(125, 130, 140))
        # Trachea air column
        draw.rectangle([250, 60, 262, 180], fill=(30, 35, 42))

        # Bilateral Diaphragmatic Hemidomes
        draw.chord([55, 380, 235, 460], start=0, end=180, fill=(110, 115, 125))
        draw.chord([277, 390, 457, 470], start=0, end=180, fill=(105, 110, 120))

        # Clavicles
        draw.arc([55, 55, 235, 105], start=0, end=180, fill=(155, 160, 170), width=6)
        draw.arc([277, 55, 457, 105], start=0, end=180, fill=(155, 160, 170), width=6)

        # Rib Shadows
        for y in range(115, 410, 32):
            draw.arc([55, y, 230, y + 45], start=0, end=180, fill=(70, 78, 88), width=3)
            draw.arc([282, y, 457, y + 45], start=0, end=180, fill=(70, 78, 88), width=3)

        if "PNEUMOTHORAX" in st_upper:
            # Normal cardiac silhouette
            draw.ellipse([205, 235, 315, 395], fill=(155, 160, 170))
            
            # SUBTLE PATHOLOGY: Faint Apical Pneumothorax (Right Apex)
            # Thin visceral pleural retraction line, with absence of broncho-vascular markings peripherally
            draw.arc([75, 85, 215, 175], start=210, end=330, fill=(65, 75, 88), width=2)
            # Slightly hyper-lucent peripheral apex (free air)
            draw.chord([80, 85, 210, 160], start=200, end=340, fill=(22, 28, 35))

            if overlay:
                # Fluorescent AI edge highlight of the visceral pleural line
                draw.arc([75, 85, 215, 175], start=210, end=330, fill=(56, 189, 248), width=3)
                draw.text((80, 70), "VISCERAL PLEURAL LINE (14% RETRACTION)", fill=(56, 189, 248))
                draw.line([(145, 95), (145, 120)], fill=(56, 189, 248), width=2)

                draw.rectangle([15, 460, 497, 498], fill=(12, 74, 110), outline=(56, 189, 248), width=2)
                draw.text((25, 468), "AI DETECTION: Subtle Right Apical Pneumothorax (Visceral Pleural Line Identified)", fill=(224, 242, 254))

            draw.text((20, 15), "CHEST RADIOGRAPHY (CXR PA VIEW) — APICAL PNEUMOTHORAX", fill=(56, 189, 248))

        elif "CARDIOMEGALY" in st_upper:
            # Greatly enlarged globular cardiac silhouette (CTR > 0.62)
            draw.ellipse([135, 210, 380, 415], fill=(175, 180, 190))
            draw.ellipse([220, 165, 260, 205], fill=(160, 165, 175))

            if overlay:
                draw.line([(135, 325), (380, 325)], fill=(239, 68, 68), width=3)
                draw.line([(135, 315), (135, 335)], fill=(239, 68, 68), width=3)
                draw.line([(380, 315), (380, 335)], fill=(239, 68, 68), width=3)
                draw.text((215, 305), "Heart: 318px", fill=(254, 202, 202))

                draw.line([(65, 410), (447, 410)], fill=(56, 189, 248), width=2)
                draw.line([(65, 402), (65, 418)], fill=(56, 189, 248), width=2)
                draw.line([(447, 402), (447, 418)], fill=(56, 189, 248), width=2)
                draw.text((220, 392), "Thorax: 512px", fill=(56, 189, 248))

                draw.rectangle([15, 460, 497, 498], fill=(127, 29, 29), outline=(239, 68, 68), width=2)
                draw.text((25, 468), "CARDIOMEGALY: CTR = 0.62 (> 0.50 Threshold) — Marked Ventricular Enlargement", fill=(254, 202, 202))

            draw.text((20, 15), "CHEST RADIOGRAPHY (CXR PA VIEW) — CARDIOMEGALY", fill=(56, 189, 248))

        elif "PNEUMONIA" in st_upper:
            draw.ellipse([205, 235, 315, 395], fill=(155, 160, 170))
            # Dense irregular consolidation opacity in Right Lower Lobe
            draw.ellipse([90, 260, 225, 415], fill=(215, 222, 232))
            draw.ellipse([110, 280, 210, 395], fill=(242, 246, 255))
            draw.ellipse([130, 300, 195, 380], fill=(255, 255, 255))

            if overlay:
                draw.rectangle([80, 250, 235, 425], outline=(239, 68, 68), width=3)
                draw.text((85, 232), "[!] CONSOLIDATION INFILTRATE (78% OPACITY)", fill=(239, 68, 68))
                draw.line([(155, 250), (155, 275)], fill=(239, 68, 68), width=2)

                draw.rectangle([15, 460, 497, 498], fill=(127, 29, 29), outline=(239, 68, 68), width=2)
                draw.text((25, 468), "PNEUMONIA DETECTED: Acute Lobar Consolidation in Right Lower Lobe", fill=(254, 202, 202))

            draw.text((20, 15), "CHEST RADIOGRAPHY (CXR PA VIEW) — BACTERIAL PNEUMONIA", fill=(56, 189, 248))

        else:
            # Normal Chest X-Ray
            draw.ellipse([205, 235, 315, 395], fill=(155, 160, 170))

            if overlay:
                draw.rectangle([15, 460, 497, 498], fill=(6, 78, 59), outline=(16, 185, 129), width=2)
                draw.text((25, 468), "NORMAL STUDY: Clear Bilateral Lung Fields | Cardiac Silhouette CTR 0.42", fill=(110, 231, 183))
                draw.text((85, 160), "Clear Right Lung", fill=(52, 211, 153))
                draw.text((310, 160), "Clear Left Lung", fill=(52, 211, 153))

            draw.text((20, 15), "CHEST RADIOGRAPHY (CXR PA VIEW) — NORMAL SCREEN", fill=(56, 189, 248))

        # Standard CXR HUD
        draw.text((430, 15), "120 kVp", fill=(148, 163, 184))
        draw.text((430, 30), "3.2 mAs", fill=(148, 163, 184))
        draw.text((20, 30), "ST. JUDE HEALTHCARE PACS | SIEMENS LUMINOS dRF", fill=(148, 163, 184))
        draw.text((475, 240), "R", fill=(56, 189, 248))
        draw.text((30, 240), "L", fill=(56, 189, 248))

        img.save(output_path, "PNG")
        return output_path

    @staticmethod
    def create_blended_highlight(raw_path: str, overlay_path: str, blend_weight: float = 0.5) -> Image.Image:
        """
        Creates an interactive alpha-blended image between the raw naked-eye scan and the AI highlight.
        blend_weight: 0.0 = 100% raw naked-eye scan, 1.0 = 100% AI highlighted overlay.
        """
        raw = Image.open(raw_path).convert("RGB")
        annotated = Image.open(overlay_path).convert("RGB")
        return Image.blend(raw, annotated, min(max(blend_weight, 0.0), 1.0))

    @staticmethod
    def analyze_image_quality(image_path: str) -> dict:
        """Calculates image dimensions, mean intensity, and contrast standard deviation."""
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found at {image_path}")

        with Image.open(image_path) as img:
            gray = img.convert("L")
            stat = ImageStat.Stat(gray)
            mean_intensity = stat.mean[0]
            contrast_dev = stat.stddev[0]
            width, height = gray.size

            is_poor_quality = contrast_dev < 15.0 or mean_intensity < 20.0

            return {
                "width": width,
                "height": height,
                "mean_intensity": round(mean_intensity, 2),
                "contrast_deviation": round(contrast_dev, 2),
                "is_poor_quality": is_poor_quality
            }
