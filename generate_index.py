import os
import html
from collections import defaultdict

def generate_html():
    path = 'pages'
    files = sorted(os.listdir(path))

    # Define the CSS style
    style = """
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
    table {
        width: 100%;
        border-collapse: collapse;
        border: 1px solid #ddd;
    }
    th, td {
        padding: 15px;
        text-align: left;
        border-bottom: 1px solid #ddd;
    }
    th {
        background-color: #f5f5f5;
        font-weight: bold;
    }
    td {
        vertical-align: middle;
    }
    .category-list {
        white-space: nowrap;
    }
    .category-list a {
        margin-right: 5px;
        color: #007BFF;
        text-decoration: none;
    }
    .category-list a:hover {
        color: #0056b3;
    }
    </style>
    """

    # Initialize HTML content
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        {style}
    </head>
    <body>
    <div class="container">
        <h1>Index</h1>
        <table>
            <tr>
                <th>Date</th>
                <th>Category</th>
            </tr>
    """

    # Create a dictionary to group categories by date
    category_dict = defaultdict(list)

    for file in files:
        if file.endswith('.html') and "index" not in file:
            # Extract date and category from filename
            filename_parts = file.split('.')[0].split('-')
            date = '-'.join(filename_parts[:3])
            category = f"<a href={file}> {filename_parts[4]} </a>"

            # Append the category to the list of categories for the date
            category_dict[date].append(category)

    # Create HTML rows for each date and its categories
    for date, categories in category_dict.items():
        # Convert categories to HTML links
        category_string = ", ".join(categories)
        # Create a row in the HTML table for the date and its categories
        html_content += f"""
        <tr>
            <td>{html.escape(date)}</td>
            <td>{category_string}</td>
        </tr>
        """

    # Close HTML content
    html_content += """
        </table>
    </div>
    </body>
    </html>
    """

    # Write HTML content to a file
    with open(os.path.join(path, 'index.html'), 'w') as f:
        f.write(html_content)

# Call the function to generate HTML
generate_html()

