<template>
  <div class="container mx-auto mt-10">
    <div class="text-center">
      <h1 class="text-4xl font-bold mb-4">Person Detection</h1>
      <p class="text-xl mb-4">Number of people detected: {{ personCount }}</p>
      <button class="btn btn-primary mb-4" @click="getPersonCount">Refresh</button>

      <div class="mb-4">
        <label class="cursor-pointer label">
          <span class="label-text">Auto Mode</span> 
          <input type="checkbox" class="toggle toggle-primary" v-model="autoMode" @change="toggleAutoMode">
        </label>
      </div>

      <div class="mb-4">
        <label class="cursor-pointer label">
          <span class="label-text">Theme</span>
          <select class="select select-primary" v-model="theme" @change="changeTheme">
            <option v-for="themeOption in themes" :key="themeOption" :value="themeOption">
              {{ themeOption }}
            </option>
          </select>
        </label>
      </div>

      <div class="grid grid-cols-2 gap-4">
        <div v-for="(status, relay) in relayStatus" :key="relay" class="card bordered">
          <div class="card-body">
            <h2 class="card-title">{{ relay }}</h2>
            <button 
              class="btn"
              :class="status ? 'btn-success' : 'btn-error'"
              @click="toggleRelay(relay, !status)"
              :disabled="autoMode"
            >
              {{ status ? 'ON' : 'OFF' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HelloWorld',
  data() {
    return {
      personCount: 0,
      personCountInterval: null,
      autoMode: false,
      relayStatus: {
        r1: false,
        r2: false,
        r3: false,
        r4: false
      },
      theme: 'light',
      themes: ['light', 'dark', 'cupcake', 'bumblebee', 'emerald', 'corporate',
        'synthwave', 'retro', 'cyberpunk', 'valentine', 'halloween',
        'garden', 'forest', 'aqua', 'lofi', 'pastel', 'fantasy',
        'wireframe', 'black', 'luxury', 'dracula', 'cmyk', 'autumn',
        'business', 'acid', 'lemonade', 'night', 'coffee', 'winter']
    };
  },
  methods: {
    async getPersonCount() {
      try {
        const response = await fetch('http://localhost:5000/detect');
        const data = await response.json();
        this.personCount = data.person_count;
        alert("Person Count", data.person_count)
        this.relayStatus = data.relay_status;
      } catch (error) {
        console.error('Error fetching person count:', error);
      }
    },
    async toggleAutoMode() {
      try {
        const response = await fetch('http://localhost:5000/auto_mode', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ auto_mode: this.autoMode })
        });
        const data = await response.json();
        this.autoMode = data.auto_mode;
      } catch (error) {
        console.error('Error toggling auto mode:', error);
      }
    },
    async toggleRelay(relay, status) {
      try {
        const response = await fetch('http://localhost:5000/relay', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ relay, status })
        });
        const data = await response.json();
        this.relayStatus = data.relay_status;
      } catch (error) {
        console.error('Error toggling relay:', error);
      }
    },
    changeTheme() {
      document.documentElement.setAttribute('data-theme', this.theme);
    },
    startPersonCountUpdater() {
      this.personCountInterval = setInterval(() => {
        this.$socket.emit('get_person_count')
      }, 2000)
    }
  },
  mounted() {
    this.getPersonCount()
    this.changeTheme()
    this.startPersonCountUpdater()

    this.$socket.on('person_count', (data) => {
      this.personCount = data.count
    })

    this.$socket.on('disconnect', () => {
      clearInterval(this.personCountInterval)
    })
    
  }
};
</script>

<style scoped>
/* Custom styles if needed */
</style>
