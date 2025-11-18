#!/usr/bin/env python3

"""
sample.py
================

Defines the sample class object which stores a sample's ID, cram path and
an optional patient identifier

"""

class Sample:
	"""
	Represents a sample cram path with metadata (sample ID and patient ID).

	   Attributes
	   ----------
	   sample_id : str
	       Unique identifier for the sample.
	   cram_path : str
	       File path to the CRAM file associated with the sample.
	   patient_id : str or None
	       Optional identifier for the patient. Defaults to None if not provided.
	"""

	# Initialise the sample object
	def __init__(self, sample_id: str, cram_path: str, patient_id: str | None = None):
		self.sample_id = sample_id
		self.cram_path = cram_path
		self.patient_id = patient_id

	# Return a string representation of the Sample object
	def __repr__(self):
		return f"Sample(id={self.sample_id}, cram={self.cram_path}, patient={self.patient_id})"
