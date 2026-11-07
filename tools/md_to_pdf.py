import os
import sys
import subprocess
import tempfile
import markdown

EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if not os.path.exists(EDGE_PATH):
    EDGE_PATH = r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"

HTML_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>{title}</title>
<style>
@page {{
    size: A4;
    margin: 18mm 15mm 18mm 15mm;
    @bottom-center {{
        content: counter(page);
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        font-size: 9pt;
        color: #8c959f;
    }}
}}
body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    font-size: 10pt;
    line-height: 1.55;
    color: #24292f;
    background-color: #ffffff;
    margin: 0;
    padding: 0;
}}
h1, h2, h3, h4, h5, h6 {{
    color: #1f2328;
    margin-top: 1.4em;
    margin-bottom: 0.5em;
    font-weight: 600;
    page-break-after: avoid;
}}
h1 {{
    font-size: 19pt;
    border-bottom: 2px solid #d0d7de;
    padding-bottom: 0.3em;
    margin-top: 0.4em;
}}
h2 {{
    font-size: 14pt;
    border-bottom: 1px solid #d0d7de;
    padding-bottom: 0.25em;
}}
h3 {{ font-size: 12pt; }}
h4 {{ font-size: 10.5pt; }}

p, ul, ol {{
    margin-top: 0.4em;
    margin-bottom: 0.7em;
}}
li {{
    margin-top: 0.2em;
    margin-bottom: 0.2em;
}}

table {{
    border-collapse: collapse;
    width: 100%;
    margin: 1.1em 0;
    font-size: 9pt;
    page-break-inside: avoid;
}}
th, td {{
    border: 1px solid #d0d7de;
    padding: 6px 9px;
    text-align: left;
    vertical-align: top;
}}
th {{
    background-color: #f6f8fa;
    font-weight: 600;
    color: #1f2328;
}}
tr:nth-child(even) {{
    background-color: #fcfcfc;
}}

blockquote {{
    margin: 0.9em 0;
    padding: 0.5em 0.9em;
    color: #57606a;
    background-color: #f6f8fa;
    border-left: 0.3em solid #0969da;
    border-radius: 0 4px 4px 0;
    page-break-inside: avoid;
}}
blockquote p {{
    margin: 0.25em 0;
}}

code {{
    font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, "Liberation Mono", monospace;
    background-color: rgba(175, 184, 193, 0.2);
    padding: 0.18em 0.35em;
    border-radius: 4px;
    font-size: 85%;
}}
pre code {{
    background-color: transparent;
    padding: 0;
    border-radius: 0;
}}
pre {{
    background-color: #f6f8fa;
    border: 1px solid #d0d7de;
    border-radius: 6px;
    padding: 10px 12px;
    overflow-x: auto;
    font-size: 8pt;
    line-height: 1.4;
    page-break-inside: avoid;
}}

hr {{
    height: 1px;
    background-color: #d0d7de;
    border: none;
    margin: 1.4em 0;
}}

a {{
    color: #0969da;
    text-decoration: none;
}}
img {{
    max-width: 100%;
}}
</style>
</head>
<body>
{body}
</body>
</html>
"""

def convert_html_to_pdf(html_path, pdf_path):
    html_path = os.path.abspath(html_path)
    pdf_path = os.path.abspath(pdf_path)
    cmd = [
        EDGE_PATH,
        "--headless",
        "--disable-gpu",
        "--no-pdf-header-footer",
        "--run-all-compositor-stages-before-draw",
        f"--print-to-pdf={pdf_path}",
        html_path
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0 or not os.path.exists(pdf_path):
        raise RuntimeError(f"Edge headless failed for {html_path}: {res.stderr}")
    return pdf_path

def convert_md_to_pdf(md_path, pdf_path=None):
    md_path = os.path.abspath(md_path)
    if not os.path.exists(md_path):
        raise FileNotFoundError(f"Markdown file not found: {md_path}")
        
    if pdf_path is None:
        pdf_path = os.path.splitext(md_path)[0] + ".pdf"
    pdf_path = os.path.abspath(pdf_path)

    with open(md_path, "r", encoding="utf-8", errors="ignore") as f:
        md_text = f.read()

    title = os.path.basename(md_path)
    for line in md_text.splitlines():
        if line.startswith("# "):
            title = line[2:].strip()
            break

    body_html = markdown.markdown(
        md_text,
        extensions=["tables", "fenced_code", "toc"]
    )

    full_html = HTML_TEMPLATE.format(title=title, body=body_html)

    temp_fd, temp_html = tempfile.mkstemp(suffix=".html", prefix="md_render_")
    os.close(temp_fd)
    
    try:
        with open(temp_html, "w", encoding="utf-8") as f:
            f.write(full_html)
        convert_html_to_pdf(temp_html, pdf_path)
        size = os.path.getsize(pdf_path)
        print(f"[OK] {os.path.basename(md_path)} -> {os.path.basename(pdf_path)} ({size:,} bytes)")
        return pdf_path
    finally:
        if os.path.exists(temp_html):
            os.remove(temp_html)

def batch_convert_folder(folder_path):
    folder_path = os.path.abspath(folder_path)
    print(f"Batch converting markdown to PDF in: {folder_path}...")
    count = 0
    for root, dirs, files in os.walk(folder_path):
        # Skip pycache and hidden
        dirs[:] = [d for d in dirs if d not in ['__pycache__', '.pytest_cache', '.git']]
        for f in files:
            if f.endswith('.md'):
                md_file = os.path.join(root, f)
                pdf_file = os.path.splitext(md_file)[0] + ".pdf"
                convert_md_to_pdf(md_file, pdf_file)
                count += 1
            elif f.endswith('.html') and 'agreement' in f:
                html_file = os.path.join(root, f)
                pdf_file = os.path.splitext(html_file)[0] + ".pdf"
                convert_html_to_pdf(html_file, pdf_file)
                count += 1
    print(f"Batch conversion completed: {count} PDFs generated.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            if os.path.isdir(arg):
                batch_convert_folder(arg)
            else:
                convert_md_to_pdf(arg)
    else:
        print("Usage: python md_to_pdf.py <file1.md|folder> ...")
