<template>
    <atom-icon :icon-name="count ? 'bell-notification' : 'bell'" />
</template>

<script setup>
    import AtomIcon from '@/components/atoms/AtomIcon.vue';

    const props = defineProps({
        count: {
            type: Number,
            default: 0
        }
    });
</script>