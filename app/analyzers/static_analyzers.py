import subprocess
import json
import logging
from typing import List, Dict, Any
from pathlib import Path
from .get_file import GetFile
import tempfile
from ..mygroq import MyGroq

logger = logging.getLogger(__name__)

class StaticAnalyzer:
    """Handle static code analysis for different file types"""
    
    def __init__(self):
        self.results = []
    
    def analyze_python_file(self, file_path: str, file_content: str = None) -> List[Dict[str, Any]]:
        """Analyze Python file with pylint"""
        try:
            # For Phase 1, we'll do basic analysis
            # In Phase 2, we'll expand this with more tools
            
            if file_content:
                # Write content to temporary file for analysis
                with tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode='w') as f:
                    f.write(file_content)
                    temp_file = f.name 
                analysis_file = temp_file
            else:
                analysis_file = file_path
            
            # Run pylint
            cmd = ['pylint', '--output-format=json', '--disable=C0114,C0115,C0116', analysis_file]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.stdout:
                issues = json.loads(result.stdout)
                return self._format_pylint_issues(issues, file_path)
            
            return []
            
        except Exception as e:
            logger.error(f"Error analyzing Python file {file_path}: {e}")
            return []
    
    def _format_pylint_issues(self, issues: List[Dict], file_path: str) -> List[Dict[str, Any]]:
        """Format pylint issues into standard format"""
        formatted_issues = []
        
        for issue in issues:
            formatted_issues.append({
                'file': file_path,
                'line': issue.get('line', 0),
                'column': issue.get('column', 0),
                'severity': self._map_pylint_severity(issue.get('type', 'info')),
                'message': issue.get('message', ''),
                'rule': issue.get('message-id', ''),
                'tool': 'pylint'
            })
        
        return formatted_issues
    
    def _map_pylint_severity(self, pylint_type: str) -> str:
        """Map pylint message types to severity levels"""
        mapping = {
            'error': 'high',
            'warning': 'medium',
            'refactor': 'low',
            'convention': 'low',
            'info': 'info'
        }
        return mapping.get(pylint_type, 'info')
    
    def analyze_javascript_file(self, file_path: str, file_content: str = None) -> List[Dict[str, Any]]:
        """Analyze JavaScript file - placeholder for Phase 2"""
        # For Phase 1, we'll just return empty list
        # In Phase 2, we'll integrate ESLint
        logger.info(f"JavaScript analysis placeholder for {file_path}")
        return []
    
    def analyze_files(self, response: Dict) -> List[Dict[str, Any]]:
        """Analyze multiple files grouped by type"""
        commits = response.get('commits', [])[0]
        modified_files = commits.get('modified', [])
        added_files = commits.get('added', [])
        commit_id = commits.get('id', '')

        file_dict = {
            'python': modified_files + added_files,
        }

        all_issues = ""
        
        # Analyze Python files
        changes_and_file= GetFile().fetch_file(commit_id)
        print("Changes and files fetched:", changes_and_file)
        for change, file_text in changes_and_file:
            issues= MyGroq.review(change,file_text)
            all_issues+=issues+'\n'
        # Analyze JavaScript files (Phase 2)
        for js_file in file_dict.get('javascript', []):
            issues = self.analyze_javascript_file(js_file)
            all_issues.extend(issues)
        
        return all_issues