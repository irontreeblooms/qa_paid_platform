<template>
  <div class="profile-container">
    <el-card class="profile-card">
      <!-- 顶部返回按钮 & 标题 -->
      <div class="profile-header">
        <el-button @click="goBack" text class="back-button">
          <el-icon><ArrowLeft /></el-icon> 返回
        </el-button>
        <h2 class="profile-title">个人资料</h2>
      </div>

      <!-- 个人资料表单 -->
      <el-form :model="profileForm" ref="profileFormRef" label-width="100px" class="profile-form">
        <el-form-item label="昵称" prop="nickname">
          <el-input v-model="profileForm.nickname" placeholder="请输入昵称" clearable :disabled="!isEditing" />
        </el-form-item>

        <el-form-item label="简介" prop="bio">
          <el-input v-model="profileForm.bio" type="textarea" placeholder="填写个人简介" :disabled="!isEditing" />
        </el-form-item>

        <el-form-item label="地址" prop="address">
          <el-input v-model="profileForm.address" placeholder="请输入地址" clearable :disabled="!isEditing" />
        </el-form-item>

        <el-form-item label="行业" prop="industry">
          <el-input v-model="profileForm.industry" placeholder="请输入行业" clearable :disabled="!isEditing" />
        </el-form-item>

        <el-form-item label="性别" prop="gender">
          <el-select v-model="profileForm.gender" placeholder="选择性别" :disabled="!isEditing">
            <el-option v-for="(label, value) in genderOptions" :key="value" :label="label" :value="value" />
          </el-select>
        </el-form-item>
      </el-form>

      <!-- 底部操作按钮 -->
      <div class="button-group">
        <el-button type="primary" @click="toggleEditMode" :loading="loading">
          {{ isEditing ? '保存' : '编辑' }}
        </el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { ElMessage } from 'element-plus';
import { ArrowLeft } from '@element-plus/icons-vue';

const router = useRouter();
const profileFormRef = ref(null);
const loading = ref(false);
const isEditing = ref(false); // 是否处于编辑模式

// 性别选项映射
const genderOptions = {
  M: '男',
  F: '女',
  O: '其他',
  N: '保密'
};

// 用户资料表单数据
const profileForm = ref({
  nickname: '',
  bio: '',
  address: '',
  industry: '',
  gender: ''
});

// 获取用户个人资料
const fetchProfile = async () => {
  try {
    const { data } = await axios.get('http://127.0.0.1:8000/api/users/user/detail/', { withCredentials: true });
    profileForm.value = { ...data };
  } catch (error) {
    ElMessage.error('获取个人资料失败');
  }
};

// 编辑模式切换
const toggleEditMode = async () => {
  if (isEditing.value) {
    try {
      loading.value = true;
      await axios.post('http://127.0.0.1:8000/api/users/user/edit/', profileForm.value, { withCredentials: true });
      ElMessage.success('个人资料更新成功');
      fetchProfile(); // 重新获取个人信息
      isEditing.value = false; // 退出编辑模式
    } catch (error) {
      ElMessage.error(error.response?.data?.error || '更新失败');
    } finally {
      loading.value = false;
    }
  } else {
    isEditing.value = true;
  }
};

// 返回主页
const goBack = () => {
  router.push({ name: 'home' });
};

// 组件加载时获取用户资料
onMounted(fetchProfile);
</script>

<style scoped>
/* 全屏背景优化 */
.profile-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh; /* 全屏覆盖 */
  padding: 40px;
  background: linear-gradient(135deg, #eef2f3 0%, #dfe9f3 100%);
}

/* 资料卡片优化，加宽加长 */
.profile-card {
  width: 100%;
  max-width: 500px;
  padding: 40px;
  border-radius: 16px;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
  transition: transform 0.3s ease;
  background: white;
}

.profile-card:hover {
  transform: translateY(-5px);
}

/* 标题居中 */
.profile-title {
  flex-grow: 1;
  text-align: center;
  font-size: 22px;
  font-weight: bold;
  color: #333;
}

/* 头部按钮布局 */
.profile-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 2rem;
}

/* 返回按钮 */
.back-button {
  display: flex;
  align-items: center;
  color: #409eff;
  font-weight: 500;
}

.back-button:hover {
  color: #337ecc;
}

/* 个人资料表单 */
.profile-form {
  display: flex;
  flex-direction: column;
  gap: 20px; /* 增大各项间距 */
}

/* 输入框、选择框优化 */
:deep(.el-input__wrapper),
:deep(.el-textarea__inner),
:deep(.el-select .el-input__wrapper) {
  font-size: 18px;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.el-form-item {
  font-size: 18px;
}

:deep(.el-input__inner) {
  font-size: 18px;
}

/* 按钮组 */
.button-group {
  display: flex;
  justify-content: center;
  margin-top: 30px;
}

:deep(.el-button--primary) {
  width: 100%;
  max-width: 250px;
  background-color: #409eff;
  border: none;
  border-radius: 8px;
  padding: 14px 20px;
  font-size: 18px;
  transition: all 0.3s ease;
}

:deep(.el-button--primary:hover) {
  background-color: #337ecc;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
</style>
