<template>
  <div>
    <h2 class="text-center">申述管理</h2>
    <table class="table">
      <thead>
        <tr>
          <th style="width: 10px;text-align: center;">申述ID</th>
          <th style="width: 10px;text-align: center;">用户</th>
          <th style="width: 200px;text-align: center;">目标</th>
          <th style="width: 150px;text-align: center;">申述理由</th>
          <th style="width: 10px;text-align: center;">状态</th>
          <th style="width: 60px;text-align: center;">操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="appeal in appeals" :key="appeal.id">
          <td style="text-align: center;">{{ appeal.id }}</td>
          <td style="text-align: center;">{{ appeal.user }}</td>
          <td style="text-align: center;">
            <span v-if="appeal.question">问题：{{ appeal.question }}</span>
            <span v-else>答案：{{ appeal.answer }}</span>
          </td>
          <td style="text-align: center;">{{ appeal.reason }}</td>
          <td style="text-align: center;">
            <span v-if="appeal.status === 'pending'" class="status pending">待处理</span>
            <span v-if="appeal.status === 'resolved'" class="status resolved">已解决</span>
            <span v-if="appeal.status === 'rejected'" class="status rejected">已驳回</span>
          </td>
          <td style="text-align: center;">
            <button
              v-if="appeal.status === 'pending'"
              @click="updateStatus(appeal.id, 'resolved')"
              class="btn btn-success"
            >
              通过
            </button>
            <button
              v-if="appeal.status === 'pending'"
              @click="updateStatus(appeal.id, 'rejected')"
              class="btn btn-danger"
            >
              驳回
            </button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- 分页 -->
<div class="pagination">
  <button class="btn" @click="changePage(currentPage - 1)" :disabled="currentPage === 1">上一页</button>
  <span style="margin: 0 10px;">第 {{ currentPage }} 页 / 共 {{ totalPages }} 页</span>
  <button class="btn" @click="changePage(currentPage + 1)" :disabled="currentPage === totalPages">下一页</button>
</div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { ElMessage } from 'element-plus'

const appeals = ref([])
const currentPage = ref(1)
const totalPages = ref(1)

// 获取申述数据
async function fetchAppeals(page = 1) {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/api/admin/appeals/?page=${page}`)
    appeals.value = response.data.appeals
    currentPage.value = response.data.current_page
    totalPages.value = response.data.total_pages
  } catch (error) {
    console.error('获取申述失败:', error)
    ElMessage.error('获取申述失败，请稍后重试')
  }
}

// 切换分页
function changePage(page) {
  if (page >= 1 && page <= totalPages.value) {
    fetchAppeals(page)
  }
}

// 更新申述状态
async function updateStatus(appealId, status) {
  try {
    await axios.put(`http://127.0.0.1:8000/api/admin/appeals/${appealId}/`, { status })
    ElMessage.success('申述状态更新成功')
    fetchAppeals(currentPage.value) // 保持在当前页刷新
  } catch (error) {
    console.error('更新申述状态失败:', error)
    ElMessage.error('更新申述状态失败，请稍后重试')
  }
}

// 初始化
onMounted(() => {
  fetchAppeals()
})
</script>


<style scoped>
.text-center {
  text-align: center;
  margin-bottom: 20px;
}

.table {
  width: 100%;
  border-collapse: collapse;
}

.table th,
.table td {
  border: 1px solid #ddd;
  padding: 8px;
}

.table th {
  background-color: #f4f4f4;
  text-align: center;
}

.status {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 4px;
  color: #fff;
  font-size: 12px;
}

.status.pending {
  background-color: #f0ad4e;
}

.status.resolved {
  background-color: #5cb85c;
}

.status.rejected {
  background-color: #d9534f;
}

.btn {
  padding: 4px 8px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  color: #fff;
  font-size: 14px;
}

.btn-success {
  background-color: #5cb85c;
}

.btn-danger {
  background-color: #d9534f;
}

.btn:hover {
  opacity: 0.8;
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
</style>