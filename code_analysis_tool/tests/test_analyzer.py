"""Tests for the code analysis tool."""
import os
import tempfile
import unittest
from pathlib import Path

from code_analysis_tool.analyzer import CodeAnalyzer, analyze_code

class TestCodeAnalyzer(unittest.TestCase):
    """Test cases for the CodeAnalyzer class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.analyzer = CodeAnalyzer()
        self.test_dir = tempfile.mkdtemp()
        
        # Create a test Python file
        self.test_file = os.path.join(self.test_dir, "test.py")
        with open(self.test_file, 'w', encoding='utf-8') as f:
            f.write('''"""Test module docstring."""

def hello(name: str) -> str:
    """Return a greeting message."""
    return f"Hello, {name}!"

class TestClass:
    """A test class."""
    
    def __init__(self, value: int):
        self.value = value
    
    def get_value(self) -> int:
        """Get the current value."""
        return self.value
''')
    
    def test_analyze_file(self):
        """Test analyzing a single file."""
        result = self.analyzer.analyze_file(self.test_file)
        self.assertIn('analysis', result)
        self.assertIn('elements', result)
        self.assertGreater(len(result['elements']), 0)
    
    def test_analyze_directory(self):
        """Test analyzing a directory."""
        results = self.analyzer.analyze_directory(self.test_dir)
        self.assertIn(self.test_file, results)
        self.assertIn('analysis', results[self.test_file])
    
    def test_extract_elements(self):
        """Test element extraction from source code."""
        with open(self.test_file, 'r', encoding='utf-8') as f:
            code = f.read()
        
        elements = self.analyzer._extract_elements(code)
        self.assertEqual(len(elements), 3)  # 1 function + 1 class + 1 method
        
        # Check function element
        func = next(e for e in elements if e['name'] == 'hello')
        self.assertEqual(func['type'], 'Function')
        self.assertIn('greeting', func['docstring'].lower())
        
        # Check class element
        cls = next(e for e in elements if e['name'] == 'TestClass')
        self.assertEqual(cls['type'], 'Class')
    
    def test_analyze_elements(self):
        """Test analysis of extracted elements."""
        with open(self.test_file, 'r', encoding='utf-8') as f:
            code = f.read()
        
        elements = self.analyzer._extract_elements(code)
        analysis = self.analyzer._analyze_elements(elements, self.test_file)
        
        self.assertIn('analysis', analysis)
        self.assertIn('elements', analysis)
        self.assertEqual(len(analysis['elements']), 3)

class TestAnalyzeCodeFunction(unittest.TestCase):
    """Test the analyze_code convenience function."""
    
    def test_analyze_code_with_file(self):
        """Test analyzing a single file."""
        with tempfile.NamedTemporaryFile(suffix='.py', mode='w', delete=False) as f:
            f.write('def test():\n    pass')
            temp_file = f.name
        
        try:
            result = analyze_code(temp_file)
            self.assertIn('analysis', result)
            self.assertIn('elements', result)
        finally:
            os.unlink(temp_file)
    
    def test_analyze_code_with_nonexistent_path(self):
        """Test with a non-existent path."""
        with self.assertRaises(ValueError):
            analyze_code("/nonexistent/path")

if __name__ == '__main__':
    unittest.main()
