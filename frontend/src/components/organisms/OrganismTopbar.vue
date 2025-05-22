<template>
    <header class="topbar">
      <div class="topbar__left">
        <slot name="title"></slot>
      </div>
      <div class="topbar__right">
        <NotificationBell />
        <UserMenu />
      </div>
    </header>
  </template>
  
  <script setup>
  import NotificationBell from '@/components/molecules/MoleculeNotificationBell.vue'
  import UserMenu from '@/components/molecules/MoleculeUserMenu.vue'
  </script>
  
  <style lang="scss" scoped>
  .topbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    height: 65px;
    padding: 15px 40px;
    background-color: #fff;
    border-bottom: 1px solid #eee;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.03);
    box-sizing: border-box;
  
    &__left {
      font-size: 20px;
      font-weight: 600;
      color: #222;
    }
  
    &__right {
      display: flex;
      align-items: center;
      gap: 10px;
    }
  }
  </style>