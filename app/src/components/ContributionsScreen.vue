<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 text-gray-900 pb-12">
    <div class="fixed inset-0 bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 -z-10"></div>
    <header class="bg-white/80 backdrop-blur-lg shadow-lg border-b border-gray-200 flex justify-between sticky top-0 z-10">
      <div class="max-w-7xl py-6 px-4 sm:px-6 lg:px-8">
        <h1 class="text-4xl font-extrabold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">Open Source Rewards</h1>
        <p class="text-sm text-gray-600 mt-2 flex items-center gap-2">
          <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
            <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
          </svg>
          Get rewarded for your open source contributions
        </p>
      </div>
      <div class="max-w-7xl py-6 px-4 sm:px-6 lg:px-8 text-right">
        <div v-if="!userAddress">
          <button
            @click="createUserAccount"
            class="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white font-bold py-3 px-6 rounded-xl shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-200"
          >
            <span class="flex items-center gap-2">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm7-5a2 2 0 11-4 0 2 2 0 014 0z"/>
              </svg>
              Connect Wallet
            </span>
          </button>
        </div>
        <div v-else class="bg-white/50 backdrop-blur-sm rounded-2xl p-4 shadow-lg">
          <p class="text-sm text-gray-600 mb-1">Your address:</p>
          <p class="font-mono text-xs mb-3"><Address :address="userAddress" /></p>
          <div class="bg-gradient-to-r from-green-500 to-emerald-500 text-white rounded-lg p-3 mb-3">
            <p class="text-xs opacity-90">Your rewards</p>
            <p class="text-2xl font-bold">{{ userRewards }} tokens</p>
          </div>
          <button
            @click="disconnectUserAccount"
            class="bg-red-500 hover:bg-red-600 text-white font-semibold py-2 px-4 rounded-lg w-full transition-colors duration-200 text-sm"
          >
            Disconnect
          </button>
        </div>
      </div>
    </header>
    <main class="mx-auto py-6 sm:px-6 lg:px-8">
      <div class="grid grid-cols-1 md:grid-cols-10 gap-8">
        <!-- Contributions List -->
        <div class="bg-white/90 backdrop-blur-sm shadow-xl overflow-hidden rounded-2xl col-span-7 border border-gray-200">
          <div class="px-6 py-5 sm:px-6 flex justify-between items-center bg-gradient-to-r from-blue-50 to-purple-50 border-b border-gray-200">
            <div>
              <h2 class="text-2xl font-bold text-gray-900 flex items-center gap-2">
                <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                </svg>
                Contributions
              </h2>
              <p class="text-xs text-gray-600 mt-1">All verified open source contributions</p>
            </div>
            <button
              @click="openSubmitModal"
              :disabled="!userAddress"
              class="bg-gradient-to-r from-green-500 to-emerald-500 hover:from-green-600 hover:to-emerald-600 text-white font-bold py-3 px-6 rounded-xl shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none flex items-center gap-2"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
              </svg>
              Submit Contribution
            </button>
          </div>
          <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gradient-to-r from-gray-50 to-gray-100">
                <tr>
                  <th
                    scope="col"
                    class="px-6 py-4 text-left text-xs font-bold text-gray-700 uppercase tracking-wider"
                  >
                    User
                  </th>
                  <th
                    scope="col"
                    class="px-6 py-4 text-left text-xs font-bold text-gray-700 uppercase tracking-wider"
                  >
                    GitHub Username
                  </th>
                  <th
                    scope="col"
                    class="px-6 py-4 text-left text-xs font-bold text-gray-700 uppercase tracking-wider"
                  >
                    Repository
                  </th>
                  <th
                    scope="col"
                    class="px-6 py-4 text-left text-xs font-bold text-gray-700 uppercase tracking-wider"
                  >
                    PR Number
                  </th>
                  <th
                    scope="col"
                    class="px-6 py-4 text-left text-xs font-bold text-gray-700 uppercase tracking-wider"
                  >
                    Status
                  </th>
                  <th
                    scope="col"
                    class="px-6 py-4 text-left text-xs font-bold text-gray-700 uppercase tracking-wider"
                  >
                    Reward
                  </th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-100">
                <tr v-for="contribution in contributions" :key="contribution.id" class="hover:bg-blue-50 transition-colors duration-150">
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 font-mono">
                    <Address :address="contribution.owner" />
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-semibold text-gray-900">
                    {{ contribution.github_username }}
                  </td>
                  <td class="px-6 py-4 text-sm text-gray-500 max-w-xs truncate">
                    <a :href="contribution.repo_url" target="_blank" class="text-blue-600 hover:text-blue-800 hover:underline font-medium flex items-center gap-1">
                      {{ contribution.repo_url.replace('https://github.com/', '') }}
                      <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/>
                      </svg>
                    </a>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    <a :href="contribution.pr_url" target="_blank" class="text-blue-600 hover:text-blue-800 hover:underline font-semibold flex items-center gap-1">
                      #{{ contribution.pr_number }}
                      <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/>
                      </svg>
                    </a>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm">
                    <span
                      :class="contribution.verified ? 'bg-green-100 text-green-800 border-green-200' : 'bg-yellow-100 text-yellow-800 border-yellow-200'"
                      class="px-3 py-1 rounded-full text-xs font-semibold border"
                    >
                      {{ contribution.verified ? "✓ Verified" : "⏳ Pending" }}
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span class="text-sm font-bold text-green-600 bg-green-50 px-3 py-1 rounded-lg">
                      {{ contribution.reward_amount }} tokens
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
            <div v-if="contributions.length === 0" class="px-6 py-12 text-center">
              <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
              </svg>
              <p class="mt-4 text-gray-500 font-medium">No contributions yet</p>
              <p class="text-sm text-gray-400">Be the first to submit your contribution!</p>
            </div>
          </div>
        </div>

        <!-- Leaderboard -->
        <div class="bg-white/90 backdrop-blur-sm shadow-xl overflow-hidden rounded-2xl col-span-3 border border-gray-200">
          <div class="px-6 py-5 bg-gradient-to-r from-yellow-50 to-orange-50 border-b border-gray-200">
            <h2 class="text-2xl font-bold text-gray-900 flex items-center gap-2">
              <svg class="w-6 h-6 text-yellow-500" fill="currentColor" viewBox="0 0 20 20">
                <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
              </svg>
              Leaderboard
            </h2>
            <p class="text-xs text-gray-600 mt-1">Top contributors</p>
          </div>
          <div class="overflow-hidden">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gradient-to-r from-gray-50 to-gray-100">
                <tr>
                  <th
                    scope="col"
                    class="px-4 py-3 text-left text-xs font-bold text-gray-700 uppercase tracking-wider"
                  >
                    Rank
                  </th>
                  <th
                    scope="col"
                    class="px-4 py-3 text-left text-xs font-bold text-gray-700 uppercase tracking-wider"
                  >
                    Address
                  </th>
                  <th
                    scope="col"
                    class="px-4 py-3 text-left text-xs font-bold text-gray-700 uppercase tracking-wider"
                  >
                    Rewards
                  </th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-100">
                <tr v-for="(user, index) in leaderboard" :key="user.address" class="hover:bg-yellow-50 transition-colors duration-150">
                  <td class="px-4 py-3 whitespace-nowrap">
                    <span
                      :class="{
                        'bg-gradient-to-r from-yellow-400 to-yellow-500 text-white': index === 0,
                        'bg-gradient-to-r from-gray-300 to-gray-400 text-white': index === 1,
                        'bg-gradient-to-r from-orange-400 to-orange-500 text-white': index === 2,
                        'bg-gray-100 text-gray-700': index > 2
                      }"
                      class="inline-flex items-center justify-center w-8 h-8 rounded-full font-bold text-sm shadow-sm"
                    >
                      {{ index === 0 ? '🥇' : index === 1 ? '🥈' : index === 2 ? '🥉' : index + 1 }}
                    </span>
                  </td>
                  <td class="px-4 py-3 whitespace-nowrap text-xs font-mono text-gray-600">
                    <Address :address="user.address" />
                  </td>
                  <td class="px-4 py-3 whitespace-nowrap">
                    <span class="text-sm font-bold text-green-600 bg-green-50 px-2 py-1 rounded-lg">
                      {{ user.rewards }}
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
            <div v-if="leaderboard.length === 0" class="px-6 py-8 text-center">
              <svg class="mx-auto h-10 w-10 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
                <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
              </svg>
              <p class="mt-3 text-gray-500 text-sm font-medium">No rewards yet</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Submit Contribution Modal -->
      <div
        v-if="showSubmitModal"
        class="fixed inset-0 bg-black/60 backdrop-blur-md overflow-y-auto h-full w-full flex items-center justify-center z-50 p-4"
        @click.self="showSubmitModal = false"
      >
        <div class="relative p-8 border-2 border-purple-200 w-full max-w-lg shadow-2xl rounded-3xl bg-white transform transition-all duration-300 scale-100 animate-fade-in">
          <!-- Header -->
          <div class="mb-6">
            <div class="flex items-center justify-between mb-3">
              <h3 class="text-3xl font-extrabold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent flex items-center gap-2">
                <svg class="w-8 h-8 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
                </svg>
                Submit Contribution
              </h3>
              <button
                @click="showSubmitModal = false"
                class="text-gray-400 hover:text-gray-600 transition-colors"
              >
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                </svg>
              </button>
            </div>
            <div class="bg-gradient-to-r from-green-50 to-emerald-50 border-l-4 border-green-500 p-3 rounded-r-lg">
              <p class="text-sm text-gray-700 flex items-center gap-2">
                <svg class="w-5 h-5 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M8.433 7.418c.155-.103.346-.196.567-.267v1.698a2.305 2.305 0 01-.567-.267C8.07 8.34 8 8.114 8 8c0-.114.07-.34.433-.582zM11 12.849v-1.698c.22.071.412.164.567.267.364.243.433.468.433.582 0 .114-.07.34-.433.582a2.305 2.305 0 01-.567.267z"/>
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-13a1 1 0 10-2 0v.092a4.535 4.535 0 00-1.676.662C6.602 6.234 6 7.009 6 8c0 .99.602 1.765 1.324 2.246.48.32 1.054.545 1.676.662v1.941c-.391-.127-.68-.317-.843-.504a1 1 0 10-1.51 1.31c.562.649 1.413 1.076 2.353 1.253V15a1 1 0 102 0v-.092a4.535 4.535 0 001.676-.662C13.398 13.766 14 12.991 14 12c0-.99-.602-1.765-1.324-2.246A4.535 4.535 0 0011 9.092V7.151c.391.127.68.317.843.504a1 1 0 101.511-1.31c-.563-.649-1.413-1.076-2.354-1.253V5z" clip-rule="evenodd"/>
                </svg>
                <span class="font-semibold">Earn {{ rewardPerContribution }} tokens</span> for each verified PR
              </p>
            </div>
          </div>

          <!-- Form Fields -->
          <div class="space-y-4 mb-6">
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-1">GitHub Username</label>
              <input
                v-model="githubUsername"
                class="w-full px-4 py-3 border-2 border-gray-200 rounded-xl shadow-sm focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all"
                placeholder="e.g., octocat"
              />
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-1">Organization/Owner</label>
              <input
                v-model="organization"
                class="w-full px-4 py-3 border-2 border-gray-200 rounded-xl shadow-sm focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all"
                placeholder="e.g., facebook"
              />
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-1">Project Name</label>
              <input
                v-model="projectName"
                class="w-full px-4 py-3 border-2 border-gray-200 rounded-xl shadow-sm focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all"
                placeholder="e.g., react"
              />
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-1">Repository URL</label>
              <input
                v-model="repoUrl"
                class="w-full px-4 py-3 border-2 border-gray-200 rounded-xl shadow-sm focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all"
                placeholder="https://github.com/facebook/react"
              />
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-1">Pull Request Number</label>
              <input
                v-model="prNumber"
                class="w-full px-4 py-3 border-2 border-gray-200 rounded-xl shadow-sm focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all"
                placeholder="e.g., 12345"
                type="number"
              />
            </div>
          </div>

          <!-- Requirements Box -->
          <div class="bg-gradient-to-br from-blue-50 to-purple-50 border-2 border-blue-200 rounded-2xl p-4 mb-6">
            <p class="text-blue-900 font-bold mb-2 flex items-center gap-2">
              <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"/>
              </svg>
              Requirements:
            </p>
            <ul class="space-y-1 text-blue-800 text-sm">
              <li class="flex items-start gap-2">
                <span class="text-green-600 font-bold">✓</span>
                <span>PR must be merged</span>
              </li>
              <li class="flex items-start gap-2">
                <span class="text-green-600 font-bold">✓</span>
                <span>PR author must match your GitHub username</span>
              </li>
              <li class="flex items-start gap-2">
                <span class="text-green-600 font-bold">✓</span>
                <span>Repository must be a legitimate open source project</span>
              </li>
              <li class="flex items-start gap-2">
                <span class="text-green-600 font-bold">✓</span>
                <span>Each PR can only be claimed once</span>
              </li>
            </ul>
          </div>

          <!-- Actions -->
          <div class="flex gap-3">
            <div v-if="!submittingContribution" class="flex gap-3 w-full">
              <button
                @click="submitContribution"
                class="flex-1 bg-gradient-to-r from-green-500 to-emerald-500 hover:from-green-600 hover:to-emerald-600 text-white font-bold py-3 px-6 rounded-xl shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-200 flex items-center justify-center gap-2"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                </svg>
                Submit
              </button>
              <button
                @click="showSubmitModal = false"
                class="flex-1 bg-gray-200 hover:bg-gray-300 text-gray-800 font-bold py-3 px-6 rounded-xl transition-all duration-200"
              >
                Cancel
              </button>
            </div>
            <div v-else class="w-full">
              <div class="bg-gradient-to-r from-blue-50 to-purple-50 rounded-xl p-6 text-center">
                <div class="flex justify-center mb-3">
                  <div class="animate-spin rounded-full h-12 w-12 border-b-4 border-purple-600"></div>
                </div>
                <p class="text-lg font-semibold text-gray-800">Verifying contribution...</p>
                <p class="text-sm text-gray-600 mt-2">This may take a moment as we verify your PR with AI</p>
              </div>
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
