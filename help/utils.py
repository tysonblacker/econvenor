import markdown


def convert_markdown_to_html(mkd_file):
	f = open(mkd_file, "r")
	mkd_content = f.read()
	html_content = markdown.markdown(mkd_content)
	f.close()
	return html_content

