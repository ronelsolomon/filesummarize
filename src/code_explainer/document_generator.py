"""
Document generation module for creating Word documents from code analysis.
"""
from typing import List, Dict, Any, Optional
from io import BytesIO

try:
    from docx import Document
    from docx.shared import Pt
    from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False

def create_document(code_elements: List[Dict[str, Any]], explanation: str, 
                   title: str = "Python Code Analysis") -> Optional[BytesIO]:
    """
    Create a Word document from code analysis and explanation.
    
    Args:
        code_elements: List of code element dictionaries, each can include 'file' key
        explanation: Generated explanation text
        title: Title for the document
        
    Returns:
        BytesIO buffer containing the document, or None if docx is not available
    """
    if not DOCX_AVAILABLE:
        return None
        
    def _get_or_create_code_style(doc):
        """Get the Code style or create it if it doesn't exist."""
        try:
            return doc.styles['Code']
        except KeyError:
            code_style = doc.styles.add_style('Code', 1)  # 1 = WD_STYLE_TYPE.PARAGRAPH
            code_style.font.name = 'Courier New'
            code_style.font.size = Pt(10)
            code_style.paragraph_format.space_after = Pt(6)
            return code_style
        
    try:
        doc = Document()
        
        # Add title
        title_para = doc.add_heading(level=0)
        title_run = title_para.add_run(title)
        title_run.bold = True
        title_para.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        
        # Ensure we have the Code style
        _get_or_create_code_style(doc)
        
        # Add summary section
        doc.add_heading("Summary", level=1)
        
        # Count elements by type and file
        elements_by_file = {}
        elements_by_type = {}
        
        for el in code_elements:
            file_name = el.get('file', 'unknown.py')
            el_type = el.get('type', 'Unknown')
            
            # Count by file
            if file_name not in elements_by_file:
                elements_by_file[file_name] = {'functions': 0, 'classes': 0, 'async_functions': 0}
            
            if el_type == 'Function':
                elements_by_file[file_name]['functions'] += 1
            elif el_type == 'AsyncFunction':
                elements_by_file[file_name]['async_functions'] += 1
            elif el_type == 'Class':
                elements_by_file[file_name]['classes'] += 1
            
            # Count by type
            if el_type not in elements_by_type:
                elements_by_type[el_type] = 0
            elements_by_type[el_type] += 1
        
        # Add summary table
        if elements_by_file:
            doc.add_heading("Files Analyzed", level=2)
            for file, counts in elements_by_file.items():
                parts = []
                if counts['classes']:
                    parts.append(f"{counts['classes']} classes")
                if counts['functions']:
                    parts.append(f"{counts['functions']} functions")
                if counts['async_functions']:
                    parts.append(f"{counts['async_functions']} async functions")
                doc.add_paragraph(f"• {file}: {', '.join(parts) if parts else 'No elements found'}")
        
        # Add element type summary
        if elements_by_type:
            doc.add_paragraph(f"Total elements found: {sum(elements_by_type.values())}")
            for el_type, count in elements_by_type.items():
                doc.add_paragraph(f"• {el_type}s: {count}", style='List Bullet')
        
        # Add code structure section
        doc.add_heading("Code Structure", level=1)
        
        # Group elements by file
        elements_by_file = {}
        for el in code_elements:
            file_name = el.get('file', 'unknown.py')
            if file_name not in elements_by_file:
                elements_by_file[file_name] = []
            elements_by_file[file_name].append(el)
        
        # Process each file
        for file_name, elements in elements_by_file.items():
            # Add file header
            doc.add_heading(f"File: {file_name}", level=2)
            
            for el in elements:
                # Add element header
                el_header = f"{el['type']}: {el['name']} (Lines {el['start_line']}-{el['end_line']})"
                doc.add_heading(el_header, level=3)
                
                # Add metadata
                if el['args']:
                    doc.add_paragraph(f"Arguments: {', '.join(el['args'])}")
                    
                if el['type'] != 'Class' and el['has_return']:
                    doc.add_paragraph("Returns: Yes")
                    
                if el['docstring']:
                    doc.add_paragraph("Documentation:")
                    doc.add_paragraph(el['docstring'], style='Intense Quote')
                
                # Add source code
                doc.add_paragraph("Source Code:")
                doc.add_paragraph(el['source'], style='Code')
                
                # Add a small separator between elements
                doc.add_paragraph()
                doc.add_paragraph("-" * 40)
                doc.add_paragraph()
        
        # Add explanation section
        doc.add_heading("AI Explanation", level=1)
        doc.add_paragraph(explanation)
        
        # Save to buffer
        buffer = BytesIO()
        doc.save(buffer)
        buffer.seek(0)
        
        return buffer
        
    except Exception as e:
        raise RuntimeError(f"Error generating document: {str(e)}")
