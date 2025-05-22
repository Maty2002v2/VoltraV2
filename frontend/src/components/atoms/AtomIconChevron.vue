<template>
    <img :src="require('@/assets/icons/arrow-down.png')" class="icon-chevron" :class="{ open }" />
</template>

<script setup>
defineProps({
    open: {
        type: Boolean,
        default: false
    }
})
</script>

<style lang="scss" scoped>
.icon-chevron {
    transition: transform 0.2s ease;

    &.open {
        transform: rotate(180deg);
    }
}
</style>
  