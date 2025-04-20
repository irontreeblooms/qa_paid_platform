<template>
  <div class="my-resources p-4">
    <!-- 返回按钮保持不变 -->

    <el-card>
      <el-tabs v-model="activeTab" type="border-card">
        <!-- 问题表格添加防抖加载 -->
        <el-tab-pane label="我发布的问题" name="questions">
          <el-table
            v-if="tableMounted"
            :data="questions"
            stripe
            style="width: 100%"
          >
            <!-- 表格列保持不变 -->
          </el-table>
          <div v-else class="loading-placeholder"></div>
        </el-tab-pane>

        <!-- 课程卡片保持不变 -->
      </el-tabs>
    </el-card>

    <!-- 优化后的问题对话框 -->
    <el-dialog
      v-model="questionDialogVisible"
      title="问题详情"
      width="500px"
      :append-to-body="true"
      @opened="handleQuestionOpened"
    >
      <div v-if="questionContentReady" class="dialog-content">
        <h3>{{ selectedQuestion.title }}</h3>
        <p><strong>悬赏：</strong>{{ selectedQuestion.reward }}</p>
        <p><strong>内容：</strong>{{ selectedQuestion.content }}</p>
        <p><strong>状态：</strong>{{ selectedQuestion.status }}</p>
        <p><strong>发布时间：</strong>{{ selectedQuestion.created_at }}</p>
      </div>
      <div v-else class="loading-placeholder"></div>
    </el-dialog>

    <!-- 优化后的课程对话框 -->
    <el-dialog
      v-model="courseDialogVisible"
      title="课程详情"
      width="700px"
      :append-to-body="true"
      @opened="handleCourseOpened"
    >
      <div v-if="courseContentReady" class="dialog-content">
        <h3>{{ selectedCourse.title }}</h3>
        <p>{{ selectedCourse.description }}</p>
        <video
          v-if="selectedCourse.video"
          :src="selectedCourse.video"
          controls
          style="width: 100%; margin-top: 15px; border-radius: 8px;"
        />
      </div>
      <div v-else class="loading-placeholder"></div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import axios from 'axios'

const router = useRouter()

// 状态管理
const activeTab = ref('questions')
const tableMounted = ref(false)

const questions = ref([])
const courses = ref([])

// 问题对话框相关
const questionDialogVisible = ref(false)
const selectedQuestion = ref({})
const questionContentReady = ref(false)
let questionResizeTimer = null

// 课程对话框相关
const courseDialogVisible = ref(false)
const selectedCourse = ref({})
const courseContentReady = ref(false)
let courseResizeTimer = null

// 数据获取方法保持不变...

// 对话框控制方法
const viewQuestion = (q) => {
  questionContentReady.value = false
  selectedQuestion.value = q
  questionDialogVisible.value = true
}

const handleQuestionOpened = () => {
  clearTimeout(questionResizeTimer)
  questionResizeTimer = setTimeout(() => {
    questionContentReady.value = true
  }, 50)
}

const viewCourse = (course) => {
  courseContentReady.value = false
  selectedCourse.value = course
  courseDialogVisible.value = true
}

const handleCourseOpened = () => {
  clearTimeout(courseResizeTimer)
  courseResizeTimer = setTimeout(() => {
    courseContentReady.value = true
  }, 50)
}

// 初始化加载
onMounted(() => {
  setTimeout(() => {
    tableMounted.value = true
  }, 100)
  fetchQuestions()
  fetchCourses()
})
</script>

<style scoped>
/* 原有样式保持不变 */

.loading-placeholder {
  height: 200px;
  animation: placeholderShimmer 1.5s linear infinite;
  background: linear-gradient(90deg, #f0f2f5 25%, #e5e9ef 50%, #f0f2f5 75%);
  background-size: 200% 100%;
  border-radius: 8px;
}

.dialog-content {
  position: relative;
  min-height: 200px;
}

@keyframes placeholderShimmer {
  0% { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}
</style>
