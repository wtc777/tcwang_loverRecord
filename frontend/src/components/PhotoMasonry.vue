<script setup lang="ts">
interface PhotoItem {
	id: number
	thumb_path?: string | null
	file_path: string
}

const props = defineProps<{ photos: PhotoItem[] }>()
</script>

<template>
	<div class="masonry">
		<div v-for="photo in props.photos" :key="photo.id" class="masonry-item">
			<img :src="photo.thumb_path || photo.file_path" alt="photo" />
		</div>
	</div>
</template>

<style scoped>
.masonry {
	column-count: 3;
	column-gap: 12px;
}

.masonry-item {
	break-inside: avoid;
	margin-bottom: 12px;
}

.masonry-item img {
	width: 100%;
	border-radius: 12px;
	box-shadow: 0 6px 18px rgba(0, 0, 0, 0.08);
}

@media (max-width: 768px) {
	.masonry {
		column-count: 2;
	}
}
</style>
