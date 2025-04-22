<template>
  <div class="zhihu-container">
    <!-- 顶部导航栏 -->
    <header class="main-header">
      <div class="nav-container">
        <div class="left-nav">
          <h1 class="logo">问知</h1>
        </div>
        <div class="right-nav">
          <el-button type="primary" plain @click="$router.push('/home')">返回首页</el-button>
        </div>
      </div>
    </header>

    <!-- 主体内容区域 -->
    <div class="content-wrapper">
      <el-tabs v-model="activeTab">
        <!-- 我购买的课程 -->
        <el-tab-pane label="我购买的课程" name="courses">
          <div class="grid-container">
            <el-card
              v-for="course in courses"
              :key="course.id"
              class="course-card"
            >
              <img :src="'http://127.0.0.1:8000' + course.cover" alt="封面" class="course-cover" />
              <h3 class="course-title">{{ course.title }}</h3>
              <p class="course-price">价格：￥{{ course.price }}</p>
              <el-button type="primary" @click="openCourseDialog(course)">查看详情</el-button>
            </el-card>
            <el-empty v-if="courses.length === 0" description="暂无购买课程" />
          </div>
        </el-tab-pane>

        <!-- 我发布的问题 -->
        <el-tab-pane label="我发布的问题" name="questions">
          <div class="question-list">
            <el-card
              v-for="question in questions"
              :key="question.id"
              class="question-card"
            >
              <div class="flex items-center justify-between">
                <div>
                  <h3 class="question-title">{{ question.title }}</h3>
                  <p class="question-content">悬赏：{{ question.reward }} ｜ 状态：{{ question.status }}</p>
                </div>
                <el-button type="primary" @click="openQuestionDialog(question)">查看详情</el-button>
                <el-button type="primary" @click="openQuestionDialog(question)">撤销发布</el-button>
              </div>
            </el-card>
            <el-empty v-if="questions.length === 0" description="暂无发布问题" />
          </div>
        </el-tab-pane>
      </el-tabs>
    </div>

    <!-- 课程详情弹窗 -->
    <el-dialog v-model="courseDialogVisible" width="50%" :title="courseDetail.title">
      <template #default>
        <p>描述：{{ courseDetail.description }}</p>
        <p>价格：￥{{ courseDetail.price }}</p>
        <video
          v-if="courseDetail.video"
          :src="'http://127.0.0.1:8000' + courseDetail.video"
          controls
          class="course-video"
        />

      </template>
      <template #footer>
        <el-button @click="courseDialogVisible = false">返回</el-button>
      </template>
    </el-dialog>

    <!-- 问题详情弹窗 -->
    <el-dialog v-model="questionDialogVisible" width="50%" :title="questionDetail.title">
      <template #default>
        <p>内容：{{ questionDetail.content }}</p>
        <p>悬赏：{{ questionDetail.reward }}</p>
        <p>状态：{{ questionDetail.status }}</p>
        <p>创建时间：{{ questionDetail.created_at }}</p>
      </template>
      <template #footer>
        <el-button @click="questionDialogVisible = false">返回</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const activeTab = ref('courses')

const courses = ref([])
const questions = ref([])

const courseDialogVisible = ref(false)
const questionDialogVisible = ref(false)

const courseDetail = ref({})
const questionDetail = ref({})

onMounted(() => {
  axios.get('http://127.0.0.1:8000/api/users/user/my-courses/').then(res => {
    courses.value = res.data.purchased_courses
  })
  axios.get('http://127.0.0.1:8000/api/users/user/my-questions/').then(res => {
    questions.value = res.data.my_questions
  })
})

function openCourseDialog(course) {
  courseDetail.value = course
  courseDialogVisible.value = true
}

function openQuestionDialog(question) {
  questionDetail.value = question
  questionDialogVisible.value = true
}
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
  box-shadow: 0 1px 3px rgba(26, 26, 26, 0.1);
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

.content-wrapper {
  max-width: 1200px;
  margin: 61px auto 0;
  padding: 0 24px 40px;
  background: #f6f6f6;
}

.el-tab-pane {
  background: #fff;
  border-radius: 10px;
  padding: 32px;
  min-height: 400px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

/* 课程列表网格布局 */
.grid-container {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
}

.course-card {
  padding: 16px;
  text-align: center;
  border-radius: 10px;
  transition: box-shadow 0.2s ease;
}

.course-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.course-cover {
  width: 100%;
  height: 140px;
  object-fit: cover;
  border-radius: 8px;
  margin-bottom: 12px;
}

.course-title {
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 8px;
  color: #333;
}

.course-price {
  font-size: 14px;
  color: #999;
  margin-bottom: 10px;
}

.question-list {
  padding: 0;
}

.question-card {
  margin-bottom: 20px;
  padding: 20px;
  border-radius: 10px;
  border: 1px solid #e0e0e0;
  transition: box-shadow 0.2s ease;
}

.question-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.question-title {
  font-size: 20px;
  font-weight: 600;
  margin-bottom: 8px;
  color: #222;
}

.question-content {
  font-size: 15px;
  color: #666;
  line-height: 1.6;
}

.course-video {
  width: 100%;
  max-height: 400px;
  border-radius: 8px;
  margin-top: 12px;
  object-fit: contain;
}

</style>
