# taxonomy_validator.pyx
import re
from typing import List

cdef class TaxonomyValidator:
    """
    Cython-optimized taxonomy validator for species names
    """

    cdef object capitalization_pattern
    cdef object strain_pattern
    cdef object invalid_chars_pattern

    def __init__(self):
        # Pre-compile regex patterns for better performance
        self.capitalization_pattern = re.compile(r'^[A-Z][a-z]+ [a-z]+')
        self.strain_pattern = re.compile(r'\b(strain|isolate|clone|var\.|ATCC|DSM)\b|[A-Z]{2,}[0-9]', re.I)
        self.invalid_chars_pattern = re.compile(r'[0-9]|[^a-zA-Z\s\-\.]')

    cpdef list validate_taxonomy(self, str name):
        """
        Validate taxonomy name and return list of flags

        Args:
            name (str): Species name to validate

        Returns:
            list: List of validation flags
        """
        cdef list flags = []

        # Kapitalisierung prüfen
        if not self.capitalization_pattern.match(name):
            flags.append("Invalid_Capitalization")

        # Strain-Info prüfen
        if self.strain_pattern.search(name):
            flags.append("Contains_Strain_Info")

        # Ungültige Zeichen prüfen
        if self.invalid_chars_pattern.search(name):
            flags.append("Invalid_Characters")

        return flags

    cpdef dict batch_validate(self, list names):
        """
        Batch validation for multiple taxonomy names

        Args:
            names (list): List of species names to validate

        Returns:
            dict: Dictionary mapping names to their validation flags
        """
        cdef dict results = {}
        cdef str name

        for name in names:
            results[name] = self.validate_taxonomy(name)

        return results

# Convenience function for single validation
cpdef list validate_taxonomy(str name):
    """
    Standalone function for single taxonomy validation

    Args:
        name (str): Species name to validate

    Returns:
        list: List of validation flags
    """
    cdef list flags = []

    # Kapitalisierung
    if not re.match(r'^[A-Z][a-z]+ [a-z]+', name):
        flags.append("Invalid_Capitalization")

    # Strain-Info
    if re.search(r'\b(strain|isolate|clone|var\.|ATCC|DSM)\b|[A-Z]{2,}[0-9]', name, re.I):
        flags.append("Contains_Strain_Info")

    # Ungültige Zeichen
    if re.search(r'[0-9]|[^a-zA-Z\s\-\.]', name):
        flags.append("Invalid_Characters")

    return flags