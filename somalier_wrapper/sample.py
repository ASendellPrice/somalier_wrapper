#!/usr/bin/env python3

"""
sample.py
=========

Defines the `Sample` class for representing genomic samples with their
unique sample ID, CRAM file path, and optional patient identifier.

This module provides basic metadata storage and normalises missing or blank
patient IDs to `None`.
"""

import math


class Sample:
	"""
	Represents a genomic sample with its ID, CRAM path, and optional patient ID.

	This class stores basic sample metadata and normalises missing patient IDs
	(from CSV or other sources) to `None`.

	Parameters
	----------
	sample_id : str
		Unique identifier for the sample.
	cram_path : str
		File path to the CRAM file associated with the sample.
	patient_id : str or None, optional
		Optional patient identifier. Missing or blank values are converted to `None`.

	Attributes
	----------
	sample_id : str
		The unique sample identifier.
	cram_path : str
		The CRAM file path for the sample.
	patient_id : str or None
		The patient identifier, or `None` if missing.
	"""

	def __init__(self, sample_id: str, cram_path: str, patient_id: str | None = None):
		self.sample_id = sample_id
		self.cram_path = cram_path
		self.patient_id = self._normalize_patient_id(patient_id)

	@staticmethod
	def _normalize_patient_id(patient_id):
		"""
		Convert missing or blank patient IDs to `None`.

		Parameters
		----------
		patient_id : str or float or None
			The patient ID value to normalize. May be a string, None, or
			Pandas NaN (float).

		Returns
		-------
		str or None
			The normalized patient ID, or `None` if missing or blank.
		"""
		if patient_id is None:
			return None

		# Handle Pandas empty cell -> float('nan')
		if isinstance(patient_id, float) and math.isnan(patient_id):
			return None

		# Handle literal empty strings
		if isinstance(patient_id, str) and patient_id.strip() == "":
			return None

		return patient_id

	def __repr__(self):
		"""
		Return a string representation of the Sample object.

		Returns
		-------
		str
			Formatted string with sample_id, cram_path, and patient_id.
		"""
		return f"Sample(id={self.sample_id}, cram={self.cram_path}, patient={self.patient_id})"
