from django.shortcuts import render_to_response
from django.template import RequestContext

from help.utils import convert_markdown_to_html
from utilities.commonutils import set_path
	
	
def user_guide(request):
	MARKDOWN_PATH = set_path('help/markdown/', '/home/econvenor/webapps/econvenor/econvenor/core/markdown/')
	page_content = convert_markdown_to_html(MARKDOWN_PATH + 'user_guide.mkd')
	return render_to_response('markdown_template.html', {'page_content': page_content}, RequestContext(request))


def faqs(request):
	MARKDOWN_PATH = set_path('help/markdown/', '/home/econvenor/webapps/econvenor/econvenor/core/markdown/')
	page_content = convert_markdown_to_html(MARKDOWN_PATH + 'faqs.mkd')
	return render_to_response('markdown_template.html', {'page_content': page_content}, RequestContext(request))
    

def ask_question(request):
	MARKDOWN_PATH = set_path('help/markdown/', '/home/econvenor/webapps/econvenor/econvenor/core/markdown/')
	page_content = convert_markdown_to_html(MARKDOWN_PATH + 'ask_question.mkd')
	return render_to_response('markdown_template.html', {'page_content': page_content}, RequestContext(request))
