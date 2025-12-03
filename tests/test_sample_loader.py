from somalier_wrapper.sample_loader import SampleLoader
import csv
import tempfile
import os
import pytest


def test_missing_csv():
    """ Test FileNotFoundError is raised when attempting to load a non-existing csv """    
    # Attempt to load a non-existant file
    with pytest.raises(FileNotFoundError):
        SampleLoader("nonexistent.csv")


def test_empty_csv():
    """ Test ValueError is raised when csv file is empty """
    # Create an empty temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.close()

    # Load the temporary file using SampleLoader & assert
    with pytest.raises(ValueError):
        SampleLoader(temp_file.name)
    
    # Remove temporary file
    os.remove(temp_file.name)


def test_no_samples():
    """ Test ValueError is raised when csv contains no samples """
    # Create csv file containing correct headers but zero samples
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    with open(temp_file.name, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["sample_id", "cram_path", "patient_id"])
    temp_file.close()

    # Load the temporary file using SampleLoader & assert
    with pytest.raises(ValueError):
        SampleLoader(temp_file.name)
    
    # Remove temporary file
    os.remove(temp_file.name)


def test_inconsistent_row_lengths():
    """ Test ValueError is raised when csv has inconsistent row lengths """
    # Create a temporary file with inconsistent row lenghts
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    with open(temp_file.name, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["sample_id", "cram_path", "patient_id"])
        writer.writerow(["S1", "/data/S1.cram", "P001"])
        writer.writerow(["S2", "/data/S2.cram", "P002", "EXTRA"])
        writer.writerow(["S3", "/data/S3.cram"])
    temp_file.close()

    # Load temporary file using SampleLoader & assert
    with pytest.raises(ValueError):
        SampleLoader(temp_file.name)

    # Remove temporary file
    os.remove(temp_file.name)


def test_missing_header():
    """ Test ValueError is raised when CSV is missing header """
    # Create a CSV missing required column names
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    with open(temp_file.name, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["S1", "/data/S1.cram", "P001"])
        writer.writerow(["S2", "/data/S2.cram", "P002"])
        writer.writerow(["S3", "/data/S3.cram", "P003"])
    temp_file.close()

    # Load temporary file using SampleLoader & assert
    with pytest.raises(ValueError):
        SampleLoader(temp_file.name)

    # Remove temporary file
    os.remove(temp_file.name)


def test_missing_sample_id_col():
    """ Test ValueError raised when sample_id column is missing """
    # Create a CSV missing required column names
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    with open(temp_file.name, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["cram_path", "patient_id"])
        writer.writerow(["/data/S1.cram", "P001"])
        writer.writerow(["/data/S2.cram", "P002"])
        writer.writerow(["/data/S3.cram", "P003"])
    temp_file.close()

    # Load temporary file using SampleLoader & assert
    with pytest.raises(ValueError):
        SampleLoader(temp_file.name)

    # Remove temporary file
    os.remove(temp_file.name)


def test_missing_cram_path_col():
    """ Test ValueError raised when sample_id column is missing """
    # Create a CSV missing required column names
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    with open(temp_file.name, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["sample_id", "patient_id"])
        writer.writerow(["S1", "P001"])
        writer.writerow(["S2", "P002"])
        writer.writerow(["S3", "P003"])
    temp_file.close()

    # Load temporary file using SampleLoader & assert
    with pytest.raises(ValueError):
        SampleLoader(temp_file.name)

    # Remove temporary file
    os.remove(temp_file.name)
    

def test_sample_missing_cram_path():
    """ Test ValueError raised when a sample is missing cram_path """
    # Create a CSV with a missing cram path
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    with open(temp_file.name, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["sample_id", "cram_path", "patient_id"])
        writer.writerow(["S1", "/data/S1.cram", "P001"])
        writer.writerow(["S2", "", "P002"])
        writer.writerow(["S3", "/data/S3.cram", "P003"])
    temp_file.close()

    # Load temporary file using SampleLoader & assert
    with pytest.raises(ValueError):
        SampleLoader(temp_file.name)

    # Remove temporary file
    os.remove(temp_file.name)


def test_sample_missing_sampleID():
    """ Test ValueError raised when a sampleID is missing """
    # Create a CSV with a missing sampleID
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    with open(temp_file.name, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["sample_id", "cram_path", "patient_id"])
        writer.writerow(["S1", "/data/S1.cram", "P001"])
        writer.writerow(["", "/data/S2.cram", "P002"])
        writer.writerow(["S3", "/data/S3.cram", "P003"])
    temp_file.close()

    # Load temporary file using SampleLoader & assert
    with pytest.raises(ValueError):
        SampleLoader(temp_file.name)

    # Remove temporary file
    os.remove(temp_file.name)


def test_valid_csv():
    """ Test SampleLoader using a valid csv file """
    # Set path to test CSV relative to test file
    csv_file = os.path.join(os.path.dirname(__file__), "data/test.csv")

    # Load csv using SampleLoader
    loader = SampleLoader(csv_file)

    # Check loader contains three Samples
    assert len(loader.samples) == 3

    # Check sample IDs are as expected
    sample_ids = [sample.sample_id for sample in loader.samples]
    assert sample_ids == ["S1", "S2", "S3"]

    # Check cram paths are as expected
    cram_paths = [sample.cram_path for sample in loader.samples]
    assert cram_paths == ["/data/S1.cram", "/data/S2.cram", "/data/S3.cram"]

    # Check patient ids are as expected
    patient_ids = [sample.patient_id for sample in loader.samples]
    assert patient_ids == ["P001", "P002", None]

