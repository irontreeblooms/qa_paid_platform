<template>
  <div class="zhihu-container">
    <!-- 导航栏 -->
    <header class="main-header">
      <div class="nav-container">
        <div class="left-nav">
          <h1 class="logo">问知</h1>
          <el-menu
            :default-active="activeNav"
            mode="horizontal"
            @select="handleNavSelect"
            class="visible-menu"
            :collapse="false"
          >
            <el-menu-item index="home">首页</el-menu-item>
            <el-menu-item index="course">课程</el-menu-item>

          </el-menu>
        </div>

        <div class="right-nav">
          <el-input
            v-model="searchKeyword"
            placeholder="请在这里搜索课程"
            class="search-box"
            @keyup.enter="handleSearch"
            clearable
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
          <el-button type="primary" @click="openUploadDialog">上传课程</el-button>



          <el-dropdown trigger="click" @command="handleUserCommand">
            <el-avatar :size="36" :src="user.avatar" class="user-avatar" />
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="profile">
                  <el-icon><User /></el-icon>个人资料
                </el-dropdown-item>
                <el-dropdown-item command="wallet">
                  <el-icon><User /></el-icon>钱包
                </el-dropdown-item>
                <el-dropdown-item command="resource">
                  <el-icon><FolderOpened /></el-icon>我的资源
                </el-dropdown-item>
                <el-dropdown-item divided command="logout">
                  <el-icon><SwitchButton /></el-icon>退出登录
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </div>
    </header>


            <!-- 上传课程弹窗 -->
        <el-dialog v-model="uploadDialogVisible" title="上传课程" width="500px">
          <el-form :model="uploadForm" label-width="80px">
            <el-form-item label="课程标题">
              <el-input v-model="uploadForm.title" />
            </el-form-item>
            <el-form-item label="课程描述">
              <el-input v-model="uploadForm.description" type="textarea" />
            </el-form-item>
            <el-form-item label="价格">
              <el-input v-model="uploadForm.price" type="number" />
            </el-form-item>
            <el-form-item label="上传视频">
              <el-upload
                class="upload-demo"
                :action="null"
                :auto-upload="false"
                :show-file-list="true"
                :on-change="handleFileChange"
                :limit="1"
              >
                <el-button type="primary">选择文件</el-button>
                <el-form-item label="上传封面">
                <el-upload
                  class="upload-demo"
                  :action="null"
                  :auto-upload="false"
                  :show-file-list="true"
                  :on-change="handleCoverChange"
                  :limit="1"
                >
                  <el-button type="primary">选择封面</el-button>
                </el-upload>
              </el-form-item>

              </el-upload>
            </el-form-item>
          </el-form>
          <template #footer>
            <el-button @click="uploadDialogVisible = false">取消</el-button>
            <el-button type="primary" @click="submitUpload">提交</el-button>
          </template>
        </el-dialog>




<!-- 课程内容区域 -->
<div v-if="loading" class="loading">
  <el-icon><Loading /></el-icon> 加载中...
</div>

<div v-else-if="courses.length > 0" class="course-container">
  <div class="course-grid">
    <div v-for="course in courses" :key="course.id" class="course-card">
      <div class="cover-container">
        <img
          v-if="course.cover"
          :src="'http://127.0.0.1:8000' + course.cover"
          alt="课程封面"
          class="course-cover"
        />
      </div>
      <div class="course-content">
        <h3 class="course-title clickable" >
          {{ course.title }}
        </h3>
        <div class="course-footer">
          <span class="course-price">课程价格：{{ course.price }}</span>
          <el-button size="small" type="primary" class="study-btn" @click="router.push(`/coursedetail/${course.id}`)">查看详情</el-button>
        </div>
      </div>
    </div>
  </div>
  <!-- 分页控件 -->
      <el-pagination
        v-if="totalPages > 1"
        layout="prev, pager, next"
        :current-page="currentPage"
        :page-size="pageSize"
        :total="totalCourses"
        @current-change="loadCourses"
        class="pagination"
      />
</div>

<el-empty v-else description="暂无课程数据" />



  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { ElMessage } from 'element-plus';
import { Search, User, FolderOpened, SwitchButton, Loading } from '@element-plus/icons-vue';
import Cookies from "js-cookie";

const router = useRouter();


// 响应式数据
const activeNav = ref('course');
const searchKeyword = ref('');
const courses = ref([]);
const loading = ref(false);
const currentPage = ref(1); // 当前页码
const totalCourses = ref(0); // 总记录数
const totalPages = ref(0); // 总页数
const pageSize = ref(12); // 每页记录数

// 加载课程数据
const loadCourses = async (page = 1) => {
  try {
    loading.value = true;
    currentPage.value = page;
    const response = await axios.get("http://127.0.0.1:8000/api/courses/list/", {
      params: { page },
    });

    courses.value = response.data.courses;
    totalCourses.value = response.data.count;
    totalPages.value = response.data.num_pages;
  } catch (error) {
    ElMessage.error("加载课程失败");
    console.error("API Error:", error);
  } finally {
    loading.value = false;
  }
};


const uploadDialogVisible = ref(false);
const uploadForm = ref({ title: '', description: '', price: '', video: null });

const openUploadDialog = () => {
  uploadDialogVisible.value = true;
};

const handleFileChange = (file) => {
  uploadForm.value.video = file.raw;
};


const submitUpload = async () => {
  if (!uploadForm.value.video) {
    ElMessage.error("请上传视频文件");
    return;
  }

  const formData = new FormData();
  formData.append('title', uploadForm.value.title);
  formData.append('description', uploadForm.value.description);
  formData.append('price', uploadForm.value.price);
  formData.append('video', uploadForm.value.video);
  if (uploadForm.value.cover) {
    formData.append('cover', uploadForm.value.cover);  // ✅ 添加封面图
  }

  try {
    const response = await axios.post('http://127.0.0.1:8000/api/courses/list/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
    ElMessage.success(response.data.message);
    uploadDialogVisible.value = false;
    loadCourses(); // ✅ 上传成功后刷新列表
  } catch (error) {
    ElMessage.error(error.response?.data?.error || '上传失败');
  }
};


// 用户数据（模拟）
const user = ref({
  avatar: 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png'
});

// 处理导航选择
const handleNavSelect = (index) => {
  if (index === 'home') {
    router.push('/home');
  } else if (index === 'course') {
    router.push('/course');
    loadCourses();
  }
};


// 用户命令处理
const handleUserCommand = (command) => {
  switch(command) {
    case 'profile':
      router.push({ name: 'profile' })
      break
    case 'resource':
      router.push('/resource')
      break
    case 'wallet':
      router.push('/wallet')
      break
    case 'logout':
      handleLogout()
      break
  }
}

// 修改后的退出登录方法
const handleLogout = async () => {
  try {
      // 清除存储在 cookie 中的 token
    Cookies.remove('token');  // 假设 token 存储在 cookie 中，名称是 'token'
    // 清除其他存储的 cookie
    Cookies.remove('username');  // 示例：清除用户名的 cookie

    // 清除 localStorage 或 sessionStorage 中的其他数据
    localStorage.removeItem('token');
    sessionStorage.removeItem('token');
    await axios.post("http://127.0.0.1:8000/api/users/user/logout/")
    router.push({ name: 'Login' })
    ElMessage.success('已退出登录')
  } catch (error) {
    ElMessage.error('账号未登录，请重新登陆')
    router.push({ name: 'Login' })
  }
}




// 处理搜索
const handleSearch = () => {
  loadCourses(1, searchKeyword.value); // 搜索时从第一页开始
};

//课程封面上传
const handleCoverChange = (file) => {
  uploadForm.value.cover = file.raw;
};

// 生命周期钩子
onMounted(() => {
  loadCourses();
});
</script>

<style scoped>

.zhihu-container {
  min-height: 100vh;
  background: #f6f6f6;
}

/* 导航栏 */
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

.search-box {
  width: 320px;
  transition: width 0.3s;
}

.search-box:focus-within {
  width: 400px;
}

.user-avatar {
  cursor: pointer;
  transition: transform 0.2s;
}

/* 课程内容 */
.content-wrapper {
  max-width: 1200px;
  margin: 120px auto 0; /* 增加上方的间距，将第一排课程与导航栏之间的间距增大 */
  padding: 24px;
  display: flex;
  flex-direction: column;
  align-items: center;
}


.loading {
  font-size: 18px;
  color: #666;
  display: flex;
  align-items: center;
}

.course-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 16px;
}

.course-card {
  background: #fff;
  border-radius: 8px;
  padding: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.course-title {
  font-size: 18px;
  font-weight: bold;
}

.course-video {
  width: 100%;
  height: 150px;
  border-radius: 8px;
}

.course-description {
  font-size: 14px;
  color: #666;
  margin: 8px 0;
}

.course-price {
  font-size: 16px;
  font-weight: bold;
  color: #ff4d4f;
}

.visible-menu {
  flex: 1;
  min-width: 200px;
}

.el-menu--horizontal {
  display: flex !important;
  border-bottom: none;
}

.el-menu--horizontal > .el-menu-item {
  flex-shrink: 0;  /* 禁止菜单项收缩 */
  height: 60px;
  line-height: 60px;
  padding: 0 20px;
  font-size: 16px;
  color: #1a1a1a;
  border-bottom: 3px solid transparent;
  transition: all 0.3s;
}

/* 保持原有悬停样式 */
.el-menu--horizontal > .el-menu-item:hover {
  background: rgba(0, 132, 255, 0.08);
  border-bottom-color: #0084ff;
}

/* 保持激活状态样式 */
.el-menu--horizontal > .el-menu-item.is-active {
  color: #0084ff;
  border-bottom-color: #0084ff;
}

/* 调整导航容器布局 */
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
  flex: 1;  /* 允许左侧导航扩展 */
}

.right-nav {
  display: flex;
  align-items: center;
  gap: 24px;
  flex-shrink: 0;  /* 禁止右侧导航收缩 */
}
/* 课程容器 */
.course-container {
  max-width: 1280px;
  margin: 100px auto 40px;
  padding: 0 20px;
}

/* 课程网格布局 */
.course-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px;
  justify-content: center;
}

/* 课程卡片 */
.course-card {
  background: #fff;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  display: flex;
  flex-direction: column;
}

.course-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.12);
}

/* 封面容器 */
.cover-container {
  position: relative;
  padding-top: 56.25%; /* 16:9 比例 */
  background: #f5f7fa;
}

.course-cover {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* 课程内容 */
.course-content {
  padding: 16px;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.course-title {
  font-size: 16px;
  line-height: 1.4;
  margin: 0 0 12px;
  color: #1a1a1a;
  flex: 1;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.course-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: auto;
}

.course-price {
  font-size: 18px;
  font-weight: 600;
  color: #ff4d4f;
}

.study-btn {
  padding: 8px 16px;
  border-radius: 20px;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .course-grid {
    grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
    gap: 16px;
  }

  .course-price {
    font-size: 16px;
  }
}
.pagination {
  margin-top: 32px;
  justify-content: center;
}
</style>
