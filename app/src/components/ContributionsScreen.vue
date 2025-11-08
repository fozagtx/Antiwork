<template>
  <div class="min-h-screen bg-gray-100 text-gray-900">
    <header class="bg-white shadow flex justify-between">
      <div class="max-w-7xl py-6 px-4 sm:px-6 lg:px-8">
        <h1 class="text-3xl font-bold text-gray-900">Open Source Rewards</h1>
        <p class="text-sm text-gray-600 mt-2">Get rewarded for your open source contributions</p>
      </div>
      <div class="max-w-7xl py-6 px-4 sm:px-6 lg:px-8 text-right">
        <div v-if="!userAddress">
          <button
            @click="createUserAccount"
            class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
          >
            Connect Wallet
          </button>
        </div>
        <div v-else>
          <p class="text-lg">Your address: <Address :address="userAddress" /></p>
          <p class="text-lg">Your rewards: <span class="font-bold text-green-600">{{ userRewards }} tokens</span></p>
          <button
            @click="disconnectUserAccount"
            class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mt-2"
          >
            Disconnect
          </button>
        </div>
      </div>
    </header>
    <main class="mx-auto py-6 sm:px-6 lg:px-8">
      <div class="grid grid-cols-1 md:grid-cols-10 gap-8">
        <!-- Contributions List -->
        <div class="bg-white shadow overflow-hidden sm:rounded-lg col-span-7">
          <div class="px-4 py-5 sm:px-6 flex justify-between items-center">
            <h2 class="text-lg leading-6 font-medium text-gray-900">Contributions</h2>
            <button
              @click="openSubmitModal"
              :disabled="!userAddress"
              class="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded text-sm disabled:bg-gray-400"
            >
              Submit Contribution
            </button>
          </div>
          <div class="border-t border-gray-200">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th
                    scope="col"
                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                  >
                    User
                  </th>
                  <th
                    scope="col"
                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                  >
                    GitHub Username
                  </th>
                  <th
                    scope="col"
                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                  >
                    Repository
                  </th>
                  <th
                    scope="col"
                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                  >
                    PR Number
                  </th>
                  <th
                    scope="col"
                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                  >
                    Status
                  </th>
                  <th
                    scope="col"
                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                  >
                    Reward
                  </th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="contribution in contributions" :key="contribution.id">
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    <Address :address="contribution.owner" />
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {{ contribution.github_username }}
                  </td>
                  <td class="px-6 py-4 text-sm text-gray-500 max-w-xs truncate">
                    <a :href="contribution.repo_url" target="_blank" class="text-blue-600 hover:underline">
                      {{ contribution.repo_url.replace('https://github.com/', '') }}
                    </a>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    <a :href="contribution.pr_url" target="_blank" class="text-blue-600 hover:underline">
                      #{{ contribution.pr_number }}
                    </a>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    <span :class="contribution.verified ? 'text-green-600' : 'text-yellow-600'">
                      {{ contribution.verified ? "Verified" : "Pending" }}
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 font-bold">
                    {{ contribution.reward_amount }} tokens
                  </td>
                </tr>
              </tbody>
            </table>
            <div v-if="contributions.length === 0" class="px-6 py-8 text-center text-gray-500">
              No contributions yet. Be the first to submit!
            </div>
          </div>
        </div>

        <!-- Leaderboard -->
        <div class="bg-white shadow overflow-hidden sm:rounded-lg col-span-3">
          <div class="px-4 py-5 sm:px-6">
            <h2 class="text-lg leading-6 font-medium text-gray-900">Leaderboard</h2>
            <p class="text-sm text-gray-500 mt-1">Top contributors</p>
          </div>
          <div class="border-t border-gray-200">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th
                    scope="col"
                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                  >
                    Rank
                  </th>
                  <th
                    scope="col"
                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                  >
                    Address
                  </th>
                  <th
                    scope="col"
                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                  >
                    Rewards
                  </th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="(user, index) in leaderboard" :key="user.address">
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ index + 1 }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    <Address :address="user.address" />
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 font-bold">{{ user.rewards }}</td>
                </tr>
              </tbody>
            </table>
            <div v-if="leaderboard.length === 0" class="px-6 py-4 text-center text-gray-500 text-sm">
              No rewards yet
            </div>
          </div>
        </div>
      </div>

      <!-- Submit Contribution Modal -->
      <div
        v-if="showSubmitModal"
        class="fixed inset-0 bg-gray-600 bg-opacity-75 overflow-y-auto h-full w-full flex items-center justify-center"
      >
        <div class="relative p-5 border w-96 shadow-lg rounded-md bg-white">
          <h3 class="text-lg font-medium leading-6 text-gray-900 mb-2">Submit Your Contribution</h3>
          <p class="text-sm text-gray-600 mb-4">Submit a merged pull request to earn {{ rewardPerContribution }} tokens</p>

          <input
            v-model="githubUsername"
            class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 mb-2"
            placeholder="Your GitHub Username"
          />
          <input
            v-model="organization"
            class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 mb-2"
            placeholder="Organization/Owner (e.g., facebook)"
          />
          <input
            v-model="projectName"
            class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 mb-2"
            placeholder="Project Name (e.g., react)"
          />
          <input
            v-model="repoUrl"
            class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 mb-2"
            placeholder="Repository URL (e.g., https://github.com/facebook/react)"
          />
          <input
            v-model="prNumber"
            class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 mb-2"
            placeholder="Pull Request Number"
            type="number"
          />

          <div class="bg-blue-50 border border-blue-200 rounded p-3 mb-4 text-sm">
            <p class="text-blue-800 mb-1">Requirements:</p>
            <ul class="list-disc list-inside text-blue-700 text-xs">
              <li>PR must be merged</li>
              <li>PR author must match your GitHub username</li>
              <li>Repository must be a legitimate open source project</li>
              <li>Each PR can only be claimed once</li>
            </ul>
          </div>

          <div class="mt-4">
            <div v-if="!submittingContribution">
              <button
                @click="submitContribution"
                class="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded mr-2"
              >
                Submit
              </button>
              <button
                @click="showSubmitModal = false"
                class="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4 rounded"
              >
                Cancel
              </button>
            </div>
            <div v-else>
              <div class="spinner">Verifying contribution...</div>
              <p class="text-xs text-gray-600 mt-2">This may take a moment as we verify your PR</p>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>

  <div class="flex items-center justify-center h-screen">
    <div class="spinner">Loading...</div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { account, createAccount, removeAccount } from "../services/genlayer";
import OpenSourceRewards from "../logic/OpenSourceRewards";
import Address from "./Address.vue";

// State
const githubUsername = ref("");
const organization = ref("");
const projectName = ref("");
const repoUrl = ref("");
const prNumber = ref("");
const submittingContribution = ref(false);
const contractAddress = import.meta.env.VITE_CONTRACT_ADDRESS;
const studioUrl = import.meta.env.VITE_STUDIO_URL;
const openSourceRewards = new OpenSourceRewards(contractAddress, account, studioUrl);
const userAccount = ref(account);
const userRewards = ref(0);
const rewardPerContribution = ref(0);
const userAddress = computed(() => userAccount.value?.address);
const contributions = ref([]);
const leaderboard = ref([]);
const showSubmitModal = ref(false);

// Methods
const createUserAccount = async () => {
  userAccount.value = createAccount();
  openSourceRewards.updateAccount(userAccount.value);
  userRewards.value = 0;
};

const disconnectUserAccount = async () => {
  userAccount.value = null;
  removeAccount();
  userRewards.value = 0;
};

const openSubmitModal = () => {
  showSubmitModal.value = true;
};

const loadContributions = async () => {
  const allContributions = await openSourceRewards.getAllContributions();
  contributions.value = allContributions;
};

const loadLeaderboard = async () => {
  leaderboard.value = await openSourceRewards.getLeaderboard();
};

const refreshUserRewards = async () => {
  if (userAddress.value) {
    userRewards.value = await openSourceRewards.getUserRewards(userAddress.value);
  }
};

const loadRewardAmount = async () => {
  rewardPerContribution.value = await openSourceRewards.getRewardPerContribution();
};

const submitContribution = async () => {
  if (githubUsername.value && organization.value && projectName.value && repoUrl.value && prNumber.value) {
    submittingContribution.value = true;
    try {
      await openSourceRewards.submitContribution(
        githubUsername.value,
        organization.value,
        projectName.value,
        repoUrl.value,
        prNumber.value
      );
      await loadContributions();
      await loadLeaderboard();
      await refreshUserRewards();
      // Reset form fields
      githubUsername.value = "";
      organization.value = "";
      projectName.value = "";
      repoUrl.value = "";
      prNumber.value = "";
      showSubmitModal.value = false;
    } catch (error) {
      alert(`Failed to submit contribution: ${error.message}`);
    } finally {
      submittingContribution.value = false;
    }
  } else {
    alert("Please fill in all fields");
  }
};

// Initialize
onMounted(async () => {
  await loadRewardAmount();
  await loadContributions();
  await loadLeaderboard();
  await refreshUserRewards();
});
</script>
