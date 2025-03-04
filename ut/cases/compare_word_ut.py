import pytest
from compare_word_files import WordFileComparator

# Test when there are no docx files in the directory
def test_find_similar_no_files():
    comparator = WordFileComparator()
    result = comparator.find_similar("empty_directory")
    assert result == []

# Test when there is only one docx file in the directory
def test_find_similar_one_file():
    comparator = WordFileComparator()
    result = comparator.find_similar("single_file_directory")
    assert len(result) == 1

# Test when there are multiple docx files with different similarities
def test_find_similar_multiple_files():
    comparator = WordFileComparator()
    # Create some docx files with different similarities
    file1 = WordFileComparator.File("file1.docx")
    file2 = WordFileComparator.File("file2.docx")
    file3 = WordFileComparator.File("file3.docx")
    file4 = WordFileComparator.File("file4.docx")

    # Set up the expected groups
    expected_groups = {
        0: [file1, file2],
        1: [file3],
        2: [file4]
    }

    # Call the find_similar method
    result = comparator.find_similar("multiple_files_directory")

    # Assert the result
    assert len(result) == len(expected_groups)
    for group in result:
        assert len(group) == len(expected_groups[group[0].hash])
        for file in group:
            assert file in expected_groups[file.hash]

# Test when the similarity threshold is very high
def test_find_similar_high_threshold():
    comparator = WordFileComparator()
    result = comparator.find_similar("directory", similarity_threshold=0.9)
    # Assert that only very similar files are grouped together

# Test when the similarity threshold is very low
def test_find_similar_low_threshold():
    comparator = WordFileComparator()
    result = comparator.find_similar("directory", similarity_threshold=0.3)
    # Assert that more files are grouped together

# Test with a large number of docx files
def test_find_similar_large_number_of_files():
    comparator = WordFileComparator()
    # Create a large number of docx files
    files = [WordFileComparator.File(f"file{i}.docx") for i in range(100)]

    # Call the find_similar method
    result = comparator.find_similar("large_directory")

    # Assert the result
    #...
