<template>
    <div :class="classObject">
        <component
            :is="itemLink ? 'router-link' : 'div'"
            :to="itemLink || undefined"
            class="sidebar-item__link"
            @click="() => emit('toggle', itemName)"
        >
            <img v-if="itemIcon.length" :src="iconPath" class="sidebar-item__icon"/>
            <span>{{ itemName }}</span>
            <img v-if="subItems.length" :src="openStateIcon" class="sidebar-item__open-state-icon"/>
        </component>

        <div v-if="subItems.length && isOpen" class="sidebar-item__subitems">
            <MoleculeSidebarItem
                v-for="(subItem, index) in subItems"
                :key="index"
                :itemName="subItem.name"
                :itemLink="subItem.link"
                :activeItemName="activeItemName"
            />
        </div>
    </div>
</template>

<script setup>
import { computed } from 'vue';

const emit = defineEmits(['toggle']);

const props = defineProps({
    itemName: {
        type: String,
        required: true
    },
    itemIcon: {
        type: String,
        default: ''
    },
    itemLink: {
        type: String,
        default: ''
    },
    subItems: {
        type: Object,
        default: () => []
    },
    activeItemName: {
        type: String,
        default: ''
    }
});

const iconPath = computed(() => require(`@/assets/icons/${props.itemIcon}.png`));

const isOpen = computed(() => props.activeItemName === props.itemName);
const openStateIcon = computed(() => require(`@/assets/icons/${isOpen.value ? 'minus' : 'plus'}.png`));

const classObject = computed(() => {
    return {
        'sidebar-item': true,
        'sidebar-item--focus': isOpen.value
    };
});
</script>

<style lang="scss" scoped>
.sidebar-item {
    -webkit-user-select: none; /* Safari */
    -ms-user-select: none; /* IE 10 and IE 11 */
    user-select: none; /* Standard syntax */

    &:hover,
    &--focus {
        & >.sidebar-item__link {
            padding-left: 26px;
            background-color: #151515;
            border-left: 2px #FFD000 solid;
            box-sizing: border-box;
        }
    }

    &__link {
        display: flex;
        align-items: center;
        gap: 15px;
        padding: 15px 28px;
        text-decoration: none;
        color: #FFFFFF;
        font-size: 0.75rem;
        font-weight: 700;
        cursor: pointer;
    }

    &__icon {
        width: 18px;
        height: 18px;
    }

    &__open-state-icon {
        width: 8px;
        height: 8px;
        margin-left: auto;
    }

    &__subitems {
        margin-top: 7px;
        margin-bottom: 18px;

        .sidebar-item__link {
            padding: 7px 0px 7px 65px;
            color: #D0D0D0;
            font-weight: 500;

            &:hover,
            &--focus,
            &.router-link-active {
                padding-left: 65px;
                border-left: unset;
                background-color: unset;
                color: #FFFFFF;
                font-weight: 500;
            }
        }
    }
}
</style>