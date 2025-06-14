import os
from pathlib import Path
from typing import List, Dict

class FileTypeDetector:
    """Detect file types and determine which analyzers to use"""
    
    PYTHON_EXTENSIONS = {'.py', '.pyi'}
    JAVASCRIPT_EXTENSIONS = {'.js', '.jsx', '.ts', '.tsx', '.mjs'}
    CONFIG_FILES = {'requirements.txt', 'package.json', 'pyproject.toml', '.eslintrc'}
    
    @classmethod
    def detect_file_type(cls, file_path: str) -> str:
        """Detect the type of a file based on its extension"""
        path = Path(file_path)
        extension = path.suffix.lower()
        filename = path.name.lower()
        
        if extension in cls.PYTHON_EXTENSIONS:
            return 'python'
        elif extension in cls.JAVASCRIPT_EXTENSIONS:
            return 'javascript'
        elif filename in cls.CONFIG_FILES:
            return 'config'
        else:
            return 'unknown'
    
    @classmethod
    def get_analyzable_files(cls, file_paths: List[str]) -> Dict[str, List[str]]:
        """Group files by type for analysis"""
        grouped_files = {
            'python': [],
            'javascript': [],
            'config': [],
            'unknown': []
        }
        
        for file_path in file_paths:
            file_type = cls.detect_file_type(file_path)
            grouped_files[file_type].append(file_path)
        
        return grouped_files
    
    @classmethod
    def should_analyze_file(cls, file_path: str) -> bool:
        """Check if a file should be analyzed"""
        file_type = cls.detect_file_type(file_path)
        return file_type in ['python', 'javascript']
