<template>
    <div class="layout-default">
        <OrganismSidebar />
        <OrganismTopbar />
    </div>
</template>

<script setup>
import OrganismSidebar from '@/components/organisms/OrganismSidebar.vue';
import OrganismTopbar from '../components/organisms/OrganismTopbar.vue';
</script>

<style lang="scss" scoped>
.layout-default {
    display: grid;
    grid-template-columns: 240px 1fr;
}
</style>