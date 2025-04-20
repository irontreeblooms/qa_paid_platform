<template>
  <div>
    <h2 class="text-center">用户管理</h2>
    <table class="table">
      <thead>
        <tr>
          <th>ID</th>
          <th>用户名</th>
          <th>邮箱</th>
          <th>管理员权限</th>
          <th>操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in users" :key="user.id">
          <td>{{ user.id }}</td>
          <td>{{ user.username }}</td>
          <td>{{ user.email }}</td>
          <td>{{ user.is_superuser ? '是' : '否' }}</td>
          <td>
            <button @click="toggleAdmin(user)" class="btn btn-primary">
              {{ user.is_superuser ? '取消管理员' : '设为管理员' }}
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      users: []
    };
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
</style>
