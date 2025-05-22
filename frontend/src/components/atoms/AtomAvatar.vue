<template>
    <img class="avatar" :src="src" alt="Avatar" />
</template>

<script setup>
defineProps({
    src: {
        type: String,
        required: true
    }
})
</script>

<style lang="scss" scoped>
.avatar {
    width: 35px;
    height: 35px;
    border-radius: 50%;
    object-fit: cover;
}
</style>
  