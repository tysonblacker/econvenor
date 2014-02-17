import socket

from io import BytesIO
from string import replace

from django.http import HttpResponse

from reportlab.lib.colors import black, CMYKColor, white
from reportlab.lib.enums import TA_JUSTIFY, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase.pdfmetrics import registerFont, registerFontFamily
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, \
	Paragraph, Spacer, Table, TableStyle 

import reportlab.rl_config

from core.models import Account, Meeting, Task
from core.utils import get_formatted_meeting_duration, \
	calculate_meeting_end_time, find_preceding_meeting_date


# Define colors
heading_color = CMYKColor(0.3,0,0.15,0.6)	
body_color = CMYKColor(0,0,0,0.85)
table_color = CMYKColor(0.3,0,0.15,0.6)
row_color = CMYKColor(0.1,0,0.05,0.2)

# Define line width
line_width = 0.75

# Set path to fonts
if socket.gethostname() == 'web439.webfaction.com':
	FONT_PATH = '/home/econvenor/webapps/static_econvener/fonts/'
else:
	FONT_PATH = 'core/static/fonts/'

# Register fonts

body_font = 'OpenSans'
heading_font = 'OpenSans'
registerFont(TTFont(body_font, FONT_PATH + body_font + "-Regular.ttf"))
registerFont(TTFont(body_font + 'Bd', FONT_PATH + body_font + "-Bold.ttf"))
registerFont(TTFont(body_font + 'It', FONT_PATH + body_font + "-Italic.ttf"))
registerFont(TTFont(body_font + 'BI', FONT_PATH + body_font + "-BoldItalic.ttf"))
registerFont(TTFont(heading_font, FONT_PATH + heading_font + "-Regular.ttf"))
registerFontFamily(body_font, normal=body_font, bold=body_font + 'Bd',
	italic=body_font + 'It', boldItalic=body_font + 'BI')
reportlab.rl_config.warnOnMissingFontGlyphs = 0

# Create text style sheet
styles = getSampleStyleSheet()

# Define 'normal' text style
normalStyle = styles['Normal']
normalStyle.fontName = body_font
normalStyle.textColor = body_color
normalStyle.alignment = TA_JUSTIFY
normalStyle.fontSize=10
normalStyle.leading=14

# Define 'item' text style
styles.add(ParagraphStyle(name='Item',
	parent=styles['Normal'],
	fontName = body_font,
	spaceBefore=2,
	spaceAfter=2,
	textColor = white))
itemStyle = styles['Item']

# Define 'rightitem' text style
styles.add(ParagraphStyle(name='RightItem',
	parent=styles['Item'],
	alignment = TA_RIGHT))
rightItemStyle = styles['RightItem']

# Define 'darkitem' text style
styles.add(ParagraphStyle(name='DarkItem',
	parent=styles['Item'],
	textColor = heading_color))
darkItemStyle = styles['DarkItem']

# Define 'heading1' text style
heading1Style = styles['Heading1']
heading1Style.fontName = heading_font
heading1Style.textColor = heading_color
heading1Style.fontSize=24
heading1Style.leading=29
heading1Style.spaceAfter=6

# Define 'heading2' text style
heading2Style = styles['Heading2']
heading2Style.fontName = heading_font
heading2Style.textColor = heading_color
heading2Style.fontSize=14
heading2Style.leading=18
heading2Style.spaceBefore=12
heading2Style.spaceAfter=6
                                  
# Define 'heading3' text style
heading3Style = styles['Heading3']
heading3Style.fontName = heading_font
heading3Style.textColor = heading_color
heading3Style.fontSize=11
heading3Style.leading=13
heading3Style.spaceBefore=3
heading3Style.spaceAfter=6

# Define table styles
MEETING_LEFT_COLUMN_STYLE = TableStyle([
	('GRID', (0,0), (-1,-1), line_width, table_color),
	('VALIGN',(0,0),(-1,-1),'TOP'),
	('ROWBACKGROUNDS', (0,0), (-1,-1), [white, row_color]),
	])

MEETING_RIGHT_COLUMN_STYLE = TableStyle([
	('GRID', (0,0), (-1,-1), line_width, table_color),
	('VALIGN',(0,0),(-1,-1),'TOP'),
	])
	
MEETING_TABLE_STYLE = TableStyle([
	('VALIGN',(0,0),(-1,-1),'TOP'),
	('LEFTPADDING', (0,0), (-1,-1), 0),
	('RIGHTPADDING', (0,0), (-1,-1), 0),
	('TOPPADDING', (0,0), (-1,-1), 0),
	('BOTTOMPADDING', (0,0), (-1,-1), 0),
	('ROWBACKGROUNDS', (0,1), (-1,-1), [white, row_color]),
	])

TASK_TABLE_STYLE = TableStyle([
	('GRID', (0,0), (2,-1), line_width, table_color),
	('VALIGN',(0,0),(-1,-1),'TOP'),
	('BACKGROUND', (0,0), (-1,0), table_color),
	('ROWBACKGROUNDS', (0,1), (-1,-1), [white, row_color]),
	])

ITEM_TABLE_STYLE = TableStyle([
	('GRID', (0,0), (1,-1), line_width, table_color),
	('VALIGN',(0,0),(-1,-1),'TOP'),
	('BACKGROUND', (0,0), (-1,0), table_color),
	('LEFTPADDING', (0,0), (-1,0), 0),
	('TOPPADDING', (0,0), (-1,0), 0),
	('BOTTOMPADDING', (0,0), (-1,0), 0),
	])

ITEM_INNER_TABLE_STYLE = TableStyle([
	('GRID', (0,0), (1,-1), line_width, table_color),
	('VALIGN',(0,0),(-1,-1),'TOP'),
	('BACKGROUND', (0,0), (-1,0), table_color),
	('LEFTPADDING', (0,0), (-1,-1), 0),
	('TOPPADDING', (0,0), (-1,0), 0),
	('TOPPADDING', (0,1), (-1,-1), 6),
	('BOTTOMPADDING', (0,0), (-1,-1), 0),
	])


def insert_page_breaks(string):
	formatted_string = string.replace('\n', '<br/>')
	return formatted_string


def footer(canvas, doc):
	canvas.saveState()
	canvas.setLineWidth(line_width)
	canvas.setFillColor(body_color)
	canvas.setStrokeColor(table_color)
	canvas.setFont(body_font, normalStyle.fontSize)
	canvas.line(25*mm,13*mm,185*mm,13*mm)
	right_text = "Page %s" % (doc.page)
	canvas.drawRightString(185*mm, 9*mm, right_text)
	left_text = doc.title
	canvas.drawString(25*mm, 9*mm, left_text)
	canvas.restoreState()


def create_short_item_table(section_heading, item_list, Document, t):
	Document.append(Paragraph(section_heading, heading2Style))
	for item in item_list:
		heading_t = Table([((
			Paragraph(item.heading, itemStyle)),
			Paragraph(str(item.time_limit) + ' minutes', rightItemStyle
			))],
			colWidths=[120*mm,40*mm])
		if item.background:
			background = insert_page_breaks(item.background)
			t = Table([
				(heading_t,),
				(Paragraph(background, normalStyle),)
				],
				colWidths=[160*mm])
		else:
			t = Table([
				(heading_t,)
				],
				colWidths=[160*mm])
		t.setStyle(ITEM_TABLE_STYLE)
		Document.append(t)
		Document.append(Spacer(0,5*mm))


def create_long_item_table(section_heading, item_list, Document, t):
	Document.append(Paragraph(section_heading, heading2Style))
	for item in item_list:
		if item.background:
			background = insert_page_breaks(item.background)
		heading_t = Table([((
			Paragraph(item.heading, itemStyle),
			Paragraph(str(item.time_limit) + ' minutes', rightItemStyle)
			))],
			colWidths=[120*mm,40*mm])
		heading_t.setStyle(TableStyle([(
			'ALIGN',(-1,0),(-1,0),'RIGHT'
			)]))
		if item.explainer and item.background:
			inner_t = Table([
				(Paragraph('<i>To be introduced by ' + str(item.explainer) +
					'</i>', normalStyle),),
				(Paragraph(background, normalStyle),)
				],
				colWidths=[160*mm])
			inner_t.setStyle(TableStyle([
				('TOPPADDING', (0,0), (-1,-1), 0)
				]))
			t = Table([
				(heading_t,),
				(inner_t,)
				],
				colWidths=[160*mm])
			t.setStyle(ITEM_INNER_TABLE_STYLE)
		else:
			if item.explainer and (item.background == ''):
				t = Table([
					(heading_t,),
					(Paragraph('<i>To be introduced by ' +
						str(item.explainer)	+ '</i>', normalStyle),)
					],
					colWidths=[160*mm])				
			elif (item.explainer == None) and item.background:
				t = Table([
					(heading_t,),
					(Paragraph(background, normalStyle),)
					],
					colWidths=[160*mm])
			elif (item.explainer == None) and (item.background == ''):
				t = Table([
					(heading_t,)
					],
					colWidths=[160*mm])		
			t.setStyle(ITEM_TABLE_STYLE)
		Document.append(t)
		Document.append(Spacer(0,5*mm))


def create_task_table(section_heading, task_list, Document, t):
	Document.append(Paragraph(section_heading, heading3Style))
	completed_tasks = [(
		Paragraph(task.description, normalStyle),
		Paragraph(str(task.participant), normalStyle),
		Paragraph(task.deadline.strftime("%d %b %Y"), normalStyle)
		)
		for task in task_list]
	headings = (
		Paragraph('Description', itemStyle),
		Paragraph('Assigned to', itemStyle),
		Paragraph('Deadline', itemStyle)
		)
	if task_list:
		t = Table([headings] + completed_tasks, colWidths=[90*mm,40*mm,30*mm])
	else:
		t = Table(
			[headings] + [(Paragraph('No tasks', normalStyle),'','')],
			colWidths=[90*mm,40*mm,30*mm]
			)
	t.setStyle(TASK_TABLE_STYLE)
	Document.append(t)
	Document.append(Spacer(0,3*mm))


def create_pdf_agenda(request, meeting_id, output, **kwargs):
    
    # Generate the data which will populate the document
	account = Account.objects.filter(owner=request.user).last()
	meeting = Meeting.objects.get(pk=int(meeting_id))
	preliminary_items = meeting.item_set.filter(owner=request.user,
		variety__exact='preliminary')
	main_items = meeting.item_set.filter(owner=request.user,
		variety__exact='main')
	report_items = meeting.item_set.filter(owner=request.user,
		variety__exact='report')
	final_items = meeting.item_set.filter(owner=request.user,
		variety__exact='final')
	incomplete_task_list = Task.objects.filter(owner=request.user,
		status="Incomplete")
	completed_task_list = []
	preceding_meeting_date = find_preceding_meeting_date(request.user,
		meeting_id)
	if preceding_meeting_date != None:
		completed_task_list = Task.objects.filter(owner=request.user,
			status="Complete", deadline__gte=preceding_meeting_date).exclude \
			(deadline__gte=meeting.date)
	meeting_duration = get_formatted_meeting_duration(meeting_id)
	meeting_end_time = calculate_meeting_end_time(meeting_id)
	location = insert_page_breaks(meeting.location)
	notes = insert_page_breaks(meeting.notes)
	
	# Set up the document framework
	buffer = BytesIO()
	doc = BaseDocTemplate(buffer,
		rightMargin=25*mm,
		leftMargin=25*mm,
		topMargin=20*mm,
		bottomMargin=25*mm,
		title = account.group_name + "  |  Meeting of " +
			meeting.date.strftime("%d %b %Y"),
		pagesize=A4)
	body_frame = Frame(doc.leftMargin,
		doc.bottomMargin,
		doc.width,
		doc.height,
		leftPadding=0,
		bottomPadding=0,
		rightPadding=0,
		topPadding=0)
	template = PageTemplate(frames=body_frame, onPage=footer)
	doc.addPageTemplates([template])
	Document = []
	
	# Add main heading to document
	Document.append(Paragraph(account.group_name, heading2Style))
	Document.append(Paragraph("Meeting Agenda", heading1Style))
	Document.append(Spacer(0,3*mm))
	
	# Add meeting details to document
	Document.append(Paragraph("Meeting details", heading2Style))
	if notes != '':
		right_column = Table([
			(Paragraph('Notes', darkItemStyle),),
			(Paragraph(notes, normalStyle),),
			],
			colWidths=[80*mm])
		right_column.setStyle(MEETING_RIGHT_COLUMN_STYLE)
	else:
		right_column = None
	left_column = Table([
		(Paragraph('Date', darkItemStyle),
			Paragraph(meeting.date.strftime("%A %B %d, %Y"), normalStyle)),
		(Paragraph('Start Time', darkItemStyle),
			Paragraph(meeting.start_time.strftime("%H:%M"), normalStyle)),
		(Paragraph('End Time', darkItemStyle),
			Paragraph(meeting_end_time.strftime("%H:%M"), normalStyle)),
		(Paragraph('Duration', darkItemStyle),
			Paragraph(meeting_duration, normalStyle)),
		(Paragraph('Location', darkItemStyle),
			Paragraph(location, normalStyle))
		],
		colWidths=[22*mm,58*mm])
	left_column.setStyle(MEETING_LEFT_COLUMN_STYLE)
	if right_column:
		t = Table([((
				left_column,
				right_column
				))],
				colWidths=[80*mm,80*mm])
	else:
		t = Table([((
				left_column,
				))],
				colWidths=[80*mm])
		t.hAlign='LEFT'
	t.setStyle(MEETING_TABLE_STYLE)
	Document.append(t)
	Document.append(Spacer(0,3*mm))
		
	# Add preliminary items to document
	create_short_item_table('Preliminary items', preliminary_items, Document, t)
	
	# Add task review to document
	Document.append(Paragraph("Task review", heading2Style))
	create_task_table("Tasks outstanding", incomplete_task_list, Document, t)
	create_task_table("Tasks completed since last meeting", completed_task_list,
		Document, t)
		
	# Add reports to document
	create_long_item_table('Reports', report_items, Document, t)
	
	# Add main items to document
	create_long_item_table('Main items', main_items, Document, t)
	
	# Add final items to document
	create_short_item_table('Final items', final_items, Document, t)
	
	# Build the PDF
	doc.build(Document)
	
	# Get the PDF
	pdf = buffer.getvalue()
	buffer.close()
	
	# Create a HttpResponse if required
	if output == 'screen':
		response = HttpResponse(content_type='application/pdf')
		response['Content-Disposition'] = 'filename="AgendaForPrinting.pdf"'
#		response['Content-Disposition'] = 'attachment;
#		filename="AgendaForPrinting.pdf"'
		response.write(pdf)
	
	# Return the PDF or HttpResponse
	if output == 'attachment':
		return pdf	
	elif output == 'screen':
		return response
