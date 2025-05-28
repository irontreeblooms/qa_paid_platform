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
                <el-button v-if="question.status === 'pending' || question.status === 'open'" type="danger" :loading="question.loading" @click="revokeQuestion(question)">撤销发布</el-button>
                <el-button v-if="question.status === 'closed'" type="primary" :loading="question.loading" @click="republishQuestion(question)">重新发布</el-button>
                <el-button v-if="question.status !== 'open' && question.status !== 'pending'"  type="danger" @click="deleteQuestion(question)">删除问题</el-button>
              </div>
            </el-card>
            <el-empty v-if="questions.length === 0" description="暂无发布问题" />
          </div>
        </el-tab-pane>


        <!-- 我发布的课程 -->
        <el-tab-pane label="我发布的课程" name="publishedcourses">
          <div class="grid-container">
            <el-card
              v-for="course in courses"
              :key="course.id"
              class="course-card"
            >
              <img :src="'http://127.0.0.1:8000' + course.cover" alt="封面" class="course-cover" />
              <h3 class="course-title">{{ course.title }}</h3>
              <p class="course-price">价格：￥{{ course.price }}</p>
              <p class="course-status">状态：{{ course.status }}</p>
              <el-button type="primary" @click="openCourseDialog(course)">查看详情</el-button>
              <el-button v-if="course.status != 'closed'" type="danger" @click="revokeCourse(course)">撤销发布</el-button>
              <el-button v-if="course.status === 'closed'" type="primary" @click="republishCourse(course)">重新发布</el-button>
            </el-card>
            <el-empty v-if="courses.length === 0" description="暂无购买课程" />
          </div>
        </el-tab-pane>

        <!-- 我的回答 -->
        <el-tab-pane label="我的回答" name="myanswers">
          <div class="question-list">
            <el-card
              v-for="question in myanswers_questions"
              :key="question.id"
              class="question-card"
            >
              <div class="flex items-center justify-between">
                <div>
                  <h3 class="question-title">{{ question.title }}</h3>
                  <p class="question-content">悬赏：{{ question.reward }} ｜ 状态：{{ question.status }}</p>
                </div>
                <el-button type="primary" @click="openAnswerDialog(question)">查看详情</el-button>
                <el-button type="primary" :loading="question.loading" @click="openAppealDialog(question)">回答申述</el-button>
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
        <p>状态：{{ courseDetail.status }}</p>
        <video
          v-if="courseDetail.video"
          :src="'http://127.0.0.1:8000' + courseDetail.video"
          controls
          class="course-video"
        />
      <el-button
      v-if="courseDetail.video"
      type="primary"
      style="margin-top: 16px"
      @click="downloadVideo"
    >
      下载视频
    </el-button>
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
        <hr />
        <h4>回答列表：</h4>
        <div v-if="answers.length > 0">
          <div v-for="answer in answers" :key="answer.id">
            <p>回答内容：{{ answer.content }}</p>
            <p>回答者：{{ answer.user }}</p>
            <p>状态：{{ answer.status }}</p>
            <p>创建时间：{{ answer.created_at }}</p>
            <div class="button-group">
              <el-button type="success" @click="acceptAnswer(answer)">接受回答</el-button>
              <el-button type="danger" @click="rejectAnswer(answer)">拒绝回答</el-button>
            </div>
            <hr />
          </div>
        </div>
        <p v-else>暂无回答。</p>
      </template>
      <template #footer>
        <el-button @click="questionDialogVisible = false">返回</el-button>
      </template>
    </el-dialog>

    <!-- 回答问题详情弹窗 -->
    <el-dialog v-model="answerDialogVisible" width="50%" :title="answeredquestionDetail.title">
      <template #default>
        <p>内容：{{ answeredquestionDetail.content }}</p>
        <p>悬赏：{{ answeredquestionDetail.reward }}</p>
        <p>回答状态：{{ answeredquestionDetail.answers.status }}</p>
        <p>创建时间：{{ answeredquestionDetail.created_at }}</p>
        <p>如对用户的判决不满意，可点击申述</p>
        <hr />
        <h4>回答列表：</h4>
        <div v-if="answeredquestionDetail.answers.length > 0">
          <div v-for="answer in answeredquestionDetail.answers" :key="answer.id">
            <p>回答内容：{{ answer.content }}</p>
            <p>回答者：{{ answer.user }}</p>
            <p>状态：{{ answer.status }}</p>
            <p>创建时间：{{ answer.created_at }}</p>
            <hr />
          </div>
        </div>
        <p v-else>暂无回答。</p>
      </template>
      <template #footer>
        <el-button @click="answerDialogVisible = false">返回</el-button>
      </template>
    </el-dialog>


    <el-dialog v-model="appealDialogVisible" title="问题申述">
      <textarea
        v-model="appealReason"
        class="fixed-textarea"
        placeholder="请输入申述理由"
      ></textarea>
      <template #footer>
        <el-button @click="appealDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitAppeal">提交</el-button>
      </template>
    </el-dialog>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import {ElMessage} from "element-plus";

const activeTab = ref('courses')
const courses = ref([])
const questions = ref([])
const courseDialogVisible = ref(false)
const questionDialogVisible = ref(false)
const courseDetail = ref({})
const questionDetail = ref({});
const answeredquestionDetail = ref({
  title: '',
  content: '',
  reward: 0,
  status: '',
  created_at: '',
  answers: [], // 初始化为一个空数组
});
const answers = ref({})
const myanswers_questions = ref({})
const answerDialogVisible = ref(false)
const appealDialogVisible = ref(false)
const appealReason = ref('')
const currentQuestion = ref(null)

onMounted(() => {
  axios.get('http://127.0.0.1:8000/api/users/user/my-courses/').then(res => {
    courses.value = res.data.purchased_courses
  })
  axios.get('http://127.0.0.1:8000/api/users/user/my-questions/').then(res => {
    questions.value = res.data.my_questions
  })
  axios.get('http://127.0.0.1:8000/api/users/myanswers/').then(res => {
    myanswers_questions.value = res.data.myanswers_questions
  })
})

// 打开申述弹窗
function openAppealDialog(question) {
  currentQuestion.value = question
  appealDialogVisible.value = true
}

// 提交申述
function submitAppeal() {
  if (!appealReason.value.trim()) {
    ElMessage.error('申述理由不能为空')
    return
  }

  axios
    .post('http://127.0.0.1:8000/api/questions/question/appeal/', {
      question_id: currentQuestion.value.id,
      reason: appealReason.value,
    })
    .then(() => {
      ElMessage.success('申述提交成功')
      appealDialogVisible.value = false
      appealReason.value = ''
    })
    .catch((err) => {
      console.error('申述提交失败:', err)
      ElMessage.error('申述提交失败，请稍后重试')
    })
}

function openCourseDialog(course) {
  courseDetail.value = course
  courseDialogVisible.value = true
}

function openQuestionDialog(question) {
  questionDetail.value = question
  questionDialogVisible.value = true
    // 请求获取指定问题的回答
  axios.get(`http://127.0.0.1:8000/api/questions/question/answer/${question.id}/`)
    .then(res => {
      // 将返回的回答数据赋值给 answers
      answers.value = res.data;
    })
    .catch(err => {
      console.error("获取回答失败：", err);
    });
}

function openAnswerDialog(question) {
  answeredquestionDetail.value = question
  answerDialogVisible.value = true

}

function revokeQuestion(question) {
  // 设置加载状态，防止重复点击
  question.loading = true;

  // 发送请求，将状态更新为 'closed'
  axios
    .put(`http://127.0.0.1:8000/api/questions/question/detail/${question.id}/`, { status: 'closed' })
    .then(() => {
      ElMessage.success('撤销发布成功');
      // 更新问题状态为 'closed'
      question.status = 'closed';
    })
    .catch(err => {
      console.error('撤销发布失败:', err);
      ElMessage.error('撤销发布失败，请稍后重试');
    })
    .finally(() => {
      // 恢复按钮状态
      question.loading = false;
    });
}

function republishQuestion(question) {
  // 设置加载状态，防止重复点击
  question.loading = true;

  axios
    .put(`http://127.0.0.1:8000/api/questions/question/detail/${question.id}/`, { status: 'pending' })
    .then(() => {
      ElMessage.success('重新发布成功，待审核');
      // 更新问题状态为 'open'
      question.status = 'pending';
    })
    .catch(err => {
      console.error('重新发布失败:', err);
      ElMessage.error('重新发布失败，请稍后重试');
    })
    .finally(() => {
      // 恢复按钮状态
      question.loading = false;
    });
}

//删除问题
function deleteQuestion(question) {
  // 设置加载状态，防止重复点击
  question.loading = true;

  // 发送 DELETE 请求
  axios
    .delete(`http://127.0.0.1:8000/api/questions/question/detail/${question.id}/`)
    .then(() => {
      ElMessage.success('问题已成功删除');

      // 从列表中移除已删除的问题
      questions.value = questions.value.filter(q => q.id !== question.id);
    })
    .catch(err => {
      console.error('删除问题失败:', err);
      ElMessage.error('删除问题失败，请稍后重试');
    })
    .finally(() => {
      // 恢复按钮状态
      question.loading = false;
    });
}

//撤销课程发布
const revokeCourse = async (course) => {
  try {
    // 调用后端接口撤销课程发布
    const response = await axios.post(`http://127.0.0.1:8000/api/courses/revoke/`, {
      course_id: course.id,
    });

    if (response.data.success) {
      ElMessage.success('课程已成功撤销发布');
      // 可选：在页面上更新课程状态
      course.status = 'closed'; // 假设撤销后状态变为 'pending'
    } else {
      ElMessage.error('撤销失败，请稍后重试');
    }
  } catch (error) {
    console.error('撤销课程发布失败:', error);
    ElMessage.error('撤销失败，请稍后重试');
  }
};

// 重新发布课程的函数
const republishCourse = async (course) => {
  try {
    console.log(course)
    // 调用后端接口重新发布课程
    const response = await axios.post('http://127.0.0.1:8000/api/courses/republish/', {
      course: course,
    });

    if (response.data.success) {
      ElMessage.success('课程已成功重新发布');
      // 可选：在页面上更新课程状态
      course.status = 'pending';
    } else {
      ElMessage.error(response.data.message || '重新发布失败');
    }
  } catch (error) {
    console.error('重新发布课程失败:', error);
    ElMessage.error('重新发布失败，请稍后重试');
  }
};

function acceptAnswer(answer) {
  if (answer.status === 'user_approved') {
    ElMessage.warning('回答已接受，请勿继续操作')
    return
  }
  axios
    .post(`http://127.0.0.1:8000/api/questions/question/accept_answer/`, {
      answer_id: answer.id,
    })
    .then(() => {
      ElMessage.success('回答已被接受');
      // 可选：更新回答状态或界面
      answer.status = 'user_approved';
    })
    .catch(err => {
      console.error('接受回答失败:', err);
      ElMessage.error('接受回答失败，请稍后重试');
    });
}

function rejectAnswer(answer) {
  if (answer.status === 'user_rejected') {
    ElMessage.warning('回答已拒绝，请勿继续操作')
    return
  }
  axios
    .post(`http://127.0.0.1:8000/api/questions/question/reject_answer/`, {
      answer_id: answer.id,
    })
    .then(() => {
      ElMessage.success('回答已被拒绝');
      // 可选：更新回答状态或界面
      answer.status = 'user_rejected';
    })
    .catch(err => {
      console.error('拒绝回答失败:', err);
      ElMessage.error('拒绝回答失败，请稍后重试');
    });
}
function downloadVideo() {
  if (!courseDetail.value.video) return;
  // 移除 "/media/" 前缀
  const serverPath = courseDetail.value.video.replace(/^\/media\//, '');
  const url = 'http://127.0.0.1:8000/api/courses/download/video/' + encodeURIComponent(serverPath);
  // 直接跳转即可，后端会弹出下载
  const a = document.createElement('a');
  a.href = url;
  a.target = '_blank';
  // download属性对带Content-Disposition的接口可有可无
  a.download = serverPath.split('/').pop() || 'video.mp4';
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
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

.fixed-textarea {
  width: 100%; /* 占满弹窗宽度 */
  height: 200px; /* 固定高度 */
  resize: none; /* 禁止用户调整大小 */
  padding: 8px;
  font-size: 14px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  box-sizing: border-box;
  outline: none;
}

.fixed-textarea:focus {
  border-color: #409eff; /* 聚焦时改变边框颜色 */
}
</style>
