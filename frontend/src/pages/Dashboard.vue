<script setup lang="ts">
import { ref } from 'vue'
import { useRouter, RouterView } from 'vue-router'

const router = useRouter()
const active = ref('timeline')

const handleSelect = (key: string) => {
	active.value = key
	if (key === 'timeline') {
		router.push('/dashboard')
	} else {
		router.push(`/dashboard/${key}`)
	}
}

const logout = () => {
	localStorage.removeItem('token')
	router.push('/')
}
</script>

<template>
	<div class="dashboard">
		<aside class="sidebar">
			<h2>情侣手账</h2>
			<el-menu :default-active="active" @select="handleSelect">
				<el-menu-item index="timeline">时间线</el-menu-item>
				<el-menu-item index="calendar">日历</el-menu-item>
				<el-menu-item index="photos">照片墙</el-menu-item>
			</el-menu>
			<el-button type="text" @click="logout">退出</el-button>
		</aside>
		<main class="content">
			<RouterView />
		</main>
	</div>
</template>

<style scoped>
.dashboard {
	display: grid;
	grid-template-columns: 240px 1fr;
	height: 100vh;
}

.sidebar {
	background: #fff0f6;
	padding: 24px;
	display: flex;
	flex-direction: column;
	gap: 16px;
	border-right: 1px solid #ffd6e7;
}

.content {
	padding: 24px;
	background: #fff;
	overflow-y: auto;
}
</style>
