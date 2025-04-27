<template>
  <div class="question-detail-container">
    <!-- 问题详情 -->
    <div v-if="question">
      <h1>{{ question.title }}</h1>
      <p>{{ question.content }}</p>
      <div class="question-meta">
        <span>奖励: ¥{{ question.reward }}</span>
        <span>状态: {{ question.status }}</span>
        <span>创建时间: {{ formatDate(question.created_at) }}</span>
      </div>
    </div>

    <!-- 回答列表 -->
    <div v-if="answers.length > 0">
      <h2>回答</h2>
      <div v-for="answer in answers" :key="answer.id" class="answer-card">
        <div class="answer-user">
          <span>用户: {{ answer.user.username }}</span>
          <span>时间: {{ formatDate(answer.created_at) }}</span>
        </div>
        <p >{{ answer.content }}</p>
      </div>
    </div>

    <!-- 如果没有回答 -->
    <div v-else>
      <p>暂无回答</p>
    </div>

    <!-- 提交回答部分 -->
    <div class="answer-form" v-if="showAnswerForm">
      <textarea v-model="newAnswerContent" placeholder="请输入你的回答..." rows="4"></textarea>
      <el-button @click="submitAnswer" type="primary">提交回答</el-button>
    </div>
    <div v-else>
      <el-button @click="showAnswerForm = true" type="primary">回答问题</el-button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import { ElButton } from 'element-plus'

const route = useRoute()

// 响应式状态
const question = ref(null)
const answers = ref([])
const showAnswerForm = ref(false)  // 控制显示/隐藏输入框
const newAnswerContent = ref('')  // 新回答内容

// 格式化时间
const formatDate = (timestamp) => {
  const date = new Date(timestamp)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 获取问题详情
const fetchQuestionDetail = async () => {
  const questionId = route.params.id
  try {
    const response = await axios.get(`http://127.0.0.1:8000/api/questions/question/detail/${questionId}/`)
    question.value = response.data
  } catch (error) {
    console.error('获取问题详情失败', error)
  }
}

// 获取问题回答
const fetchAnswers = async () => {
  const questionId = route.params.id
  try {
    const response = await axios.get(`http://127.0.0.1:8000/api/questions/question/answer/${questionId}/`)
    answers.value = response.data
  } catch (error) {
    console.error('获取回答失败', error)
  }
}


// 提交回答
const submitAnswer = async () => {
  const questionId = route.params.id
  if (!newAnswerContent.value.trim()) {
    alert("回答内容不能为空")
    return
  }

  try {
    const response = await axios.post(`http://127.0.0.1:8000/api/questions/question/answer/${questionId}/`, {
      content: newAnswerContent.value
    })

    // 提交成功后清空输入框，刷新回答列表
    newAnswerContent.value = ''
    showAnswerForm.value = false
    fetchAnswers()  // 重新获取回答列表
  } catch (error) {
    console.error('提交回答失败', error)
    alert('提交回答失败，请稍后再试')
  }
}

// 生命周期钩子
onMounted(() => {
  fetchQuestionDetail()
  fetchAnswers()
})
</script>

<style scoped>
.question-detail-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 32px;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  border: 1px solid #ccc;  /* 边框颜色加深 */
}

h1 {
  font-size: 28px;
  color: #1a1a1a;
  margin-bottom: 16px;
  line-height: 1.4;
}

.question-meta {
  display: flex;
  gap: 20px;
  margin: 24px 0;
  padding: 16px 0;
  border-bottom: 1px solid #eee;
  font-size: 13px;
  color: #666;
}

h2 {
  font-size: 20px;
  color: #333;
  margin: 32px 0 24px;
  padding-bottom: 8px;
  border-bottom: 2px solid #409eff;
}

.answer-card {
  padding: 20px;
  margin-bottom: 16px;
  border: 1px solid #dcdfe6;  /* 边框颜色加深 */
  border-radius: 8px;
  transition: all 0.2s ease;
  background: #fafcff;
}

.answer-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 3px 8px rgba(64, 158, 255, 0.08);
}

.answer-user {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  font-size: 13px;
  color: #909399;
}

.answer-card p {
  font-size: 15px;
  line-height: 1.6;
  color: #303133;
  margin: 0;
}

.el-button {
  margin-left: auto;
  display: block;
  margin-top: 12px;
}

.answer-form {
  margin-top: 40px;
  border-top: 1px solid #eee;
  padding-top: 32px;
}

textarea {
  width: 100%;
  padding: 12px;
  font-size: 14px;
  margin-bottom: 16px;
  border: 1px solid #dcdfe6;
  border-radius: 6px;
  transition: border-color 0.2s;
  min-height: 100px;
}

textarea:focus {
  border-color: #409eff;
  outline: none;
  box-shadow: 0 0 0 2px rgba(64, 158, 255, 0.2);
}

[type="primary"] {
  background: #409eff;
  padding: 10px 24px;
}

/* 付费内容样式优化 */
.answer-card p > span {
  color: #f56c6c;
  margin-right: 12px;
  font-size: 13px;
}

/* 无回答样式 */
div[v-else] {
  text-align: center;
  padding: 40px 0;
  color: #999;
  font-size: 14px;
}
</style>
