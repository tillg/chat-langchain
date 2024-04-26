import os
import glob
import html2text


def html2markdown_file(html_file_path, markdown_file_path):
    with open(html_file_path, 'r') as html_file:
        html_content = html_file.read()

    markdown_content = html2text.html2text(html_content)

    with open(markdown_file_path, 'w') as markdown_file:
        markdown_file.write(markdown_content)


def html2markdown_dir(html_dir, markdown_dir):
    os.makedirs(markdown_dir, exist_ok=True)
    html_files = glob.glob(html_dir + '/*.html')

    for html_file in html_files:
        markdown_file = os.path.join(markdown_dir, os.path.splitext(
            os.path.basename(html_file))[0] + '.md')
        html2markdown_file(html_file, markdown_file)
