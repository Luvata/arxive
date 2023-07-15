import os
import xml.etree.ElementTree as ET
from html import escape


def xml_to_html(xml_file, output_dir):
    # Parse the XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Start building the HTML file content
    html = '<!DOCTYPE html>\n<html>\n<head>\n<title>{}</title>\n'.format(xml_file.split('.')[0])

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
    @media (max-width: 768px) {
        .container {
            width: 90%;
            font-size: 0.8em;
        }
        h1 {
            font-size: 1.4em;
        }
    }
    </style>
    </head>
    <body>
    <div class="container">
    '''
    
    namespaces = {
        'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
        'dc': 'http://purl.org/dc/elements/1.1/',
        'default': 'http://purl.org/rss/1.0/',
    } 

    for item in root.findall('default:item', namespaces):
        title = item.find('default:title', namespaces).text
        authors = item.find('dc:creator', namespaces).text
        abstract = item.find('default:description', namespaces).text.strip("<p>").strip(" </p>")
        link = item.find('default:link', namespaces).text

        html += '<div class="article">\n'
        html += '<h1><a href="{}">{}</a></h1>\n'.format(escape(link), escape(title))
        html += '<p><b>Authors:</b> {}</p>\n'.format(authors)
        html += '<p>{}</p>\n'.format(abstract)
        html += '</div>\n'

    html += '''
    </div>
    </body>
    '''

    # Save HTML file
    with open(os.path.join(output_dir, '{}.html'.format(xml_file.split('.')[0])), 'w') as f:
        f.write(html)

def parse_all_files(input_dir, output_dir):
    # Create the output directory if it does not exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Parse each XML file in the directory
    convert = 0
    skip = 0

    for file_name in os.listdir(input_dir):
        if file_name.endswith('.xml'):
            html_file = os.path.join(output_dir, '{}.html'.format(file_name.split('.')[0]))
            if not os.path.exists(html_file):
                xml_to_html(file_name, output_dir)
                convert += 1
            else:
                skip += 1
    print(f"Page build completed!, convert: {convert}, skip: {skip}")

# Call the function to parse all XML files in the current directory
parse_all_files('.', 'pages')
