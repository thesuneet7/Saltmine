<template>
  <div id="particles-js"></div>
  <div class="container">
    <h1 class="gradient-text">Grid Generator</h1>
    
    <div class="right-column">
      <div class="form-container" v-if="activeTab">
        <div class="constraint-selector">
          <h3>Choose Constraint : </h3>
          <select v-model="activeTab" class="constraint-select">
            <option v-for="tab in tabs" :key="tab.id" :value="tab.id">
              {{ tab.label }}
            </option>
          </select>
        </div>

    
        <template v-for="(value, key) in formValues[activeTab]" :key="key">
    <div class="form-row">
      <div class="input-slider-group" v-if="!key.includes('ColorsInput') && key !== 'block_color'">
        <input 
          type="number" 
          v-model="formValues[activeTab][key]"
          :placeholder="fieldLabels[key] || key"
          min="0"
          max="50"
        >
        <input
          type="range"
          v-model="formValues[activeTab][key]"
          min="0"
          max="50"
          class="slider"
        >
      </div>
      <input 
        v-else 
        type="number" 
        v-model="formValues[activeTab][key]"
        :placeholder="fieldLabels[key] || key"
      />
    </div>
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
        { id: 'block', label: 'Coloured Block' },
        { id: 'patternnn', label: 'Pattern' }
      ],
      formValues: {
        periphery: { n: null, m: null, red: null, green: null, blue: null, peripheryColorsInput: '' },
        diagonal: { dimension: null, red: null, green: null, blue: null, diagonalColorsInput: '' },
        adj_const: { n: null, m: null, red: null, green: null, blue: null, adjColorsInput: '' },
        no_adj_const: { n: null, m: null, red: null, green: null, blue: null },
        block: { n: null, m: null, red: null, green: null, blue: null, block_color: '', block_size: null, block_count: null },
        patternnn: { n: null, m: null, red: null, green: null, blue: null, pattern_length: null, patternColorsInput: '' }
      },
      fieldLabels: {
  n: "Rows",
  m: "Columns",
  red: "Red Count",
  green: "Green Count",
  blue: "Blue Count",
  peripheryColorsInput: "Periphery Colors",
  diagonalColorsInput: "Diagonal Colors",
  adjColorsInput: "Adjacency Colors",
  patternColorsInput: "Pattern Colors",
  dimension: "Dimension",
  block_color: "Block Color",
  block_size: "Block Size",
  block_count: "Block Count",
  pattern_length: "Pattern Length"
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
      if (Object.prototype.hasOwnProperty.call(form, 'patternColorsInput')) 
        payload.pattern = form.patternColorsInput.split('');


      
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
  display: grid;
  grid-template-columns: 50% 50%;
  gap: 20px;
  max-width: 100%;
  margin: auto;
  font-family: 'Poppins', sans-serif;
  text-align: center;
}

.gradient-text {
  grid-column: 1 / -1;
}

.right-column {
  grid-column: 2;
  text-align: left;
  padding-left: 20px;
}

.tabs {
  display: none;
}

.constraint-selector {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
  width: 96%;
  gap: 20px;
}

.constraint-selector h3 {
  margin: 0;
  font-size: 1.2rem;
  color: #363636;
  white-space: nowrap;
}

.constraint-select {
  width: 100%;
  padding: 12px;
  border: 2px solid #4b4b4b;
  border-radius: 12px;
  font-size: 16px;
  font-weight: bold;
  appearance: none;
  background-image: url("data:image/svg+xml;charset=US-ASCII,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%22292.4%22%20height%3D%22292.4%22%3E%3Cpath%20fill%3D%22%23000000%22%20d%3D%22M287%2069.4a17.6%2017.6%200%200%200-13-5.4H18.4c-5%200-9.3%201.8-12.9%205.4A17.6%2017.6%200%200%200%200%2082.2c0%205%201.8%209.3%205.4%2012.9l128%20127.9c3.6%203.6%207.8%205.4%2012.8%205.4s9.2-1.8%2012.8-5.4L287%2095c3.5-3.5%205.4-7.8%205.4-12.8%200-5-1.9-9.2-5.5-12.8z%22%2F%3E%3C%2Fsvg%3E");
  background-repeat: no-repeat;
  background-position: right 12px center;
  background-size: 12px auto;
  cursor: pointer;
  transition: all 0.3s ease;
}

.constraint-select:focus {
  outline: none;
  border-color: #1e90ff;
  box-shadow: 0 0 0 3px rgba(30, 144, 255, 0.2);
}

.grid-container {
  justify-content: flex-start;
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
  align-items: flex-start;
}

.form-row {
  display: flex;
  margin-bottom: 15px;
  width: 100%;
}

.input-slider-group {
  display: flex;
  align-items: center;
  gap: 15px;
  width: 100%;
}

input[type="number"] {
  width: 80px;
  text-align: center;
}

.slider {
  flex-grow: 1;
  -webkit-appearance: none;
  height: 6px;
  background: #e0e0e0;
  border-radius: 5px;
  outline: none;
  margin-right: 30px;
}

/* Slider Thumb */
.slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 20px;
  height: 20px;
  background: #767676;
  border-radius: 50%;
  cursor: pointer;
  transition: transform 0.2s;
}

.slider::-moz-range-thumb {
  width: 20px;
  height: 20px;
  background: linear-gradient(90deg, #1e90ff, #ff6347);
  border-radius: 50%;
  cursor: pointer;
}

.slider::-webkit-slider-thumb:hover {
  transform: scale(1.1);
}


label {
  display: none;
}

input[type="number"], 
input[type="text"] {
  width: 20%;
  padding: 12px;
  border: 2px solid #4b4b4b;
  border-radius: 12px;
  font-size: 14px;
  font-weight: bold;
  transition: all 0.3s ease;
}

input[type="number"]::placeholder,
input[type="text"]::placeholder {
  color: #666;
  opacity: 0.8;
}

input:focus {
  outline: none;
  border-color: #1e90ff;
  box-shadow: 0 0 0 3px rgba(30, 144, 255, 0.2);
}

input[type="number"] {
  -moz-appearance: textfield;
  appearance: textfield;
}

input[type="number"]::-webkit-outer-spin-button,
input[type="number"]::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
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
  margin-top: 30px;
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