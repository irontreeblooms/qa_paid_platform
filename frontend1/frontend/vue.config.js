const { defineConfig } = require('@vue/cli-service');

module.exports = defineConfig({
  transpileDependencies: true,

  // 关闭 ESLint（如果你不想让 ESLint 报错）
  lintOnSave: false,

  // 配置开发服务器
  devServer: {
    port: 8080, // 指定 Vue 运行端口
    host: 'localhost', // 服务器地址
    open: true, // 运行时自动打开浏览器
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000', // 你的 Django 服务器地址
        changeOrigin: true,
        secure: false, // 如果 Django 使用 HTTPS，设置为 true
        pathRewrite: { '^/api': '' } // 将 /api 替换为空，确保正确映射 Django 端点
      }
    }
  },

  // 允许跨域请求（适用于 Django REST API）
  configureWebpack: {
    devtool: 'source-map',
  }
});
