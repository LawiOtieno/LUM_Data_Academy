"""
Utility classes and functions for courses app
"""
import os
from io import BytesIO
from django.conf import settings
from django.core.files.base import ContentFile
from django.utils import timezone
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import textwrap


class CertificateGenerator:
    """Generate PDF certificates for completed projects"""
    
    # LUM Data Academy theme colors (based on the website design)
    PRIMARY_COLOR = colors.Color(0.04, 0.30, 0.57)  # Primary blue
    SECONDARY_COLOR = colors.Color(0.95, 0.64, 0.13)  # Secondary yellow/orange
    ACCENT_COLOR = colors.Color(0.65, 0.16, 0.94)  # Purple accent
    TEXT_COLOR = colors.Color(0.2, 0.2, 0.2)  # Dark gray
    
    @classmethod
    def generate_project_certificate(cls, project_enrollment):
        """
        Generate a landscape PDF certificate for a completed capstone project
        """
        try:
            # Create a BytesIO buffer to store the PDF
            buffer = BytesIO()
            
            # Set up the document with landscape orientation
            page_width, page_height = landscape(A4)
            doc = SimpleDocTemplate(
                buffer,
                pagesize=landscape(A4),
                rightMargin=0.5 * inch,
                leftMargin=0.5 * inch,
                topMargin=0.5 * inch,
                bottomMargin=0.5 * inch
            )
            
            # Create the certificate content
            story = []
            styles = getSampleStyleSheet()
            
            # Custom styles
            title_style = ParagraphStyle(
                'CertificateTitle',
                parent=styles['Title'],
                fontSize=36,
                textColor=cls.PRIMARY_COLOR,
                alignment=TA_CENTER,
                spaceAfter=30,
                fontName='Helvetica-Bold'
            )
            
            subtitle_style = ParagraphStyle(
                'CertificateSubtitle',
                parent=styles['Normal'],
                fontSize=24,
                textColor=cls.SECONDARY_COLOR,
                alignment=TA_CENTER,
                spaceAfter=20,
                fontName='Helvetica-Bold'
            )
            
            body_style = ParagraphStyle(
                'CertificateBody',
                parent=styles['Normal'],
                fontSize=16,
                textColor=cls.TEXT_COLOR,
                alignment=TA_CENTER,
                spaceAfter=15,
                fontName='Helvetica'
            )
            
            recipient_style = ParagraphStyle(
                'CertificateRecipient',
                parent=styles['Normal'],
                fontSize=28,
                textColor=cls.PRIMARY_COLOR,
                alignment=TA_CENTER,
                spaceAfter=20,
                fontName='Helvetica-Bold'
            )
            
            # Add certificate content
            story.append(Spacer(1, 0.5 * inch))
            
            # Header
            story.append(Paragraph("LUM DATA ACADEMY", title_style))
            story.append(Paragraph("CERTIFICATE OF COMPLETION", subtitle_style))
            
            story.append(Spacer(1, 0.3 * inch))
            
            # Body text
            story.append(Paragraph("This is to certify that", body_style))
            
            # Recipient name
            recipient_name = project_enrollment.enrollment.user.get_full_name() or project_enrollment.enrollment.user.username
            story.append(Paragraph(f"<u>{recipient_name}</u>", recipient_style))
            
            story.append(Paragraph("has successfully completed the capstone project", body_style))
            
            # Project and course details
            course_style = ParagraphStyle(
                'CourseDetail',
                parent=styles['Normal'],
                fontSize=20,
                textColor=cls.ACCENT_COLOR,
                alignment=TA_CENTER,
                spaceAfter=15,
                fontName='Helvetica-Bold'
            )
            
            story.append(Paragraph(f'"{project_enrollment.project.title}"', course_style))
            story.append(Paragraph(f"as part of the {project_enrollment.enrollment.course.title} program", body_style))
            
            # Date and grade
            completion_date = project_enrollment.completed_at.strftime("%B %d, %Y") if project_enrollment.completed_at else timezone.now().strftime("%B %d, %Y")
            story.append(Paragraph(f"Completed on {completion_date}", body_style))
            
            if project_enrollment.grade:
                story.append(Paragraph(f"Grade: {project_enrollment.grade}%", body_style))
            
            story.append(Spacer(1, 0.5 * inch))
            
            # Signature section
            signature_data = [
                ['Course Director', 'Course Instructor'],
                ['David Joel', project_enrollment.enrollment.course.instructor.get_full_name() if project_enrollment.enrollment.course.instructor else 'LUM Data Academy'],
                ['', ''],  # Signature line
                ['________________', '________________'],
                ['Signature and Stamp', 'Signature and Stamp']
            ]
            
            signature_table = Table(signature_data, colWidths=[3.5 * inch, 3.5 * inch])
            signature_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 1), 'Helvetica-Bold'),
                ('FONTNAME', (0, 2), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 12),
                ('TEXTCOLOR', (0, 0), (-1, -1), cls.TEXT_COLOR),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('TOPPADDING', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ]))
            
            story.append(signature_table)
            
            # Footer
            story.append(Spacer(1, 0.2 * inch))
            footer_style = ParagraphStyle(
                'Footer',
                parent=styles['Normal'],
                fontSize=10,
                textColor=cls.TEXT_COLOR,
                alignment=TA_CENTER,
                fontName='Helvetica'
            )
            
            certificate_id = f"CERT-{project_enrollment.id}-{timezone.now().strftime('%Y%m%d')}"
            story.append(Paragraph(f"Certificate ID: {certificate_id}", footer_style))
            story.append(Paragraph("Equipping Africa with Future-Ready Data Skills", footer_style))
            
            # Build the PDF
            doc.build(story)
            
            # Save the certificate file
            buffer.seek(0)
            filename = f"certificate_{project_enrollment.enrollment.user.username}_{project_enrollment.project.id}_{timezone.now().strftime('%Y%m%d')}.pdf"
            
            # Create a Django file object
            certificate_file = ContentFile(buffer.getvalue(), name=filename)
            
            # Return the file path for saving to the model
            return certificate_file
            
        except Exception as e:
            print(f"Error generating certificate: {e}")
            return None