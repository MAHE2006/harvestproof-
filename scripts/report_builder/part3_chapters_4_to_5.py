import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from report_builder.styles import add_p, add_bp, add_h1, add_h2, add_h3, add_bullet, add_table_data, add_fig, page_break

def build_chapters_4_to_5(doc):
    # ====================================================
    # CHAPTER 4: SYSTEM SPECIFICATION
    # ====================================================
    add_h1(doc, "CHAPTER 4\nSYSTEM SPECIFICATIONS")
    
    add_p(doc, "To ensure that HarvestProof operates reliably across diverse deployment environments—ranging from rural field conditions with low-cost smartphones to cloud enterprise hosting—rigorous hardware, software, and regulatory specifications were established.",
          space_after=12)

    add_h2(doc, "4.1 HARDWARE SPECIFICATIONS")
    add_p(doc, "The hardware architecture of HarvestProof is intentionally bifurcated into client-side edge capture hardware and server-side inference/storage infrastructure, as outlined in Table 4.1.", space_after=8)

    hw_headers = ["COMPONENT / SUBSYSTEM", "MINIMUM SPECIFICATION", "RECOMMENDED SPECIFICATION"]
    hw_rows = [
        ["Client Processor", "Quad-core ARM Cortex-A53 1.4 GHz", "Octa-core ARM Cortex-A76+ 2.0 GHz+"],
        ["Client System Memory (RAM)", "2 GB LPDDR3", "4 GB LPDDR4X or higher"],
        ["Client Primary Camera", "5.0 Megapixels with Autofocus", "12.0 Megapixels with LED Flash & Macro"],
        ["Client Network Interface", "3G / 4G Cellular (Band 3/5/40) or Wi-Fi", "4G LTE / 5G / High-Speed Wi-Fi"],
        ["Server CPU Architecture", "x86_64 Dual-Core (e.g., Intel Xeon / AMD)", "x86_64 Quad-Core 2.5 GHz+ (Dedicated)"],
        ["Server System Memory (RAM)", "2 GB System RAM", "4 GB to 8 GB DDR4 ECC RAM"],
        ["Server Non-Volatile Storage", "20 GB SSD / NVMe Storage", "50 GB High-Throughput NVMe SSD"],
        ["Edge Barcode Scanning Sensor", "Rear camera video feed (720p @ 30fps)", "Autofocus camera (1080p @ 60fps)"]
    ]
    add_table_data(doc, hw_headers, hw_rows, [Inches(2.4), Inches(2.3), Inches(2.3)])
    add_p(doc, "Table 4.1: Hardware Specifications of Development and Target Client Platforms", size=10.5, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=12)

    add_h2(doc, "4.2 SOFTWARE SPECIFICATIONS")
    add_p(doc, "The software stack prioritizes performance, open standards, regulatory compliance, and complete platform independence, as tabulated in Table 4.2.", space_after=8)

    sw_headers = ["SOFTWARE COMPONENT", "FRAMEWORK / TECHNOLOGY", "PURPOSE AND ROLE IN HARVESTPROOF"]
    sw_rows = [
        ["Backend Runtime", "Python 3.12 / 3.14 (64-bit)", "Core execution engine and mathematical computations"],
        ["Web Application Server", "FastAPI (v0.110+) & Starlette", "Asynchronous high-throughput REST API gateway"],
        ["ASGI Server", "Uvicorn (v0.29+) with uvloop", "Lightning-fast asynchronous HTTP server"],
        ["Object Relational Mapper", "SQLModel (v0.0.16+) & SQLAlchemy", "Unified relational data schema and type safety"],
        ["Relational Database", "SQLite 3 (Dev) / PostgreSQL 15+", "Storage for users, batches, scans, sprays, and shares"],
        ["Machine Learning Library", "scikit-learn (v1.3+) & NumPy", "Histogram gradient boosting, priors, Bayesian logic"],
        ["Computer Vision Library", "Pillow (PIL Fork v10.0+)", "Foliar image decoding, downsampling, and color arrays"],
        ["Security & Cryptography", "PyJWT (v2.8+) & hashlib/hmac", "PBKDF2-HMAC password hashing, HMAC pack signatures"],
        ["QR Generation Subsystem", "qrcode[pil] (v7.4+)", "Cryptographic QR matrix generation for public passports"],
        ["Frontend UI Framework", "React 18.3+ & Vite 5.4+", "Component-based reactive mobile web client"],
        ["Speech Interfaces", "W3C Web Speech API (STT & TTS)", "Native browser Tamil/English recognition and synthesis"],
        ["Barcode Detection Engine", "BarcodeDetector Web API", "Zero-dependency client-side QR scanning via camera"]
    ]
    add_table_data(doc, sw_headers, sw_rows, [Inches(1.8), Inches(2.2), Inches(3.0)])
    add_p(doc, "Table 4.2: Software Specifications and Computational Frameworks", size=10.5, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=12)

    add_h2(doc, "4.3 REGULATORY DATASETS AND REFERENCE STANDARDS")
    add_p(doc, "Unlike generic agricultural applications that utilize unverified internet scraping, HarvestProof grounds all agronomic recommendations in verified statutory databases:", space_after=8)
    add_bullet(doc, "Contains 26 officially registered commercial fungicide formulations across tea, chilli, rice, and grapes. Each record documents official active ingredients, commercial trade formulations (SC, WP, EC), statutory dose per hectare, and mandatory Pre-Harvest Intervals (ranging from 0 days for biopesticides up to 40 days for systemic triazoles).", "• CIB&RC Registered Uses of Fungicides (Govt. of India): ")
    add_bullet(doc, "Encodes Fungicide Resistance Action Committee codes (FRAC 1, 3, 11, 19, M03) to track modes of action, biochemical targets, and cross-resistance risks.", "• FRAC Mode of Action Classification Scheme: ")
    add_bullet(doc, "Establishes Maximum Residue Limits for export crops (such as Azoxystrobin, Kresoxim-methyl, Hexaconazole), identifying chemicals with ultra-strict limits (≤ 0.05 mg/kg) that trigger export warnings.", "• APEDA & European Commission Pesticide Residue Limits: ")
    add_bullet(doc, "Publicly available, peer-reviewed foliar pathology leaf datasets (CC BY 4.0) covering 6,393 validated field images across healthy and diseased classes for model training and held-out validation.", "• Validated Foliar Pathology Dataset: ", space_after=16)

    page_break(doc)

    # ====================================================
    # CHAPTER 5: SYSTEM DESIGN
    # ====================================================
    add_h1(doc, "CHAPTER 5\nSYSTEM DESIGN")
    
    add_h2(doc, "5.1 SYSTEM ARCHITECTURE")
    add_p(doc, "The HarvestProof architecture is structured into five distinct, decoupled layers designed to maximize execution throughput, guarantee security, and provide an ultra-responsive user experience across low-bandwidth cellular environments. Fig. 5.1 illustrates the complete system architecture.",
          space_after=10)

    add_fig(doc, "fig_5_1_architecture.png", "Fig. 5.1: HarvestProof Comprehensive Layered System Architecture", width=Inches(6.0))

    add_p(doc, "The functional responsibilities of each architectural tier are defined as follows:", space_after=8)
    add_bullet(doc, "Engineered in React 18 and compiled via Vite into a highly compressed 60 kB production bundle. It manages the 4-step wizard journey, provides responsive touch targets, coordinates local image downscaling, and controls native browser SpeechRecognition and SpeechSynthesis.", "1. Client Presentation & Speech Layer: ")
    add_bullet(doc, "Implemented in FastAPI with asynchronous endpoints. It enforces strict HTTPBearer JWT token validation, rate-limiting algorithms to prevent automated brute-force attacks on pack verification and login endpoints, and GZip compression on all network responses exceeding 1 kB.", "2. Gateway & Security Subsystem: ")
    add_bullet(doc, "The computational core. It encapsulates the non-neural leaf feature extractor (extracting 11 morphological metrics in 31 ms), the Bayesian evidence-fusion engine (operating in 12 ms), the Tamil/English NLU parser (operating in 6.5 ms), and the first-order residue dissipation calculator.", "3. Multimodal AI & Mathematical Engine Layer: ")
    add_bullet(doc, "Maintains cryptographic pack verification logic, evaluating HMAC-SHA256 signatures and analyzing 30-day multi-district scan patterns from database records to flag counterfeit pack cloning.", "4. Anti-Counterfeiting & Pack Integrity Layer: ")
    add_bullet(doc, "Powered by SQLModel over SQLite (development) and PostgreSQL (production). Indexes product codes, batch registries, crop labels, efficacy matrices, logged sprays, and shared passports for single-round-trip retrieval.", "5. Persistence & Regulatory Knowledge Layer: ", space_after=12)

    add_h2(doc, "5.2 MULTIMODAL INGESTION PIPELINE")
    add_p(doc, "A critical engineering bottleneck in rural mobile applications is network bandwidth. Standard smartphone cameras capture images between 3 MB and 12 MB (resolutions of 12 to 48 megapixels). Transmitting such large uncompressed images over rural 3G/4G connections incurs 15 to 45 seconds of upload latency, frequently leading to dropped connections. HarvestProof implements an intelligent client-side image downscaling pipeline:",
          space_after=8)
    add_bullet(doc, "When a farmer captures a leaf photo, the browser intercepts the file using the HTML5 Canvas API and createImageBitmap.")
    add_bullet(doc, "The image is downscaled to a maximum dimension of 1280 pixels while preserving aspect ratio, and compressed to JPEG format with 0.9 quality factor.")
    add_bullet(doc, "This client-side transformation reduces payload size by over 92% (from ~5 MB down to ~250 kB) in less than 80 ms on device, reducing upload transmission to under 400 ms on typical mobile networks.")
    add_bullet(doc, "For speech input, audio never leaves the phone as raw WAV/PCM audio; the browser SpeechRecognition API transcribes audio locally or via low-overhead streaming, delivering plain text tokens to the backend NLU parser.", space_after=12)

    add_h2(doc, "5.3 DATABASE DESIGN AND ENTITY-RELATIONSHIP SCHEMA")
    add_p(doc, "The relational database schema is modeled to support high-throughput lookups, multi-tenant farmer isolation, and cryptographic auditing, as described in Table 5.1.", space_after=8)

    db_headers = ["TABLE NAME", "PRIMARY KEY", "INDEXED ATTRIBUTES", "RELATIONAL DESCRIPTION & ROLE"]
    db_rows = [
        ["User", "id (Integer)", "email (Unique)", "Stores farmer profile, district, role (farmer/issuer/admin), salt, and PBKDF2 hash"],
        ["Product", "id (Integer)", "code (Unique)", "Registered agrochemicals with standardized codes, brand names, and FRAC MOA codes"],
        ["Label", "id (Integer)", "product_id, crop", "Official statutory parameters: crop target, dose/ha, PHI waiting days, EU MRL limits"],
        ["Efficacy", "id (Integer)", "product_id, disease", "Efficacy coefficients (0.0 to 1.0) linking products to specific foliar pathogens"],
        ["Batch", "id (Integer)", "code (Unique)", "Batch registry records storing product_id, manufacturing date, expiry date, signed flag"],
        ["Scan", "id (Integer)", "code, ts", "Immutable audit trail of pack scans recording user_id, district, timestamp for clone risk"],
        ["Spray", "id (Integer)", "user_id, field, crop", "Farmer treatment log storing field name, crop, product_id, sprayed date, disease ID"],
        ["Share", "token (String)", "token (Primary)", "HMAC-signed shared passport tokens linking buyers to specific plot and crop records"]
    ]
    add_table_data(doc, db_headers, db_rows, [Inches(1.2), Inches(1.3), Inches(1.8), Inches(2.7)])
    add_p(doc, "Table 5.1: Database Schema, Tables, and Key Relational Attributes", size=10.5, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=12)

    add_h2(doc, "5.4 STATE MACHINE AND WIZARD JOURNEY FLOW")
    add_p(doc, "HarvestProof enforces a logical, stateful 4-step wizard journey that mirrors the real-world operational sequence required for safe, certified crop production:",
          space_after=8)
    add_bullet(doc, "Step 1 (Diagnose): State dx begins as null. The farmer selects a crop (Tea, Chilli, Rice, Grapes) and supplies visual or spoken evidence. The system computes posterior probabilities P(c|E). If the leading class achieves confidence threshold (e.g. 74% for tea, 80% for questions), state dx is populated with the settled disease ID and name. If healthy, further spraying is blocked.")
    add_bullet(doc, "Step 2 (Verify): State pack begins as null. The farmer scans or types the batch code. The system executes the 5 security checks. Only if all checks pass is state pack populated with verified product code, expiry dates, and registered crops.")
    add_bullet(doc, "Step 3 (Plan & Log): The planner pulls state dx (problem) and state pack (pesticide). It filters all products registered for that crop and problem, matches waiting days against planned harvest date, penalizes identical FRAC modes of action, and enables the 'I sprayed this: log it' action only for the verified pack.")
    add_bullet(doc, "Step 4 (Passport): The system queries all sprays logged for that field/crop, computes the longest residual waiting date, and displays the safe harvest status. The farmer clicks 'Create a link for my buyer', which generates a public URL (/p/token) containing an HMAC-SHA256 signature and scannable QR code.", space_after=16)

    page_break(doc)

print('Chapters 4-5 module ready.')
