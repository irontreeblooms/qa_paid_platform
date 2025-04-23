<template>
  <div class="zhihu-container">
    <!-- 导航栏 -->
    <header class="main-header">
      <div class="nav-container">
        <div class="left-nav">
          <h1 class="logo">问知</h1>
          <el-menu
            :default-active="activeNav"
            mode="horizontal"
            @select="handleNavSelect"
            class="visible-menu"
            :collapse="false"
          >
            <el-menu-item index="home">首页</el-menu-item>
            <el-menu-item index="course">课程</el-menu-item>

          </el-menu>
        </div>

        <div class="right-nav">
          <el-input
            v-model="searchKeyword"
            placeholder="请在这里搜索问题"
            class="search-box"
            @keyup.enter="handleSearch"
            clearable
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
          <el-button type="primary" @click="openAskDialog">提问</el-button>



          <el-dropdown trigger="click" @command="handleUserCommand">
            <el-avatar :size="36" :src="user.avatar" class="user-avatar" />
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="profile">
                  <el-icon><User /></el-icon>个人资料
                </el-dropdown-item>
                <el-dropdown-item command="wallet">
                  <el-icon><User /></el-icon>钱包
                </el-dropdown-item>
                <el-dropdown-item command="resource">
                  <el-icon><FolderOpened /></el-icon>我的资源
                </el-dropdown-item>
                <el-dropdown-item divided command="logout">
                  <el-icon><SwitchButton /></el-icon>退出登录
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </div>
    </header>

        <el-dialog v-model="askDialogVisible" title="提问" width="500px">
      <el-form :model="questionForm" label-width="80px">
        <el-form-item label="标题">
          <el-input v-model="questionForm.title" placeholder="请输入问题标题" />
        </el-form-item>
        <el-form-item label="内容">
          <el-input v-model="questionForm.content" type="textarea" placeholder="请输入问题内容" />
        </el-form-item>
        <el-form-item label="悬赏">
          <el-input-number v-model="questionForm.reward" :min="0" />
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="askDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitQuestion">提交</el-button>
      </template>
    </el-dialog>

    <!-- 内容区域 -->
    <main class="content-wrapper">
      <div v-loading="loading" class="question-list">
        <template v-if="questions.length > 0">
          <article
            v-for="question in questions"
            :key="question.id"
            class="question-card"
          >
            <h3 class="question-title">
              <router-link :to="`/questiondetail/${question.id}`">
                {{ question.title }}
              </router-link>
            </h3>
            <p class="question-content">{{ truncateContent(question.content) }}</p>
            <div class="question-meta">
              <span class="answer-count">
                <el-icon><ChatDotRound /></el-icon>
                {{ question.answer_count }} 个回答
              </span>
              <span class="view-count">
                <el-icon><View /></el-icon>
                {{ question.view_count }} 次浏览
              </span>
              <time class="create-time">{{ formatTime(question.created_at) }}</time>
            </div>
          </article>

          <el-pagination
            v-model:current-page="currentPage"
            :page-size="pageSize"
            :total="totalCount"
            :pager-count="5"
            layout="prev, pager, next, jumper"
            background
            @current-change="loadQuestions"
            class="pagination"
          />
        </template>

        <el-empty v-else description="暂无问题" />
      </div>
    </main>
  </div>
</template>


<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios, {request} from 'axios'
import {
  ElMessage,
  ElIcon
} from 'element-plus'
import {
  Search,
  User,
  FolderOpened,
  SwitchButton,
  ChatDotRound,
  View
} from '@element-plus/icons-vue'
import Cookies from 'js-cookie';

// 配置axios
axios.defaults.withCredentials = true
axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFToken'

const router = useRouter()

// 响应式状态
const activeNav = ref('home')
const searchKeyword = ref('')
const questions = ref([])
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(10)
const totalCount = ref(0)
const user = ref({
  avatar: 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png',
  name: '用户昵称'
})

// API配置
const API_BASE = 'http://127.0.0.1:8000/api/questions/question/list/'

// 加载问题列表
const loadQuestions = async () => {
  try {
    loading.value = true
    const params = {
      page: currentPage.value,
      search: searchKeyword.value
    }

    const response = await axios.get(API_BASE, { params })
    const { questions: data, count } = response.data

    questions.value = data
    totalCount.value = count
  } catch (error) {
    ElMessage.error('加载问题失败')
    console.error('API Error:', error)
  } finally {
    loading.value = false
  }
}

// 搜索处理
const handleSearch = () => {
  currentPage.value = 1
  loadQuestions()
}

// 控制弹窗显示
const askDialogVisible = ref(false)

// 提问表单
const questionForm = ref({
  title: '',
  content: '',
  reward: 0
})


// 打开提问弹窗
const openAskDialog = () => {
  askDialogVisible.value = true
}


// 修改后的提交问题方法
const submitQuestion = async () => {
  if (!questionForm.value.title || !questionForm.value.content) {
    ElMessage.error('标题和内容不能为空')
    return
  }

  try {
    await axios.post(API_BASE, questionForm.value)
    ElMessage.success('问题发布成功')
    askDialogVisible.value = false
    questionForm.value = { title: '', content: '', reward: 0 }
    loadQuestions()
  } catch (error) {
    ElMessage.error('发布失败，请稍后重试')
    console.error('提交错误:', error)
  }
}


// 用户命令处理
const handleUserCommand = (command) => {
  switch(command) {
    case 'profile':
      router.push({ name: 'profile' })
      break
    case 'resource':
      router.push('/resource')
      break
    case 'wallet':
      router.push('/wallet')
      break
    case 'logout':
      handleLogout()
      break
  }
}

const handleNavSelect = (index) => {
  if (index === 'home') {
    router.push('/home');
  } else if (index === 'course') {
    router.push({name: 'course'});
  }
};




// 修改后的退出登录方法
const handleLogout = async () => {
  try {
      // 清除存储在 cookie 中的 token
    Cookies.remove('token');  // 假设 token 存储在 cookie 中，名称是 'token'
    // 清除其他存储的 cookie
    Cookies.remove('username');  // 示例：清除用户名的 cookie

    // 清除 localStorage 或 sessionStorage 中的其他数据
    localStorage.removeItem('token');
    sessionStorage.removeItem('token');
    await axios.post("http://127.0.0.1:8000/api/users/user/logout/")
    router.push({ name: 'Login' })
    ElMessage.success('已退出登录')
  } catch (error) {
    ElMessage.error('账号未登录，请重新登陆')
    router.push({ name: 'Login' })
  }
}


// 工具函数
const truncateContent = (text, length = 140) => {
  return text.length > length ? text.substring(0, length) + '...' : text
}

const formatTime = (timestamp) => {
  const date = new Date(timestamp)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  })
}


// 生命周期钩子
onMounted(() => {
  loadQuestions()
})
</script>

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
