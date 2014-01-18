from io import BytesIO

from django.http import HttpResponse

from reportlab.lib.colors import CMYKColor, black
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from core.models import Account, Meeting, Task

from core.utils import calculate_meeting_duration


def create_pdf_agenda(request, meeting_id, **kwargs):
	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'filename="AgendaForPrinting.pdf"'
#	Replace line above with the line below after testing is finished
#	response['Content-Disposition'] = 'attachment; filename="AgendaForPrinting.pdf"'
    
	styles = getSampleStyleSheet()
	buffer = BytesIO()
	doc = SimpleDocTemplate(buffer,
		rightMargin=20*mm,
		leftMargin=20*mm,
		topMargin=20*mm,
		bottomMargin=20*mm,
		pagesize=A4)
	Document = []
	style = styles["Normal"]
	heading_color = CMYKColor(0.4,0,0.2,0)	
	background_color = CMYKColor(0.2,0,0.1,0)
	
	account = Account.objects.filter(owner=request.user).last()
	meeting = Meeting.objects.get(pk=int(meeting_id))
	meeting_duration = calculate_meeting_duration(meeting_id)
		
	# Agenda heading
	Document.append(Paragraph(account.group_name, styles['Heading2']))
	Document.append(Paragraph("Meeting Agenda", styles['Heading1']))
	Document.append(Spacer(0,3*mm))
	
	# Meeting details
	Document.append(Paragraph("Meeting details", styles['Heading2']))
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
	
		
	# Build and return the PDF
	doc.build(Document)
	
	pdf = buffer.getvalue()
	buffer.close()
	
	response.write(pdf)
	return response
