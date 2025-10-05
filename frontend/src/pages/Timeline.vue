<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { ElMessage } from 'element-plus'

import apiClient from '../api/http'
import EventEditor from '../components/EventEditor.vue'
import TimelineList from '../components/TimelineList.vue'

interface EventItem {
	id: number
	title: string
	description?: string | null
	event_date: string
	media_items: { id: number; thumb_path?: string | null }[]
}

const events = ref<EventItem[]>([])

const loadEvents = async () => {
	try {
		const { data } = await apiClient.get('/api/events')
		events.value = data
	} catch (error) {
		ElMessage.error('加载时间线失败')
	}
}

onMounted(loadEvents)
</script>

<template>
	<div class="timeline-page">
		<EventEditor @created="loadEvents" />
		<TimelineList :events="events" />
	</div>
</template>

<style scoped>
.timeline-page {
	display: grid;
	grid-template-columns: 1fr;
	gap: 24px;
}
</style>
