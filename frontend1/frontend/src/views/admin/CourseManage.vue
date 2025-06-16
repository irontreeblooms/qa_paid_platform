<template>
  <div>
    <h2 class="text-center">课程管理</h2>
    <div style="text-align: center; margin: 20px 0;">
  <input
    v-model="searchKeyword"
    @keyup.enter="fetchQuestions(1)"
    placeholder="请输入课堂标题关键词"
    style="padding: 6px 12px; border: 1px solid #ccc; border-radius: 4px; width: 200px;"
  />
  <button @click="fetchCourses(1)" class="btn btn-primary" style="margin-left: 10px;">
    搜索
  </button>
</div>

    <table class="table">
      <thead>
        <tr>
          <th style="width: 20px;text-align: center;">ID</th>
          <th style="width: 50px;text-align: center;">标题</th>
          <th style="width: 300px;text-align: center;">描述</th>
          <th style="width: 30px;text-align: center;">价格</th>
          <th style="width: 30px;text-align: center;">状态</th>
          <th style="width: 50px;text-align: center;">操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="course in courses" :key="course.id">
          <td style="text-align: center;">
            <span class="link-like" @click="openCourseDetail(course.id)">
              {{ course.id }}
            </span>
          </td>
          <td style="text-align: center;">{{ course.title }}</td>
          <td style="text-align: center;">{{ course.description }}</td>
          <td style="text-align: center;">{{ course.price }}</td>
          <td style="text-align: center;">{{ course.status }}</td>
          <td style="text-align: center;">
            <button @click="deleteCourse(course.id)" class="btn btn-danger">删除</button>
          </td>
        </tr>
      </tbody>
    </table>

        <div class="pagination">
      <button :disabled="currentPage === 1" @click="changePage(currentPage - 1)">上一页</button>
      <span>第 {{ currentPage }} 页 / 共 {{ totalPages }} 页</span>
      <button :disabled="currentPage === totalPages" @click="changePage(currentPage + 1)">下一页</button>
    </div>

    <!-- 课程详情弹窗 -->
    <el-dialog v-model="dialogVisible" width="800px">
      <template #header>
        <h3 style="text-align: center; width: 100%;">课程详情</h3>
      </template>
      <div v-if="courseDetail">
        <img :src="'http://127.0.0.1:8000' + courseDetail.cover" alt="课程封面" class="course-cover" />
        <video
        v-if="courseDetail.video"
        class="course-video"
        controls
        :src="'http://127.0.0.1:8000' +courseDetail.video"
        >
          您的浏览器不支持视频播放。
        </video>

        <h2 class="course-title">课程标题：{{ courseDetail.title }}</h2>
        <p class="course-description">课程描述：{{ courseDetail.description }}</p>
        <p class="course-price">课程价格：{{ courseDetail.price }} 元</p>
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
      courses: [],
      dialogVisible: false,
      courseDetail: null
    }
  },
  methods: {
    async fetchCourses(page = 1) {
      try {
        const response = await axios.get(`http://127.0.0.1:8000/api/courses/list/`,{
      params: { page , search: this.searchKeyword}, // 添加 search 参数
    })
        this.courses = response.data.courses
        this.currentPage = response.data.current_page
        this.totalPages = response.data.num_pages
      } catch (error) {
        console.error('获取课程失败:', error)
      }
    },
    async deleteCourse(courseId) {
      try {
        await axios.delete(`http://127.0.0.1:8000/api/courses/list/`, {
            data: {
            course_id: courseId
            }
        })
        this.fetchCourses() // 重新获取课程列表
        ElMessage.success('操作成功')
      } catch (error) {
        console.error('审核失败:', error)
        ElMessage.error('操作失败')
      }
    },
    async openCourseDetail(courseId) {
      try {
        const response = await axios.get(`http://127.0.0.1:8000/api/courses/detail/${courseId}/`)
        if (response.data) {
          this.courseDetail = response.data[0]
          this.dialogVisible = true
        } else {
          ElMessage.error('课程详情未找到')
        }
      } catch (error) {
        console.error('加载课程详情失败:', error)
        ElMessage.error('加载课程详情失败')
      }
    },
    changePage(page) {
    this.fetchCourses(page)
  }
  },
  mounted() {
    this.fetchCourses()
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
.course-cover {
  width: 100%;
  height: 300px;
  object-fit: cover;
  border-radius: 8px;
}
.course-title {
  font-size: 24px;
  font-weight: bold;
  margin: 16px 0;
}
.course-description {
  font-size: 16px;
  color: #555;
  margin: 12px 0;
}
.course-price {
  font-size: 20px;
  font-weight: bold;
  color: #ff4d4f;
  margin: 12px 0;
}

.course-video {
  width: 100%;
  height: 400px;
  margin-top: 20px;
  border-radius: 8px;
  background-color: #000;
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
