<template>
  <div class="course-detail-container">
    <!-- 顶部返回按钮 & 课程标题 -->
    <div class="course-header">
      <el-button @click="goBack" text class="back-button" >
        <el-icon><ArrowLeft /></el-icon> 返回
      </el-button>
      <h1 class="page-title">课程详情</h1>
    </div>

    <div v-if="loading" class="loading">
      <el-icon><Loading /></el-icon> 加载中...
    </div>

    <div v-else-if="course" class="course-detail">
      <img :src="'http://127.0.0.1:8000' + course.cover" alt="课程封面" class="course-cover" />
      <h2 class="course-title">视频标题：{{ course.title }}</h2>
      <p class="course-description">描述：{{ course.description }}</p>
      <p class="course-price">价格：<span>{{ course.price }}</span> 元</p>
      <hr class="divider" />
      <el-button type="primary" @click="handlePurchase" class="purchase-button">购买课程</el-button>
    </div>

    <el-empty v-else description="课程信息未加载" class="empty-state" />
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
      ElMessage.success('购买成功');
    } else {
      ElMessage.error('购买失败');
    }
  })
  .catch(error => {
    ElMessage.error('购买请求出错');
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
  max-width: 900px;
  margin: 40px auto;
  padding: 24px;
  background-color: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.course-header {
  display: flex;
  align-items: center;
  justify-content: center; /* 让标题居中 */
  margin-bottom: 24px;
}

.page-title {
  font-size: 24px;
  font-weight: bold;
  color: #333;
  text-align: center;
  margin: 0;
}

.back-button {
  position: absolute;
  left: 350px;
  color: #409eff;
  font-weight: 500;
}

.back-button:hover {
  color: #337ecc;
}

/* 加载中提示样式 */
.loading {
  font-size: 18px;
  color: #666;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 300px;
}

/* 课程封面、标题、描述等样式 */
.course-cover {
  width: 100%;
  height: 400px;
  object-fit: cover;
  border-radius: 12px;
  margin-bottom: 20px;
}

.course-title {
  font-size: 28px;
  font-weight: bold;
  color: #222;
  margin: 16px 0;
}

.course-description {
  font-size: 16px;
  line-height: 1.6;
  color: #555;
  margin: 12px 0;
}

.course-price {
  font-size: 20px;
  font-weight: bold;
  color: #ff4d4f;
}

.course-price span {
  font-size: 24px;
  color: #f56c6c;
}

/* 分隔线样式 */
.divider {
  margin: 24px 0;
  border: none;
  border-top: 1px solid #ddd;
}

/* 按钮样式 */
.purchase-button {
  width: 100%;
  height: 48px;
  font-size: 16px;
  font-weight: bold;
  background-color: #409eff;
  border-color: #409eff;
  color: #fff;
  border-radius: 8px;
}

.purchase-button:hover {
  background-color: #66b1ff;
  border-color: #66b1ff;
}

.purchase-button:active {
  background-color: #3a8ee6;
  border-color: #3a8ee6;
}

/* 空状态样式 */
.empty-state {
  margin-top: 40px;
  text-align: center;
}

@media (max-width: 768px) {
  .course-detail-container {
    padding: 16px;
    margin: 20px auto;
  }

  .course-cover {
    height: 250px;
  }

  .course-title {
    font-size: 22px;
  }

  .course-price {
    font-size: 18px;
  }

  .purchase-button {
    font-size: 14px;
  }
}
</style>