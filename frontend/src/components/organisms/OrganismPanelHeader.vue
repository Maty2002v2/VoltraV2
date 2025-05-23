<template>
    <header class="panel-header">
        <div class="panel-header__header">
            <img src="@/assets/logo-mini.png" alt="Logo" class="panel-header__logo" />
            <h1 class="panel-header__title">{{ title }}</h1>
        </div>
        <div class="panel-header__actions">
            <slot name="actions" />
        </div>
    </header>
</template>

<script setup>
    defineProps({
        title: {
            type: String,
            default: ''
        }
    });
</script>

<style lang="scss" scoped>
    .panel-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        height: 85px;

        &__header {
            display: flex;
            flex-direction: column;
        }

        &__logo {
            width: 69px;
        }

        &__title {
            margin: 0;
            color: #000000;
            font-size: 3.75rem;
            font-weight: 700;
        }

        &__actions {
            display: flex;
            align-items: center;
            gap: 30px;
        }
    }
</style>