import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from report_builder.styles import add_p, add_bp, add_h1, add_h2, add_h3, add_bullet, add_table_data, page_break

def build_front_matter(doc):
    # ----------------------------------------------------
    # 1. OUTER COVER PAGE
    # ----------------------------------------------------
    add_p(doc, "HARVESTPROOF – MULTIMODAL AI LEAF PATHOLOGY, BILINGUAL VOICE ASSISTANCE, AGROCHEMICAL INTEGRITY VERIFICATION, AND CRYPTOGRAPHIC HARVEST PASSPORT ECOSYSTEM", 
          size=15, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=24, space_after=28)
    
    add_p(doc, "A PROJECT REPORT", size=13, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=18)
    
    add_p(doc, "Submitted by", size=12, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=24)
    
    # Students Table
    headers = ["CANDIDATE NAME", "REGISTER NUMBER"]
    rows = [
        ["MAKILINI K", "2303811714822013"],
        ["MONIKA S", "2303811714822020"],
        ["RAKSHANA PON", "2303811714822036"],
        ["VISVAJEET R S", "2303811714821059"]
    ]
    add_table_data(doc, headers, rows, [Inches(3.2), Inches(2.8)])
    
    add_p(doc, "in partial fulfillment of the requirements for the award of the course", 
          size=11.5, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=20, space_after=14)
    
    add_p(doc, "AGB1303 – AI PROBLEM SOLVING TECHNIQUES", size=12.5, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=18)
    
    add_p(doc, "DEPARTMENT OF ARTIFICIAL INTELLIGENCE AND MACHINE LEARNING", size=12.5, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=6)
    add_p(doc, "K.RAMAKRISHNAN COLLEGE OF TECHNOLOGY (AUTONOMOUS)", size=13, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=4)
    add_p(doc, "SAMAYAPURAM, TIRUCHIRAPPALLI – 621112", size=11.5, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=18)
    add_p(doc, "DECEMBER 2025", size=12, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=0)
    
    page_break(doc)
    
    # ----------------------------------------------------
    # 2. INNER TITLE PAGE
    # ----------------------------------------------------
    add_p(doc, "HARVESTPROOF – MULTIMODAL AI LEAF PATHOLOGY, BILINGUAL VOICE ASSISTANCE, AGROCHEMICAL INTEGRITY VERIFICATION, AND CRYPTOGRAPHIC HARVEST PASSPORT ECOSYSTEM", 
          size=15, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=24, space_after=28)
    
    add_p(doc, "A PROJECT REPORT", size=13, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=18)
    add_p(doc, "Submitted by", size=12, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=24)
    
    add_table_data(doc, headers, rows, [Inches(3.2), Inches(2.8)])
    
    add_p(doc, "in partial fulfillment of the requirements for the award of the course", 
          size=11.5, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=20, space_after=14)
    add_p(doc, "AGB1303 – AI PROBLEM SOLVING TECHNIQUES", size=12.5, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=18)
    add_p(doc, "DEPARTMENT OF ARTIFICIAL INTELLIGENCE AND MACHINE LEARNING", size=12.5, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=6)
    add_p(doc, "K.RAMAKRISHNAN COLLEGE OF TECHNOLOGY (AUTONOMOUS)", size=13, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=4)
    add_p(doc, "SAMAYAPURAM, TIRUCHIRAPPALLI – 621112", size=11.5, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=18)
    add_p(doc, "DECEMBER 2025", size=12, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=28)
    add_p(doc, "i", size=11, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
    
    page_break(doc)
    
    # ----------------------------------------------------
    # 3. BONAFIDE CERTIFICATE
    # ----------------------------------------------------
    add_p(doc, "K.RAMAKRISHNAN COLLEGE OF TECHNOLOGY", size=13.5, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
    add_p(doc, "(AUTONOMOUS)", size=12, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
    add_p(doc, "SAMAYAPURAM – 621 112", size=11.5, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=16)
    
    add_p(doc, "BONAFIDE CERTIFICATE", size=13.5, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=16)
    
    add_p(doc, "The work embodied in the present project report entitled \"HARVESTPROOF – MULTIMODAL AI LEAF PATHOLOGY, BILINGUAL VOICE ASSISTANCE, AGROCHEMICAL INTEGRITY VERIFICATION, AND CRYPTOGRAPHIC HARVEST PASSPORT ECOSYSTEM\" has been carried out by the students Makilini K (2303811714822013), Monika S (2303811714822020), Rakshana Pon (2303811714822036), and Visvajeet R S (2303811714821059). The work reported herein is original and we declare that the project is their own work, except where specifically acknowledged, and has not been copied from other sources or been previously submitted for assessment.",
          size=12, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=16)
    
    add_p(doc, "Date of Viva Voce: .......................................", size=11.5, bold=True, space_after=28)
    
    sig_tbl = doc.add_table(rows=2, cols=2)
    sig_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    sig_cells_0 = sig_tbl.rows[0].cells
    sig_cells_1 = sig_tbl.rows[1].cells
    
    sig_cells_0[0].text = "Mrs. E. SRI SANTHOSHINI M.E., (Ph.D)\nSUPERVISOR\nAssistant Professor\nDepartment of AI & ML\nK.Ramakrishnan College of Technology\nSamayapuram – 621 112"
    sig_cells_0[1].text = "Dr. T. AVUDAIAPPAN M.E., Ph.D.\nHEAD OF THE DEPARTMENT\nProfessor & Head\nDepartment of AI & ML\nK.Ramakrishnan College of Technology\nSamayapuram – 621 112"
    
    sig_cells_1[0].text = "\n\nINTERNAL EXAMINER"
    sig_cells_1[1].text = "\n\nEXTERNAL EXAMINER"
    
    for row in sig_tbl.rows:
        for c in row.cells:
            for p in c.paragraphs:
                p.paragraph_format.line_spacing = 1.15
                for r in p.runs:
                    r.font.name = 'Times New Roman'
                    r.font.size = Pt(10.5)
    
    add_p(doc, "\nii", size=11, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
    page_break(doc)
    
    # ----------------------------------------------------
    # 4. ACKNOWLEDGEMENT
    # ----------------------------------------------------
    add_p(doc, "ACKNOWLEDGEMENT", size=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=16)
    
    add_p(doc, "We express our sincere gratitude to our respected Principal, Dr. N. Vasudevan, for providing the state-of-the-art computational infrastructure, encouraging academic atmosphere, and valuable suggestions during the progression of our project work.",
          size=12, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=10)
    
    add_p(doc, "We extend our heartfelt thanks to our Head of the Department, Dr. T. Avudaiappan, M.E., Ph.D., Professor, Department of Artificial Intelligence and Machine Learning, for his continuous encouragement, constructive critiques, and technical leadership throughout the design and realization of this work.",
          size=12, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=10)
    
    add_p(doc, "We wish to record our deepest sense of gratitude and profound thanks to our Project Supervisor and Guide, Mrs. E. Sri Santhoshini, M.E., (Ph.D), Assistant Professor, Department of Artificial Intelligence and Machine Learning, for her inspiring mentorship, unwavering guidance, meticulous reviews, and constant motivation at every phase of development, which helped bring this comprehensive project report to fruition.",
          size=12, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=10)
    
    add_p(doc, "We are also deeply thankful to all the faculty and non-teaching staff members of the Department of Artificial Intelligence and Machine Learning, K. Ramakrishnan College of Technology (Autonomous), for their generous technical assistance and continuous support.",
          size=12, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=10)
    
    add_p(doc, "Finally, we place on record our affectionate gratitude to our parents, family members, and friends whose enduring encouragement, sacrifices, and moral support served as our greatest pillars of strength.",
          size=12, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=20)
    
    add_p(doc, "SIGNATURE OF THE CANDIDATES:", size=11.5, bold=True, space_after=12)
    add_p(doc, "1. MAKILINI K                     ............................................", size=11, space_after=4)
    add_p(doc, "2. MONIKA S                       ............................................", size=11, space_after=4)
    add_p(doc, "3. RAKSHANA PON             ............................................", size=11, space_after=4)
    add_p(doc, "4. VISVAJEET R S               ............................................", size=11, space_after=18)
    
    add_p(doc, "iii", size=11, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
    page_break(doc)
    
    # ----------------------------------------------------
    # 5. ABSTRACT
    # ----------------------------------------------------
    add_p(doc, "ABSTRACT", size=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=16)
    
    add_p(doc, "Agrochemical misuse, spurious pesticide formulations, and non-compliance with Pre-Harvest Intervals (PHI) constitute severe threats to global food security, public health, and international agricultural export trade. In developing economies such as India, smallholder farmers face a complex dilemma: lack of immediate access to plant pathologists, reliance on untrained agrochemical retailers who frequently sell mislabeled or cloned chemical batches, and severe literacy and language barriers that render complex safety labels inaccessible. This results in heavy pesticide residues that exceed Maximum Residue Limits (MRL), leading to frequent export rejections and ecosystem degradation.",
          size=12, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=10)
    
    add_p(doc, "To resolve these systemic challenges, this project presents HARVESTPROOF, an end-to-end intelligent agricultural decision-support and cryptographic verification ecosystem. HarvestProof uniquely unifies five foundational capabilities into a lightweight, cohesive web application that requires zero proprietary AI subscription fees and functions seamlessly on low-cost mobile hardware:",
          size=12, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=8)
    
    add_bullet(doc, "A calibrated non-neural computer vision classifier that measures 11 morphological, geometric, and color features (lesion burden, spindle/round aspect ratios, HSV color distributions) from leaf images. The visual likelihoods are dynamically synthesized with farmer answers through Bayesian evidence fusion, utilizing Shannon entropy reduction to ask only the most informative follow-up questions.", "1. Multimodal Evidence-Fusion Diagnosis: ")
    add_bullet(doc, "A voice-first natural language understanding (NLU) interface operating natively in Tamil (தமிழ்) and English via the browser Web Speech API. The system parses spoken vernacular descriptions, extracts crop entities, symptom keywords, and linguistic negations (e.g., 'no rain', 'மழை இல்லை'), and vocalizes diagnosed remedies in natural Tamil speech.", "2. Bilingual Conversational Voice Assistant: ")
    add_bullet(doc, "A 5-tier batch verification engine that checks code syntax (BATCH-SERIAL-SIG), verifies central batch registries, evaluates HMAC-SHA256 manufacturer digital signatures, checks product expiration, and flags counterfeit cloned codes using 30-day multi-district scan pattern analytics.", "3. Anti-Counterfeiting Pack Integrity Engine: ")
    add_bullet(doc, "A regulatory spray queue based on official Central Insecticide Board & Registration Committee (CIB&RC) schedules that matches chemical efficacy to the identified pathogen, enforces mandatory waiting days, and enforces Fungicide Resistance Action Committee (FRAC) mode-of-action rotation to prevent pathogen resistance.", "4. CIB&RC Label-Compliant Rotation Planner: ")
    add_bullet(doc, "A publicly verifiable, HMAC-signed digital credential displaying earliest safe harvest dates, logged spray histories, and strict EU residue threshold warnings, accessible to buyers and food safety inspectors via a tamper-proof QR code.", "5. Cryptographic Digital Harvest Passport: ")
    
    add_p(doc, "Rigorous automated testing over 61 backend test suites and 14 frontend integration tests verifies system reliability. Optimization benchmarks show question-choice latency reduced from 137 ms to 12 ms, database query count slashed by 94%, and voice request latency held under 7 ms. HarvestProof bridges the digital and linguistic divide, providing smallholders with an empowering, verifiable pathway toward safe, sustainable, and export-compliant agriculture.",
          size=12, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=8, space_after=16)
    
    add_p(doc, "iv", size=11, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
    page_break(doc)
    
    # ----------------------------------------------------
    # 6. TABLE OF CONTENTS
    # ----------------------------------------------------
    add_p(doc, "TABLE OF CONTENTS", size=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=14)
    
    toc_data = [
        ["ABSTRACT", "iv"],
        ["LIST OF FIGURES", "vii"],
        ["LIST OF TABLES", "viii"],
        ["LIST OF ABBREVIATIONS", "ix"],
        ["1  INTRODUCTION", "1"],
        ["    1.1  OVERVIEW", "1"],
        ["    1.2  AGROCHEMICAL OVERUSE AND THE RESIDUE CRISIS", "2"],
        ["    1.3  COUNTERFEIT FORMULATIONS AND TRACEABILITY DEFICIT", "3"],
        ["    1.4  LINGUISTIC AND TECHNOLOGICAL EXCLUSION", "4"],
        ["    1.5  OBJECTIVES OF THE PROJECT", "5"],
        ["    1.6  SCOPE AND METHODOLOGICAL CONTRIBUTIONS", "6"],
        ["    1.7  ORGANIZATION OF THE REPORT", "7"],
        ["2  LITERATURE SURVEY", "8"],
        ["    2.1  DEEP LEARNING VS MORPHOLOGICAL FEATURE CLASSIFIERS", "8"],
        ["    2.2  CRYPTOGRAPHIC VERIFICATION AND ANTI-COUNTERFEITING", "10"],
        ["    2.3  MATHEMATICAL MODELING OF RESIDUE DISSIPATION & PHI", "12"],
        ["    2.4  VERNACULAR VOICE INTERFACES AND INDIC NLP IN FARMING", "14"],
        ["    2.5  DIGITAL PRODUCT PASSPORTS AND FOOD TRACEABILITY", "16"],
        ["3  SYSTEM ANALYSIS", "18"],
        ["    3.1  EXISTING SYSTEM", "18"],
        ["        3.1.1  Demerits of Existing System", "19"],
        ["    3.2  PROPOSED SYSTEM", "20"],
        ["        3.2.1  Merits of Proposed System", "21"],
        ["    3.3  FEASIBILITY STUDY", "22"],
        ["        3.3.1  Technical Feasibility", "22"],
        ["        3.3.2  Economic Feasibility", "23"],
        ["        3.3.3  Operational Feasibility", "23"],
        ["4  SYSTEM SPECIFICATION", "25"],
        ["    4.1  HARDWARE SPECIFICATIONS", "25"],
        ["    4.2  SOFTWARE SPECIFICATIONS", "26"],
        ["    4.3  REGULATORY DATASETS AND REFERENCE STANDARDS", "27"],
        ["5  SYSTEM DESIGN", "29"],
        ["    5.1  SYSTEM ARCHITECTURE", "29"],
        ["    5.2  MULTIMODAL INGESTION PIPELINE", "31"],
        ["    5.3  DATABASE DESIGN AND ENTITY-RELATIONSHIP SCHEMA", "32"],
        ["    5.4  STATE MACHINE AND WIZARD JOURNEY FLOW", "34"],
        ["6  MODULE DESCRIPTION", "36"],
        ["    6.1  METHODOLOGY AND MATHEMATICAL FORMULATIONS", "36"],
        ["        6.1.1  Morphological Feature Extraction Formulation", "36"],
        ["        6.1.2  Calibrated Histogram Gradient Boosting Classifier", "38"],
        ["        6.1.3  Bayesian Evidence Fusion and Shannon Entropy Questioning", "40"],
        ["        6.1.4  Bilingual Tamil/English Speech Recognition and NLU Grammar", "42"],
        ["        6.1.5  First-Order Kinetic Residue Dissipation & PHI Planning", "44"],
        ["        6.1.6  HMAC-SHA256 Cryptographic Verification & Anti-Clone Geo-Scoring", "46"],
        ["    6.2  MODULES", "47"],
        ["        6.2.1  Module 1: Leaf Vision and Morphological Pathology Module", "47"],
        ["        6.2.2  Module 2: Bilingual Voice Assistant and Tamil Speech Engine", "48"],
        ["        6.2.3  Module 3: Agrochemical Pack Integrity Verification Module", "49"],
        ["        6.2.4  Module 4: CIB&RC Label-Compliant Rotation Planner Module", "50"],
        ["        6.2.5  Module 5: Cryptographic Digital Harvest Passport Module", "51"],
        ["7  RESULT AND DISCUSSION", "53"],
        ["    7.1  VISUAL DIAGNOSTIC MODEL PERFORMANCE & CALIBRATION", "53"],
        ["    7.2  EVIDENCE-FUSION OPTIMIZATION AND SPEEDUP BENCHMARKS", "56"],
        ["    7.3  BILINGUAL VOICE ASSISTANT AND NLU ACCURACY", "57"],
        ["    7.4  PACK VERIFICATION AND ANTI-COUNTERFEITING VALIDATION", "59"],
        ["    7.5  SPRAY ROTATION AND RESIDUE SAFETY COMPLIANCE", "60"],
        ["    7.6  END-TO-END SYSTEM BENCHMARKS & RESOURCE PROFILING", "61"],
        ["8  CONCLUSION AND FUTURE ENHANCEMENT", "63"],
        ["    8.1  CONCLUSION", "63"],
        ["    8.2  FUTURE ENHANCEMENT", "64"],
        ["APPENDIX A: SOURCE CODE", "66"],
        ["APPENDIX B: SCREENSHOTS", "72"],
        ["REFERENCES", "76"]
    ]
    add_table_data(doc, ["TOPIC", "PAGE NO."], toc_data, [Inches(5.2), Inches(1.0)])
    
    add_p(doc, "v - vi", size=11, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
    page_break(doc)
    
    # ----------------------------------------------------
    # 7. LIST OF FIGURES
    # ----------------------------------------------------
    add_p(doc, "LIST OF FIGURES", size=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=14)
    
    figs_data = [
        ["5.1", "HarvestProof Comprehensive Layered System Architecture", "30"],
        ["6.1", "First-Order Kinetic Residue Dissipation Dynamics (Azoxystrobin)", "45"],
        ["6.2", "Multi-Tiered Anti-Counterfeiting Pack Verification Pipeline", "47"],
        ["6.3", "Bilingual Tamil/English Voice Interaction and NLU Pipeline", "49"],
        ["7.1", "Leaf Visual Classifier Diagnostic Performance Comparison", "55"],
        ["7.2", "Computational Speedup and Latency Benchmarks", "57"],
        ["B.1", "HarvestProof Leaf Vision & Voice Diagnosis Interface", "72"],
        ["B.2", "Anti-Counterfeiting Pack Verification and Multi-Check Output", "73"],
        ["B.3", "Mode-of-Action Spray Recommendation and Safety Queue", "74"],
        ["B.4", "Digital Harvest Passport with Residue Countdown and QR Link", "75"]
    ]
    add_table_data(doc, ["FIGURE NO.", "TITLE", "PAGE NO."], figs_data, [Inches(1.2), Inches(4.2), Inches(1.0)])
    
    add_p(doc, "vii", size=11, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
    page_break(doc)
    
    # ----------------------------------------------------
    # 8. LIST OF TABLES
    # ----------------------------------------------------
    add_p(doc, "LIST OF TABLES", size=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=14)
    
    tables_data = [
        ["4.1", "Hardware Specifications of Development and Target Client Platforms", "25"],
        ["4.2", "Software Specifications and Computational Frameworks", "26"],
        ["5.1", "Database Schema, Tables, and Key Relational Attributes", "33"],
        ["6.1", "Morphological, Colorimetric, and Geometric Features Extracted from Leaves", "37"],
        ["6.2", "Official CIB&RC Products, Doses, PHI Waiting Days, and FRAC Codes", "44"],
        ["7.1", "Diagnostic Classifier Validation and Test Evaluation Metrics", "54"],
        ["7.2", "Confusion Matrix for Tea Foliar Pathology Visual Classifier (6 Classes)", "54"],
        ["7.3", "Confusion Matrix for Chilli Foliar Pathology Visual Classifier (5 Classes)", "55"],
        ["7.4", "Bilingual Voice Assistant Intent & Entity Recognition Accuracy", "58"],
        ["7.5", "Pack Verification and Clone Risk Detection Evaluation Matrix", "59"],
        ["7.6", "System Latency, Memory Footprint, and Web Asset Profiling", "62"]
    ]
    add_table_data(doc, ["TABLE NO.", "TITLE", "PAGE NO."], tables_data, [Inches(1.2), Inches(4.2), Inches(1.0)])
    
    add_p(doc, "viii", size=11, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
    page_break(doc)
    
    # ----------------------------------------------------
    # 9. LIST OF ABBREVIATIONS
    # ----------------------------------------------------
    add_p(doc, "LIST OF ABBREVIATIONS", size=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=14)
    
    abbrevs = [
        ["AI", "Artificial Intelligence"],
        ["APEDA", "Agricultural and Processed Food Products Export Development Authority"],
        ["API", "Application Programming Interface"],
        ["CIB&RC", "Central Insecticide Board & Registration Committee"],
        ["CNN", "Convolutional Neural Network"],
        ["CSS", "Cascading Style Sheets"],
        ["CSV", "Comma-Separated Values"],
        ["ECE", "Expected Calibration Error"],
        ["EU", "European Union"],
        ["FRAC", "Fungicide Resistance Action Committee"],
        ["GATT", "Generic Attribute Profile"],
        ["GZip", "GNU Zip Compression Format"],
        ["HMAC", "Hash-based Message Authentication Code"],
        ["HSV", "Hue, Saturation, Value Color Space"],
        ["HTML", "HyperText Markup Language"],
        ["HTTP", "Hypertext Transfer Protocol"],
        ["IPM", "Integrated Pest Management"],
        ["ISO", "International Organization for Standardization"],
        ["JSON", "JavaScript Object Notation"],
        ["JWT", "JSON Web Token"],
        ["LAB", "CIELAB Lightness, A, B Color Space"],
        ["ML", "Machine Learning"],
        ["MOA", "Mode of Action"],
        ["MRL", "Maximum Residue Limit"],
        ["NLU", "Natural Language Understanding"],
        ["PHI", "Pre-Harvest Interval"],
        ["PNG", "Portable Network Graphics"],
        ["QR", "Quick Response Code"],
        ["REST", "Representational State Transfer"],
        ["RFC", "Request for Comments"],
        ["RGB", "Red, Green, Blue Color Space"],
        ["SC", "Suspension Concentrate"],
        ["SHA", "Secure Hash Algorithm"],
        ["SVM", "Support Vector Machine"],
        ["TTS", "Text-To-Speech"],
        ["UI", "User Interface"],
        ["URL", "Uniform Resource Locator"],
        ["UTC", "Coordinated Universal Time"],
        ["Vite", "Next Generation Frontend Tooling"],
        ["WP", "Wettable Powder"]
    ]
    add_table_data(doc, ["ABBREVIATION", "EXPANSION / MEANING"], abbrevs, [Inches(1.8), Inches(4.4)])
    
    add_p(doc, "ix", size=11, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
    page_break(doc)

print('Front matter module ready.')
