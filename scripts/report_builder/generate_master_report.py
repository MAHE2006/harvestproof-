import os, sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

# Ensure scripts dir is in sys.path
sys.path.append(r"C:\Users\Admin\Downloads\harvestproof\hp\scripts")

from report_builder.styles import ASSETS_DIR
from report_builder.part1_front_matter import build_front_matter
from report_builder.part2_chapters_1_to_3 import build_chapters_1_to_3
from report_builder.part3_chapters_4_to_5 import build_chapters_4_to_5
from report_builder.part4_chapters_6_to_8 import build_chapters_6_to_8
from report_builder.part5_appendices_and_refs import build_appendices_and_refs

FINAL_DOCX_PATH = r"C:\Users\Admin\Downloads\harvestproof\HarvestProof_Project_Report.docx"

def main():
    print("=" * 60)
    print("Initializing HarvestProof Project Report Generation...")
    print("=" * 60)
    
    doc = docx.Document()
    
    # Configure Initial Margins & Dimensions
    section = doc.sections[0]
    section.top_margin = Inches(1.0)
    section.bottom_margin = Inches(1.0)
    section.left_margin = Inches(1.2)
    section.right_margin = Inches(1.0)
    section.page_width = Inches(8.5)
    section.page_height = Inches(11.0)
    
    # Unlink first page header/footer for clean cover page
    section.different_first_page_header_footer = True
    
    # Configure Running Header
    header = section.header
    p_hdr = header.paragraphs[0]
    p_hdr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r_hdr = p_hdr.add_run("HARVESTPROOF: MULTIMODAL AI AGROCHEMICAL SAFETY ECOSYSTEM")
    r_hdr.font.name = "Times New Roman"
    r_hdr.font.size = Pt(8.5)
    r_hdr.font.color.rgb = RGBColor(0x77, 0x77, 0x77)
    
    # Configure Running Footer
    footer = section.footer
    p_ftr = footer.paragraphs[0]
    p_ftr.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_ftr = p_ftr.add_run("DEPARTMENT OF AI & ML | K.RAMAKRISHNAN COLLEGE OF TECHNOLOGY (AUTONOMOUS)")
    r_ftr.font.name = "Times New Roman"
    r_ftr.font.size = Pt(8.5)
    r_ftr.font.color.rgb = RGBColor(0x77, 0x77, 0x77)

    print("[1/5] Building Front Matter (Cover, Certificate, Abstract, TOC, Lists)...")
    build_front_matter(doc)
    
    print("[2/5] Building Chapters 1 to 3 (Introduction, Literature Survey, System Analysis)...")
    build_chapters_1_to_3(doc)
    
    print("[3/5] Building Chapters 4 to 5 (Specifications, System Design & Architecture)...")
    build_chapters_4_to_5(doc)
    
    print("[4/5] Building Chapters 6 to 8 (Methodology, Modules, Results, Conclusion)...")
    build_chapters_6_to_8(doc)
    
    print("[5/5] Building Appendices and References (Source Code, UI Screenshots, IEEE References)...")
    build_appendices_and_refs(doc)
    
    print(f"Saving compiled document to: {FINAL_DOCX_PATH} ...")
    doc.save(FINAL_DOCX_PATH)
    
    size_bytes = os.path.getsize(FINAL_DOCX_PATH)
    print(f"SUCCESS! HarvestProof Project Report generated successfully.")
    print(f"File Size: {size_bytes / (1024 * 1024):.2f} MB ({size_bytes} bytes)")
    print(f"Location: {FINAL_DOCX_PATH}")

if __name__ == "__main__":
    main()
