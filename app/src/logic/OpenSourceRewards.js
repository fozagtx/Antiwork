import { createClient } from "genlayer-js";
import { studionet } from "genlayer-js/chains";

class OpenSourceRewards {
  contractAddress;
  client;

  constructor(contractAddress, account = null, studioUrl = null) {
    this.contractAddress = contractAddress;
    const config = {
      chain: studionet,
      ...(account ? { account } : {}),
      ...(studioUrl ? { endpoint: studioUrl } : {}),
    };
    this.client = createClient(config);
  }

  updateAccount(account) {
    this.client = createClient({ chain: studionet, account });
  }

  async getAllContributions() {
    const contributions = await this.client.readContract({
      address: this.contractAddress,
      functionName: "get_all_contributions",
      args: [],
    });
    return Array.from(contributions.entries()).flatMap(([owner, contributionMap]) => {
      return Array.from(contributionMap.entries()).map(([id, contributionData]) => {
        const contributionObj = Array.from(contributionData.entries()).reduce((obj, [key, value]) => {
          obj[key] = value;
          return obj;
        }, {});

        return {
          id,
          ...contributionObj,
          owner,
        };
      });
    });
  }

  async getMyContributions() {
    const contributions = await this.client.readContract({
      address: this.contractAddress,
      functionName: "get_my_contributions",
      args: [],
    });
    return Array.from(contributions.entries()).map(([id, contributionData]) => {
      const contributionObj = Array.from(contributionData.entries()).reduce((obj, [key, value]) => {
        obj[key] = value;
        return obj;
      }, {});

      return {
        id,
        ...contributionObj,
      };
    });
  }

  async getUserRewards(address) {
    if (!address) {
      return 0;
    }
    const rewards = await this.client.readContract({
      address: this.contractAddress,
      functionName: "get_user_rewards",
      args: [address],
    });
    return Number(rewards);
  }

  async getMyRewards() {
    const rewards = await this.client.readContract({
      address: this.contractAddress,
      functionName: "get_my_rewards",
      args: [],
    });
    return Number(rewards);
  }

  async getLeaderboard() {
    const rewards = await this.client.readContract({
      address: this.contractAddress,
      functionName: "get_all_rewards",
      args: [],
    });
    return Array.from(rewards.entries())
      .map(([address, rewards]) => ({
        address,
        rewards: Number(rewards),
      }))
      .sort((a, b) => b.rewards - a.rewards);
  }

  async getRewardPerContribution() {
    const reward = await this.client.readContract({
      address: this.contractAddress,
      functionName: "get_reward_per_contribution",
      args: [],
    });
    return Number(reward);
  }

  async submitContribution(githubUsername, organization, projectName, repoUrl, prNumber) {
    const txHash = await this.client.writeContract({
      address: this.contractAddress,
      functionName: "submit_contribution",
      args: [githubUsername, organization, projectName, repoUrl, prNumber],
    });
    const receipt = await this.client.waitForTransactionReceipt({
      hash: txHash,
      status: "FINALIZED",
      interval: 10000,
      retries: 30,
    });
    return receipt;
  }
}

export default OpenSourceRewards;
