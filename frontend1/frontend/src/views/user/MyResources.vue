<template>
  <div class="my-resources p-4">
    <el-button type="primary" @click="goHome" icon="el-icon-arrow-left" class="mb-4">
      返回首页
    </el-button>

    <el-card>
      <el-tabs v-model="activeTab" type="border-card">
        <el-tab-pane label="我发布的问题" name="questions">
          <el-table :data="questions" stripe style="width: 100%">
            <el-table-column prop="id" label="ID" width="60" />
            <el-table-column prop="title" label="标题" />
            <el-table-column prop="reward" label="悬赏金额" width="100" />
            <el-table-column prop="status" label="状态" width="100" />
            <el-table-column prop="created_at" label="发布时间" width="180" />
            <el-table-column label="操作" width="100">
              <template #default="scope">
                <el-button size="small" type="text" @click="viewQuestion(scope.row)">查看</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>

        <el-tab-pane label="我购买的课程" name="courses">
          <el-row :gutter="20">
            <el-col :span="8" v-for="course in courses" :key="course.id">
              <el-card shadow="hover" class="course-card" @click="viewCourse(course)">
                <img
                  :src="course.cover"
                  alt="封面"
                  class="cover"
                  loading="lazy"
                />
                <h3>{{ course.title }}</h3>
                <p class="price">￥{{ course.price }}</p>
              </el-card>
            </el-col>
          </el-row>
        </el-tab-pane>
      </el-tabs>
    </el-card>

    <!-- 优化后的对话框组件 -->
    <el-dialog v-model="questionDialogVisible" title="问题详情" width="500px">
      <template v-if="selectedQuestion.title">
        <h3>{{ selectedQuestion.title }}</h3>
        <p><strong>悬赏：</strong>{{ selectedQuestion.reward }}</p>
        <p><strong>内容：</strong>{{ selectedQuestion.content }}</p>
        <p><strong>状态：</strong>{{ selectedQuestion.status }}</p>
        <p><strong>发布时间：</strong>{{ selectedQuestion.created_at }}</p>
      </template>
    </el-dialog>

    <el-dialog v-model="courseDialogVisible" title="课程详情" width="700px">
      <template v-if="selectedCourse.title">
        <h3>{{ selectedCourse.title }}</h3>
        <p>{{ selectedCourse.description }}</p>
        <video
          v-if="selectedCourse.video"
          :src="selectedCourse.video"
          controls
          style="width: 100%; margin-top: 15px; border-radius: 8px;"
        />
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import axios from 'axios'

const router = useRouter()
const activeTab = ref('questions')

const questions = ref([])
const courses = ref([])

const questionDialogVisible = ref(false)
const selectedQuestion = ref({})

const courseDialogVisible = ref(false)
const selectedCourse = ref({})

const fetchQuestions = async () => {
  try {
    const res = await axios.get('http://127.0.0.1:8000/api/users/user/my-questions/')
    questions.value = res.data.my_questions
  } catch (err) {
    ElMessage.error('获取问题列表失败')
  }
}

const fetchCourses = async () => {
  try {
    const res = await axios.get('http://127.0.0.1:8000/api/users/user/my-courses/')
    courses.value = res.data.purchased_courses
  } catch (err) {
    ElMessage.error('获取课程列表失败')
  }
}

const viewQuestion = (q) => {
  selectedQuestion.value = q
  questionDialogVisible.value = true
}

const viewCourse = (course) => {
  selectedCourse.value = course
  courseDialogVisible.value = true
}

const goHome = () => {
  router.push({ path: '/' })
}

onMounted(() => {
  fetchQuestions()
  fetchCourses()
})
</script>

<style scoped>
.my-resources {
  max-width: 1200px;
  margin: auto;
}

.cover {
  width: 100%;
  height: 180px;
  object-fit: cover;
  border-radius: 8px;
  margin-bottom: 10px;
  background: #f5f7fa; /* 添加加载背景色 */
}

.course-card {
  cursor: pointer;
  transition: transform 0.2s ease-in-out;
  will-change: transform;
  overflow: hidden;
}

.course-card:hover {
  transform: scale(1.02);
}

.price {
  font-weight: bold;
  color: #409eff;
}

/* 添加加载动画 */
@keyframes placeholderShimmer {
  0% { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}

.loading-placeholder {
  animation: placeholderShimmer 1.5s linear infinite;
  background: linear-gradient(90deg, #f0f2f5 25%, #e5e9ef 50%, #f0f2f5 75%);
  background-size: 200% 100%;
}
</style>
