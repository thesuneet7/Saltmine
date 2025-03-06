<template>
  <div id="particles-js"></div>
  <div class="container">
    <h1 class="gradient-text">Grid Generator</h1>
    
    <div class="tabs">
      <button v-for="tab in tabs" :key="tab.id" :class="{ active: activeTab === tab.id }" @click="setActiveTab(tab.id)">{{ tab.label }}</button>
    </div>

    <div class="form-container" v-if="activeTab">
      <template v-for="(value, key) in formValues[activeTab]" :key="key">
        <label>{{ key.replace(/([A-Z])/g, ' $1') }}:</label>
        <input v-if="key.includes('ColorsInput') || key === 'block_color'" type="text" v-model="formValues[activeTab][key]" />
        <input v-else type="number" v-model="formValues[activeTab][key]" />
      </template>
      <button class="generate-btn" @click="generateGrid">Generate Grid</button>
    </div>
    
    <div v-if="grid.length" class="grid-container">
      <table>
        <tr v-for="(row, rowIndex) in grid" :key="rowIndex">
          <td v-for="(cell, cellIndex) in row" :key="cellIndex" :style="getCellStyle(cell)"></td>
        </tr>
      </table>
    </div>
    
    <div v-if="error" class="error-message">
      <p>{{ error }}</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      activeTab: 'periphery',
      tabs: [
        { id: 'periphery', label: 'Periphery' },
        { id: 'diagonal', label: 'Diagonal' },
        { id: 'adj_const', label: 'Adjacency' },
        { id: 'no_adj_const', label: 'No Adjacency' },
        { id: 'block', label: 'Coloured Block' }
      ],
      formValues: {
        periphery: { n: 5, m: 5, red: 5, green: 5, blue: 5, peripheryColorsInput: 'RGB' },
        diagonal: { dimension: 5, red: 5, green: 5, blue: 5, diagonalColorsInput: 'RGB' },
        adj_const: { n: 5, m: 5, red: 5, green: 5, blue: 5, adjColorsInput: 'RGB' },
        no_adj_const: { n: 5, m: 5, red: 5, green: 5, blue: 5 },
        block: { n: 5, m: 5, red: 5, green: 5, blue: 5, block_color: 'R', block_size: 5, block_count: 5 },
      },
      grid: [],
      error: null,
    };
  },
  methods: {
    setActiveTab(tab) {
      this.activeTab = tab;
      this.grid = [];
      this.error = null;
    },
    generateGrid() {
      const form = this.formValues[this.activeTab];
      const payload = { ...form, constraint_type: this.activeTab };
      if (Object.prototype.hasOwnProperty.call(form, 'peripheryColorsInput')) 
        payload.periphery_colors = form.peripheryColorsInput.split('');
      if (Object.prototype.hasOwnProperty.call(form, 'diagonalColorsInput')) 
        payload.diagonal_colors = form.diagonalColorsInput.split('');
      if (Object.prototype.hasOwnProperty.call(form, 'adjColorsInput')) 
        payload.adjacency_cons = form.adjColorsInput.split('');
      //if (Object.prototype.hasOwnProperty.call(form, 'blockColorsInput')) 
        //payload.block_color = form.blockColorsInput.split('');


      
      console.log("Sending Payload:", payload);
      axios.post('http://127.0.0.1:8000/generate-grid', payload)
        .then(response => {
          this.grid = response.data.grid;
          this.error = null;
        })
        .catch(error => {
          this.grid = [];
          this.error = error.response?.data?.error || 'An error occurred.';
        });
    },
    getCellStyle(cell) {
      return { backgroundColor: cell === 'R' ? 'red' : cell === 'G' ? 'green' : cell === 'B' ? 'blue' : 'white' };
    },
  },
};
</script>


<style scoped>

#particles-js {
  position: fixed;
  width: 100%;
  height: 100%;
  z-index: -1;
  top: 0;
  left: 0;
  background: #ffffff; /* Optional: You can change this */
}

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@600&display=swap');

.container {
  max-width: 600px;
  margin: auto;
  font-family: 'Poppins', sans-serif;
  text-align: center;
}

.gradient-text {
  font-size: 2.5rem;
  font-weight: 700;
  background: linear-gradient(90deg, #1e90ff, #ff6347);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.tabs {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
}
button {
  padding: 10px 20px;
  border: none;
  cursor: pointer;
  font-size: 16px;
  font-weight: bold;
  background-color: #f0f0f0;
  margin: 0 10px;
  transition: 0.3s;
  border-radius: 12px;
}
button.active {
  background-color: #363636;
  color: white;
}
button:hover {
  background-color: #363636;
  color: white;
  transform: scale(1.05);
}
.form-container {
  display: flex;
  flex-direction: column;
  gap: 10px;
  align-items: center;
}
input {
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 8px;
  width: 80%;
  font-size: 14px;
  font-weight: bold;
}
.generate-btn {
  background-color: #ffffff;
  color: rgb(192, 120, 120);
  font-weight: bold;
  border: none;
  padding: 12px 24px;
  font-size: 16px;
  border-radius: 12px;
  position: relative;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s ease-in-out;
  box-shadow: 0px 0px 10px rgba(30, 143, 255, 0.6);
}

.generate-btn::before {
  content: "";
  position: absolute;
  inset: -4px;
  border-radius: 12px;
  padding: 2px;
  background: linear-gradient(90deg, #1e90ff, #ff6347);
  -webkit-mask: 
    linear-gradient(#fff 0 0) content-box, 
    linear-gradient(#fff 0 0);
  -webkit-mask-composite: destination-out;
  mask-composite: exclude;
}
.generate-btn:hover {
  box-shadow: 0px 0px 20px rgba(30, 144, 255, 0.4);
  transform: scale(1.05);
}
.grid-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}
table {
  border-collapse: collapse;
}
td {
  width: 30px;
  height: 30px;
  border: 1px solid #ccc;
}
.error-message {
  color: red;
  margin-top: 10px;
}
</style>