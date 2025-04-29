<template>
  <el-container>
    <!-- 侧边栏 -->
    <el-aside width="200px">
      <el-menu default-active="1" class="el-menu-vertical-demo" @select="handleSelect">
        <el-menu-item index="questions">审核问题</el-menu-item>
        <el-menu-item index="answers">审核回答</el-menu-item>
        <el-menu-item index="courses">审核课程</el-menu-item>
        <el-menu-item index="users">管理用户</el-menu-item>
        <el-menu-item index="appeals">查看申述</el-menu-item>
      </el-menu>
      <!-- 注销按钮 -->
      <el-button type="danger" class="logout-button" @click="logout">退出</el-button>
    </el-aside>

    <!-- 内容区 -->
    <el-main>
      <div v-if="activeTab === 'questions'">
        <QuestionAudit />
      </div>
      <div v-if="activeTab === 'answers'">
        <AnswerAudit />
      </div>
      <div v-if="activeTab === 'courses'">
        <CourseAudit />
      </div>
      <div v-if="activeTab === 'users'">
        <UserManagement />
      </div>
      <div v-if="activeTab === 'appeals'"> <!-- 新增申述模块 -->
        <AppealAudit />
      </div>
    </el-main>
  </el-container>
</template>

<script>
import QuestionAudit from "@/views/admin/QuestionAudit.vue";
import AnswerAudit from "@/views/admin/AnswerAudit.vue";
import CourseAudit from "@/views/admin/CourseAudit.vue";
import UserManagement from "@/views/admin/UserManage.vue";
import AppealAudit from "@/views/admin/AppealAudit.vue";
import axios from "axios";
import {ElMessage} from "element-plus";

export default {
  components: { QuestionAudit, AnswerAudit, CourseAudit, UserManagement ,AppealAudit},
  data() {
    return {
      activeTab: "questions",
    };
  },
  methods: {
    handleSelect(index) {
      this.activeTab = index;
    },
    async logout() {
      try {
        // 发送 POST 请求注销用户
        await axios.post("http://127.0.0.1:8000/api/users/user/logout/");
        ElMessage.success('已退出登录')
        // 注销成功后跳转到登录页
        this.$router.push({ name: "Login" });
      } catch (error) {
        console.error("退出失败", error);
      }
    },
  },
};
</script>

<style>
.el-menu {
  height: 100vh;
}

.logout-button {
  position: absolute;
  bottom: 20px;
  left: 20px;
  width: 160px;
}
</style>
