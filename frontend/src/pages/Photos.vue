<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { ElMessage } from 'element-plus'

import apiClient from '../api/http'
import PhotoMasonry from '../components/PhotoMasonry.vue'

interface PhotoItem {
	id: number
	file_path: string
	thumb_path?: string | null
}

const photos = ref<PhotoItem[]>([])

const loadPhotos = async () => {
	try {
		const { data } = await apiClient.get('/api/media')
		photos.value = data
	} catch (error) {
		ElMessage.error('加载照片失败')
	}
}

onMounted(loadPhotos)
</script>

<template>
	<div class="photos-page">
		<PhotoMasonry :photos="photos" />
	</div>
</template>

<style scoped>
.photos-page {
	background: #fff;
	padding: 24px;
	border-radius: 12px;
	box-shadow: inset 0 0 0 1px #ffe0ec;
}
</style>
