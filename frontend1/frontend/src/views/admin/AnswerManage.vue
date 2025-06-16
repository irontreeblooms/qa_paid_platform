<template>
  <div>
    <h2 class="text-center">回答管理</h2>
    <table class="table">
      <thead>
        <tr>
          <th style="width: 20px;text-align: center;">ID</th>
          <th style="width: 20px;text-align: center;">问题ID</th>
          <th style="width: 200px;text-align: center;">回答内容</th>
          <th style="width: 20px;text-align: center;">状态</th>
          <th style="width: 20px;text-align: center;">操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="answer in answers" :key="answer.id">
          <td style="text-align: center;">{{ answer.id }}</td>
          <td style="text-align: center;">
            <span class="link-like" @click="openQuestionDetail(answer.question)">
              {{ answer.question }}
            </span>
          </td>
          <td style="text-align: center;">{{ answer.content }}</td>
          <td style="text-align: center;">{{ answer.status }}</td>
          <td style="text-align: center;">
            <button @click="deleteAnswer(answer.question,answer.id)" class="btn btn-danger">删除</button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- 分页组件 -->
    <div class="pagination">
      <button :disabled="currentPage === 1" @click="changePage(currentPage - 1)">上一页</button>
      <span>第 {{ currentPage }} 页 / 共 {{ totalPages }} 页</span>
      <button :disabled="currentPage === totalPages" @click="changePage(currentPage + 1)">下一页</button>
    </div>


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
      answers: [],
      dialogVisible: false,
      questionDetail: null,
      currentPage: 1,
      totalPages: 1
    }
  },
  methods: {
    async fetchAnswers(page = 1) {
      try {
        const response = await axios.get(`http://127.0.0.1:8000/api/admin/answers/?page=${page}`)
        this.answers = response.data.answers
        this.currentPage = response.data.current_page
        this.totalPages = response.data.total_pages
      } catch (error) {
        console.error('获取回答失败:', error)
      }
    },
    async deleteAnswer(questionId,answerId) {
      try {
        await axios.delete(`http://127.0.0.1:8000/api/questions/question/answer/${questionId}/?answerId=${answerId}`)
        this.fetchAnswers()
        ElMessage.success('操作成功')
      } catch (error) {
        console.error('删除失败:', error)
        ElMessage.error('操作失败')
      }
    },
    async openQuestionDetail(questionId) {
      try {
        const res = await axios.get(`http://127.0.0.1:8000/api/questions/question/detail/${questionId}/`)
        this.questionDetail = res.data
        this.dialogVisible = true
      } catch (error) {
        console.error('加载问题详情失败', error)
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
    },
    changePage(page) {
    this.fetchAnswers(page)
  }
  },
  mounted() {
    this.fetchAnswers()
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
  background-color: #f2f2f2;
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
.meta p {
  margin: 6px 0;
  color: #666;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
  gap: 10px;
}

.pagination button {
  padding: 5px 12px;
  background-color: #409eff;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.pagination button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}
.btn {
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  color: #fff;
  cursor: pointer;
}
/* 拒绝按钮：红色 */
.btn-danger {
  background-color: #f56c6c;
}

.btn-danger:hover {
  background-color: #dd6161;
}
</style>
