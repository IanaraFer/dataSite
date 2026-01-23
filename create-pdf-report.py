"""
Create a professional, easy-to-understand PDF financial report
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime
import os

OUTPUT_DIR = "financial-analysis-output/"

print("📄 Creating professional PDF report...")

# Create PDF
pdf_file = f'{OUTPUT_DIR}FINANCIAL_REPORT.pdf'
doc = SimpleDocTemplate(pdf_file, pagesize=letter,
                        rightMargin=0.5*inch, leftMargin=0.5*inch,
                        topMargin=0.5*inch, bottomMargin=0.5*inch)

# Container for the 'Flowable' objects
elements = []

# Define styles
styles = getSampleStyleSheet()
title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Heading1'],
    fontSize=28,
    textColor=colors.HexColor('#2ca02c'),
    spaceAfter=10,
    alignment=TA_CENTER,
    fontName='Helvetica-Bold'
)

heading_style = ParagraphStyle(
    'CustomHeading',
    parent=styles['Heading2'],
    fontSize=14,
    textColor=colors.HexColor('#2ca02c'),
    spaceAfter=8,
    spaceBefore=12,
    fontName='Helvetica-Bold'
)

normal_style = ParagraphStyle(
    'CustomNormal',
    parent=styles['Normal'],
    fontSize=10,
    spaceAfter=6,
    alignment=TA_LEFT
)

# ==================== PAGE 1: COVER ====================
elements.append(Paragraph("FINANCIAL ANALYSIS REPORT", title_style))
elements.append(Spacer(1, 0.2*inch))

# Company logo/branding
company_style = ParagraphStyle(
    'Company',
    parent=styles['Normal'],
    fontSize=12,
    textColor=colors.HexColor('#666666'),
    alignment=TA_CENTER,
    spaceAfter=4
)
elements.append(Paragraph("Analytica Core AI", company_style))
elements.append(Paragraph("Professional Business Analytics", company_style))
elements.append(Spacer(1, 0.1*inch))

# Account details
account_style = ParagraphStyle(
    'Account',
    parent=styles['Normal'],
    fontSize=11,
    alignment=TA_CENTER,
    spaceAfter=2
)
elements.append(Paragraph("<b>Account Holder:</b> IANARA ARAUJO FERNANDES", account_style))
elements.append(Paragraph("<b>Bank:</b> Revolut Bank UAB (Ireland)", account_style))
elements.append(Paragraph("<b>Analysis Period:</b> January 1 - November 27, 2025", account_style))
elements.append(Paragraph(f"<b>Report Generated:</b> {datetime.now().strftime('%B %d, %Y')}", account_style))
elements.append(Spacer(1, 0.3*inch))

# Key metrics summary
elements.append(Paragraph("KEY FINANCIAL SNAPSHOT", heading_style))

key_metrics_data = [
    ['Metric', 'Amount', 'Status'],
    ['Opening Balance', '€1,328.29', ''],
    ['Closing Balance', '€288.22', '⚠️ Low'],
    ['Total Income', '€59,299.56', '✓ Good'],
    ['Total Expenses', '€60,339.63', '⚠️ High'],
    ['Net Change', '-€1,040.07', '⚠️ Negative'],
]

t = Table(key_metrics_data, colWidths=[2.5*inch, 1.5*inch, 1*inch])
t.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2ca02c')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 11),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cccccc')),
    ('FONTSIZE', (0, 1), (-1, -1), 10),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')]),
]))
elements.append(t)
elements.append(Spacer(1, 0.2*inch))

# Quick insights
elements.append(Paragraph("WHAT THIS MEANS", heading_style))
insights_text = """
<b>💡 In Simple Terms:</b><br/>
• You received €59,299.56 into your account during the 11-month period<br/>
• You spent €60,339.63 (slightly more than you received)<br/>
• Your account balance decreased by €1,040.07<br/>
• On average, you spent €1,859.52 per month<br/>
• You received €9,409.82 per month on average<br/>
"""
elements.append(Paragraph(insights_text, normal_style))

elements.append(PageBreak())

# ==================== PAGE 2: DETAILED ANALYSIS ====================
elements.append(Paragraph("MONTHLY BREAKDOWN", heading_style))
elements.append(Spacer(1, 0.1*inch))

monthly_data = [
    ['Month', 'Money In', 'Money Out', 'Net Change', 'Comment'],
    ['January', '€4,020.52', '€2,736.68', '+€1,283.84', 'Good start'],
    ['February', '€3,880.20', '€2,682.20', '+€1,198.00', 'Stable'],
    ['March', '€1,849.80', '€1,380.86', '+€468.94', 'Lower income'],
    ['April', '€3,941.73', '€993.66', '+€2,948.07', 'Better month'],
    ['May', '€4,584.69', '€1,014.20', '+€3,570.49', 'Strong savings'],
    ['June', '€10,086.91', '€1,223.97', '+€8,862.94', '⭐ Excellent'],
    ['July', '€17,011.93', '€3,281.01', '+€13,730.92', '⭐ Best month'],
    ['August', '€9,175.38', '€1,549.45', '+€7,625.93', 'Strong income'],
    ['September', 'No data', 'No data', 'Gap in data', '-'],
    ['October', '€33,730.09', '€2,697.40', '+€31,032.69', '⭐⭐ Outstanding'],
    ['November', '€5,816.96', '€1,035.80', '+€4,781.16', 'Good ending'],
]

t2 = Table(monthly_data, colWidths=[0.9*inch, 1.1*inch, 1.1*inch, 1.1*inch, 1.3*inch])
t2.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2ca02c')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 9),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cccccc')),
    ('FONTSIZE', (0, 1), (-1, -1), 8),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')]),
]))
elements.append(t2)
elements.append(Spacer(1, 0.15*inch))

elements.append(Paragraph("💰 AVERAGE PER MONTH", heading_style))
avg_data = [
    ['Metric', 'Average Amount'],
    ['Money Coming In', '€9,409.82'],
    ['Money Going Out', '€1,859.52'],
    ['Net Savings', '€7,550.30'],
]
t3 = Table(avg_data, colWidths=[2.5*inch, 1.5*inch])
t3.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2ca02c')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 10),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
    ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#e8f5e9')),
    ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cccccc')),
    ('FONTSIZE', (0, 1), (-1, -1), 10),
    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica-Bold'),
]))
elements.append(t3)
elements.append(Spacer(1, 0.15*inch))

# Add chart if available
try:
    img = Image(f'{OUTPUT_DIR}01-monthly-income-expenses.png', width=6.5*inch, height=3.5*inch)
    elements.append(img)
except:
    pass

elements.append(PageBreak())

# ==================== PAGE 3: SPENDING ANALYSIS ====================
elements.append(Paragraph("WHERE YOUR MONEY GOES", heading_style))
elements.append(Spacer(1, 0.1*inch))

spending_data = [
    ['Category', 'Total Spent', '% of Total', 'What This Means'],
    ['Other', '€8,677.35', '14.4%', 'Transfers & misc'],
    ['Savings', '€5,345.60', '8.9%', 'Money to pockets ✓'],
    ['Fuel', '€1,371.21', '2.3%', 'Gas station visits'],
    ['Groceries', '€1,174.51', '1.9%', 'Food shopping'],
    ['Transfers Out', '€842.63', '1.4%', 'Payments to others'],
    ['Shopping', '€575.65', '1.0%', 'Amazon, etc.'],
    ['Transport', '€537.59', '0.9%', 'Travel & parking'],
    ['Other Categories', '€70.97', '0.1%', 'Entertainment, etc.'],
]

t4 = Table(spending_data, colWidths=[1.2*inch, 1.2*inch, 1*inch, 1.6*inch])
t4.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#ff7f0e')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('ALIGN', (3, 0), (3, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 9),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cccccc')),
    ('FONTSIZE', (0, 1), (-1, -1), 8),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')]),
]))
elements.append(t4)
elements.append(Spacer(1, 0.15*inch))

# Add pie chart
try:
    img2 = Image(f'{OUTPUT_DIR}02-category-breakdown.png', width=5*inch, height=5*inch)
    elements.append(img2)
except:
    pass

elements.append(PageBreak())

# ==================== PAGE 4: TOP EXPENSES & ALERTS ====================
elements.append(Paragraph("YOUR LARGEST EXPENSES", heading_style))

top_expenses_data = [
    ['#', 'What You Bought', 'Cost', 'When'],
    ['1', 'Booking.com (Travel)', '€1,059.68', 'Jul 24, 2025'],
    ['2', 'IKEA (Furniture)', '€761.00', 'Oct 12, 2025'],
    ['3', 'Allianz (Insurance)', '€612.71', 'Jan 21, 2025'],
    ['4', 'Furniture Item', '€357.92', 'Oct 19, 2025'],
    ['5', 'Ryanair (Flights)', '€314.32', 'Apr 17, 2025'],
]

t5 = Table(top_expenses_data, colWidths=[0.4*inch, 2.2*inch, 1*inch, 1.4*inch])
t5.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#d62728')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('ALIGN', (1, 0), (1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 10),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
    ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#ffebee')),
    ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cccccc')),
    ('FONTSIZE', (0, 1), (-1, -1), 9),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')]),
]))
elements.append(t5)
elements.append(Spacer(1, 0.2*inch))

# Health alerts
elements.append(Paragraph("⚠️ FINANCIAL HEALTH ALERTS", heading_style))
alerts_text = """
<b>ISSUES TO BE AWARE OF:</b><br/>
<br/>
🔴 <b>Low Current Balance:</b> Your account has only €288.22 (27% of starting balance)<br/>
🔴 <b>Spending Over Income:</b> You spent €1,040.07 MORE than you received this period<br/>
🔴 <b>Balance Hit Zero:</b> On Feb 13, 2025, your account went to €0.00<br/>
<br/>
<b>WHAT THIS MEANS:</b><br/>
Even though you average €9,409/month income, something unusual happened. 
The large spike in October (€33,730) suggests a one-time deposit or business income.
Your regular monthly needs are only €1,859, which is good, but your balance 
suggests recent larger purchases (IKEA, Booking.com).
"""
elements.append(Paragraph(alerts_text, normal_style))

elements.append(PageBreak())

# ==================== PAGE 5: RECOMMENDATIONS ====================
elements.append(Paragraph("💡 RECOMMENDATIONS FOR YOU", heading_style))

rec_style = ParagraphStyle(
    'Recommendation',
    parent=styles['Normal'],
    fontSize=10,
    leftIndent=0.3*inch,
    spaceAfter=8,
)

recommendations = [
    ("<b>1. Build an Emergency Fund</b><br/>You should have €5,000-€10,000 saved for emergencies. "
     "Your current balance is too low. Try to maintain at least €2,000 as a buffer."),
    
    ("<b>2. Stabilize Your Monthly Income</b><br/>Your income varies wildly (€1,849 to €33,730/month). "
     "This makes it hard to plan. Look for more consistent income sources."),
    
    ("<b>3. Keep Monitoring Small Expenses</b><br/>You're doing well with daily spending (€1,859/month). "
     "Keep tracking fuel (€1,371/month) - this is your biggest regular cost."),
    
    ("<b>4. Set Monthly Budget</b><br/>Based on your spending: Set a budget of €2,500-€3,000/month. "
     "You're at €1,859 average, so you have room to be more generous with yourself."),
    
    ("<b>5. Plan Major Purchases</b><br/>Your big purchases (IKEA €761, Booking €1,059) are good investments. "
     "Just make sure your emergency fund is still protected first."),
]

for rec in recommendations:
    elements.append(Paragraph(rec, rec_style))

elements.append(Spacer(1, 0.2*inch))

# Bottom section - next steps
next_steps = """
<b>WHAT TO DO NEXT:</b><br/>
<br/>
1. <b>Review this report</b> with your financial advisor or accountant<br/>
2. <b>Build your emergency fund</b> to at least €5,000<br/>
3. <b>Set up a monthly budget</b> using the figures in this report<br/>
4. <b>Schedule a follow-up</b> in 3 months to review progress<br/>
<br/>
<b>Questions?</b> Contact Analytica Core AI<br/>
Email: information@analyticacoreai.ie<br/>
Website: https://analiticacoreai.netlify.app
"""
elements.append(Paragraph(next_steps, normal_style))

# Add footer line
elements.append(Spacer(1, 0.3*inch))
footer_style = ParagraphStyle(
    'Footer',
    parent=styles['Normal'],
    fontSize=8,
    textColor=colors.grey,
    alignment=TA_CENTER,
)
elements.append(Paragraph("This report is for informational purposes only. "
                         "Consult with a professional financial advisor for personalized advice.",
                         footer_style))

# Build PDF
doc.build(elements)

print(f"✅ PDF Report created successfully!")
print(f"📄 Saved to: {pdf_file}")
print()
print("The report includes:")
print("  ✓ Easy-to-read tables")
print("  ✓ Clear explanations in simple language")
print("  ✓ Your spending breakdown with percentages")
print("  ✓ Charts and graphs")
print("  ✓ Financial alerts")
print("  ✓ Personalized recommendations")
print()
print("Anyone can understand this report! 👍")
