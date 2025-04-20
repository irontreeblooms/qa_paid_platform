<template>
  <div class="wallet-container">
    <div class="wallet-header">
      <!-- 返回按钮 -->
      <el-button type="text" @click="goHome" class="back-button">返回</el-button>
      <h2>我的钱包</h2>
      <div class="balance">
        <span>账户余额: ¥{{ balance }}</span>
      </div>
    </div>

    <!-- 充值和提现按钮 -->
    <div class="recharge-withdraw-section">
      <el-button type="primary" @click="handleRecharge">充值</el-button>
      <el-button type="danger" @click="handleWithdraw">提现</el-button>
    </div>

    <!-- 交易记录列表 -->
    <div class="transactions">
      <h3>交易记录</h3>
      <div v-if="loading">
        <el-spin></el-spin> <!-- Loading spinner -->
      </div>
      <div v-else>
        <div v-if="transactions.length > 0">
          <div v-for="transaction in transactions" :key="transaction.id" class="transaction-item">
            <p>类型: {{ transaction.transaction_type }}</p>
            <p>金额: ¥{{ transaction.amount }}</p>
            <p>时间: {{ formatDate(transaction.created_at) }}</p>
            <p>描述: {{ transaction.description }}</p>
            <hr />
          </div>
        </div>
        <div v-else>
          <p>暂无交易记录</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { ElButton, ElSpin } from 'element-plus'
import router from "@/router";

// 响应式数据
const balance = ref(0)  // 用户余额
const transactions = ref([])  // 交易记录
const loading = ref(true)  // Loading 状态

// 格式化时间
const formatDate = (timestamp) => {
  const date = new Date(timestamp)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 获取用户钱包信息和交易记录
const fetchWalletData = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/api/payment/list/')  // 获取交易记录的接口
    balance.value = response.data.balance
    transactions.value = response.data.transactions
    // 保存数据到 localStorage
    localStorage.setItem('balance', response.data.balance)
    localStorage.setItem('transactions', JSON.stringify(response.data.transactions))
  } catch (error) {
    console.error('获取钱包数据失败', error)
  } finally {
    loading.value = false  // 请求结束，停止加载动画
  }
}

// 页面刷新后从 localStorage 恢复数据
const restoreWalletData = () => {
  const savedBalance = localStorage.getItem('balance')
  const savedTransactions = localStorage.getItem('transactions')

  if (savedBalance && savedTransactions) {
    balance.value = savedBalance
    transactions.value = JSON.parse(savedTransactions)
  }
}

// 充值功能的处理
const handleRecharge = () => {
  alert('充值功能尚未实现')  // 这里可以跳转到充值页面或显示支付弹窗
}

// 提现功能的处理
const handleWithdraw = () => {
  alert('提现功能尚未实现')  // 这里可以跳转到提现页面或显示提现弹窗
}

// 跳转到主页
const goHome = () => {
  router.push({ name: 'home' })
}

// 生命周期钩子
onMounted(() => {
  restoreWalletData()  // 恢复余额和交易记录
  fetchWalletData()  // 加载余额和交易记录
})
</script>

<style scoped>
.wallet-container {
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  max-width: 800px;
  margin: 20px auto;
}

.wallet-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.balance {
  font-size: 20px;
  color: #409eff;
}

.recharge-withdraw-section {
  margin-top: 20px;
  text-align: center;
  display: flex;
  justify-content: center;
  gap: 20px;
}

.transactions {
  margin-top: 20px;
}

.transaction-item {
  padding: 10px;
  border: 1px solid #f0f0f0;
  border-radius: 8px;
  margin-bottom: 15px;
  background-color: #f9f9f9;
}

.el-button {
  padding: 10px 20px;
  font-size: 16px;
}

.back-button {
  font-size: 16px;
  margin-right: 10px;
}
</style>
