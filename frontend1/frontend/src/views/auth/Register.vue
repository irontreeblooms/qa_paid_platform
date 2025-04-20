<template>
  <div class="register-container">
    <el-card class="register-card">
      <h2 class="register-title">用户注册</h2>
      <el-form :model="form" :rules="rules" ref="formRef">
        <el-form-item prop="username">
          <el-input v-model="form.username" placeholder="请输入用户名" clearable>
            <template #prefix>
              <el-icon><User /></el-icon>
            </template>
          </el-input>
        </el-form-item>

        <el-form-item prop="password">
          <el-input v-model="form.password" placeholder="请输入密码" show-password clearable>
            <template #prefix>
              <el-icon><Lock /></el-icon>
            </template>
          </el-input>
        </el-form-item>

        <el-form-item prop="confirmPassword">
          <el-input v-model="form.confirmPassword" placeholder="确认密码" show-password clearable>
            <template #prefix>
              <el-icon><Lock /></el-icon>
            </template>
          </el-input>
        </el-form-item>

        <el-form-item prop="email">
          <el-input v-model="form.email" placeholder="请输入邮箱" clearable>
            <template #prefix>
              <el-icon><Message /></el-icon>
            </template>
          </el-input>
        </el-form-item>

        <el-form-item prop="code">
          <div style="display: flex; width: 100%;">
            <el-input v-model="form.code" placeholder="验证码" style="flex: 1;" />
            <el-button @click="sendCode" :disabled="countdown > 0" style="margin-left: 10px;">
              {{ countdown > 0 ? `${countdown}s后重发` : '发送验证码' }}
            </el-button>
          </div>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" :loading="loading" style="width: 100%;" @click="submit">
            注册
          </el-button>
        </el-form-item>
      </el-form>

      <p class="register-footer">
        已有账号？
        <router-link to="/login">立即登录</router-link>
      </p>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { ElMessage } from 'element-plus';
import { User, Lock, Message } from '@element-plus/icons-vue';

const router = useRouter();
const formRef = ref(null);
const form = ref({
  username: '',
  password: '',
  confirmPassword: '',
  email: '',
  code: ''
});

const loading = ref(false);
const countdown = ref(0);
let timer = null;

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 16, message: '长度在3到16个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '长度在6到20个字符', trigger: 'blur' }
  ],
  confirmPassword: [
    {
      validator: (rule, value, callback) => {
        if (value !== form.value.password) {
          callback(new Error('两次密码输入不一致'));
        } else {
          callback();
        }
      },
      trigger: 'blur'
    }
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '邮箱格式不正确', trigger: 'blur' }
  ],
  code: [{ required: true, message: '请输入验证码', trigger: 'blur' }]
};

const sendCode = async () => {
  try {
    if (!form.value.email) {
      ElMessage.warning('请先输入邮箱');
      return;
    }

    await axios.post('http://127.0.0.1:8000/api/users/send-code/', {
      email: form.value.email
    });

    ElMessage.success('验证码已发送');
    countdown.value = 60;
    timer = setInterval(() => {
      countdown.value -= 1;
      if (countdown.value <= 0) {
        clearInterval(timer);
      }
    }, 1000);
  } catch (err) {
    ElMessage.error('验证码发送失败');
  }
};

const submit = async () => {
  try {
    await formRef.value.validate();
    loading.value = true;

    await axios.post('http://127.0.0.1:8000/api/users/register/', {
      username: form.value.username,
      password: form.value.password,
      email: form.value.email,
      code: form.value.code
    });

    ElMessage.success('注册成功');
    router.push('/login');
  } catch (err) {
    ElMessage.error(err.response?.data?.error || '注册失败');
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #43cea2 0%, #185a9d 100%);
  padding: 20px;
}

.register-card {
  width: 100%;
  max-width: 450px;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  transition: transform 0.3s ease;
}

.register-card:hover {
  transform: translateY(-5px);
}

.register-title {
  margin: 0 0 1.5rem;
  font-size: 2.2rem;
  font-weight: 700;
  color: #2d3748;
  text-align: center;
}

.register-footer {
  margin-top: 15px;
  text-align: center;
}
</style>
