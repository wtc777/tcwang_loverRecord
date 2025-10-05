import axios from 'axios'

const apiClient = axios.create({
	baseURL: 'http://localhost:8000',
	timeout: 10000
})

apiClient.interceptors.request.use((config) => {
	const token = localStorage.getItem('token')
	if (token) {
		config.headers.Authorization = `Bearer ${token}`
	}
	return config
})

apiClient.interceptors.response.use(
	(response) => response,
	(error) => {
		if (error.response?.status === 401) {
			localStorage.removeItem('token')
		}
		return Promise.reject(error)
	}
)

export default apiClient
