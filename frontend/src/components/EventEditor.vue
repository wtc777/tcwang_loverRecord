<script setup lang="ts">
import { reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'

import apiClient from '../api/http'

interface EventForm {
	title: string
	description: string
	date: string
}

const emit = defineEmits<{ (e: 'created'): void }>()

const form = reactive<EventForm>({
	title: '',
	description: '',
	date: ''
})

const uploading = ref(false)
const fileInput = ref<HTMLInputElement | null>(null)

const submit = async () => {
	if (!form.title || !form.date) {
		ElMessage.warning('请填写标题和日期')
		return
	}
	try {
		const payload = {
			title: form.title,
			description: form.description,
			event_date: new Date(form.date).toISOString()
		}
		const { data } = await apiClient.post('/api/events', payload)
		await uploadMediaIfNeeded(data.id)
		ElMessage.success('事件已创建')
		emit('created')
		reset()
	} catch (error) {
		ElMessage.error('创建失败，请稍后重试')
	}
}

const uploadMediaIfNeeded = async (eventId: number) => {
	const file = fileInput.value?.files?.[0]
	if (!file) {
		return
	}
	uploading.value = true
	try {
		const formData = new FormData()
		formData.append('file', file)
		formData.append('event_id', String(eventId))
		await apiClient.post('/api/media/upload', formData, {
			headers: { 'Content-Type': 'multipart/form-data' }
		})
	} finally {
		uploading.value = false
		if (fileInput.value) {
			fileInput.value.value = ''
		}
	}
}

const reset = () => {
	form.title = ''
	form.description = ''
	form.date = ''
}
</script>

<template>
	<el-form label-width="72px" class="event-editor" @submit.prevent>
		<el-form-item label="标题">
			<el-input v-model="form.title" placeholder="今天的甜蜜瞬间" />
		</el-form-item>
		<el-form-item label="时间">
			<el-date-picker v-model="form.date" type="datetime" placeholder="选择时间" />
		</el-form-item>
		<el-form-item label="描述">
			<el-input v-model="form.description" type="textarea" rows="3" />
		</el-form-item>
		<el-form-item label="照片">
			<input ref="fileInput" type="file" accept="image/*" />
		</el-form-item>
		<el-form-item>
			<el-button type="primary" :loading="uploading" @click="submit">发布</el-button>
		</el-form-item>
	</el-form>
</template>

<style scoped>
.event-editor {
	background: #fff;
	padding: 24px;
	border-radius: 12px;
	box-shadow: inset 0 0 0 1px #ffe0ec;
	display: flex;
	flex-direction: column;
	gap: 12px;
}
</style>
