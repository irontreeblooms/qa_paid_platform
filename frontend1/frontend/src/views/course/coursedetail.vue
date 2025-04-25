<template>
  <div class="course-detail-container">
    <!-- 顶部返回按钮 & 课程标题 -->
    <div class="course-header">
      <el-button @click="goBack" text class="back-button">
          <el-icon><ArrowLeft /></el-icon> 返回
        </el-button>
    </div>

    <div v-if="loading" class="loading">
      <el-icon><Loading /></el-icon> 加载中...
    </div>

    <div v-else-if="course" class="course-detail">
      <img :src="'http://127.0.0.1:8000' + course.cover" alt="课程封面" class="course-cover" />
      <h2 class="course-title">{{ course.title }}</h2>
      <p class="course-description">{{ course.description }}</p>
      <p class="course-price">价格：{{ course.price }} 元</p>
      <el-button type="primary" @click="handlePurchase">购买课程</el-button>
    </div>

    <el-empty v-else description="课程信息未加载" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';
import { ElMessage } from 'element-plus';
import { ArrowLeft } from '@element-plus/icons-vue';
import { Loading } from '@element-plus/icons-vue';

const route = useRoute();
const router = useRouter();
const course = ref(null);
const loading = ref(true);

// 获取课程详情
const getCourseDetail = async (courseId) => {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/api/courses/detail/${courseId}/`);
    if (response.data && response.data[0]) {
      course.value = response.data[0]; // 从列表中获取第一个课程对象
    } else {
      ElMessage.error('课程未找到');
    }
  } catch (error) {
    ElMessage.error('加载课程详情失败');
    console.error('API Error:', error);
  } finally {
    loading.value = false;
  }
};

// 获取路由中的课程ID
const courseId = route.params.id;

// 生命周期钩子
onMounted(() => {
  getCourseDetail(courseId);
});

// 处理购买课程
const handlePurchase = () => {
  axios.post('http://127.0.0.1:8000/api/courses/purchase/', { course_id: course.value.id })
  .then(response => {
    if (response.data.success) {
      // 购买成功的处理逻辑
      console.log('购买成功');
    } else {
      // 购买失败的处理逻辑
      console.log('购买失败');
    }
  })
  .catch(error => {
    console.error('购买请求出错:', error);
  });
};

// 返回按钮的处理函数
const goBack = () => {
  router.push({ name: 'course' }); // 根据您的路由配置修改返回页面的名称
};
</script>

<style scoped>
/* 课程详情容器样式 */
.course-detail-container {
  max-width: 800px;
  margin: 40px auto;
  padding: 24px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

/* 顶部返回按钮样式 */
.course-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 2rem;
}

/* 返回按钮 */
.back-button {
  display: flex;
  justify-content: flex-start;  /* 水平靠左 */
  align-items: center;          /* 垂直居中 */
  color: #409eff;
  font-weight: 500;
}

.back-button:hover {
  color: #337ecc;
}

/* 课程封面、标题、描述等样式 */
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

/* 购买按钮样式 */
.el-button {
  margin-top: 20px;
  width: 100%;
}

/* 加载中提示样式 */
.loading {
  font-size: 18px;
  color: #666;
  display: flex;
  align-items: center;
}

.el-empty {
  text-align: center;
  margin-top: 40px;
}
</style>
