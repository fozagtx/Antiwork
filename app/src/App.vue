<template>
  <Suspense>
    <template #default>
      <ContributionsScreen />
    </template>
    <template #fallback>
      <div class="flex items-center justify-center h-screen">
        <div class="spinner">Loading...</div>
      </div>
    </template>
  </Suspense>
</template>

<script setup>
import ContributionsScreen from "./components/ContributionsScreen.vue";
</script>
