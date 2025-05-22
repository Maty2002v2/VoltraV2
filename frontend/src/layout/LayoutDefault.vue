<template>
    <div class="layout-default">
        <OrganismSidebar />
    </div>
</template>

<script setup>
import OrganismSidebar from '@/components/organisms/OrganismSidebar.vue';
</script>

<style lang="scss" scoped>
.layout-default {
    display: grid;
    grid-template-columns: 240px 1fr;
}
</style>