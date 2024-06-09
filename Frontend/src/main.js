import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import io from 'socket.io-client'

const app = createApp(App)

app.use(router)

// Set up Socket.IO client
const socket = io('http://localhost:5000') // Replace with your Flask server URL
app.config.globalProperties.$socket = socket

app.mount('#app')
