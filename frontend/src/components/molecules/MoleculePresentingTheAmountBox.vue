<template>
    <div class="presenting-the-mmount-box">
        <atom-icon :icon-name="iconName" />
        <div class="presenting-the-mmount-box__content">
            <p class="presenting-the-mmount-box__title">{{ title }}</p>
            <p class="presenting-the-mmount-box__amount">{{ amount }}</p>
        </div>
        <router-link v-if="link.length" :href="link" class="presenting-the-mmount-box__link">
            <img src="@/assets/icons/lead-arrow.png" alt="Arrow" />
        </router-link>
    </div>
</template>

<script setup>
    import AtomIcon from '@/components/atoms/AtomIcon.vue';

    defineProps({
        iconName: {
            type: String,
            default: ''
        },
        title: {
            type: String,
            default: ''
        },
        amount: {
            type: String,
            default: ''
        },
        link: {
            type: String,
            default: ''
        }
    });
</script>

<style lang="scss" scoped>
    .presenting-the-mmount-box {
        position: relative;
        display: grid;
        grid-template-columns: 59px 1fr;
        gap: 15px;
        padding: 13px 79px 13px 16px;
        background: #FFFFFF;
        border-radius: 5px;

        &__content {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: flex-start;
        }

        &__title {
            margin: 0;
            color: #0A0A0A;
            font-size: 0.75rem;
        }

        &__amount {
            margin: 0;
            color: #0A0A0A;
            font-size: 1.25rem;
            font-weight: 700;
        }

        &__link {
            position: absolute;
            top: 10px;
            right: 10px;
        }
    }
</style>