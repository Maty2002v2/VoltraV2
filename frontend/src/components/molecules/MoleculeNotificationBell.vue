<template>
    <div class="notification-bell">
        <img :src="icon" alt="notification bell" class="bell-icon" />
    </div>
</template>

<script setup>
const props = defineProps({
    count: {
        type: Number,
        default: 0
    }
});

const icon = require(`@/assets/icons/${ props.count ? 'bell-notification' : 'bell'}.png`);
</script>

<style lang="scss" scoped>
.notification-bell {
    position: relative;
    display: flex;
    justify-content: center;
    align-items: center;
    width: 35px;
    height: 35px;
    border-radius: 50%;
    border: 1px solid #F0F0F0;
    cursor: pointer;
    box-sizing: border-box;

    .bell-icon {
        width: 14px;
        height: 15px;
    }
}
</style>