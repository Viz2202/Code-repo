from github import Github
import logging

from .config import settings

logger = logging.getLogger(__name__)

class GitHubClient:
    def __init__(self):
        self.client = Github(settings.GITHUB_TOKEN)
        
    def get_user(self):
        """Get the authenticated user"""
        return self.client.get_user()
    
    def get_repo(self, repo_full_name):
        """Get repository by full name (owner/repo)"""
        return self.client.get_repo(repo_full_name)
    
    def get_pull_request(self, repo_full_name, pr_number):
        """Get pull request by number"""
        repo = self.get_repo(repo_full_name)
        return repo.get_pull(pr_number)
    
    def post_pr_comment(self, repo_full_name, pr_number, comment_body):
        """Post a comment on a pull request"""
        try:
            pr = self.get_pull_request(repo_full_name, pr_number)
            pr.create_issue_comment(comment_body)
            logger.info(f"Posted comment on PR #{pr_number} in {repo_full_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to post comment: {e}")
            return False
    
    def test_connection(self):
        """Test GitHub API connection"""
        try:
            user = self.get_user()
            logger.info(f"GitHub connection successful. User: {user.login}")
            return True, user.login
        except Exception as e:
            logger.error(f"GitHub connection failed: {e}")
            return False, str(e)

# Global client instance
github_client = GitHubClient()
