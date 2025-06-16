<template>
  <el-container>
    <!-- 侧边栏 -->
    <el-aside width="200px">
      <el-menu default-active="1" class="el-menu-vertical-demo" @select="handleSelect">
        <el-menu-item index="questions">审核问题</el-menu-item>
        <el-menu-item index="answers">审核回答</el-menu-item>
        <el-menu-item index="courses">审核课程</el-menu-item>
        <el-menu-item index="questionsmanage">问题管理</el-menu-item>
        <el-menu-item index="answersmanage">回答管理</el-menu-item>
        <el-menu-item index="coursesmanage">课程管理</el-menu-item>
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
      <div v-if="activeTab === 'appeals'">
        <AppealAudit />
      </div>
      <div v-if="activeTab === 'questionsmanage'">
        <QuestionManage />
      </div>
      <div v-if="activeTab === 'answersmanage'">
        <AnswerManage />
      </div>
      <div v-if="activeTab === 'coursesmanage'">
        <CourseManage />
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
import QuestionManage from "@/views/admin/QuestionManage.vue";
import AnswerManage from "@/views/admin/AnswerManage.vue";
import CourseManage from "@/views/admin/CourseManage.vue";
import axios from "axios";
import {ElMessage} from "element-plus";

export default {
  components: { QuestionAudit, AnswerAudit, CourseAudit, UserManagement ,AppealAudit ,QuestionManage, AnswerManage, CourseManage},
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
/* 外层容器，高度固定，防止全局滚动影响布局 */
.admin-layout {
  height: 100vh;
  overflow: hidden;
}

/* 左侧菜单固定 */
.el-aside {
  position: fixed;
  top: 0;
  left: 0;
  width: 200px;
  height: 100vh;
  background-color: #fff;
  border-right: 1px solid #ebeef5;
  z-index: 1000;
  display: flex;
  flex-direction: column;
}

/* 菜单可滚动 */
.el-menu {
  flex: 1;
  overflow-y: auto;
  border-right: none;
}

/* 退出按钮固定在底部 */
.logout-button {
  margin: 20px;
  width: 160px;
}

/* 主内容区域需要“避开”固定的左侧菜单 */
.el-main {
  margin-left: 200px; /* 与 aside 宽度保持一致 */
  height: 100vh;
  overflow-y: auto;
  padding: 20px;
  background-color: #f5f7fa;
}

</style>
