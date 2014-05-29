import os
import reportlab.rl_config
import socket

from datetime import date, datetime
from io import BytesIO
from string import replace
from subprocess import call

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.utils.text import slugify

from reportlab.lib.colors import black, CMYKColor, white
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase.pdfmetrics import registerFont, \
                                         registerFontFamily, \
                                         stringWidth
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, \
                               PageBreak, Paragraph, Spacer, Table, TableStyle 
from reportlab.platypus.flowables import KeepTogether

from accounts.models import Group
from decisions.models import Decision
from docs.utils import calculate_meeting_duration, \
                       calculate_meeting_end_time, \
                       get_completed_tasks_list, \
                       get_outstanding_tasks_list, \
                       get_overdue_tasks_list
from meetings.models import Meeting
from meetings.utils import find_or_create_distribution_record
from participants.models import Participant
from tasks.models import Task
from utilities.commonutils import set_path


# Define colors
heading_color = CMYKColor(0,0,0,0.85)	
body_color = CMYKColor(0,0,0,0.85)
table_color = CMYKColor(0,0,0,0.85)
shading_color = CMYKColor(0,0,0,0.2)

# Define dimensions
line_width = 0.75
printable_width = 170*mm

# Set path to fonts
FONT_PATH = os.path.join(settings.BASE_DIR, 'commonstatic/fonts/')

# Register fonts
body_font = 'DejaVuSansCondensed'
heading_font = 'DejaVuSansCondensed'
registerFont(TTFont(body_font, FONT_PATH + body_font + ".ttf"))
registerFont(TTFont(body_font + 'Bd', FONT_PATH + body_font + "-Bold.ttf"))
registerFont(TTFont(body_font + 'It', FONT_PATH + body_font + "-Oblique.ttf"))
registerFont(TTFont(body_font + 'BI', 
                    FONT_PATH + body_font + "-BoldOblique.ttf"))
registerFont(TTFont(heading_font, FONT_PATH + heading_font + ".ttf"))
registerFontFamily(body_font, normal=body_font, bold=body_font + 'Bd',
	italic=body_font + 'It', boldItalic=body_font + 'BI')
reportlab.rl_config.warnOnMissingFontGlyphs = 0

# Create text style sheet
styles = getSampleStyleSheet()

# Define 'Normal' text style
normalStyle = styles['Normal']
normalStyle.fontName = body_font
normalStyle.textColor = body_color
normalStyle.alignment = TA_JUSTIFY
normalStyle.fontSize=10
normalStyle.leading=14
normalStyle.spaceBefore=2
normalStyle.spaceAfter=2

# Define 'LeftAligned' text style
styles.add(ParagraphStyle(
           name='LeftAligned',
           parent=styles['Normal'],
           alignment = TA_LEFT,
           ))
leftAlignedStyle = styles['LeftAligned']

# Define 'ItemHeading' text style
styles.add(ParagraphStyle(
           name='ItemHeading',
           parent=styles['Normal'],
           fontName = body_font,
           textColor = white
           ))
itemHeadingStyle = styles['ItemHeading']

# Define 'ItemHeadingRight' text style
styles.add(ParagraphStyle(
           name='ItemHeadingRight',
           parent=styles['ItemHeading'],
           alignment = TA_RIGHT
           ))
itemHeadingRightStyle = styles['ItemHeadingRight']

# Define 'Shaded' text style
styles.add(ParagraphStyle(
           name='Shaded',
           parent=styles['Normal'],
           textColor = heading_color
           ))
shadedStyle = styles['Shaded']

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

# Define a skeleton table style
SUPERSTRUCTURE_STYLE = TableStyle([
    ('VALIGN',(0,0),(-1,-1), 'TOP'),
    ('LEFTPADDING', (0,0), (-1,-1), 0),
    ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ('TOPPADDING', (0,0), (-1,-1), 0),
    ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ])

# Define table styles that relate to meeting details
MEETING_DETAILS_STYLE = TableStyle([
    ('GRID', (0,0), (-1,-1), line_width, table_color),
    ('VALIGN',(0,0),(-1,-1), 'TOP'),
    ('TOPPADDING', (0,0), (-1,-1), 4),
    ('BACKGROUND', (0,0), (-0,-1), shading_color),
    ])

SINGLE_DETAILS_ITEM_STYLE = TableStyle([
    ('BOX', (0,0), (-1,-1), line_width, table_color),
    ('LINEBEFORE', (1,0), (1,-1), line_width, table_color),
    ('VALIGN',(0,0),(-1,-1), 'TOP'),
    ('BACKGROUND', (0,0), (-0,-1), shading_color),
    ('TOPPADDING', (0,0), (-1, 0), 6),
    ('BOTTOMPADDING', (0,-1), (-1,-1), 6),
    ])

# Define table styles that relate to agenda items only
AGENDA_ITEM_HEADING_STYLE = TableStyle([
    ('GRID', (0,0), (-1,0), line_width, table_color),
    ('ALIGN',(-1,0),(-1,0),'RIGHT'),
    ('TOPPADDING', (0,0), (-1,-1), 4),
    ('BACKGROUND', (0,0), (-1,-1), table_color),
    ])    

# Define table styles that relate to minutes items only
MINUTES_ITEM_HEADING_STYLE = TableStyle([
    ('GRID', (0,0), (-1,0), line_width, table_color),
    ('TOPPADDING', (0,0), (-1,-1), 4),
    ('BACKGROUND', (0,0), (-1,-1), table_color),
    ])

# Define table styles that relate to agenda and minutes items
SHADED_STYLE = TableStyle([
    ('GRID', (0,0), (1,-1), line_width, table_color),
    ('VALIGN',(0,0),(-1,-1),'TOP'),
    ('TOPPADDING', (0,0), (-1,-1), 4),
    ('BACKGROUND', (0,0), (-1,-1), shading_color),
    ])
    
ITEM_STYLE = TableStyle([
    ('BOX', (0,0), (-1,-1), line_width, table_color),
    ('VALIGN',(0,0),(-1,-1), 'TOP'),
    ('TOPPADDING', (0,0), (-1, 0), 6),
    ('BOTTOMPADDING', (0,-1), (-1,-1), 6),
    ])

# Define table style that relates to tasks and decisions
DECISIONS_AND_TASKS_STYLE = TableStyle([
    ('GRID', (0,0), (-1,-1), line_width, table_color),
    ('VALIGN',(0,0),(-1,-1),'TOP'),
    ('TOPPADDING', (0,0), (-1,-1), 4),
    ('BACKGROUND', (0,0), (-1,0), shading_color),
    ])

# Define table style that relates to tasks
TASKS_STYLE = TableStyle([
    ('GRID', (0,0), (-1,-1), line_width, table_color),
    ('VALIGN',(0,0),(-1,-1),'TOP'),
    ('SPAN', (0,0), (-1,0)),
    ('TOPPADDING', (0,0), (-1,-1), 4),
    ('BACKGROUND', (0,0), (-1,0), table_color),
    ('BACKGROUND', (0,1), (-1,1), shading_color),
    ])


def fit_to_table_cell(content, cell_width,
                      font_name=leftAlignedStyle.fontName,
                      font_size=leftAlignedStyle.fontSize):
    """
    Makes sure that single line contents of a table cell always fit within it.
    They are truncated and ellipsis added if necessary.
    """
    available_width = cell_width - 8*mm
    content_width = stringWidth(content, font_name, font_size)
    add_ellipsis = False
    while content_width > available_width:
        content = content[:-1]
        content_width = stringWidth(content, font_name, font_size)
        add_ellipsis = True
    if add_ellipsis:
        content += u'\u2026'
    return content


def insert_line_breaks(string_data):
    """
    Replaces line break characters in strings with <br/> tags.
    """
    formatted_string = replace(string_data, '\n', '<br/>')
    return formatted_string


def create_paragraph_list(string_data):
    """
    Creates a list of paragraphs from a string.
    """
    paragraph_list = string_data.splitlines()
    return paragraph_list


def create_details_item_bottom_table(label, field):
    """
    Creates a table for each of the fields 'attendance', 'apologies' and 
    'notes' fields.
    """
    paragraphs = create_paragraph_list(field)
    contents = []
    for paragraph in paragraphs:
        contents.append((Paragraph(label, shadedStyle),
                         Paragraph(paragraph, normalStyle)))
        label = ''
    t = Table(contents, colWidths=[21*mm,149*mm])
    t.setStyle(SINGLE_DETAILS_ITEM_STYLE)
    return t


def create_item_table(field):
    """
    Creates a table for 'background' and 'minute_notes' fields.
    """
    paragraphs = create_paragraph_list(field)
    contents = []
    for paragraph in paragraphs:
        contents.append((Paragraph(paragraph, normalStyle),))
    t = Table(contents, colWidths=[printable_width])
    t.setStyle(ITEM_STYLE)
    return t

  
def footer(canvas, doc):
    """
    Creates the footer for each page of the PDF.
    """
    canvas.saveState()
    canvas.setLineWidth(line_width)
    canvas.setFillColor(body_color)
    canvas.setStrokeColor(table_color)
    canvas.setFont(body_font, normalStyle.fontSize)
    canvas.line(20*mm,13*mm,190*mm,13*mm)
    right_text = "Page %s" % (doc.page)
    canvas.drawRightString(190*mm, 9*mm, right_text)
    left_text = doc.title
    canvas.drawString(20*mm, 9*mm, left_text)
    canvas.restoreState()


def create_document_header(meeting, group_name, doc_type, Document):
    """
    Creates the heading for the document.
    """
    if doc_type == 'agenda':
        title = 'Agenda'
    if doc_type == 'minutes':
        title = 'Minutes'
 
    Document.append(Paragraph(group_name, heading2Style))
    Document.append(Paragraph(title, heading1Style))    
    Document.append(Paragraph(meeting.meeting_type, heading2Style))
    Document.append(Spacer(0,5*mm))    


def create_details_table(meeting, doc_type, Document):
    """
    Creates the meeting details table.
    """
    # Set up the data
    if doc_type == 'agenda':
        date = meeting.date_scheduled.strftime("%A %B %d, %Y")
        start_time = meeting.start_time_scheduled.strftime("%I:%M %p").\
                     lstrip('0').lower()
        duration = calculate_meeting_duration(meeting)
        if duration != 0:
            end_time = calculate_meeting_end_time(meeting).\
                       strftime("%I:%M %p").lstrip('0').lower() + \
                       ' (estimated)'
        else:
            end_time = 'To be decided'
        location = insert_line_breaks(meeting.location_scheduled)
        if meeting.facilitator_scheduled:
            facilitator = str(meeting.facilitator_scheduled)
        else:
            facilitator = 'To be decided'
        if meeting.minute_taker_scheduled:
            minute_taker = str(meeting.minute_taker_scheduled)
        else:
            minute_taker = 'To be decided'
        notes = meeting.instructions_scheduled
    if doc_type == 'minutes':
        date = meeting.date_actual.strftime("%A %B %d, %Y")
        start_time = meeting.start_time_actual.strftime("%I:%M %p").\
                     lstrip('0').lower()
        end_time = meeting.end_time_actual.strftime("%I:%M %p").lstrip('0').\
                   lower()
        location = insert_line_breaks(meeting.location_actual)
        notes = meeting.instructions_actual
        facilitator = str(meeting.facilitator_actual)
        minute_taker = str(meeting.minute_taker_actual)
        attendance = meeting.attendance               
        apologies = meeting.apologies        
    # Trim contents to fit cells where necessary
    facilitator = fit_to_table_cell(facilitator, 63*mm)
    meeting_no = fit_to_table_cell(meeting.meeting_no, 63*mm)
    minute_taker = fit_to_table_cell(minute_taker, 63*mm)
    # Set up top left block
    top_left_contents = [
        (Paragraph('Meeting', shadedStyle),
            Paragraph(meeting_no, leftAlignedStyle)),
        (Paragraph('Date', shadedStyle),
            Paragraph(date, leftAlignedStyle)),
        (Paragraph('Start time', shadedStyle),
            Paragraph(start_time, leftAlignedStyle)),
        (Paragraph('End time', shadedStyle),
            Paragraph(end_time, leftAlignedStyle)),
        ]     
    top_left_block = Table(top_left_contents, colWidths=[21*mm,63*mm],
                           rowHeights=[21,21,21,21])
    top_left_block.setStyle(MEETING_DETAILS_STYLE)
    # Set up top row middle block
    top_middle_block = Table([
            ('',), ('',), ('',), ('',),
            ],
        colWidths=[2*mm])
    # Set up the top row right block
    top_right_contents = [
        (Paragraph('Location', shadedStyle),
            Paragraph(location, leftAlignedStyle)),
        (Paragraph('Facilitator', shadedStyle),
            Paragraph(facilitator, leftAlignedStyle)),
        (Paragraph('Minutes', shadedStyle),
            Paragraph(minute_taker, leftAlignedStyle)),
        ]     
    top_right_block = Table(top_right_contents, colWidths=[21*mm,63*mm],
                            rowHeights=[42,21,21])
    top_right_block.setStyle(MEETING_DETAILS_STYLE)
    #Create the top row table
    top_t = Table([((
           top_left_block,
           top_middle_block,
           top_right_block
           ))],)
    top_t.setStyle(SUPERSTRUCTURE_STYLE)
    # Set up the bottom row
    bottom_contents = []
    if doc_type == 'minutes':
        if attendance:
            attendance_t = create_details_item_bottom_table('Attendees',
                                                            attendance)
        if apologies:
            apologies_t = create_details_item_bottom_table('Apologies',
                                                           apologies)
    if notes:
        notes_t = create_details_item_bottom_table('Notes', notes)
    #Create the bottom row table
    bottom_contents = []
    if doc_type == 'minutes':
        if attendance:
            bottom_contents.append([(attendance_t,)])
        if apologies:
            bottom_contents.append([(apologies_t,)])    
    if notes:
        bottom_contents.append([(notes_t,)])
    if bottom_contents:
        bottom_t = Table(bottom_contents, colWidths=[printable_width])
        bottom_t.setStyle(SUPERSTRUCTURE_STYLE)
    #Add bottom and top rows to the document
    Document.append(top_t)
    if bottom_contents:
       Document.append(Spacer(0,2*mm))
       Document.append(bottom_t)
    Document.append(Spacer(0,7*mm))


def create_agenda_item_table(items, Document):
    """
    Creates the agenda items tables.
    """
    for item in items:
        # Create the heading sub-table
        raw_title = 'Item ' + str(item.item_no) + ':&nbsp;&nbsp;' + item.title
        title = fit_to_table_cell(raw_title, 165*mm,
                                  font_name=itemHeadingStyle.fontName,
                                  font_size=itemHeadingStyle.fontSize)
        if item.time_limit:
            time_limit_content = Paragraph(str(item.time_limit) + ' mins',
                                           itemHeadingRightStyle)
        else: 
            time_limit_content = ''
        heading_t = Table([((
                Paragraph(title, itemHeadingStyle),
                time_limit_content,
                ))],
            colWidths=[150*mm,20*mm]
            )
        heading_t.setStyle(AGENDA_ITEM_HEADING_STYLE)
        # Create the explainer sub-table
        if item.explainer:
            explainer_t = Table([((
                          Paragraph('To be introduced by '+str(item.explainer),
                           shadedStyle),))
                          ],
                  colWidths=[printable_width])
            explainer_t.setStyle(SHADED_STYLE)
        # Create the background sub-table            
        if item.background:
            background_t = create_item_table(item.background)
        #Create the item table
        item_contents = [[(heading_t,)]]
        if item.explainer:
            item_contents.append([(explainer_t,)])
        if item.background:
            item_contents.append([(background_t,)])
        t = Table(item_contents, colWidths=[printable_width])
        t.setStyle(SUPERSTRUCTURE_STYLE)
        #Add the item table to the document
        Document.append(KeepTogether(t))
        Document.append(Spacer(0,7*mm))
    
    Document.append(Paragraph('NOTE: A summary of tasks for review is on the '
                              'next page.', normalStyle))
    Document.append(PageBreak())


def create_minutes_item_table(items, group, Document):
    """
    Creates the minutes items tables.
    """
    for item in items:
        # Create the heading sub-table
        raw_title = 'Item ' + str(item.item_no) + ':&nbsp;&nbsp;' + item.title
        title = fit_to_table_cell(raw_title, 165*mm,
                                  font_name=itemHeadingStyle.fontName,
                                  font_size=itemHeadingStyle.fontSize)
        heading_t = Table([((
                Paragraph(title, itemHeadingStyle),
                ))],
            colWidths=[printable_width]
            )
        heading_t.setStyle(MINUTES_ITEM_HEADING_STYLE)
        # Set up the minute notes as a sub-table
        if item.minute_notes:
            notes_t = create_item_table(item.minute_notes)
        # Set up decisions as a sub-table
        decisions_list = Decision.lists.ordered_decisions().\
                         filter(group=group, item=item)
        if decisions_list:
            decisions_heading = (
                Paragraph('Decisions', shadedStyle),
                )
            decisions = [(
                Paragraph(decision.description, normalStyle),
                )
                for decision in decisions_list]
            decisions_t = Table([decisions_heading] + decisions,
                            colWidths=[printable_width])
            decisions_t.setStyle(DECISIONS_AND_TASKS_STYLE)
        # Set up tasks as a sub-table
        tasks_list = Task.lists.ordered_tasks().filter(group=group, item=item)
        if tasks_list:
            column_headings = (
                Paragraph('Task', shadedStyle),
                Paragraph('Assigned to', shadedStyle),
                Paragraph('Deadline', shadedStyle)
                )
            tasks = [(
                Paragraph(task.description, leftAlignedStyle),
                Paragraph(fit_to_table_cell(str(task.participant), 40*mm), normalStyle),
                Paragraph(task.deadline.strftime("%d %b %Y"), normalStyle)
                )
                for task in tasks_list]
            tasks_t = Table([column_headings] + tasks,
                            colWidths=[100*mm,40*mm,30*mm])
            tasks_t.setStyle(DECISIONS_AND_TASKS_STYLE) 
        # Generate the complete table
        table_contents = [[(heading_t,)]]
        if item.minute_notes:
            table_contents.append([(notes_t,)]) 
        if decisions_list:
            table_contents.append([(decisions_t,)])        
        if tasks_list:
            table_contents.append([(tasks_t,)])
        t = Table(table_contents, colWidths=[printable_width], repeatRows=1)
        t.setStyle(SUPERSTRUCTURE_STYLE)
        # Add this table to the document and put some space after it
        Document.append(t)
        Document.append(Spacer(0,7*mm))


def create_task_table(section_heading, task_list, task_type, meeting, \
                      doc_type, Document):
    """
    Creates the tasks tables.
    """
    if task_type == 'overdue':
        empty_message = 'There are no overdue tasks.'
        time_column_heading = 'Deadline'
    elif task_type == 'outstanding':
        empty_message = 'There are no tasks to be completed.'
        time_column_heading = 'Deadline'
    elif task_type == 'completed':
        empty_message = 'No tasks have been completed since last meeting.'
        time_column_heading = 'Completed'    
    if task_type == 'new':
        empty_message = 'No tasks were assigned in this meeting.'
        time_column_heading = 'Deadline'
    # Create the heading row           
    heading = (Paragraph(section_heading, itemHeadingStyle),'','')
    # Create the column labels row           
    column_headings = (
        Paragraph('Description', shadedStyle),
        Paragraph('Assigned to', shadedStyle),
        Paragraph(time_column_heading, shadedStyle)
        )
    # Create the tasks rows           
    if task_type == 'completed':
        tasks = [(
            Paragraph(task.description, leftAlignedStyle),
            Paragraph(fit_to_table_cell(str(task.participant), 40*mm), normalStyle),
            Paragraph(task.completion_date.strftime("%d %b %Y"), normalStyle)
            )
            for task in task_list]
    else:
        tasks = [(
            Paragraph(task.description, leftAlignedStyle),
            Paragraph(fit_to_table_cell(str(task.participant), 40*mm), normalStyle),
            Paragraph(task.deadline.strftime("%d %b %Y"), normalStyle)
            )
            for task in task_list]
    # Generate the complete table
    if task_list:
        t = Table([heading] + [column_headings] + tasks,
                  colWidths=[105*mm,40*mm,25*mm],
                  repeatRows=2)
    else:
        if doc_type == 'minutes':
            if meeting.date_actual > date.today():
                empty_message = 'This table can\'t be populated before the' \
                                ' date of the meeting'
        t = Table([heading] + [column_headings] + \
                  [(Paragraph(empty_message, 
                    normalStyle),'','')],
              colWidths=[105*mm,40*mm,25*mm]
              )
    t.setStyle(TASKS_STYLE) 
    # Add this table to the document and put some space after it
    Document.append(t)
    Document.append(Spacer(0,5*mm))


def create_next_meeting_table(meeting, Document):
    """
    Creates a table in minutes for details of the next meeting.
    """
    date = meeting.next_meeting_date
    start_time = meeting.next_meeting_start_time
    location = insert_line_breaks(meeting.next_meeting_location)
    facilitator = meeting.next_meeting_facilitator
    minute_taker = meeting.next_meeting_minute_taker
    notes = insert_line_breaks(meeting.next_meeting_instructions)
    # Trim contents to fit cells where necessary
    if facilitator:
        facilitator = fit_to_table_cell(str(facilitator), 64*mm)
    if minute_taker:
        minute_taker = fit_to_table_cell(str(minute_taker), 64*mm)
    # Set up the heading row as a sub-table   
    heading_t = Table([((
                Paragraph('Details of next meeting', itemHeadingStyle),
                ))],
            colWidths=[printable_width/2]
            )    
    heading_t.setStyle(MINUTES_ITEM_HEADING_STYLE)
    # Set up the contents rows
    contents = []
    if date:
        contents.append(
            (Paragraph('Date', shadedStyle),
                Paragraph(date.strftime("%A %B %d, %Y"), normalStyle)))
    if start_time:
        contents.append(
            (Paragraph('Start time', shadedStyle),
             Paragraph(start_time.strftime("%I:%M %p").lstrip('0').lower(),
                       normalStyle)))  
    if location:
        contents.append(
            (Paragraph('Location', shadedStyle),
             Paragraph(location, normalStyle)))
    if facilitator:
       contents.append(
            (Paragraph('Facilitator', shadedStyle),
             Paragraph(facilitator, normalStyle)))
    if minute_taker:
        contents.append(
            (Paragraph('Minutes', shadedStyle),
             Paragraph(minute_taker, normalStyle)))
    if notes:
        contents.append(
            (Paragraph('Notes', shadedStyle),
                Paragraph(notes, normalStyle)))
    # Set up the body sub-table                                  
    if contents:
        body_t = Table(contents, colWidths=[21*mm,64*mm])
        body_t.setStyle(MEETING_DETAILS_STYLE)
        # Set up the whole table
        table_contents = [[(heading_t,)], [(body_t,)]]
        t = Table(table_contents, colWidths=[printable_width/2])
        t.setStyle(SUPERSTRUCTURE_STYLE)
        t.hAlign = 'LEFT'
        Document.append(KeepTogether(t))
        Document.append(Spacer(0,5*mm))
    Document.append(Paragraph('NOTE: A summary of tasks assigned in this '
                              'meeting is on the next page.', shadedStyle))
    Document.append(PageBreak())


def create_pdf(request, group, meeting, doc_type):
    """
    Constructs the PDF document.
    """
    # Set up the document framework
    group_name = group.name
    buffer = BytesIO()
    doc = BaseDocTemplate(buffer,
        rightMargin=20*mm,
        leftMargin=20*mm,
        topMargin=20*mm,
        bottomMargin=20*mm,
        title = fit_to_table_cell(group_name, 90*mm) + "  |  Meeting no.: " +
            meeting.meeting_no,
        pagesize=A4,
        allowSplitting = 1,)
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
    create_document_header(meeting, group_name, doc_type, Document)
    
    # Add meeting details to document
    create_details_table(meeting, doc_type, Document)

    # Add items to document
    items = meeting.item_set.filter(group=group).order_by('item_no')
    if doc_type == 'agenda':
        create_agenda_item_table(items, Document)
    if doc_type == 'minutes':
        create_minutes_item_table(items, group, Document)

    # Add next meeting table to minutes
    if doc_type == 'minutes':
        create_next_meeting_table(meeting, Document)

    # Add new task summary to minutes
    if doc_type == 'minutes':
        new_tasks_list = Task.lists.all_tasks().filter(group=group,
                                                            meeting=meeting)
        create_task_table(
            'New tasks assigned in this meeting (ordered by deadline)',
            new_tasks_list, 'new', meeting, doc_type, Document)
                
    # Add task review
    overdue_tasks = get_overdue_tasks_list(group=group,
                                               meeting=meeting,
                                               doc_type=doc_type)
    outstanding_tasks = get_outstanding_tasks_list(group=group,
                                                   meeting=meeting,
                                                   doc_type=doc_type)
    completed_tasks = get_completed_tasks_list(group=group,
                                                 meeting=meeting,
                                                 doc_type=doc_type)
    if doc_type == 'agenda':
        if meeting.date_scheduled < date.today():
            list_date = meeting.date_scheduled.strftime("%d %b %Y")
        else:
            list_date = date.today().strftime("%d %b %Y")
            
        completed_tasks_heading = 'Existing tasks:&nbsp;&nbsp;' + \
                                  'Completed since last meeting' + \
                                  ' (this list current at ' + \
                                  list_date + ')'
    elif doc_type == 'minutes':
        completed_tasks_heading = 'Existing tasks:&nbsp;&nbsp;' + \
                                  'Completed since last meeting'
    if (doc_type == 'agenda') or meeting.existing_tasks_in_minutes:
        create_task_table(
            'Existing tasks:&nbsp;&nbsp;Overdue',
            overdue_tasks, 'overdue', meeting, doc_type, Document)
        create_task_table(
            'Existing tasks:&nbsp;&nbsp;Incomplete and not overdue',
            outstanding_tasks, 'outstanding', meeting, doc_type, Document)
        create_task_table(
            completed_tasks_heading, completed_tasks, 'completed', meeting,
            doc_type, Document)
       
    # Build the PDF
    doc.build(Document)

    # Get the PDF
    pdf = buffer.getvalue()
    buffer.close()

    # Define locations to save files to
    pdf_path = get_pdf_path()
    preview_path = get_preview_path()

    # Define name of PDF file
    base_file_name = get_base_file_name(request, group, meeting, doc_type) 
    pdf_name = base_file_name + '.pdf'

    # Delete any old PDF versions for this meeting
    path_to_pdf = pdf_path + pdf_name
    path_to_previews = preview_path + base_file_name + '*'	

    call('rm ' + path_to_pdf , shell=True)
    call('rm ' + path_to_previews , shell=True)	

    # Save the PDF temporarily without assigning a version to it
    f = open(path_to_pdf, 'w')
    f.write(pdf)
    f.close()

    # Generate the preview images
    pages = create_images_from_pdf(base_file_name)
    return pages
    

def create_images_from_pdf(base_file_name, **kwargs):
    """
    Creates preview images from a PDF.
    Returns a list of their file paths.
    """
    # Create and save the images
    preview_path = get_preview_path()
    pdf_path = get_pdf_path()
    if kwargs:
        version = str(kwargs['version'])
        pdf_name = base_file_name + '_v' + version + '.pdf'
        output_path = preview_path + base_file_name + '_v' + \
                      version + '_page%d.png' 
    else:
        pdf_name = base_file_name + '.pdf'
        output_path = preview_path + base_file_name + '_page%d.png' 
    pdf_location = pdf_path + pdf_name
    ghostscript_command = "gs -q -dSAFER -dBATCH -dNOPAUSE -sDEVICE=png16m \
                          -r135 -dTextAlphaBits=4 -sPAPERSIZE=a4 \
                          -sOutputFile=" + output_path + ' ' + pdf_location

    call(ghostscript_command, shell=True)

    # Calculate the number of preview pages plus 1
    image_exists = True
    count = 0
    while image_exists:
        count += 1
        filename_to_test = preview_path + base_file_name + '_page' + \
                           str(count) + '.png' 
        image_exists = os.path.isfile(filename_to_test)

    # Make a list of the names of all the preview files
    pages = []
    for i in range(1, count):
        file_name = 'tmp/' + base_file_name + '_page' + str(i) + '.png'
        pages.append((i, file_name))
    return pages


def get_base_file_name(request, group, meeting, doc_type):
    """
    Returns the base file name with no suffix.
    """
    cleaned_meeting_no = meeting.meeting_no.replace('/', '-')
    cleaned_meeting_no = cleaned_meeting_no.replace('_', '-')
    meeting_no_slug = slugify(cleaned_meeting_no)
    if doc_type == 'agenda':
        base_file_name = str(group.id) + '_' + group.slug + '_agenda_' + \
                         meeting_no_slug
    elif doc_type == 'minutes':
        base_file_name = str(group.id) + '_' + group.slug + '_minutes_' + \
                         meeting_no_slug   
    
    return base_file_name


def get_pdf_path():
    """
    Returns the location that the document will be saved to.
    """
    pdf_path = os.path.join(settings.MEDIA_ROOT, 'meeting_docs/')
    return pdf_path


def get_preview_path():
    """
    Returns the location that the preview images will be saved to.
    """
    preview_path = os.path.join(settings.MEDIA_ROOT, 'tmp/')
    if not os.path.exists(preview_path):
        os.makedirs(preview_path)
    return preview_path
    

def get_pdf_preview_contents(request, group, meeting, doc_type):
    """
    Returns the contents of the PDF document.
    """
    pdf_path = get_pdf_path()
    base_file_name = get_base_file_name(request, group, meeting, doc_type)
    path_to_pdf = pdf_path + base_file_name + ".pdf"
    f = open(path_to_pdf, 'r')
    contents = f.read()
    f.close()

    return contents
    

def get_pdf_contents(request, group, meeting, doc_type):
    """
    Returns the contents of the PDF document.
    """
    
    if doc_type == 'agenda':
        contents = meeting.agenda_pdf
    elif doc_type == 'minutes':
        contents = meeting.minutes_pdf

    return contents


def distribute_pdf(request, group, meeting, doc_type):
    """
    Emails out the document.
    """  	
    recipients = []
    group_name = group.name

    # build recipients list if "all_participants" box is checked
    if 'all_participants' in request.POST:
        participants = Participant.lists.active().filter(group=group)
        for participant in participants:
            email = participant.email
            recipients.append(email)

    # build recipients list if "all_participants" box is not checked
    else:
        # create recipients list in this format: [participant1, participant4]
        distribution_list = []
        for key in request.POST:
            if request.POST[key] == 'checked':
                distribution_list.append(key)

        # create recipients list in this format: [1, 4]
        id_list = []
        for participant in distribution_list:
            participant_id = participant[11:]
            id_list.append(int(participant_id))

        # create recipients list with email addresses
        for item in id_list:
            participant = Participant.objects.get(pk=item, group=group)
            participant_email = participant.email
            recipients.append(participant_email)
   
    # retrieve the contents of the temporary PDF
    base_file_name = get_base_file_name(request, group, meeting, doc_type)
    base_pdf_path = get_pdf_path()
    temp_pdf = base_pdf_path + base_file_name + '.pdf'
    f = open(temp_pdf, 'r')
    pdf_contents = f.read()
    f.close()  

    # TODO delete the temporary pdf file to avoid clutter

    # save the pdf as the correct version number
    if doc_type == 'agenda':
        version = meeting.current_agenda_version
        if version:
            version += 1
        else:
            version = 1
        meeting.current_agenda_version = version
        meeting.save()
    elif doc_type == 'minutes':
        version = meeting.current_minutes_version
        if version:
            version += 1
        else:
            version = 1
        meeting.current_minutes_version = version
        meeting.save()
    pdf_name = base_pdf_path + base_file_name + '_v' + str(version) + '.pdf'
    pdf = ContentFile(pdf_contents)
    if doc_type == 'agenda':
        meeting.agenda_pdf.save(pdf_name, pdf, save=True)    
    elif doc_type == 'minutes':
        meeting.minutes_pdf.save(pdf_name, pdf, save=True)    

    # set up the email fields
    sender = 'eConvenor <noreply@econvenor.org>'
    if doc_type == 'agenda':
        subject = group_name + ' Meeting ' + meeting.meeting_no +\
                  ': Agenda for the meeting on ' + \
                  meeting.date_scheduled.strftime("%d %B %Y")
        body = 'The agenda for ' + group_name + ' Meeting ' + \
               meeting.meeting_no + ' scheduled for ' + \
               meeting.date_scheduled.strftime("%d %B %Y") + \
               ' is attached.\n\nThis email was sent by eConvenor' + \
               ' (beta version)'
    elif doc_type == 'minutes':
        subject = group_name + ' Meeting ' + meeting.meeting_no + \
                  ': Minutes of the meeting on ' + \
                  meeting.date_actual.strftime("%d %B %Y")
        body = 'The minutes of ' + group_name + ' Meeting ' + \
               meeting.meeting_no + ' held on ' + \
               meeting.date_scheduled.strftime("%d %B %Y") + \
               ' are attached.\n\nThis email was sent by eConvenor' + \
               ' (beta version)'

    # email the agenda
    email = EmailMessage(subject, body, sender, bcc=recipients)
    email.attach_file(pdf_name)
    email.send()

    #record the distribution of the document    
    distribution_record = find_or_create_distribution_record(group, meeting,
                                                             doc_type)
    if 'all_participants' in request.POST:
        id_list = []
        for participant in participants:
            id = participant.id
            id_list.append(id)                                                          
    distribution_record.distribution_list = str(id_list)
    distribution_record.save()
