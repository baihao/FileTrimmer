from docx import Document
import os

def create_docx_file(file_path, content):
    doc = Document()
    doc.add_paragraph(content)
    doc.save(file_path)

def create_test_files(directory):
    # Create directory if it doesn't exist
    os.makedirs(directory, exist_ok=True)
    
    # Base content for each group
    group1_base = "This is the base content for group 1. " * 10
    group2_base = "This is the base content for group 2. " * 10
    
    # Create group 1 files with 90% similarity
    create_docx_file(os.path.join(directory, "group1_file1.docx"), group1_base)
    create_docx_file(os.path.join(directory, "group1_file2.docx"), group1_base[:int(len(group1_base)*0.9)] + "Some unique text.")
    create_docx_file(os.path.join(directory, "group1_file3.docx"), group1_base[:int(len(group1_base)*0.9)] + "Different unique text.")
    
    # Create group 2 files with 90% similarity
    create_docx_file(os.path.join(directory, "group2_file1.docx"), group2_base)
    create_docx_file(os.path.join(directory, "group2_file2.docx"), group2_base[:int(len(group2_base)*0.9)] + "Group 2 variation.")
    create_docx_file(os.path.join(directory, "group2_file3.docx"), group2_base[:int(len(group2_base)*0.9)] + "Another variation.")

if __name__ == "__main__":
    test_directory = "ut/resources/test_files"
    create_test_files(test_directory)
    print(f"Test files created in {test_directory} directory")
