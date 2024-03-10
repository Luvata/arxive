import os
import xml.etree.ElementTree as ET
from html import escape
from datetime import datetime
import re

def xml_to_html(xml_file, output_dir):
    # Parse the XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Start building the HTML file content
    pub_date = root.find('channel/pubDate').text
    pub_date_obj = datetime.strptime(pub_date, '%a, %d %b %Y %H:%M:%S %z')
    pub_date_formatted = pub_date_obj.strftime('%Y-%m-%d')
    file_title = "-".join(root.find("channel/title").text.split(" ")[0].lower().split("."))
    file_title = pub_date_formatted + "-" + file_title
    print(xml_file, ">>>>>", file_title)

    html = f"<!DOCTYPE html>\n<html>\n<head>\n<title>{file_title}</title>\n"
    html += '''
    <style>
    body {
        font-family: Arial, sans-serif;
        margin: 0;
        padding: 0;
        display: flex;
        justify-content: center;
        background-color: #f2f2f2;
    }
    .container {
        width: 60%;
        max-width: 900px;
        min-width: 300px;
        background-color: #fff;
        padding: 20px;
        margin: 20px;
        border-radius: 10px;
        box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.05);
        font-size: 0.9em;
    }
    @media (max-width: 768px) {
        .container {
            width: 90%;
            font-size: 0.8em;
        }
        h1 {
            font-size: 1.4em;
        }
    h1 {
        color: #333;
        font-size: 1.6em;
    }
    .article {
        border-bottom: 1px solid #ddd;
        padding: 10px 0;
    }
    .article a {
        color: #007BFF;
        text-decoration: none;
    }
    .article a:hover {
        color: #0056b3;
    }
    .copy-button {
        background-color: #007BFF;
        color: #fff;
        border: none;
        padding: 5px 10px;
        cursor: pointer;
        margin-top: 10px;
    }
    .copy-button:active {
        background-color: #0056b3;
    }
    .copy-message {
        display: none;
        background-color: #4CAF50;
        color: #fff;
        padding: 5px;
        margin-top: 10px;
        border-radius: 3px;
    }
    </style>
    <script>
    function copyToClipboard(text, buttonId) {
        const el = document.createElement('textarea');
        el.value = text;
        document.body.appendChild(el);
        el.select();
        document.execCommand('copy');
        document.body.removeChild(el);
        
        const messageElement = document.getElementById('copy-message-' + buttonId);
        messageElement.innerHTML = 'Copied "' + text + '" to clipboard';
        messageElement.style.display = 'block';
        setTimeout(function() {
            messageElement.style.display = 'none';
        }, 3000);
    }
    </script>
    </head>
    <body>
    <div class="container">
    '''

    namespaces = {
        'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
        'dc': 'http://purl.org/dc/elements/1.1/',
        'default': 'http://purl.org/rss/1.0/',
    }

    items = root[0].findall('item')
    if not items:
        html += '<p>No articles found for this date.</p>\n'
    else:
        button_id = 0
        for item in items:
            title = item.find('title').text
            authors = item.find('dc:creator', namespaces).text if item.find('dc:creator', namespaces) is not None else ''
            abstract = item.find('description').text
            info = abstract.split("\n")[0]
            abstract = "\n".join(abstract.split("\n")[1:])
            link = item.find('link').text

            # Extract URLs from the abstract
            urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', abstract)
            url_links = ', '.join(f'<a href="{url}">{url}</a>' for url in urls)

            html += '<div class="article">\n'
            html += '<h1><a href="{}">{}</a></h1>\n'.format(escape(link), escape(title))
            html += '<p><b>Authors:</b> {}</p>\n'.format(authors)
            html += '<p>{}</p>\n'.format(abstract)
            if url_links:
                html += f'<p>URLs: {url_links}</p>\n'
            html += f'<button class="copy-button" onclick="copyToClipboard(\'{link}{", " + ", ".join(urls) if urls else ""}\', {button_id})">'
            html += 'Copy Link</button>\n'
            html += f'<div id="copy-message-{button_id}" class="copy-message"></div>\n'
            html += '</div>\n'
            button_id += 1

    html += '''
    </div>
    </body>
    '''

    # Save HTML file
    with open(os.path.join(output_dir, f"{file_title}.html"), "w") as f:
        f.write(html)

def parse_all_files(input_dir, output_dir):
    # Create the output directory if it does not exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Parse each XML file in the directory
    convert = 0
    skip = 0
    for file_name in sorted(os.listdir(input_dir)):
        file_path = os.path.join(input_dir, file_name)
        if file_name.endswith('.xml'):
            html_file = os.path.join(output_dir, '{}.html'.format(file_name.split('.')[0]))
            if not os.path.exists(html_file):
                xml_to_html(file_path, output_dir)
                convert += 1
            else:
                skip += 1
    print(f"Page build completed!, convert: {convert}, skip: {skip}")

# Call the function to parse all XML files in the current directory
parse_all_files('xml', 'pages')