<script setup lang="ts">
import { computed } from 'vue'

interface CalendarEvent {
	id: number
	title: string
	event_date: string
}

const props = defineProps<{ events: CalendarEvent[] }>()

const now = new Date()
const year = now.getFullYear()
const month = now.getMonth()
const startDate = new Date(year, month, 1)
const startDay = startDate.getDay()
const daysInMonth = new Date(year, month + 1, 0).getDate()

const cells = computed(() => {
	const arr: { date: number | null; events: CalendarEvent[] }[] = []
	for (let i = 0; i < startDay; i += 1) {
		arr.push({ date: null, events: [] })
	}
	for (let day = 1; day <= daysInMonth; day += 1) {
		const cellDate = new Date(year, month, day)
		const events = props.events.filter((event) => {
			const eventDate = new Date(event.event_date)
			return eventDate.getFullYear() === year && eventDate.getMonth() === month && eventDate.getDate() === day
		})
		arr.push({ date: day, events })
	}
	return arr
})
</script>

<template>
	<div class="calendar-grid">
		<div v-for="cell in cells" :key="`${cell.date}-${Math.random()}`" class="calendar-cell">
			<div v-if="cell.date" class="calendar-date">{{ cell.date }}</div>
			<ul>
				<li v-for="event in cell.events" :key="event.id">{{ event.title }}</li>
			</ul>
		</div>
	</div>
</template>

<style scoped>
.calendar-grid {
	display: grid;
	grid-template-columns: repeat(7, 1fr);
	gap: 8px;
}

.calendar-cell {
	min-height: 100px;
	background: #fff9fb;
	border-radius: 10px;
	padding: 8px;
	box-shadow: inset 0 0 0 1px #ffe0ec;
}

.calendar-date {
	font-weight: bold;
	margin-bottom: 8px;
}
</style>
