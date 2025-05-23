<template>
<div class="user-menu" @click="toggleDropdown" ref="menu">
    <avatar :src="avatarSrc" />
    <span class="user-menu__name">{{ name }}</span>
    <icon-chevron :open="dropdownOpen" />

    <transition name="fade">
        <div v-if="dropdownOpen" class="user-menu__dropdown">
            <ul>
            <li><a href="#">Profil</a></li>
            <li><a href="#">Ustawienia</a></li>
            <li><a href="#">Wyloguj</a></li>
            </ul>
        </div>
    </transition>
</div>
</template>

<script setup>
    import { onMounted, onUnmounted, ref, computed } from 'vue';
    import Avatar from '@/components/atoms/AtomAvatar.vue';
    import IconChevron from '@/components/atoms/AtomIconChevron.vue';

    const name = 'Michalina';
    const avatarSrc = computed(()=> require('@/assets/tmp-avatar.png'));
    const dropdownOpen = ref(false);
    const menu = ref(null);

    const toggleDropdown = () => {
        dropdownOpen.value = !dropdownOpen.value;
    }

    const handleClickOutside = (event) => {
        if (menu.value && !menu.value.contains(event.target)) {
            dropdownOpen.value = false;
        }
    };
    onMounted(() => {
        document.addEventListener('click', handleClickOutside);
    });
    onUnmounted(() => {
        document.removeEventListener('click', handleClickOutside);
    });
</script>

<style lang="scss" scoped>
    .user-menu {
        position: relative;
        display: flex;
        align-items: center;
        gap: 10px;
        cursor: pointer;
        user-select: none;

        &__name {
            font-weight: 600;
            font-size: 0.75rem;
            color: #000000;
        }

        &__dropdown {
            position: absolute;
            top: calc(100% + 8px);
            right: 0;
            width: 160px;
            background-color: #fff;
            border-radius: 8px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
            z-index: 100;

            ul {
                margin: 0;
                padding: 0;
                list-style: none;

            li {
                border-bottom: 1px solid #eee;

                &:last-child {
                    border-bottom: none;
                }

                a {
                    display: block;
                    padding: 10px 16px;
                    font-size: 14px;
                    color: #333;
                    text-decoration: none;

                &:hover {
                    background-color: #f7f7f7;
                }
                }
            }
            }
        }
    }

    .fade-enter-active,
    .fade-leave-active {
        transition: opacity 0.15s ease;
    }
    .fade-enter-from,
    .fade-leave-to {
        opacity: 0;
    }
</style>
  