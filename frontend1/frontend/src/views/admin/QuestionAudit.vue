<template>
  <div>
    <h2 class="text-center">问题审核</h2>
    <table class="table">
      <thead>
        <tr>
          <th>ID</th>
          <th>标题</th>
          <th>状态</th>
          <th>操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="question in questions" :key="question.id">
          <td>
            <span class="link-like" @click="openDetail(question.id)">
              {{ question.id }}
            </span>
          </td>
          <td>{{ question.title }}</td>
          <td>{{ question.status }}</td>
          <td>
            <button @click="approveQuestion(question.id)" class="btn btn-success">通过</button>
            <button @click="rejectQuestion(question.id)" class="btn btn-danger">拒绝</button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- 问题详情弹窗 -->
    <el-dialog v-model="dialogVisible" title="问题详情" width="700px" :close-on-click-modal="false" center>
      <div v-if="questionDetail" class="dialog-content">
        <h3 class="detail-title">标题：{{ questionDetail.title }}</h3>
        <p class="detail-content">问题内容：{{ questionDetail.content }}</p>
        <el-descriptions :column="2" border>
          <el-descriptions-item label="奖励">¥{{ questionDetail.reward }}</el-descriptions-item>
          <el-descriptions-item label="状态">
            {{ questionDetail.status === 'open' ? '已通过' : questionDetail.status === 'false' ? '已拒绝' : '待审核' }}
          </el-descriptions-item>
          <el-descriptions-item label="创建时间" :span="2">
            {{ formatDate(questionDetail.created_at) }}
          </el-descriptions-item>
        </el-descriptions>
      </div>
      <template #footer>
        <el-button @click="dialogVisible = false">关闭</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import axios from 'axios'
import { ElMessage } from 'element-plus'

export default {
  data() {
    return {
      questions: [],
      dialogVisible: false,
      questionDetail: null
    }
  },
  methods: {
    async fetchQuestions() {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/admin/questions/')
        this.questions = response.data.questions
      } catch (error) {
        console.error('获取问题失败:', error)
      }
    },
    async approveQuestion(questionId) {
      await this.updateQuestionStatus(questionId, 'open')
    },
    async rejectQuestion(questionId) {
      await this.updateQuestionStatus(questionId, 'false')
    },
    async updateQuestionStatus(questionId, status) {
      try {
        await axios.post('http://127.0.0.1:8000/api/admin/questions/', {
          question_id: questionId,
          status: status
        })
        this.fetchQuestions()
        ElMessage.success('操作成功')
      } catch (error) {
        console.error('审核失败:', error)
        ElMessage.error('操作失败')
      }
    },
    async openDetail(id) {
      try {
        const res = await axios.get(`http://127.0.0.1:8000/api/questions/question/detail/${id}/`)
        this.questionDetail = res.data
        this.dialogVisible = true
      } catch (error) {
        console.error('加载详情失败', error)
      }
    },
    formatDate(timestamp) {
      const date = new Date(timestamp)
      return date.toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      })
    }
  },
  mounted() {
    this.fetchQuestions()
  }
}
</script>

<style scoped>
.text-center {
  text-align: center;
}
.table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}
.table th, .table td {
  border: 1px solid #ddd;
  padding: 8px;
}
.table th {
  background-color: #f9f9f9;
  text-align: left;
}
.btn {
  margin-right: 5px;
}
.link-like {
  color: #409eff;
  cursor: pointer;
  text-decoration: underline;
}
.dialog-content {
  padding: 10px;
}
.detail-title {
  text-align: left;
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 16px;
  color: #333;
}
.detail-content {
  margin-bottom: 20px;
  line-height: 1.6;
  color: #555;
}
</style>
