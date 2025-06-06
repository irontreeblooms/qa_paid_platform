<script setup>
import { defineProps, defineEmits } from 'vue'

const props = defineProps(['questions', 'currentPage', 'pageSize', 'totalCount'])
const emit = defineEmits(['update:currentPage'])

const handlePageChange = (newPage) => {
  emit('update:currentPage', newPage) // 让父组件更新 currentPage
}
</script>

<template>
  <div>
    <div v-if="questions.length">
      <article v-for="question in questions" :key="question.id" class="question-item">
        <h3>{{ question.title }}</h3>
        <p>{{ question.description }}</p>
      </article>
    </div>
    <el-empty v-else description="暂无问题" />

    <!-- 分页 -->
    <el-pagination
      :current-page="currentPage"
      :page-size="pageSize"
      :total="totalCount"
      layout="prev, pager, next, jumper"
      background
      @current-change="handlePageChange"
    />
  </div>
</template>



<style scoped>
.zhihu-container {
  min-height: 100vh;
  background: #f6f6f6;
}

.main-header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  background: #fff;
  box-shadow: 0 1px 3px rgba(26,26,26,.1);
}

.nav-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
  height: 60px;
}

.left-nav {
  display: flex;
  align-items: center;
  gap: 32px;
}

.logo {
  color: #0084ff;
  font-size: 28px;
  font-weight: 600;
  margin: 0;
}

.right-nav {
  display: flex;
  align-items: center;
  gap: 24px;
}

.search-box {
  width: 320px;
  transition: width 0.3s;
}

.search-box:focus-within {
  width: 400px;
}

.user-avatar {
  cursor: pointer;
  transition: transform 0.2s;
}

.user-avatar:hover {
  transform: scale(1.05);
}

.content-wrapper {
  max-width: 1200px;
  margin: 80px auto 0;
  padding: 24px;
}

.question-list {
  background: #fff;
  border-radius: 8px;
  padding: 24px;
}

.question-card {
  padding: 20px;
  margin-bottom: 16px;
  border-radius: 4px;
  transition: box-shadow 0.3s;
  border-bottom: 1px solid #eee;
}

.question-card:hover {
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.question-title {
  margin: 0 0 12px;
  font-size: 18px;
}

.question-title a {
  color: #1a1a1a;
  text-decoration: none;
}

.question-title a:hover {
  color: #175199;
}

.question-content {
  color: #646464;
  font-size: 15px;
  line-height: 1.6;
  margin: 0 0 16px;
}

.question-meta {
  display: flex;
  align-items: center;
  gap: 24px;
  color: #8590a6;
  font-size: 14px;
}

.question-meta .el-icon {
  margin-right: 4px;
}

.pagination {
  margin-top: 32px;
  justify-content: center;
}
.visible-menu {
  flex: 1;
  min-width: 200px;
}

.el-menu--horizontal {
  display: flex !important;
  border-bottom: none;
}

.el-menu--horizontal > .el-menu-item {
  flex-shrink: 0;  /* 禁止菜单项收缩 */
  height: 60px;
  line-height: 60px;
  padding: 0 20px;
  font-size: 16px;
  color: #1a1a1a;
  border-bottom: 3px solid transparent;
  transition: all 0.3s;
}

/* 保持原有悬停样式 */
.el-menu--horizontal > .el-menu-item:hover {
  background: rgba(0, 132, 255, 0.08);
  border-bottom-color: #0084ff;
}

/* 保持激活状态样式 */
.el-menu--horizontal > .el-menu-item.is-active {
  color: #0084ff;
  border-bottom-color: #0084ff;
}

/* 调整导航容器布局 */
.nav-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
  height: 60px;
}

.left-nav {
  display: flex;
  align-items: center;
  gap: 32px;
  flex: 1;  /* 允许左侧导航扩展 */
}

.right-nav {
  display: flex;
  align-items: center;
  gap: 24px;
  flex-shrink: 0;  /* 禁止右侧导航收缩 */
}
</style>
