<script setup>
const p = defineProps({
  props: null,
});
</script>

<template>
  <q-btn outline :to="p.props.toManga">Chapters</q-btn>
  <q-btn
    outline
    @click="$router.push(p.props.prevChapter)"
    :disable="!p.props.prevChapter"
    >Prev</q-btn
  >
  <q-btn
    outline
    @click="$router.push(p.props.nextChapter)"
    :disable="!p.props.nextChapter"
    >Next</q-btn
  >
</template>
