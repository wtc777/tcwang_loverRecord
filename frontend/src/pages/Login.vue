<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

import apiClient from '../api/http'

const email = ref('')
const password = ref('')
const started = ref(false)
const audioRef = ref<HTMLAudioElement | null>(null)
const router = useRouter()

const login = async () => {
	if (!email.value || !password.value) {
		ElMessage.warning('请输入邮箱和密码')
		return
	}
	try {
		const { data } = await apiClient.post('/api/auth/login', {
			email: email.value,
			password: password.value
		})
		localStorage.setItem('token', data.access_token)
		router.push('/dashboard')
	} catch (error) {
		ElMessage.error('登录失败，请检查账号信息')
	}
}

const startMusic = () => {
        if (audioRef.value) {
                audioRef.value.play()
                started.value = true
        }
}

const goToRegister = () => {
        router.push('/register')
}
</script>

<template>
        <div class="login-hero">
                <div class="floating-hearts"></div>
                <div class="panel">
                        <h1>甜心手账</h1>
                        <el-input v-model="email" placeholder="邮箱" />
                        <el-input v-model="password" placeholder="密码" type="password" />
                        <el-button type="primary" class="w-full" @click="login">登录</el-button>
                        <div class="helper-text">
                                <span>还没有账号？</span>
                                <el-button link type="primary" @click="goToRegister">去注册</el-button>
                        </div>
                        <el-button v-if="!started" class="w-full" @click="startMusic">开启浪漫BGM</el-button>
                        <audio ref="audioRef" src="/static/assets/bgm.mp3" loop></audio>
                </div>
        </div>
</template>

<style scoped>
.login-hero {
	height: 100vh;
	display: flex;
	align-items: center;
	justify-content: center;
	position: relative;
	background: radial-gradient(#ffe6f2, #fff);
}

.panel {
	width: 360px;
	background: #fff9fb;
	border-radius: 16px;
	padding: 24px;
	box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
	position: relative;
	z-index: 1;
	display: flex;
	flex-direction: column;
	gap: 16px;
}

.floating-hearts {
	position: absolute;
	inset: 0;
	background: url('https://raw.githubusercontent.com/encharm/Font-Awesome-SVG-PNG/master/black/svg/heart.svg') center/64px no-repeat;
	opacity: 0.15;
	animation: pulse 6s infinite ease-in-out;
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

@keyframes pulse {
	0%,
	100% {
		transform: scale(1);
	}
	50% {
		transform: scale(1.05);
	}
}
</style>
