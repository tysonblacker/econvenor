import socket
import os

from io import BytesIO
from string import replace
from subprocess import call

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.utils.text import slugify

from reportlab.lib.colors import black, CMYKColor, white
from reportlab.lib.enums import TA_JUSTIFY, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase.pdfmetrics import registerFont, registerFontFamily
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, \
                               PageBreak, Paragraph, Spacer, Table, TableStyle 

import reportlab.rl_config

from accounts.models import Group
from decisions.models import Decision
from docs.utils import calculate_meeting_duration, \
                       calculate_meeting_end_time, \
                       get_completed_tasks_list
from meetings.models import Meeting
from participants.models import Participant
from tasks.models import Task
from utilities.commonutils import set_path


# Define colors
heading_color = CMYKColor(0.3,0,0.15,0.6)	
body_color = CMYKColor(0,0,0,0.85)
table_color = CMYKColor(0.3,0,0.15,0.6)
shading_color = CMYKColor(0.1,0,0.05,0.2)

# Define line width
line_width = 0.75

# Set path to fonts
FONT_PATH = os.path.join(settings.BASE_DIR, 'commonstatic/fonts/')

# Register fonts
body_font = 'OpenSans'
heading_font = 'OpenSans'
registerFont(TTFont(body_font, FONT_PATH + body_font + "-Regular.ttf"))
registerFont(TTFont(body_font + 'Bd', FONT_PATH + body_font + "-Bold.ttf"))
registerFont(TTFont(body_font + 'It', FONT_PATH + body_font + "-Italic.ttf"))
registerFont(TTFont(body_font + 'BI', 
                    FONT_PATH + body_font + "-BoldItalic.ttf"))
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
styles.add(ParagraphStyle(
           name='Item',
           parent=styles['Normal'],
           fontName = body_font,
           spaceBefore=2,
           spaceAfter=2,
           textColor = white
           ))
itemStyle = styles['Item']

# Define 'rightitem' text style
styles.add(ParagraphStyle(
           name='RightItem',
           parent=styles['Item'],
           alignment = TA_RIGHT
           ))
rightItemStyle = styles['RightItem']

# Define 'shadeditem' text style
styles.add(ParagraphStyle(
           name='ShadedItem',
           parent=styles['Item'],
           textColor = heading_color
           ))
shadedItemStyle = styles['ShadedItem']

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
MEETING_COLUMN_STYLE = TableStyle([
    ('GRID', (0,0), (-1,-1), line_width, table_color),
    ('VALIGN',(0,0),(-1,-1),'TOP'),
    ('BACKGROUND', (0,0), (-0,-1), shading_color),
    ])

MEETING_TABLE_STYLE = TableStyle([
    ('VALIGN',(0,0),(-1,-1),'TOP'),
    ('LEFTPADDING', (0,0), (-1,-1), 0),
    ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ('TOPPADDING', (0,0), (-1,-1), 0),
    ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [white, shading_color]),
    ])

TASK_TABLE_STYLE = TableStyle([
    ('GRID', (0,0), (2,-1), line_width, table_color),
    ('VALIGN',(0,0),(-1,-1),'TOP'),
    ('BACKGROUND', (0,0), (-1,0), table_color),
    ('BACKGROUND', (0,1), (-1,1), shading_color),
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
    ('TOPPADDING', (0,0), (-1,-1), 3),
    ('BACKGROUND', (0,0), (-1,0), shading_color),
    ('GRID', (0,0), (-1,0), line_width, table_color),
    ])

ITEM_EXPLAINER_TABLE_STYLE = TableStyle([
    ('GRID', (0,0), (1,-1), line_width, table_color),
    ('VALIGN',(0,0),(-1,-1),'TOP'),
    ('BACKGROUND', (0,0), (-1,0), table_color),
    ('BACKGROUND', (0,1), (-1,1), shading_color),
    ('LEFTPADDING', (0,0), (-1,0), 0),
    ('TOPPADDING', (0,0), (-1,0), 0),
    ('BOTTOMPADDING', (0,0), (-1,0), 0),
    ])
    
ITEM_EXPLAINER_AND_BACKGROUND_TABLE_STYLE = TableStyle([
    ('GRID', (0,0), (1,-1), line_width, table_color),
    ('VALIGN',(0,0),(-1,-1),'TOP'),
    ('BACKGROUND', (0,0), (-1,0), table_color),
    ('LEFTPADDING', (0,0), (-1,-1), 0),
    ('TOPPADDING', (0,0), (-1,0), 0),
    ('TOPPADDING', (0,1), (-1,-1), 0),
    ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ])

MINUTES_ITEMS_TABLE_STYLE = TableStyle([
    ('GRID', (0,0), (1,-1), line_width, table_color),
    ('VALIGN',(0,0),(-1,-1),'TOP'),
    ('BACKGROUND', (0,0), (-1,0), table_color),
    ('LEFTPADDING', (0,0), (-1,-1), 0),
    ('TOPPADDING', (0,0), (-1,0), 0),
    ('BOTTOMPADDING', (0,0), (-1,0), 0),
    ('TOPPADDING', (0,1), (-1,1), 6),
    ('BOTTOMPADDING', (0,1), (-1,1), 6),
    ('TOPPADDING', (0,2), (-1,-1), 0),
    ('BOTTOMPADDING', (0,2), (-1,-1), 0),
    ])

MINUTES_ITEMS_SUBTABLE_STYLE = TableStyle([
    ('GRID', (0,0), (-1,-1), line_width, table_color),
    ('VALIGN',(0,0),(-1,-1),'TOP'),
    ('BACKGROUND', (0,0), (-1,0), shading_color),
    ])
    
NEXT_MEETING_TABLE_STYLE = TableStyle([
    ('GRID', (0,0), (-1,-1), line_width, table_color),
    ('VALIGN',(0,0),(-1,-1),'TOP'),
    ('BACKGROUND', (0,0), (-1,0), table_color),
    ('LEFTPADDING', (0,0), (-1,-1), 0),
    ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ('TOPPADDING', (0,0), (-1,-1), 0),
    ('BOTTOMPADDING', (0,0), (-1,-1), 0),])    
    
def insert_line_breaks(string_data):
    """
    Replaces line break characters in strings with <br> tags.
    """
    formatted_string = replace(string_data, '\n', '<br/>')
    return formatted_string


def footer(canvas, doc):
    """
    Creates the footer for each page of the PDF.
    """
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
    Document.append(Spacer(0,7*mm))    


def create_details_table(meeting, doc_type, Document):
    """
    Creates the meeting details table.
    """
    if doc_type == 'agenda':
        date = meeting.date_scheduled
        duration = calculate_meeting_duration(meeting)
        start_time = meeting.start_time_scheduled
        end_time = calculate_meeting_end_time(meeting)
        location = insert_line_breaks(meeting.location_scheduled)
        notes = insert_line_breaks(meeting.instructions_scheduled)
    if doc_type == 'minutes':
        date = meeting.date_actual
        start_time = meeting.start_time_actual
        end_time = meeting.end_time_actual
        location = insert_line_breaks(meeting.location_actual)
        notes = insert_line_breaks(meeting.instructions_actual)
        facilitator = str(meeting.facilitator_actual)
        minute_taker = str(meeting.minute_taker_actual)
        attendance = meeting.attendance               
        apologies = meeting.apologies        
    # Set up the right hand column
    right_column_contents = []
    if doc_type == 'agenda':
        right_column_contents.append(
            (Paragraph('Location', shadedItemStyle),
                Paragraph(location, normalStyle)))
    if doc_type == 'minutes':
        right_column_contents.append(
            (Paragraph('Facilitator', shadedItemStyle),
                Paragraph(facilitator, normalStyle)))
        right_column_contents.append(
            (Paragraph('Minutes', shadedItemStyle),
                Paragraph(minute_taker, normalStyle)))
        right_column_contents.append(
            (Paragraph('Attendance', shadedItemStyle),
                Paragraph(attendance, normalStyle)))
        if apologies:
            right_column_contents.append(
                (Paragraph('Apologies', shadedItemStyle),
                   Paragraph(apologies, normalStyle)))
    if notes:
        right_column_contents.append((Paragraph('Notes', shadedItemStyle),
                                     Paragraph(notes, normalStyle)))   
    right_column = Table(right_column_contents, colWidths=[25*mm,52.5*mm])
    right_column.setStyle(MEETING_COLUMN_STYLE)
    # Set up the middle column to seperate the left and right columns
    middle_column = Table([
            ('',), ('',),
            ],
        colWidths=[5*mm])
    # Set up the left hand column
    left_column_contents = [
        (Paragraph('Meeting', shadedItemStyle),
            Paragraph(meeting.meeting_no, normalStyle)),
        (Paragraph('Date', shadedItemStyle),
            Paragraph(date.strftime("%A %B %d, %Y"), normalStyle)),
        (Paragraph('Start time', shadedItemStyle),
            Paragraph(start_time.strftime("%H:%M"), normalStyle)),]     
    if doc_type == 'agenda':
        if duration != 0:
            left_column_contents.append(        
            (Paragraph('End time', shadedItemStyle),
                Paragraph(end_time.strftime("%H:%M"), normalStyle)))
    if doc_type == 'minutes':
        left_column_contents.append(        
            (Paragraph('End time', shadedItemStyle),
             Paragraph(end_time.strftime("%H:%M"), normalStyle)))
        left_column_contents.append(        
            (Paragraph('Location', shadedItemStyle),
             Paragraph(location, normalStyle)))
             
    left_column = Table(left_column_contents, colWidths=[25*mm,52.5*mm])
    left_column.setStyle(MEETING_COLUMN_STYLE)
    t = Table([((
           left_column,
           middle_column,
           right_column
           ))],)
    t.setStyle(MEETING_TABLE_STYLE)
    Document.append(t)
    Document.append(Spacer(0,10*mm))


def create_agenda_item_table(items, Document):
    """
    Creates the agenda items tables.
    """
    for item in items:
        if item.background:
            background = insert_line_breaks(item.background)
        if item.time_limit:
            time_limit_content = Paragraph(str(item.time_limit) + ' minutes',
                                           rightItemStyle)
        else: 
            time_limit_content = ''
        
        heading_t = Table([((
                Paragraph('Item ' + str(item.item_no) + ':&nbsp;&nbsp;' + \
                          item.title, itemStyle),
                time_limit_content,
                ))],
            colWidths=[135*mm,25*mm]
            )
        heading_t.setStyle(TableStyle([(
                'ALIGN',(-1,0),(-1,0),'RIGHT'
                )])
            )
        if item.explainer and item.background:
            body_t = Table([
                    (Paragraph('To be introduced by ' + \
                          str(item.explainer), shadedItemStyle),),
                    (Paragraph(background, normalStyle),)
                    ],
                colWidths=[160*mm])
            body_t.setStyle(ITEM_INNER_TABLE_STYLE)
            t = Table([
                    (heading_t,),
                    (body_t,)
                    ],
                colWidths=[160*mm])
            t.setStyle(ITEM_EXPLAINER_AND_BACKGROUND_TABLE_STYLE)
        elif item.explainer and (item.background == ''):
            t = Table([(heading_t,),
                       (Paragraph('To be introduced by ' + str(item.explainer),
                           shadedItemStyle),)
                      ],
                  colWidths=[160*mm])
            t.setStyle(ITEM_EXPLAINER_TABLE_STYLE)
        else:				
            if (item.explainer == None) and item.background:
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
        Document.append(Spacer(0,7*mm))
    
    Document.append(Paragraph('A summary of tasks for review',
                              shadedItemStyle))
    Document.append(Paragraph('is on the next page.', shadedItemStyle))
    Document.append(PageBreak())




def create_minutes_item_table(items, group, Document):
    """
    Creates the minutes items tables.
    """
    for item in items:
        minute_notes = insert_line_breaks(item.minute_notes)
        # Set up the heading row as a sub-table   
        heading_t = Table([((
                Paragraph('Item ' + str(item.item_no) + ':&nbsp;&nbsp;' + \
                          item.title, itemStyle),
                ))],
            colWidths=[160*mm]
            )
        # Set up the minute notes as a sub-table
        
        notes_t = Table([
                    (Paragraph(minute_notes, normalStyle),),
                    ],
                colWidths=[160*mm])
        # Set up decisions as a sub-table
        decisions_list = Decision.objects.filter(group=group, item=item)
        if decisions_list:
            decisions_heading = (
                Paragraph('Decisions', shadedItemStyle),
                )
            decisions = [(
                Paragraph(decision.description, normalStyle),
                )
                for decision in decisions_list]
            decisions_t = Table([decisions_heading] + decisions,
                            colWidths=[160*mm])
            decisions_t.setStyle(MINUTES_ITEMS_SUBTABLE_STYLE)
        # Set up tasks as a sub-table
        tasks_list = Task.objects.filter(group=group, item=item)
        if tasks_list:
            column_headings = (
                Paragraph('Task', shadedItemStyle),
                Paragraph('Assigned to', shadedItemStyle),
                Paragraph('Deadline', shadedItemStyle)
                )
            tasks = [(
                Paragraph(task.description, normalStyle),
                Paragraph(str(task.participant), normalStyle),
                Paragraph(task.deadline.strftime("%d %b %Y"), normalStyle)
                )
                for task in tasks_list]
            tasks_t = Table([column_headings] + tasks,
                            colWidths=[90*mm,40*mm,30*mm])
            tasks_t.setStyle(MINUTES_ITEMS_SUBTABLE_STYLE) 
        # Generate the complete table
        table_contents = [[(heading_t,)], [(notes_t,)]]
        if decisions_list:
            table_contents.append([(decisions_t,)])        
        if tasks_list:
            table_contents.append([(tasks_t,)])
        t = Table(table_contents, colWidths=[160*mm])
        t.setStyle(MINUTES_ITEMS_TABLE_STYLE)
        # Add this table to the document and put some space after it
        Document.append(t)
        Document.append(Spacer(0,7*mm))


def create_task_table(section_heading, task_list, task_type, Document):
    """
    Creates the tasks tables.
    """
    if task_type == 'overdue':
        empty_message = 'There are no overdue tasks.'
        time_column_heading = 'Deadline'
    elif task_type == 'incomplete':
        empty_message = 'There are no tasks to be completed.'
        time_column_heading = 'Deadline'
    elif task_type == 'completed':
        empty_message = 'No tasks have been completed since last meeting.'
        time_column_heading = 'Completed'    
    if task_type == 'new':
        empty_message = 'No tasks were assigned in this meeting.'
        time_column_heading = 'Deadline'
            
    table_heading = (Paragraph(section_heading, itemStyle), '', '')
    column_headings = (
        Paragraph('Description', shadedItemStyle),
        Paragraph('Assigned to', shadedItemStyle),
        Paragraph(time_column_heading, shadedItemStyle)
        )
    tasks = [(
        Paragraph(task.description, normalStyle),
        Paragraph(str(task.participant), normalStyle),
        Paragraph(task.deadline.strftime("%d %b %Y"), normalStyle)
        )
        for task in task_list]
    
    if task_list:
        t = Table([table_heading] + [column_headings] + tasks,
                  colWidths=[90*mm,40*mm,30*mm])
    else:
        t = Table([table_heading] + [column_headings] + \
                  [(Paragraph(empty_message, 
                    normalStyle),'','')],
              colWidths=[90*mm,40*mm,30*mm]
              )
    t.setStyle(TASK_TABLE_STYLE)
    Document.append(t)
    Document.append(Spacer(0,5*mm))


def create_next_meeting_table(meeting, Document):
    """
    Creates a table in minutes for details of the next meeting.
    """
    date = meeting.next_meeting_date
    start_time = meeting.next_meeting_start_time
    location = insert_line_breaks(meeting.next_meeting_location)
    facilitator = str(meeting.next_meeting_facilitator)
    minute_taker = str(meeting.next_meeting_minute_taker)
    notes = insert_line_breaks(meeting.next_meeting_instructions)
    # Set up the heading row as a sub-table   
    heading_t = Table([((
                Paragraph('Details of next meeting', itemStyle),
                ))],
            colWidths=[160*mm]
            )    
    # Set up the contents rows
    contents = []
    if date:
        contents.append(
            (Paragraph('Date', shadedItemStyle),
                Paragraph(date.strftime("%A %B %d, %Y"), normalStyle)))
    if start_time:
        contents.append(
            (Paragraph('Start time', shadedItemStyle),
             Paragraph(start_time.strftime("%H:%M"), normalStyle)))  
    if location:
        contents.append(
            (Paragraph('Location', shadedItemStyle),
             Paragraph(location, normalStyle)))
    if facilitator:
       contents.append(
            (Paragraph('Facilitator', shadedItemStyle),
             Paragraph(facilitator, normalStyle)))
    if minute_taker:
        contents.append(
            (Paragraph('Minutes', shadedItemStyle),
             Paragraph(minute_taker, normalStyle)))
    if notes:
        contents.append(
            (Paragraph('Notes', shadedItemStyle),
                Paragraph(notes, normalStyle)))
    # Set up the body sub-table                                  
    body_t = Table(contents, colWidths=[25*mm,55*mm])
    body_t.setStyle(MEETING_COLUMN_STYLE)
    # Set up the whole table
    table_contents = [[(heading_t,)], [(body_t,)]]
    t = Table(table_contents, colWidths=[80*mm])
    t.setStyle(NEXT_MEETING_TABLE_STYLE)
    t.hAlign = 'LEFT'
    Document.append(t)
    Document.append(Spacer(0,5*mm))
    Document.append(Paragraph('A summary of tasks assigned in this meeting',
                              shadedItemStyle))
    Document.append(Paragraph('is on the next page.', shadedItemStyle))
    Document.append(PageBreak())


def create_pdf(request, group, meeting, doc_type):
    """
    Constructs the PDF document.
    """
    # Set up the document framework
    group_name = group.name
    buffer = BytesIO()
    doc = BaseDocTemplate(buffer,
        rightMargin=25*mm,
        leftMargin=25*mm,
        topMargin=20*mm,
        bottomMargin=25*mm,
        title = group_name + "  |  Meeting " +
            meeting.meeting_no,
        pagesize=A4,
        allowSplitting = 0,)
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
    
    # Add task review to agenda
    if doc_type == 'agenda':
        overdue_tasks_list = Task.lists.overdue_tasks().filter(group=group)
        incomplete_tasks_list = Task.lists.incomplete_tasks().\
                                filter(group=group)
        completed_tasks_list = get_completed_tasks_list(group)
        create_task_table(
            'Attachment 1:  Overdue tasks',
            overdue_tasks_list, 'overdue', Document)
        create_task_table(
            'Attachment 2:  Tasks to be completed',
            incomplete_tasks_list, 'incomplete', Document)
        create_task_table(
            'Attachment 3:  Tasks completed since last meeting',
            completed_tasks_list, 'completed', Document)

    # Add next meeting table to minutes
    if doc_type == 'minutes':
        create_next_meeting_table(meeting, Document)

    # Add new task summary to minutes
    if doc_type == 'minutes':
        new_tasks_list = Task.lists.by_participant().filter(group=group,
                                                            meeting=meeting)
        create_task_table(
            'Summary of tasks assigned in this meeting',
            new_tasks_list, 'new', Document)
       
    # Build the PDF
    doc.build(Document)

    # Get the PDF
    pdf = buffer.getvalue()
    buffer.close()

    # Define locations to save files to
    pdf_path = get_pdf_path()
    preview_path = os.path.join(settings.MEDIA_ROOT, 'tmp/')
    if not os.path.exists(preview_path):
        os.makedirs(preview_path)

    # Define name of PDF file
    base_file_name = get_base_file_name(request, group, meeting) 
    pdf_name = base_file_name + '.pdf'

    # Delete any old PDF versions for this meeting
    path_to_old_pdf = pdf_path + pdf_name
    path_to_old_previews = preview_path + base_file_name + '*'	

    call('rm ' + path_to_old_pdf , shell=True)
    call('rm ' + path_to_old_previews , shell=True)	

    # Save the PDF
    pdf_file = ContentFile(pdf)
    meeting.agenda_pdf.save(pdf_name, pdf_file, save=True)

    # Create and save the images
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


def get_base_file_name(request, group, meeting):
    """
    Returns the base file name with no suffix.
    """
    cleaned_meeting_no = meeting.meeting_no.replace('/', '-')
    cleaned_meeting_no = cleaned_meeting_no.replace('_', '-')
    meeting_no_slug = slugify(cleaned_meeting_no)
    base_file_name = str(group.id) + '_' + group.slug + '_agenda_' + \
                     meeting_no_slug
    return base_file_name


def get_pdf_path():
    """
    Returns the location that the document will be saved to.
    """
    pdf_path = os.path.join(settings.MEDIA_ROOT, 'meeting_docs/')
    return pdf_path

def get_pdf_contents(request, group, meeting):
    """
    Returns the contents of the PDF document.
    """
    pdf_name = get_base_file_name(request, group, meeting) + '.pdf'
    pdf_path = get_pdf_path()
    pdf_location = pdf_path + pdf_name

    f = open(pdf_location, 'r')
    pdf_contents = f.read()
    f.close()

    return pdf_contents


def distribute_agenda(request, group, meeting):
    """
    Emails out the agenda.
    """  	
    recipients = []
    group_name = group.name

    # build recipients list if "all_participants" box is checked
    if 'all_participants' in request.POST:
        participants = Participant.objects.filter(group=group)
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
            id_list.append(participant_id)

        # create recipients list with email addresses
        for item in id_list:
            participant = Participant.objects.get(pk=int(item), group=group)
            participant_email = participant.email
            recipients.append(participant_email)

    # set up the email fields
    base_file_name = get_base_file_name(request, group, meeting)
    base_pdf_path = get_pdf_path()
    pdf_path = base_pdf_path + base_file_name + '.pdf'	
    subject = group_name + ': You agenda is attached'
    body = 'Here is your agenda'
    sender = 'noreply@econvenor.org'

    # email the agenda
    email = EmailMessage(subject, body, sender, recipients)
    email.attach_file(pdf_path)
    email.send()
