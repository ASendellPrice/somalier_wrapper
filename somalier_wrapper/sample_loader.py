#!/usr/bin/env python3

"""
sample_loader.py
================

Defines the `SampleLoader` class for reading sample metadata from a CSV file
and constructing `Sample` objects (see `sample.py`).

This class validates the CSV, ensures required columns are present, and
converts each row into a `Sample` instance. Missing patient IDs are
automatically handled by the `Sample` class.
"""

import pandas as pd
from .sample import Sample


class SampleLoader:
	"""
	Loads sample metadata from a CSV file and constructs Sample objects.

	Parameters
	----------
	path : str
		Path to the CSV file containing sample metadata. Must contain at least
		`sample_id` and `cram_path` columns. Optionally may include `patient_id`.

	Attributes
	----------
	path : str
		The CSV file path provided to the loader.
	samples : list of Sample
		List of Sample objects loaded from the CSV.
	"""

	def __init__(self, path: str):
		"""
		Initialize the SampleLoader and automatically load samples from CSV.

		Parameters
		----------
		path : str
			Path to the CSV file containing sample metadata.
		"""
		self.path = path
		self.samples = self.load_csv()

	def load_csv(self):
		"""
		Load the CSV file and construct Sample objects.

		Validates that required columns are present, the file is not empty,
		and each row contains the necessary data. Missing patient IDs are
		handled automatically.

		Returns
		-------
		list of Sample
			List of Sample objects created from the CSV.

		Raises
		------
		FileNotFoundError
			If the CSV file does not exist.
		ValueError
			If the CSV is empty, has parsing errors, is missing required columns,
			or contains rows with missing sample_id or cram_path.
		"""
		# Load the CSV file
		try:
			df = pd.read_csv(self.path)
		except FileNotFoundError:
			raise FileNotFoundError(f"CSV file not found: {self.path}")
		except pd.errors.EmptyDataError:
			raise ValueError(f"CSV file is empty: {self.path}")
		except pd.errors.ParserError as e:
			raise ValueError(f"Error parsing CSV file {self.path}: {e}")

		# Validate required columns
		required_cols = {"sample_id", "cram_path"}
		missing = required_cols - set(df.columns)
		if missing:
			raise ValueError(f"Missing required columns in CSV: {', '.join(missing)}")

		# Check the CSV contains rows
		if df.empty:
			raise ValueError(f"CSV file {self.path} contains no samples.")

		# Handle optional patient_id column
		has_patient_id = "patient_id" in df.columns

		# Construct Sample objects
		samples = []
		for _, row in df.iterrows():
			if pd.isna(row["sample_id"]) or pd.isna(row["cram_path"]):
				raise ValueError(
					f"CSV row has missing sample_id or cram_path: {row.to_dict()}"
				)
			samples.append(
				Sample(
					row["sample_id"],
					row["cram_path"],
					row["patient_id"] if has_patient_id else None,
				)
			)

		return samples
