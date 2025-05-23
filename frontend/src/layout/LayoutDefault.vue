<template>
    <div class="layout-default">
        <OrganismSidebar />
        <div>
            <OrganismTopbar />
            <div class="layout-default__content">
                <slot />
            </div>
        </div>
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

    &__content {
        padding: 40px;
        background: #f4f6f8;
    }
}
</style>