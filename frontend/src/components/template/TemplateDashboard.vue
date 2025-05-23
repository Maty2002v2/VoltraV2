<template>
    <layout-default>
        <organism-panel-header title="Witaj Michalina">
            <template #actions>
                <molecule-presenting-the-amount-box icon-name="wallet" title="Bieżące saldo" amount="288,55 zł" />
                <molecule-presenting-the-amount-box icon-name="arrears" title="Zaległości" amount="125,55 zł" link="#" />
            </template>
        </organism-panel-header>
    </layout-default>
</template>

<script setup>
    import LayoutDefault from '@/layout/LayoutDefault.vue';
    import OrganismPanelHeader from '@/components/organisms/OrganismPanelHeader.vue';
    import MoleculePresentingTheAmountBox from '@/components/molecules/MoleculePresentingTheAmountBox.vue';
</script>