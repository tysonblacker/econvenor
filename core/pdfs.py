from io import BytesIO

from django.http import HttpResponse

from reportlab.lib.colors import CMYKColor, black
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle, Frame, PageTemplate

from core.models import Account, Meeting, Task

from core.utils import calculate_meeting_duration, find_preceding_meeting_date


# Define text styles
styles = getSampleStyleSheet()
normalStyle = styles['Normal']
heading1Style = styles['Heading1']
heading2Style = styles['Heading2']
heading3Style = styles['Heading3']

# Define colors
heading_color = CMYKColor(0.4,0,0.2,0)	
background_color = CMYKColor(0.2,0,0.1,0)


def footer(canvas, doc):
    canvas.saveState()
    P = Paragraph("Page %d" % doc.page,
                  normalStyle)
    w, h = P.wrap(doc.width, doc.bottomMargin)
    P.drawOn(canvas, doc.leftMargin, h)
    canvas.restoreState()


def create_short_table(section_heading, item_list, Document, t):
	Document.append(Paragraph(section_heading, heading2Style))
	for item in item_list:
		heading_t = Table([(item.heading, str(item.time_limit) + ' minutes')],
			colWidths=[350,100],
			hAlign='LEFT')
		heading_t.setStyle(TableStyle(
			[('ALIGN',(-1,0),(-1,0),'RIGHT')]))
		if item.background:
			t = Table([(heading_t,),
				(item.background,)],
				colWidths=[450],
				hAlign='LEFT')
		else:
			t = Table([(heading_t,)],
				colWidths=[450],
				hAlign='LEFT')
		t.setStyle(TableStyle(
			[('GRID', (0,0), (1,-1), 0.5, black),
			('BACKGROUND', (0, 0), (-1, 0), background_color),
			('LEFTPADDING', (0, 0), (-1, 0), 0),
			('TOPPADDING', (0, 0), (-1, 0), 0),
			('BOTTOMPADDING', (0, 0), (-1, 0), 0),]))
		Document.append(t)
		Document.append(Spacer(0,3*mm))

def create_long_table(section_heading, item_list, Document, t):
	Document.append(Paragraph(section_heading, heading2Style))
	for item in item_list:
		heading_t = Table([(item.heading, str(item.time_limit) + ' minutes')],
			colWidths=[350,100],
			hAlign='LEFT')
		heading_t.setStyle(TableStyle(
			[('ALIGN',(-1,0),(-1,0),'RIGHT')]))
		t = Table([(heading_t,),
			(Paragraph('To be introduced by ' + str(item.explainer), normalStyle),),
			(Paragraph(item.background, normalStyle),),],
			colWidths=[450],
			hAlign='LEFT')
		t.setStyle(TableStyle(
			[('GRID', (0,0), (1,-1), 0.5, black),
			('BACKGROUND', (0, 0), (-1, 0), background_color),
			('LEFTPADDING', (0, 0), (-1, 0), 0),
			('TOPPADDING', (0, 0), (-1, 0), 0),
			('BOTTOMPADDING', (0, 0), (-1, 0), 0),]))
		Document.append(t)
		Document.append(Spacer(0,3*mm))


def create_pdf_agenda(request, meeting_id, **kwargs):
	# Set up the HttpResponse
	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'filename="AgendaForPrinting.pdf"'
#	Replace line above with the line below after testing is finished
#	response['Content-Disposition'] = 'attachment; filename="AgendaForPrinting.pdf"'
    
    # Set up the document framework
	buffer = BytesIO()
	doc = SimpleDocTemplate(buffer,
		rightMargin=20*mm,
		leftMargin=20*mm,
		topMargin=20*mm,
		bottomMargin=20*mm,
		pagesize=A4)
	Document = []
    		
	# Generate the data which will populate the document
	account = Account.objects.filter(owner=request.user).last()
	meeting = Meeting.objects.get(pk=int(meeting_id))
	preliminary_items = meeting.item_set.filter(owner=request.user, variety__exact='preliminary')
	main_items = meeting.item_set.filter(owner=request.user, variety__exact='main')
	report_items = meeting.item_set.filter(owner=request.user, variety__exact='report')
	final_items = meeting.item_set.filter(owner=request.user, variety__exact='final')
	incomplete_task_list = Task.objects.filter(owner=request.user, status="Incomplete")
	completed_task_list = []
	preceding_meeting_date = find_preceding_meeting_date(request.user, meeting_id)
	if preceding_meeting_date != None:
		completed_task_list = Task.objects.filter(owner=request.user, status="Complete", deadline__gte=preceding_meeting_date).exclude(deadline__gte=meeting.date)
	meeting_duration = calculate_meeting_duration(meeting_id)
		
	# Agenda heading
	Document.append(Paragraph(account.group_name, heading2Style))
	Document.append(Paragraph("Meeting Agenda", heading1Style))
	Document.append(Spacer(0,3*mm))
	
	# Meeting details
	Document.append(Paragraph("Meeting details", heading2Style))
	t = Table([('Date', meeting.date),
		('Time', '*14:00*'),
		('Duration', str(meeting_duration) + " minutes"),
		('Location', meeting.location)],
		colWidths=[70,150],
		hAlign='LEFT')
	t.setStyle(TableStyle([('GRID', (0,0), (-1,-1), 0.5, black),
		('VALIGN',(0,0),(-1,-1),'TOP'),
		('BACKGROUND', (0, 0), (0, -1), background_color),
		]))
	Document.append(t)
	Document.append(Spacer(0,3*mm))
		
	# Preliminary items
	create_short_table('Preliminary items', preliminary_items, Document, t)
	
	# Task review - Tasks outstanding
	Document.append(Paragraph("Task review", heading2Style))
	Document.append(Paragraph("Tasks outstanding", heading3Style))
	headings = ('Description', 'Assigned to', 'Deadline')
	incomplete_tasks = [(task.description, task.participant, task.deadline) for task in incomplete_task_list]
	t = Table([headings] + incomplete_tasks, colWidths=[280,100,70], hAlign='LEFT')
	t.setStyle(TableStyle(
		[('GRID', (0,0), (-1,-1), 0.5, black),
		('BACKGROUND', (0, 0), (-1, 0), background_color)]))
	Document.append(t)
	Document.append(Spacer(0,3*mm))
	
	# Task review - Tasks completed since last meeting
	Document.append(Paragraph("Tasks completed since last meeting", heading3Style))
	completed_tasks = [(task.description, task.participant, task.deadline) for task in completed_task_list]
	if completed_task_list:
		t = Table([headings] + completed_tasks, colWidths=[280,100,70], hAlign='LEFT')
	else:
		t = Table([headings] + [('No tasks','','')], colWidths=[280,100,70], hAlign='LEFT')
	t.setStyle(TableStyle(
		[('GRID', (0,0), (-1,-1), 0.5, black),
		('BACKGROUND', (0, 0), (-1, 0), background_color)]))
	Document.append(t)
	Document.append(Spacer(0,3*mm))
	
	# Reports
	create_long_table('Reports', report_items, Document, t)
	
	# Main items
	create_long_table('Main items', main_items, Document, t)
	
	# Final items
	create_short_table('Final items', final_items, Document, t)
	
	frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height,
               id='body')
	template = PageTemplate(id='footer', frames=frame, onPage=footer)
	doc.addPageTemplates([template])
	
	
	# Build and return the PDF
	doc.build(Document)
	
	pdf = buffer.getvalue()
	buffer.close()
	
	response.write(pdf)
	return response