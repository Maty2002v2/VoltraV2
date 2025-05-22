<template>
    <aside>
        <nav class="sidebar">
            <ul class="sidebar__list">
                <li class="sidebar__logo">
                    <AtomLogo />
                </li>
                <li v-for="(item, index) in items" :key="index">
                    <MoleculeSidebarItem
                        :itemName="item.name"
                        :itemIcon="item.icon"
                        :itemLink="item.link"
                        :subItems="item.subItems"
                        :activeItemName="activeItemName"
                        @toggle="handleToggleItem"
                    />
                </li>
            </ul>
        </nav>
    </aside>
</template>

<script setup>
import { ref } from 'vue';

import MoleculeSidebarItem from '@/components/molecules/MoleculeSidebarItem.vue';
import AtomLogo from '@/components/atoms/AtomLogo.vue';

const items = [
    {
        name: 'PULPIT',
        icon: 'home',
        link: '/'
    },
    {
        name: 'MÓJ PANEL',
        icon: 'user',
        subItems: [
            {
                name: 'Klienci',
                link: '/my-data'
            },
            {
                name: 'PPE',
                link: '/panel/ppe'
            },
            {
                name: 'Biblioteka dokumentów',
                link: '/my-payments'
            },
            {
                name: 'Zgłoszenia',
                link: '/my-payments'
            },
            {
                name: 'Powiadomienia',
                link: '/my-payments'
            }
        ]
    },
    {
        name: 'ANALITYKA',
        icon: 'chart-histogram',
        subItems: [
            {
                name: 'Test 1',
                link: '/my-data'
            },
            {
                name: 'Test 2',
                link: '/my-orders'
            },
        ]
    },
    {
        name: 'ADMINISTRACJA',
        icon: 'admin',
    },
    {
        name: 'VOLTRA',
        icon: 'admin',
    }
];

const activeItemName = ref();
const handleToggleItem = (itemName) => {
    if (activeItemName.value === itemName) {
        activeItemName.value = null;
        return;
    }

    activeItemName.value = itemName;
};
</script>

<style lang="scss" scoped>
.sidebar {
    height: 100vh;
    background: #000000;

    &__logo {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 39px 52px 40px 52px;
    }

    &__list {
        list-style: none;
        padding: 0;
        margin: 0;
    }
}
</style>