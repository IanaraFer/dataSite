from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from pathlib import Path

out_path = Path('financial-analysis-output/PUBLIC_SUMMARY.pdf')
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='Heading', parent=styles['Heading1'], fontSize=18, leading=22, spaceAfter=10))
styles.add(ParagraphStyle(name='Subheading', parent=styles['Heading2'], fontSize=13, leading=16, spaceAfter=6))
styles.add(ParagraphStyle(name='Body', parent=styles['BodyText'], fontSize=10.5, leading=14))
styles.add(ParagraphStyle(name='Small', parent=styles['BodyText'], fontSize=9, leading=12))

story = []

story.append(Paragraph('AI Financial Analysis — Public Summary', styles['Heading']))
story.append(Paragraph('Period: 1 Jan 2025 – 27 Nov 2025', styles['Body']))
story.append(Paragraph('All personally identifiable information (names, IBANs, card details) has been removed for public sharing.', styles['Small']))
story.append(Spacer(1, 12))

metrics = [
    ['Opening Balance', '€1,328.29'],
    ['Closing Balance', '€288.22'],
    ['Total Income', '€59,299.56'],
    ['Total Expenses', '€60,339.63'],
    ['Net Change', '€-1,040.07 (decrease)'],
    ['Transactions', '3,293'],
]
mt = Table(metrics, colWidths=[180, 140])
mt.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.whitesmoke),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('ALIGN', (0,0), (-1,-1), 'LEFT'),
    ('INNERGRID', (0,0), (-1,-1), 0.25, colors.lightgrey),
    ('BOX', (0,0), (-1,-1), 0.25, colors.lightgrey),
]))
story.append(Paragraph('Key Figures', styles['Subheading']))
story.append(mt)
story.append(Spacer(1, 12))

monthly = [
    ['2025-01', '€4,020.52', '€2,736.68', '€1,283.84'],
    ['2025-02', '€3,880.20', '€2,682.20', '€1,198.00'],
    ['2025-03', '€1,849.80', '€1,380.86', '€468.94'],
    ['2025-04', '€3,941.73', '€993.66', '€2,948.07'],
    ['2025-05', '€4,584.69', '€1,014.20', '€3,570.49'],
    ['2025-06', '€10,086.91', '€1,223.97', '€8,862.94'],
    ['2025-07', '€17,011.93', '€3,281.01', '€13,730.92'],
    ['2025-08', '€9,175.38', '€1,549.45', '€7,625.93'],
    ['2025-10', '€33,730.09', '€2,697.40', '€31,032.69'],
    ['2025-11', '€5,816.96', '€1,035.80', '€4,781.16'],
]
monthly_table = Table([['Month','Income','Expenses','Net']] + monthly, colWidths=[70,80,80,90])
monthly_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.whitesmoke),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('ALIGN', (1,1), (-1,-1), 'RIGHT'),
    ('INNERGRID', (0,0), (-1,-1), 0.25, colors.lightgrey),
    ('BOX', (0,0), (-1,-1), 0.25, colors.lightgrey),
]))
story.append(Paragraph('Monthly Breakdown', styles['Subheading']))
story.append(monthly_table)
story.append(Spacer(1, 12))

categories = [
    ['Other', '€8,677.35', '14.4%'],
    ['Savings', '€5,345.60', '8.9%'],
    ['Fuel', '€1,371.21', '2.3%'],
    ['Groceries', '€1,174.51', '1.9%'],
    ['Transfers Out', '€842.63', '1.4%'],
    ['Shopping', '€575.65', '1.0%'],
    ['Transport', '€537.59', '0.9%'],
    ['Entertainment', '€40.60', '0.1%'],
    ['Restaurants', '€29.72', '0.0%'],
    ['Crypto', '€0.37', '0.0%'],
]
cat_table = Table([['Category','Amount','Share']] + categories, colWidths=[120,80,60])
cat_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.whitesmoke),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('ALIGN', (1,1), (-1,-1), 'RIGHT'),
    ('INNERGRID', (0,0), (-1,-1), 0.25, colors.lightgrey),
    ('BOX', (0,0), (-1,-1), 0.25, colors.lightgrey),
]))
story.append(Paragraph('Spending by Category', styles['Subheading']))
story.append(cat_table)
story.append(Spacer(1, 12))

top_exp = [
    ['Booking.com', '€1,059.68', '24 Jul 2025'],
    ['IKEA', '€761.00', '12 Oct 2025'],
    ['Allianz', '€612.71', '21 Jan 2025'],
    ['Tst Foxhunter Elepha', '€357.92', '19 Oct 2025'],
    ['Ryanair', '€314.32', '17 Apr 2025'],
]
top_table = Table([['Merchant','Amount','Date']] + top_exp, colWidths=[160,80,100])
top_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.whitesmoke),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('ALIGN', (1,1), (-1,-1), 'RIGHT'),
    ('INNERGRID', (0,0), (-1,-1), 0.25, colors.lightgrey),
    ('BOX', (0,0), (-1,-1), 0.25, colors.lightgrey),
]))
story.append(Paragraph('Top 5 Expenses', styles['Subheading']))
story.append(top_table)
story.append(Spacer(1, 12))

alerts = [
    'Balance decreased by €1,040.07 (78.3%).',
    'Current balance is low (€288.22).',
    'Spending exceeds income by €1,040.07.',
]
story.append(Paragraph('Financial Health Alerts', styles['Subheading']))
for a in alerts:
    story.append(Paragraph('• ' + a, styles['Body']))
story.append(Spacer(1, 12))

recs = [
    'Increase savings allocation: automate 10–15% of incoming transfers to savings.',
    'Monitor small recurring expenses (€2–€20) to reduce leakage.',
    'Build an emergency fund of 3–6 months of expenses (€5,579–€11,157).',
    'Review top categories (Other, Savings, Fuel) for alignment with goals.',
    'Maintain a minimum buffer to avoid low balances.',
]
story.append(Paragraph('Recommendations', styles['Subheading']))
for r in recs:
    story.append(Paragraph('• ' + r, styles['Body']))
story.append(Spacer(1, 14))

story.append(PageBreak())
story.append(Paragraph('Visuals (Sanitized)', styles['Heading']))
img_paths = [
    ('Monthly Income vs Expenses', 'financial-analysis-output/01-monthly-income-expenses.png'),
    ('Category Breakdown', 'financial-analysis-output/02-category-breakdown.png'),
    ('Balance Timeline', 'financial-analysis-output/03-balance-timeline.png'),
    ('Top Expenses', 'financial-analysis-output/04-top-expenses.png'),
]
max_width = 460
for title, path in img_paths:
    p = Path(path)
    if p.exists():
        story.append(Paragraph(title, styles['Subheading']))
        story.append(Image(str(p), width=max_width, height=max_width*0.6, kind='proportional'))
        story.append(Spacer(1, 12))

story.append(Paragraph('Prepared by Analytica Core AI — Sample public summary (PII removed).', styles['Small']))

SimpleDocTemplate(str(out_path), pagesize=A4, leftMargin=36, rightMargin=36, topMargin=36, bottomMargin=36).build(story)
print(f"Wrote {out_path}")
