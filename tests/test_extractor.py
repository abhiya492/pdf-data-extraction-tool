import os
import sys
import unittest
import tempfile
from pathlib import Path

# Add the src directory to the path
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.append(src_path)

from pdf_extractor import PDFExtractor


class TestPDFExtractor(unittest.TestCase):
    """Test cases for the PDFExtractor class"""
    
    def setUp(self):
        """Set up test environment"""
        # Create a temporary PDF file for testing
        self.test_dir = tempfile.TemporaryDirectory()
        self.temp_pdf_path = os.path.join(self.test_dir.name, "test.pdf")
        
        # Create an empty PDF file
        with open(self.temp_pdf_path, "wb") as f:
            f.write(b"%PDF-1.7\n%\xe2\xe3\xcf\xd3\n1 0 obj\n<</Type/Catalog/Pages 2 0 R>>\nendobj\n2 0 obj\n<</Type/Pages/Kids[3 0 R]/Count 1>>\nendobj\n3 0 obj\n<</Type/Page/MediaBox[0 0 612 792]/Parent 2 0 R/Resources<<>>>>\nendobj\nxref\n0 4\n0000000000 65535 f \n0000000015 00000 n \n0000000060 00000 n \n0000000111 00000 n \n\ntrailer\n<</Size 4/Root 1 0 R>>\n%%EOF")
        
    def tearDown(self):
        """Clean up test environment"""
        self.test_dir.cleanup()
        
    def test_init(self):
        """Test initializing the PDFExtractor"""
        extractor = PDFExtractor(self.temp_pdf_path)
        self.assertEqual(extractor.pdf_path, self.temp_pdf_path)
        
    def test_validate_file_exists(self):
        """Test file validation with an existing file"""
        extractor = PDFExtractor(self.temp_pdf_path)
        # Should not raise an exception
        extractor._validate_file()
        
    def test_validate_file_not_exists(self):
        """Test file validation with a non-existent file"""
        non_existent_path = os.path.join(self.test_dir.name, "nonexistent.pdf")
        with self.assertRaises(FileNotFoundError):
            PDFExtractor(non_existent_path)
            
    def test_validate_file_not_pdf(self):
        """Test file validation with a non-PDF file"""
        non_pdf_path = os.path.join(self.test_dir.name, "test.txt")
        with open(non_pdf_path, "w") as f:
            f.write("This is not a PDF")
            
        with self.assertRaises(ValueError):
            PDFExtractor(non_pdf_path)


if __name__ == '__main__':
    unittest.main() 