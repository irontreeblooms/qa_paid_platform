<template>
  <div>
    <h2 class="text-center">课程审核</h2>
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
            <button @click="approveCourse(course.id)" class="btn btn-success">通过</button>
            <button @click="rejectCourse(course.id)" class="btn btn-danger">拒绝</button>
          </td>
        </tr>
      </tbody>
    </table>

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
    async fetchCourses() {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/admin/courses/')
        this.courses = response.data.courses
      } catch (error) {
        console.error('获取课程失败:', error)
      }
    },
    async approveCourse(courseId) {
      await this.updateCourseStatus(courseId, 'approved')
    },
    async rejectCourse(courseId) {
      await this.updateCourseStatus(courseId, 'rejected')
    },
    async updateCourseStatus(courseId, status) {
      try {
        await axios.post('http://127.0.0.1:8000/api/admin/courses/', {
          course_id: courseId,
          status: status
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

</style>
