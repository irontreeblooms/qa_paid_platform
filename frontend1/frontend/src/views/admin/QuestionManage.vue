<template>
  <div>
    <h2 class="text-center">问题管理</h2>
    <div style="text-align: center; margin: 20px 0;">
  <input
    v-model="searchKeyword"
    @keyup.enter="fetchQuestions(1)"
    placeholder="请输入问题标题关键词"
    style="padding: 6px 12px; border: 1px solid #ccc; border-radius: 4px; width: 200px;"
  />
  <button @click="fetchQuestions(1)" class="btn btn-primary" style="margin-left: 10px;">
    搜索
  </button>
</div>

    <table class="table">
      <thead>
        <tr>
          <th style="width: 10px;text-align: center;">ID</th>
          <th style="width: 100px;text-align: center;">标题</th>
          <th style="width: 10px;text-align: center;">状态</th>
          <th style="width: 20px;text-align: center;">操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="question in questions" :key="question.id">
          <td style="text-align: center;">
            <span class="link-like" @click="openDetail(question.id)">
              {{ question.id }}
            </span>
          </td>
          <td style="text-align: center;">{{ question.title }}</td>
          <td style="text-align: center;">{{ question.status }}</td>
          <td style="text-align: center;">
            <button @click="deleteQuestion(question.id)" class="btn btn-danger">删除</button>
          </td>
        </tr>
      </tbody>
    </table>

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
      questions: [],
      dialogVisible: false,
      questionDetail: null,
      currentPage: 1,
      totalPages: 1
    }
  },
  methods: {
    async fetchQuestions(page = 1) {
      try {
        const response = await axios.get(`http://127.0.0.1:8000/api/questions/question/list/`,{
      params: {
        page: page,
        search: this.searchKeyword
      }
        })
        this.questions = response.data.questions
        this.currentPage = page  // 使用传入的 page 参数作为当前页
        this.totalPages = response.data.num_pages
      } catch (error) {
        console.error('获取问题失败:', error)
      }
    },

    async deleteQuestion(questionId) {
      try {
        await axios.delete(`http://127.0.0.1:8000/api/questions/question/detail/${questionId}/`)
        this.fetchQuestions()
        ElMessage.success('操作成功')
      } catch (error) {
        console.error('删除失败:', error)
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
    },
    changePage(page) {
    this.fetchQuestions(page)
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
.btn-primary {
  background-color: #67c23a;
}
.btn-primary:hover {
  background-color: #5daf34;
}

</style>
