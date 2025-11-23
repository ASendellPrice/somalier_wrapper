#!/usr/bin/env python3

"""
sample_loader.py
================

Defines the SampleLoader class for reading sample metadata from a CSV file
and constructing Sample objects (see sample.py).

"""

import pandas as pd
from .sample import Sample


class SampleLoader:

	# Initialize the SampleLoader with a CSV path
	def __init__(self, path: str):
		self.path = path
		self.samples = self.load_csv()

	# Read the CSV file and construct Sample objects
	def load_csv(self):

		# Load the csv file
		try:
			df = pd.read_csv(self.path)
		except FileNotFoundError:
			raise FileNotFoundError(f"CSV file not found: {self.path}")
		except pd.errors.EmptyDataError:
			raise ValueError(f"CSV file is empty: {self.path}")
		except pd.errors.ParserError as e:
			raise ValueError(f"Error passing csv file {self.path}: {e}")

		# Validate required columns
		required_cols = {"sample_id", "cram_path"}
		missing = required_cols - set(df.columns)
		if missing:
			raise ValueError(f"Missing required columns in CSV: {', '.join(missing)}")

		# Check the csv contains rows
		if df.empty:
			raise ValueError(f"CSV file {self.path} contains no samples.")

		# Handle optional patient_id column
		has_patient_id = "patient_id" in df.columns

		# Construct Sample object while checking for missing values
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

		# Return the Sample objects
		return samples
