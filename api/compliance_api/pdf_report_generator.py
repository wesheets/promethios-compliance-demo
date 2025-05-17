"""
PDF Report Generator for Compliance Decisions

This module provides functionality to generate detailed PDF reports for compliance decisions,
including trust factor analysis, regulatory alignment, and recommendations.
"""

import os
import io
import base64
from datetime import datetime
from typing import Dict, Any, List, Optional

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.linecharts import HorizontalLineChart

class ComplianceReportGenerator:
    """
    A class that generates PDF reports for compliance decisions.
    """
    
    def __init__(self, logo_path: Optional[str] = None):
        """
        Initialize the report generator.
        
        Args:
            logo_path: Optional path to a logo image for the reports
        """
        self.logo_path = logo_path
        self.styles = getSampleStyleSheet()
        
        # Add custom styles
        self.styles.add(ParagraphStyle(
            name='Title',
            parent=self.styles['Heading1'],
            fontSize=18,
            spaceAfter=12,
            textColor=colors.HexColor('#6610f2')
        ))
        
        self.styles.add(ParagraphStyle(
            name='Heading2',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=8,
            textColor=colors.HexColor('#6610f2')
        ))
        
        self.styles.add(ParagraphStyle(
            name='Heading3',
            parent=self.styles['Heading3'],
            fontSize=12,
            spaceAfter=6,
            textColor=colors.HexColor('#6610f2')
        ))
        
        self.styles.add(ParagraphStyle(
            name='Normal',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=6
        ))
        
        self.styles.add(ParagraphStyle(
            name='Compliant',
            parent=self.styles['Normal'],
            textColor=colors.green
        ))
        
        self.styles.add(ParagraphStyle(
            name='NonCompliant',
            parent=self.styles['Normal'],
            textColor=colors.red
        ))
    
    def generate_report(self, decision_data: Dict[str, Any], trust_factors: Dict[str, Any], 
                        recommendations: List[Dict[str, str]]) -> bytes:
        """
        Generate a PDF report for a compliance decision.
        
        Args:
            decision_data: Dictionary containing decision data and compliance results
            trust_factors: Dictionary containing trust factor scores and details
            recommendations: List of recommendation dictionaries
            
        Returns:
            PDF report as bytes
        """
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, 
                               rightMargin=72, leftMargin=72,
                               topMargin=72, bottomMargin=72)
        
        # Build the report content
        story = []
        
        # Add report header
        self._add_header(story, decision_data)
        
        # Add executive summary
        self._add_executive_summary(story, decision_data)
        
        # Add trust factor analysis
        self._add_trust_factor_analysis(story, trust_factors)
        
        # Add regulatory alignment
        self._add_regulatory_alignment(story, decision_data)
        
        # Add recommendations
        self._add_recommendations(story, recommendations)
        
        # Add footer with timestamp
        self._add_footer(story)
        
        # Build the PDF
        doc.build(story)
        
        # Get the PDF data
        pdf_data = buffer.getvalue()
        buffer.close()
        
        return pdf_data
    
    def _add_header(self, story: List, decision_data: Dict[str, Any]) -> None:
        """Add the report header section."""
        # Add logo if available
        if self.logo_path and os.path.exists(self.logo_path):
            img = Image(self.logo_path, width=100, height=30)
            story.append(img)
            story.append(Spacer(1, 12))
        
        # Add title
        title = Paragraph("Compliance Decision Report", self.styles['Title'])
        story.append(title)
        
        # Add application details
        app_id = decision_data.get('application_id', 'Unknown')
        framework = decision_data.get('framework', 'Unknown')
        date = datetime.now().strftime("%B %d, %Y")
        
        details = [
            ["Report Date:", date],
            ["Application ID:", app_id],
            ["Regulatory Framework:", framework],
            ["Decision ID:", decision_data.get('decision_id', 'Unknown')]
        ]
        
        table = Table(details, colWidths=[150, 300])
        table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
            ('BACKGROUND', (0, 0), (0, -1), colors.lavender)
        ]))
        
        story.append(table)
        story.append(Spacer(1, 20))
    
    def _add_executive_summary(self, story: List, decision_data: Dict[str, Any]) -> None:
        """Add the executive summary section."""
        story.append(Paragraph("Executive Summary", self.styles['Heading2']))
        
        # Determine compliance status
        is_compliant = decision_data.get('is_compliant', False)
        compliance_score = decision_data.get('compliance_score', 0)
        
        if is_compliant:
            status_style = self.styles['Compliant']
            status_text = "COMPLIANT"
        else:
            status_style = self.styles['NonCompliant']
            status_text = "NON-COMPLIANT"
        
        status = Paragraph(f"Compliance Status: {status_text}", status_style)
        story.append(status)
        
        # Add compliance score
        score_text = f"Overall Compliance Score: {compliance_score:.1f}%"
        story.append(Paragraph(score_text, self.styles['Normal']))
        
        # Add summary text
        summary = decision_data.get('summary', 'No summary available.')
        story.append(Paragraph(summary, self.styles['Normal']))
        
        # Add primary reason for decision
        reason = decision_data.get('primary_reason', 'No reason specified.')
        story.append(Paragraph(f"Primary Reason: {reason}", self.styles['Normal']))
        
        story.append(Spacer(1, 12))
    
    def _add_trust_factor_analysis(self, story: List, trust_factors: Dict[str, Any]) -> None:
        """Add the trust factor analysis section."""
        story.append(Paragraph("Trust Factor Analysis", self.styles['Heading2']))
        
        # Create a table for trust factor scores
        factor_data = [["Trust Factor", "Score", "Status"]]
        
        factors = trust_factors.get('factors', {})
        for factor_name, factor_info in factors.items():
            score = factor_info.get('score', 0)
            threshold = factor_info.get('threshold', 80)
            status = "Pass" if score >= threshold else "Fail"
            
            factor_data.append([
                factor_name,
                f"{score:.1f}%",
                status
            ])
        
        if len(factor_data) > 1:
            table = Table(factor_data, colWidths=[200, 100, 100])
            table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
                ('BACKGROUND', (0, 0), (-1, 0), colors.lavender),
                ('TEXTCOLOR', (2, 1), (2, -1), 
                 lambda row, col, text=None: colors.green if text == "Pass" else colors.red)
            ]))
            
            story.append(table)
        else:
            story.append(Paragraph("No trust factor data available.", self.styles['Normal']))
        
        # Add trust factor chart
        if len(factor_data) > 1:
            story.append(Spacer(1, 12))
            story.append(self._create_trust_factor_chart(factors))
        
        story.append(Spacer(1, 12))
        
        # Add detailed analysis for each factor
        story.append(Paragraph("Detailed Analysis", self.styles['Heading3']))
        
        for factor_name, factor_info in factors.items():
            story.append(Paragraph(factor_name, self.styles['Heading3']))
            
            description = factor_info.get('description', 'No description available.')
            story.append(Paragraph(description, self.styles['Normal']))
            
            details = factor_info.get('details', [])
            if details:
                detail_text = "<ul>"
                for detail in details:
                    detail_text += f"<li>{detail}</li>"
                detail_text += "</ul>"
                story.append(Paragraph(detail_text, self.styles['Normal']))
            
            story.append(Spacer(1, 6))
        
        story.append(PageBreak())
    
    def _add_regulatory_alignment(self, story: List, decision_data: Dict[str, Any]) -> None:
        """Add the regulatory alignment section."""
        story.append(Paragraph("Regulatory Alignment", self.styles['Heading2']))
        
        framework = decision_data.get('framework', 'Unknown')
        story.append(Paragraph(f"Framework: {framework}", self.styles['Normal']))
        
        # Add regulatory requirements table
        requirements = decision_data.get('requirements', [])
        if requirements:
            req_data = [["Requirement", "Status", "Details"]]
            
            for req in requirements:
                req_name = req.get('name', 'Unknown')
                req_status = req.get('status', 'Unknown')
                req_details = req.get('details', 'No details available.')
                
                req_data.append([req_name, req_status, req_details])
            
            table = Table(req_data, colWidths=[150, 80, 250])
            table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
                ('BACKGROUND', (0, 0), (-1, 0), colors.lavender),
                ('TEXTCOLOR', (1, 1), (1, -1), 
                 lambda row, col, text=None: colors.green if text == "Compliant" else colors.red)
            ]))
            
            story.append(table)
        else:
            story.append(Paragraph("No regulatory requirements data available.", self.styles['Normal']))
        
        story.append(Spacer(1, 20))
    
    def _add_recommendations(self, story: List, recommendations: List[Dict[str, str]]) -> None:
        """Add the recommendations section."""
        story.append(Paragraph("Recommendations", self.styles['Heading2']))
        
        if recommendations:
            for i, rec in enumerate(recommendations):
                title = rec.get('title', f'Recommendation {i+1}')
                description = rec.get('description', 'No description available.')
                priority = rec.get('priority', 'medium')
                
                # Format priority with appropriate color
                if priority.lower() == 'high':
                    priority_color = colors.red
                elif priority.lower() == 'medium':
                    priority_color = colors.orange
                else:
                    priority_color = colors.green
                
                # Add recommendation title with priority
                title_style = ParagraphStyle(
                    name=f'RecTitle{i}',
                    parent=self.styles['Heading3'],
                    textColor=colors.black
                )
                story.append(Paragraph(f"{title} <font color='{priority_color}'>[{priority.upper()}]</font>", title_style))
                
                # Add recommendation description
                story.append(Paragraph(description, self.styles['Normal']))
                story.append(Spacer(1, 6))
        else:
            story.append(Paragraph("No recommendations available.", self.styles['Normal']))
        
        story.append(Spacer(1, 12))
    
    def _add_footer(self, story: List) -> None:
        """Add the report footer."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        footer_text = f"Generated by Promethios Compliance System on {timestamp}"
        footer = Paragraph(footer_text, self.styles['Normal'])
        story.append(Spacer(1, 20))
        story.append(footer)
    
    def _create_trust_factor_chart(self, factors: Dict[str, Dict[str, Any]]) -> Drawing:
        """Create a bar chart for trust factors."""
        drawing = Drawing(400, 200)
        
        # Extract data for the chart
        factor_names = []
        factor_scores = []
        factor_thresholds = []
        
        for name, info in factors.items():
            factor_names.append(name)
            factor_scores.append(info.get('score', 0))
            factor_thresholds.append(info.get('threshold', 80))
        
        # Create the chart
        chart = VerticalBarChart()
        chart.x = 50
        chart.y = 50
        chart.height = 125
        chart.width = 300
        chart.data = [factor_scores, factor_thresholds]
        chart.bars[0].fillColor = colors.HexColor('#6610f2')
        chart.bars[1].fillColor = colors.lightgrey
        
        # Set axis labels
        chart.valueAxis.valueMin = 0
        chart.valueAxis.valueMax = 100
        chart.valueAxis.valueStep = 20
        chart.categoryAxis.labels.boxAnchor = 'ne'
        chart.categoryAxis.labels.dx = -8
        chart.categoryAxis.labels.dy = -2
        chart.categoryAxis.labels.angle = 30
        chart.categoryAxis.categoryNames = factor_names
        
        drawing.add(chart)
        return drawing

    def encode_pdf_to_base64(self, pdf_data: bytes) -> str:
        """
        Encode PDF data to base64 for API responses.
        
        Args:
            pdf_data: PDF report as bytes
            
        Returns:
            Base64 encoded PDF data
        """
        return base64.b64encode(pdf_data).decode('utf-8')
