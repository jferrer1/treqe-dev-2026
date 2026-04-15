import docx
import re

def convert_to_markdown_with_strikethrough(input_path, output_path):
    """Convert Word doc to Markdown, preserving strikethrough info."""
    doc = docx.Document(input_path)
    
    markdown_lines = []
    current_heading = "Documento"
    
    for i, para in enumerate(doc.paragraphs):
        text = para.text.strip()
        if not text:
            continue
        
        # Check for strikethrough
        has_strikethrough = False
        strikethrough_parts = []
        
        for run in para.runs:
            if run.font.strike:
                has_strikethrough = True
                strikethrough_parts.append(run.text)
        
        # Get style
        style = para.style.name
        
        # Update current heading
        if style.startswith('Heading'):
            current_heading = text
            level = int(style[-1]) if style[-1].isdigit() else 1
            markdown_lines.append(f'\n{"#" * level} {text}')
        else:
            # Regular paragraph with possible strikethrough
            if has_strikethrough:
                # Mark as