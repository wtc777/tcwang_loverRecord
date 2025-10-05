<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { ElMessage } from 'element-plus'

import apiClient from '../api/http'
import CalendarBoard from '../components/CalendarBoard.vue'

interface EventItem {
	id: number
	title: string
	event_date: string
}

const events = ref<EventItem[]>([])

const loadEvents = async () => {
	try {
		const { data } = await apiClient.get('/api/events')
		events.value = data
	} catch (error) {
		ElMessage.error('加载日历失败')
	}
}

onMounted(loadEvents)
</script>

<template>
	<div class="calendar-page">
		<CalendarBoard :events="events" />
	</div>
</template>

<style scoped>
.calendar-page {
	background: #fff;
	padding: 24px;
	border-radius: 12px;
	box-shadow: inset 0 0 0 1px #ffe0ec;
}
</style>
