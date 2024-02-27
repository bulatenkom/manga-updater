<template>
  <suspense>
    <router-view />
    <template #fallback> Loading... </template>
  </suspense>
</template>

<script setup lang="ts"></script>
