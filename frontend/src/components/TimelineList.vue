<script setup lang="ts">
interface TimelineEvent {
	id: number
	title: string
	description?: string | null
	event_date: string
	media_items: { id: number; thumb_path?: string | null }[]
}

const props = defineProps<{ events: TimelineEvent[] }>()
</script>

<template>
	<div class="timeline">
		<div v-for="event in props.events" :key="event.id" class="timeline-item">
			<h3>{{ event.title }}</h3>
			<p class="date">{{ new Date(event.event_date).toLocaleString() }}</p>
			<p v-if="event.description">{{ event.description }}</p>
			<div class="media">
				<img
					 v-for="media in event.media_items"
					 :key="media.id"
					 v-if="media.thumb_path"
					 :src="media.thumb_path"
					 alt="thumb"
				/>
			</div>
		</div>
	</div>
</template>

<style scoped>
.timeline {
	display: flex;
	flex-direction: column;
	gap: 24px;
}

.timeline-item {
	background: #fff9fb;
	padding: 16px;
	border-radius: 12px;
	box-shadow: 0 8px 20px rgba(0, 0, 0, 0.05);
}

.date {
	color: #fa7296;
	font-size: 14px;
}

.media {
	display: flex;
	gap: 8px;
	margin-top: 12px;
}

.media img {
	width: 80px;
	height: 80px;
	object-fit: cover;
	border-radius: 8px;
}
</style>
