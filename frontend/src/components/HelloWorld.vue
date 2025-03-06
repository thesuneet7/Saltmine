<template>
  <div id="particles-js"></div>
  <div class="container">
    <h1 class="gradient-text">Grid Generator</h1>
    <div class="tabs">
      <button :class="{ active: activeTab === 'periphery' }" @click="setActiveTab('periphery')">Periphery</button>
      <button :class="{ active: activeTab === 'diagonal' }" @click="setActiveTab('diagonal')">Diagonal</button>
      <button :class="{ active: activeTab === 'adj_const' }" @click="setActiveTab('adj_const')">Adjacency</button>
    </div>

    <div class="form-container" v-if="activeTab === 'periphery'">
      <label>Dimension:</label>
      <input type="number" v-model="peripheryForm.dimension" />
      <label>Red:</label>
      <input type="number" v-model="peripheryForm.red" />
      <label>Green:</label>
      <input type="number" v-model="peripheryForm.green" />
      <label>Blue:</label>
      <input type="number" v-model="peripheryForm.blue" />
      <label>Periphery Colors (e.g., RGB):</label>
      <input type="text" v-model="peripheryForm.peripheryColorsInput" />
      <button class="generate-btn" @click="generatePeripheryGrid">Generate Grid</button>
    </div>

    <div class="form-container" v-if="activeTab === 'diagonal'">
      <label>Dimension:</label>
      <input type="number" v-model="diagonalForm.dimension" />
      <label>Red:</label>
      <input type="number" v-model="diagonalForm.red" />
      <label>Green:</label>
      <input type="number" v-model="diagonalForm.green" />
      <label>Blue:</label>
      <input type="number" v-model="diagonalForm.blue" />
      <label>Diagonal Colors (e.g., RGB):</label>
      <input type="text" v-model="diagonalForm.diagonalColorsInput" />
      <button class="generate-btn" @click="generateDiagonalGrid">Generate Grid</button>
    </div>

    <div class="form-container" v-if="activeTab === 'adj_const'">
      <label>Row:</label>
      <input type="number" v-model="adjForm.n" />
      <label>Column:</label>
      <input type="number" v-model="adjForm.m" />
      <label>Red:</label>
      <input type="number" v-model="adjForm.red" />
      <label>Green:</label>
      <input type="number" v-model="adjForm.green" />
      <label>Blue:</label>
      <input type="number" v-model="adjForm.blue" />
      <label>Adjacent Colors (e.g., RGB):</label>
      <input type="text" v-model="adjForm.adjColorsInput" />
      <button class="generate-btn" @click="generateAdjacentGrid">Generate Grid</button>
    </div>

    <div v-if="grid.length > 0" class="grid-container">
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
      peripheryForm: {
        dimension: 5,
        red: 5,
        green: 5,
        blue: 5,
        peripheryColorsInput: 'RGB',
      },

      diagonalForm: {
        dimension: 5,
        red: 5,
        green: 5,
        blue: 5,
        diagonalColorsInput: 'RGB',
      },

      adjForm: {
        n: 5,
        m: 5,
        red: 5,
        green: 5,
        blue: 5,
        adjColorsInput: 'RGB',
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
    generatePeripheryGrid() {
      const payload = {
        dimension: this.peripheryForm.dimension,
        red: this.peripheryForm.red,
        green: this.peripheryForm.green,
        blue: this.peripheryForm.blue,
        constraint_type: 'periphery',
        periphery_colors: this.peripheryForm.peripheryColorsInput.split(''),  // Ensure it's split correctly
      };
      
      console.log("Sending Payload:", payload);
      axios
        .post('http://127.0.0.1:8000/generate-grid', {
          dimension: this.peripheryForm.dimension,
          red: this.peripheryForm.red,
          green: this.peripheryForm.green,
          blue: this.peripheryForm.blue,
          constraint_type: 'periphery',
          periphery_colors: this.peripheryForm.peripheryColorsInput.split(''),
        })
        .then(response => {
          this.grid = response.data.grid;
          this.error = null;
        })
        .catch(error => {
          this.grid = [];
          this.error = error.response?.data?.error || 'An error occurred.';
        });
    },
    generateDiagonalGrid() {
      const payload = {
        dimension: this.diagonalForm.dimension,
        red: this.diagonalForm.red,
        green: this.diagonalForm.green,
        blue: this.diagonalForm.blue,
        constraint_type: 'diagonal',
        diagonal_colors: this.diagonalForm.diagonalColorsInput.split(''), // Fix split
  };
      
      console.log("Sending Payload:", payload);
      axios
        .post('http://127.0.0.1:8000/generate-grid', {
          dimension: this.diagonalForm.dimension,
          red: this.diagonalForm.red,
          green: this.diagonalForm.green,
          blue: this.diagonalForm.blue,
          constraint_type: 'diagonal',
          diagonal_colors: this.diagonalForm.diagonalColorsInput.split(''),
        })
        .then(response => {
          this.grid = response.data.grid;
          this.error = null;
        })
        .catch(error => {
          this.grid = [];
          this.error = error.response?.data?.error || 'An error occurred.';
        });
    },
    generateAdjacentGrid() {
      console.log("Adjacency Colors Input:", this.adjForm.adjColorsInput);
      const payload = {
        n: this.adjForm.n,
        m: this.adjForm.m,
        red: this.adjForm.red,
        green: this.adjForm.green,
        blue: this.adjForm.blue,
        constraint_type: 'adj_const',
        adjacency_cons: this.adjForm.adjColorsInput.split(''), // Fix split
  };
      
      console.log("Sending Payload:", payload);
      axios
        .post('http://127.0.0.1:8000/generate-grid', {
          n: this.adjForm.n,
          m: this.adjForm.m,
          red: this.adjForm.red,
          green: this.adjForm.green,
          blue: this.adjForm.blue,
          constraint_type: 'adj_const',
          adjacency_cons: this.adjForm.adjColorsInput.split(''),
        })
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