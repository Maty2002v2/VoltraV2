<template>
    <div class="icon-box">
        <img :src="icon" alt="notification bell" class="icon" />
    </div>
</template>

<script setup>
    const props = defineProps({
        iconName: {
            type: Number,
            default: 0
        }
    });

    const icon = require(`@/assets/icons/${props.iconName}.png`);
</script>

<style lang="scss" scoped>
    .icon-box {
        position: relative;
        display: flex;
        justify-content: center;
        align-items: center;
        width: auto;
        height: 100%;
        padding: 13px;
        border-radius: 50%;
        border: 1px solid #F0F0F0;
        cursor: pointer;
        box-sizing: border-box;

        .icon {
            width: 100%;
            height: 100%;
        }
    }
</style>