<template>
  <div>
    <h2 class="text-center">用户管理</h2>

    <!-- 搜索框 -->
    <div class="search-bar">
      <input
        v-model="searchQuery"
        type="text"
        placeholder="搜索用户 (用户名或邮箱)"
        class="search-input"
      />
    </div>

    <table class="table">
      <thead>
        <tr>
          <th style="text-align: center;">ID</th>
          <th style="text-align: center;">用户名</th>
          <th style="text-align: center;">邮箱</th>
          <th style="text-align: center;">管理员权限</th>
          <th style="text-align: center;">操作</th>
        </tr>
      </thead>
      <tbody>
        <!-- 过滤后的用户列表 -->
        <tr v-for="user in filteredUsers" :key="user.id">
          <td style="text-align: center;">
            <a href="#" @click="showDetails(user)">{{ user.id }}</a>
          </td>
          <td style="text-align: center;">{{ user.username }}</td>
          <td style="text-align: center;">{{ user.email }}</td>
          <td style="text-align: center;">{{ user.is_superuser ? '是' : '否' }}</td>
          <td style="text-align: center;">
            <button @click="toggleAdmin(user)" class="btn btn-primary">
              {{ user.is_superuser ? '取消管理员' : '设为管理员' }}
            </button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- 用户详情弹窗 -->
    <div v-if="selectedUser" class="modal">
      <div class="modal-content">
        <span class="close" @click="closeModal">&times;</span>
        <h3>用户详情</h3>
        <p>ID: {{ selectedUser.id }}</p>
        <p>用户名: {{ selectedUser.username }}</p>
        <p>邮箱: {{ selectedUser.email }}</p>
        <p>管理员权限: {{ selectedUser.is_superuser ? '是' : '否' }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      users: [],
      searchQuery: '', // 搜索关键字
      selectedUser: null // 当前选中的用户
    };
  },
  computed: {
    filteredUsers() {
      // 根据搜索关键字筛选用户
      return this.users.filter(user => {
        const query = this.searchQuery.toLowerCase();
        return (
          user.username.toLowerCase().includes(query) ||
          user.email.toLowerCase().includes(query)
        );
      });
    }
  },
  methods: {
    async fetchUsers() {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/admin/users/');
        this.users = response.data.users;
      } catch (error) {
        console.error('获取用户失败:', error);
      }
    },
    async toggleAdmin(user) {
      try {
        await axios.post('http://127.0.0.1:8000/api/admin/users/', {
          user_id: user.id,
          is_superuser: !user.is_superuser
        });
        this.fetchUsers(); // 重新获取用户列表
      } catch (error) {
        console.error('更新用户权限失败:', error);
      }
    },
    showDetails(user) {
      this.selectedUser = user; // 设置为当前用户
    },
    closeModal() {
      this.selectedUser = null; // 关闭弹窗
    }
  },
  mounted() {
    this.fetchUsers();
  }
};
</script>

<style scoped>
.text-center {
  text-align: center;
}
.search-bar {
  margin-bottom: 20px;
  text-align: center;
}
.search-input {
  padding: 10px;
  width: 300px;
  border: 1px solid #ddd;
  border-radius: 5px;
}
.table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}
.table th,
.table td {
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
.modal {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: #fff;
  padding: 30px;
  border-radius: 10px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  z-index: 1000;
  width: 400px;
  max-width: 90%;
  animation: fadeIn 0.3s ease-in-out;
}
.modal-content {
  position: relative;
}
.close {
  position: absolute;
  top: 10px;
  right: 10px;
  font-size: 18px;
  font-weight: bold;
  color: #888;
  cursor: pointer;
  transition: color 0.2s;
}
.close:hover {
  color: #000;
}
</style>