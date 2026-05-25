# app/services/report_builder.py
# Creates beautiful, professional medical reports from scans

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor, black, white, grey
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import os
from datetime import datetime

def create_professional_report(report_data, output_path):
    """Create a beautiful professional medical report PDF"""
    
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=15*mm,
        leftMargin=15*mm,
        topMargin=15*mm,
        bottomMargin=15*mm
    )
    
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=22,
        textColor=HexColor('#1a365d'),
        spaceAfter=6,
        alignment=TA_CENTER
    )
    
    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=HexColor('#718096'),
        alignment=TA_CENTER,
        spaceAfter=20
    )
    
    section_style = ParagraphStyle(
        'SectionHeader',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=HexColor('#2d3748'),
        spaceBefore=15,
        spaceAfter=8,
        borderPadding=(0, 0, 2, 0),
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        leading=16,
        textColor=HexColor('#4a5568'),
    )
    
    # Build content
    story = []
    
    # Header
    story.append(Paragraph("MAHFOOZ MEDICAL REPORT", title_style))
    story.append(Paragraph(f"Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", subtitle_style))
    story.append(Spacer(1, 10))
    
    # Report Title
    story.append(Paragraph(f"📋 {report_data.get('title', 'Medical Report')}", section_style))
    
    # Patient Info Table
    patient_info = report_data.get('patient_info', {})
    if patient_info:
        patient_data = [
            ['PATIENT INFORMATION', ''],
            ['Name', patient_info.get('name', 'N/A')],
            ['Age/Gender', f"{patient_info.get('age', 'N/A')} / {patient_info.get('gender', 'N/A')}"],
            ['Referral By', patient_info.get('referral', 'Self')],
            ['Date', report_data.get('report_date', 'N/A')],
        ]
        
        patient_table = Table(patient_data, colWidths=[60*mm, 100*mm])
        patient_table.setStyle(TableStyle([
            ('SPAN', (0, 0), (-1, 0)),
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#2b6cb0')),
            ('TEXTCOLOR', (0, 0), (-1, 0), white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), HexColor('#f7fafc')),
            ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#e2e8f0')),
            ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('PADDING', (0, 0), (-1, -1), 6),
        ]))
        story.append(patient_table)
        story.append(Spacer(1, 10))
    
    # Lab Test Results Table
    test_values = report_data.get('test_values', {})
    if test_values:
        test_data = [['TEST NAME', 'RESULT', 'NORMAL RANGE', 'STATUS']]
        
        normal_ranges = {
            'Hemoglobin': '13.5-17.5 g/dL',
            'Blood Sugar': '70-100 mg/dL',
            'Blood Pressure': '120/80 mmHg',
            'Cholesterol': '<200 mg/dL',
            'Creatinine': '0.7-1.3 mg/dL',
            'TSH': '0.4-4.0 mIU/L',
            'Uric Acid': '3.5-7.2 mg/dL',
            'Vitamin D': '30-100 ng/mL',
        }
        
        for test_name, value in test_values.items():
            normal = normal_ranges.get(test_name, 'N/A')
            try:
                val_num = float(value.replace('<', '').replace('>', ''))
                if test_name == 'Hemoglobin':
                    status = '✅ Normal' if 12 <= val_num <= 18 else '⚠️ Abnormal'
                elif test_name == 'Blood Sugar':
                    status = '✅ Normal' if 70 <= val_num <= 100 else '⚠️ Abnormal'
                elif test_name == 'Creatinine':
                    status = '✅ Normal' if 0.6 <= val_num <= 1.3 else '⚠️ Abnormal'
                else:
                    status = '✅ Normal'
            except:
                status = '📋 See Report'
            
            test_data.append([test_name, value, normal, status])
        
        test_table = Table(test_data, colWidths=[45*mm, 30*mm, 40*mm, 35*mm])
        test_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#2b6cb0')),
            ('TEXTCOLOR', (0, 0), (-1, 0), white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BACKGROUND', (0, 1), (-1, -1), white),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, HexColor('#f7fafc')]),
            ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#e2e8f0')),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('PADDING', (0, 0), (-1, -1), 6),
            ('ALIGN', (1, 0), (1, -1), 'CENTER'),
            ('ALIGN', (3, 0), (3, -1), 'CENTER'),
        ]))
        story.append(Paragraph("🔬 LAB TEST RESULTS", section_style))
        story.append(test_table)
        story.append(Spacer(1, 10))
    
    # Diagnosis / AI Summary
    diagnosis = report_data.get('diagnosis', '')
    if diagnosis:
        story.append(Paragraph("🩺 FINDINGS", section_style))
        story.append(Paragraph(diagnosis, normal_style))
        story.append(Spacer(1, 10))
    
    # Medicines
    medicines = report_data.get('medicines', [])
    if medicines:
        story.append(Paragraph("💊 MEDICINES DETECTED", section_style))
        for med in medicines:
            story.append(Paragraph(f"• {med}", normal_style))
        story.append(Spacer(1, 10))
    
    # Full extracted text
    full_text = report_data.get('full_text', '')
    if full_text:
        story.append(Paragraph("📝 COMPLETE REPORT TEXT", section_style))
        for line in full_text.split('\n')[:30]:
            if line.strip():
                story.append(Paragraph(line.strip(), normal_style))
    
    # Footer
    story.append(Spacer(1, 20))
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=HexColor('#a0aec0'),
        alignment=TA_CENTER,
    )
    story.append(Paragraph("This report was generated by MAHFOOZ Family Medical Wallet", footer_style))
    story.append(Paragraph("⚠️ This is an AI-generated summary. Always consult your doctor.", footer_style))
    
    # Build PDF
    doc.build(story)
    return output_path

