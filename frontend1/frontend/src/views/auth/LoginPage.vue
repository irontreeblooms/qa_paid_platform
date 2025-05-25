<template>
  <div class="login-container">
    <el-card class="login-card">
      <h2 class="login-title">问知</h2>
      <el-form
        :model="loginForm"
        :rules="rules"
        ref="loginFormRef"
        @keyup.enter="handleLogin"
      >
        <el-form-item prop="role">
          <el-select
            v-model="loginForm.role"
            placeholder="请选择身份"
            style="width: 100%;"
          >
            <el-option label="用户" value="user" />
            <el-option label="管理员" value="admin" />
          </el-select>
        </el-form-item>

        <el-form-item prop="username">
          <el-input
            v-model="loginForm.username"
            placeholder="请输入用户名"
            clearable
          >
            <template #prefix>
              <el-icon><User /></el-icon>
            </template>
          </el-input>
        </el-form-item>

        <el-form-item prop="password">
          <el-input
            v-model="loginForm.password"
            placeholder="请输入密码"
            show-password
            clearable
          >
            <template #prefix>
              <el-icon><Lock /></el-icon>
            </template>
          </el-input>
        </el-form-item>

        <el-form-item>
          <el-button
            type="primary"
            :loading="loading"
            @click="handleLogin"
            style="width: 100%;"
          >
            登录
          </el-button>
        </el-form-item>
      </el-form>

      <p class="login-footer">
        还没有账户？
        <router-link to="/register">立即注册</router-link>
      </p>

      <p class="login-footer">
        忘记密码？
        <router-link to="/register">找回密码</router-link>
      </p>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { ElMessage } from 'element-plus';
import { User, Lock } from '@element-plus/icons-vue';

const router = useRouter();
const loginFormRef = ref(null);

const loginForm = ref({
  role: 'user', // 默认选择用户
  username: '',
  password: ''
});

const loading = ref(false);

const rules = {
  role: [{ required: true, message: '请选择身份', trigger: 'change' }],
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 16, message: '长度在3到16个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '长度在6到20个字符', trigger: 'blur' }
  ]
};

const handleLogin = async () => {
  try {
    // 执行表单验证
    await loginFormRef.value.validate();

    loading.value = true;

    const loginUrl = loginForm.value.role === 'admin'
      ? 'http://127.0.0.1:8000/api/users/admin/login/'
      : 'http://127.0.0.1:8000/api/users/user/login/';

    const { data } = await axios.post(
      loginUrl,
      {
        role: loginForm.value.role,
        username: loginForm.value.username,
        password: loginForm.value.password
      },
      { withCredentials: true }
    );

    ElMessage.success('登录成功'); // 显示登录成功消息
    window.sessionStorage.setItem("token", data.token); // 存储 token

    // 根据角色跳转
    const targetRoute = loginForm.value.role === 'admin'
      ? '/admin'
      : '/home';

    await router.push(targetRoute); // 跳转到目标页面
  } catch (error) {
    const errorMessage = error.response?.data?.error
      || error.message
      || '账户或者用户名错误';

    ElMessage.error(errorMessage); // 显示错误消息
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #43cea2 0%, #185a9d 100%);
  padding: 20px;
}

.login-card {
  width: 100%;
  max-width: 400px;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  transition: transform 0.3s ease;
}

.login-card:hover {
  transform: translateY(-5px);
}

.login-title {
  margin: 0 0 1.5rem;
  font-size: 2.5rem;
  font-weight: 700;
  color: #2d3748;
  text-align: center;
}
</style>