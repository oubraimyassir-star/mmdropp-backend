from fpdf import FPDF
import json
from typing import Dict, Any

class TechSheetPDF(FPDF):
    def header(self):
        # Logo placeholder or just title
        self.set_font('Arial', 'B', 20)
        self.set_text_color(99, 102, 241) # brand color
        self.cell(0, 15, 'ConvertAI - Fiche Technique', 0, 1, 'C')
        self.ln(5)
        
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}} - Généré par ConvertAI', 0, 0, 'C')

    def section_title(self, title):
        self.set_font('Arial', 'B', 14)
        self.set_fill_color(243, 244, 246)
        self.set_text_color(31, 41, 55)
        self.cell(0, 10, f'  {title}', 0, 1, 'L', fill=True)
        self.ln(3)

    def add_item(self, label, value):
        self.set_font('Arial', 'B', 10)
        self.set_text_color(75, 85, 99)
        self.write(7, f"{label}: ")
        self.set_font('Arial', '', 10)
        self.set_text_color(31, 41, 55)
        self.write(7, f"{value}\n")

def generate_tech_sheet_pdf(data: Dict[str, Any], output_path: str):
    pdf = TechSheetPDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    
    # Header Info
    header = data.get('header', {})
    pdf.set_font('Arial', 'B', 16)
    pdf.set_text_color(17, 24, 39)
    pdf.cell(0, 10, header.get('title', 'Spécifications Produit'), 0, 1, 'L')
    
    pdf.set_font('Arial', 'I', 10)
    pdf.set_text_color(107, 114, 128)
    pdf.cell(0, 7, f"Référence : {header.get('model_reference', 'N/A')}", 0, 1, 'L')
    pdf.cell(0, 7, f"Mise à jour : {header.get('last_update', 'N/A')}", 0, 1, 'L')
    pdf.ln(10)
    
    # Sections
    for section in data.get('sections', []):
        pdf.section_title(section.get('title', 'Détails'))
        
        items = section.get('items', [])
        if isinstance(items, list):
            for item in items:
                if isinstance(item, dict):
                    pdf.add_item(item.get('label', 'Propriété'), item.get('value', 'Valeur'))
                else:
                    pdf.set_font('Arial', '', 10)
                    pdf.set_text_color(31, 41, 55)
                    pdf.multi_cell(0, 7, f"• {str(item)}")
        pdf.ln(5)
        
    # Certifications & Warranty
    if data.get('certifications'):
        pdf.section_title("Certifications & Normes")
        pdf.set_font('Arial', '', 10)
        pdf.set_text_color(31, 41, 55)
        certs = ", ".join(data.get('certifications', []))
        pdf.multi_cell(0, 7, certs)
        pdf.ln(5)
        
    if data.get('warranty_info'):
        pdf.section_title("Garantie & Support")
        pdf.set_font('Arial', '', 10)
        pdf.set_text_color(31, 41, 55)
        pdf.multi_cell(0, 7, data.get('warranty_info'))
        
    pdf.output(output_path)
    return output_path
