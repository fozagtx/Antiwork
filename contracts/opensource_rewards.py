# { "Depends": "py-genlayer:test" }

import json
from dataclasses import dataclass
from genlayer import *


@allow_storage
@dataclass
class Contribution:
    id: str
    github_username: str
    organization: str
    project_name: str
    repo_url: str
    pr_number: str
    pr_url: str
    submitted_at: str
    verified: bool
    reward_amount: u256


class OpenSourceRewards(gl.Contract):
    contributions: TreeMap[Address, TreeMap[str, Contribution]]
    total_rewards: TreeMap[Address, u256]
    reward_per_contribution: u256
    submitted_prs: TreeMap[str, bool]  # Track submitted PRs to prevent duplicates

    def __init__(self, reward_amount: u256):
        self.reward_per_contribution = reward_amount

    def _verify_pull_request(
        self, repo_url: str, pr_number: str, github_username: str, organization: str, project_name: str
    ) -> dict:
        """
        Verifies that a pull request exists, is merged, and belongs to the claimed user.
        Also verifies the organization and project name match.
        """

        def check_pr_details() -> str:
            # Construct GitHub API URL for the PR
            pr_api_url = f"{repo_url}/pull/{pr_number}"

            # Fetch the PR page
            web_data = gl.nondet.web.render(pr_api_url, mode="text")

            task = f"""
Analyze this GitHub pull request page and extract information:

Expected PR Author: {github_username}
Expected Organization: {organization}
Expected Project Name: {project_name}
PR Number: {pr_number}
Repository: {repo_url}

Web content:
{web_data}

Verify the following and respond in JSON:
{{
    "is_merged": bool,  // true if PR is merged, false otherwise
    "author": str,  // GitHub username of the PR author
    "organization": str,  // The organization/owner name from the repository
    "project": str,  // The project/repository name
    "title": str,  // PR title
    "is_spam": bool,  // true if this appears to be a spam/low-quality PR
    "error": str  // empty string if no error, otherwise describe the error
}}

Important:
- is_merged should be true ONLY if you can confirm the PR was merged
- author should be the exact GitHub username of who created the PR
- organization should match the expected organization name
- project should match the expected project name
- is_spam should be true if the PR appears to be low-quality, spam, or test content
- Respond ONLY with valid JSON, no other text
"""
            result = gl.nondet.exec_prompt(task, response_format="json")
            return json.dumps(result, sort_keys=True)

        result_json = json.loads(gl.eq_principle.strict_eq(check_pr_details))
        return result_json

    @gl.public.write
    def submit_contribution(
        self, github_username: str, organization: str, project_name: str, repo_url: str, pr_number: str
    ) -> None:
        """
        Submit an open source contribution for verification and reward.
        """
        sender_address = gl.message.sender_address

        # Create unique ID for this PR
        pr_id = f"{repo_url}_{pr_number}".lower()
        pr_url = f"{repo_url}/pull/{pr_number}"

        # Check if this PR has already been submitted by anyone
        if pr_id in self.submitted_prs:
            raise Exception("This pull request has already been claimed")

        # Check if user already submitted this specific PR
        if sender_address in self.contributions:
            if pr_id in self.contributions[sender_address]:
                raise Exception("You have already submitted this pull request")

        # Verify the pull request using AI
        pr_details = self._verify_pull_request(repo_url, pr_number, github_username, organization, project_name)

        # Check for errors
        if pr_details.get("error"):
            raise Exception(f"Verification failed: {pr_details['error']}")

        # Verify PR is merged
        if not pr_details.get("is_merged", False):
            raise Exception("Pull request must be merged to be eligible for rewards")

        # Verify author matches claimed username
        if pr_details.get("author", "").lower() != github_username.lower():
            raise Exception(
                f"Pull request author ({pr_details.get('author')}) does not match claimed username ({github_username})"
            )

        # Verify organization matches
        if pr_details.get("organization", "").lower() != organization.lower():
            raise Exception(
                f"Repository organization ({pr_details.get('organization')}) does not match claimed organization ({organization})"
            )

        # Verify project name matches
        if pr_details.get("project", "").lower() != project_name.lower():
            raise Exception(
                f"Repository project ({pr_details.get('project')}) does not match claimed project name ({project_name})"
            )

        # Check if it's spam
        if pr_details.get("is_spam", False):
            raise Exception("This pull request appears to be spam or low-quality")

        # Create contribution record
        contribution = Contribution(
            id=pr_id,
            github_username=github_username,
            organization=organization,
            project_name=project_name,
            repo_url=repo_url,
            pr_number=pr_number,
            pr_url=pr_url,
            submitted_at="",  # In production, you'd add timestamp
            verified=True,
            reward_amount=self.reward_per_contribution,
        )

        # Store the contribution
        self.contributions.get_or_insert_default(sender_address)[pr_id] = contribution

        # Mark this PR as submitted globally
        self.submitted_prs[pr_id] = True

        # Award the reward
        if sender_address not in self.total_rewards:
            self.total_rewards[sender_address] = 0
        self.total_rewards[sender_address] += self.reward_per_contribution

    @gl.public.view
    def get_my_contributions(self) -> dict:
        """
        Get all contributions for the caller.
        """
        sender_address = gl.message.sender_address
        if sender_address not in self.contributions:
            return {}
        return {k: v for k, v in self.contributions[sender_address].items()}

    @gl.public.view
    def get_all_contributions(self) -> dict:
        """
        Get all contributions from all users.
        """
        return {k.as_hex: v for k, v in self.contributions.items()}

    @gl.public.view
    def get_my_rewards(self) -> int:
        """
        Get total rewards for the caller.
        """
        sender_address = gl.message.sender_address
        return self.total_rewards.get(sender_address, 0)

    @gl.public.view
    def get_all_rewards(self) -> dict:
        """
        Get all rewards (leaderboard).
        """
        return {k.as_hex: v for k, v in self.total_rewards.items()}

    @gl.public.view
    def get_user_rewards(self, user_address: str) -> int:
        """
        Get total rewards for a specific user.
        """
        return self.total_rewards.get(Address(user_address), 0)

    @gl.public.view
    def get_reward_per_contribution(self) -> int:
        """
        Get the fixed reward amount per contribution.
        """
        return self.reward_per_contribution
