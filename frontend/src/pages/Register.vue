<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import type { AxiosError } from 'axios'

import apiClient from '../api/http'

const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const isSubmitting = ref(false)
const router = useRouter()

const register = async () => {
        if (!email.value || !password.value || !confirmPassword.value) {
                ElMessage.warning('请填写全部信息')
                return
        }
        if (password.value !== confirmPassword.value) {
                ElMessage.warning('两次输入的密码不一致')
                return
        }

        try {
                isSubmitting.value = true
                await apiClient.post('/api/auth/register', {
                        email: email.value,
                        password: password.value
                })
                ElMessage.success('注册成功，请登录')
                router.push('/')
        } catch (error) {
                console.error('注册失败', error)
                const err = error as AxiosError<{ detail?: string | string[] }>
                const detail = err.response?.data?.detail
                const message = Array.isArray(detail)
                        ? detail.join('\n')
                        : detail || '注册失败，请稍后再试'
                ElMessage.error(message)
        } finally {
                isSubmitting.value = false
        }
}

const goToLogin = () => {
        router.push('/')
}
</script>

<template>
        <div class="register-hero">
                <div class="panel">
                        <h1>创建账户</h1>
                        <el-input v-model="email" placeholder="邮箱" />
                        <el-input v-model="password" placeholder="密码" type="password" />
                        <el-input v-model="confirmPassword" placeholder="确认密码" type="password" />
                        <el-button type="primary" class="w-full" :loading="isSubmitting" @click="register">
                                注册
                        </el-button>
                        <div class="helper-text">
                                <span>已经有账号了？</span>
                                <el-button link type="primary" @click="goToLogin">去登录</el-button>
                        </div>
                </div>
        </div>
</template>

<style scoped>
.register-hero {
        height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
        background: radial-gradient(#e8f7ff, #fff);
}

.panel {
        width: 360px;
        background: #ffffff;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
        display: flex;
        flex-direction: column;
        gap: 16px;
}

.w-full {
        width: 100%;
}

.helper-text {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 4px;
        font-size: 14px;
        color: #666;
}
</style>
