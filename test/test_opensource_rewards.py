import pytest
from genlayer.py.tests.conftest import *


@pytest.fixture
def contract_instance(accounts, deployer):
    """Deploy the OpenSourceRewards contract with a reward amount."""
    reward_per_contribution = 100
    return deployer.deploy(
        "contracts/opensource_rewards.py",
        reward_amount=reward_per_contribution
    )


@pytest.mark.asyncio
async def test_submit_contribution(contract_instance, accounts):
    """
    Test submitting a valid contribution.

    Note: This test requires a valid merged PR from GitHub.
    For testing purposes, use a known merged PR from a public repository.
    """
    # Example: A merged PR from a public repository
    # You should replace these with actual values for a real merged PR
    github_username = "example_user"
    organization = "example_org"
    project_name = "example_project"
    repo_url = "https://github.com/example_org/example_project"
    pr_number = "1"

    # Submit the contribution
    result = await contract_instance.submit_contribution(
        github_username,
        organization,
        project_name,
        repo_url,
        pr_number,
        from_=accounts[0]
    )

    # Verify the transaction was successful
    assert result is not None

    # Check that rewards were granted
    rewards = await contract_instance.get_my_rewards(from_=accounts[0])
    assert rewards == 100, "User should have received 100 tokens"


@pytest.mark.asyncio
async def test_get_reward_per_contribution(contract_instance, accounts):
    """Test getting the reward amount per contribution."""
    reward = await contract_instance.get_reward_per_contribution(from_=accounts[0])
    assert reward == 100, "Reward per contribution should be 100"


@pytest.mark.asyncio
async def test_get_my_rewards_initial(contract_instance, accounts):
    """Test getting rewards for a user with no contributions."""
    rewards = await contract_instance.get_my_rewards(from_=accounts[0])
    assert rewards == 0, "User should have 0 rewards initially"


@pytest.mark.asyncio
async def test_get_all_rewards(contract_instance, accounts):
    """Test getting all rewards (leaderboard)."""
    all_rewards = await contract_instance.get_all_rewards(from_=accounts[0])
    assert isinstance(all_rewards, dict), "Should return a dictionary of rewards"


@pytest.mark.asyncio
async def test_get_all_contributions(contract_instance, accounts):
    """Test getting all contributions."""
    all_contributions = await contract_instance.get_all_contributions(from_=accounts[0])
    assert isinstance(all_contributions, dict), "Should return a dictionary of contributions"


@pytest.mark.asyncio
async def test_duplicate_submission_prevention(contract_instance, accounts):
    """
    Test that duplicate PR submissions are prevented.

    Note: This test assumes the first submission succeeds.
    """
    github_username = "example_user"
    organization = "example_org"
    project_name = "example_project"
    repo_url = "https://github.com/example_org/example_project"
    pr_number = "1"

    # First submission
    await contract_instance.submit_contribution(
        github_username,
        organization,
        project_name,
        repo_url,
        pr_number,
        from_=accounts[0]
    )

    # Second submission should fail
    with pytest.raises(Exception) as exc_info:
        await contract_instance.submit_contribution(
            github_username,
            organization,
            project_name,
            repo_url,
            pr_number,
            from_=accounts[1]  # Different account trying to claim same PR
        )

    assert "already been claimed" in str(exc_info.value).lower(), \
        "Should prevent duplicate PR submissions"


@pytest.mark.asyncio
async def test_get_user_rewards(contract_instance, accounts):
    """Test getting rewards for a specific user address."""
    # Get rewards for the first account
    rewards = await contract_instance.get_user_rewards(
        accounts[0].address,
        from_=accounts[0]
    )
    assert isinstance(rewards, int), "Should return an integer reward amount"
    assert rewards >= 0, "Rewards should be non-negative"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
