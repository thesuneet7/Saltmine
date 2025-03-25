<template>
  <div id="particles-js"></div>
  <div class="container">
    <h1 class="gradient-text">Grid Generator</h1>

    <!-- Left Column -->
    <div class="left-column">
      <div class="input-wrapper">
        <textarea
          class="input-box"
          placeholder="Enter your grid constraints here"
          v-model="inputText"
          @keydown.enter.prevent="generatePrompt"
        ></textarea>
        <button class="send-btn" @click="generatePrompt">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M5 12l7-7 7 7"></path>
            <path d="M12 19V5"></path>
          </svg>
        </button>
      </div>

      <div v-if="loading" class="loader">
        <span class="dot"></span>
        <span class="dot"></span>
        <span class="dot"></span>
      </div>

      <div v-if="displayText" class="response-box">
        {{ displayText }}
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
        type="text" 
        v-model="formValues[activeTab][key]"
        :placeholder="fieldLabels[key] || key"
      />
    </div>
  </template>
      <button class="generate-btn" @click="generateGrid">Generate Grid</button>
    </div>


    
    
  </div>
</div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      inputText: "",
      response: "",
      displayText: "",
      loading: false,
      activeTab: 'periphery',
      tabs: [
        { id: 'periphery', label: 'Periphery' },
        { id: 'diagonal', label: 'Diagonal' },
        { id: 'adj_const', label: 'Adjacency' },
        { id: 'no_adj_const', label: 'No Adjacency' },
        { id: 'block', label: 'Coloured Block' },
        { id: 'patternnn', label: 'Pattern' },
        { id: 'diagonal_adj_const', label: 'Diagonal & Adjacent' },
        { id: 'periphery_bb_const', label: 'Periphery & Big-Block' },
        { id: 'dpp1_const', label: 'Periphery & Diagonal & Pattern' },
        { id: 'dpp2_const', label: 'Periphery & Diagonal with Priority' },
        { id: 'periphery_pattern_const', label: 'Periphery & Pattern'},
        { id: 'periphery_nadj_const', label: 'Periphery & Non-Adjacent'},
        { id: 'adp_const', label: 'Periphery & Diagonal & Adjacent' }
      ],
      formValues: {
        periphery: { n: 8, m: 8, red: 20, green: 23, blue: 21, peripheryColorsInput: 'R' },
        diagonal: { dimension: 8, red: 19, green: 33, blue: 12, diagonalColorsInput: 'B' },
        adj_const: { n: 8, m: 8, red: 20, green: 33, blue: 11, adjColorsInput: 'BR' },
        no_adj_const: { n: 10, m: 10, red: 20, green: 50, blue: 30 },
        block: { n: 10, m: 10, red: 20, green: 30, blue: 50, block_color: 'B', block_size: 3, block_count: 2 },
        patternnn: { n: 8, m: 8, red: 17, green: 19, blue: 28, pattern_length: 3, patternColorsInput: 'BBG' },
        diagonal_adj_const: { dimension: 10, red: 22, green: 30, blue: 48, diagonalColorsInput: 'R', adjColorsInput: 'GB'},
        periphery_bb_const: { n: 10, m: 10, red: 25, green: 30, blue: 45, peripheryColorsInput: 'G', block_color: 'B', block_size: 4, block_count: 2 },
        dpp1_const: { dimension: 8, red: 23, green: 32, blue: 9, peripheryColorsInput: 'RG', diagonalColorsInput: 'BG' },
        dpp2_const: { dimension: 8, red: 24, green: 15, blue: 25, peripheryColorsInput: 'R', diagonalColorsInput: 'G' },
        periphery_pattern_const: { n: 10, m: 10, red: 30, green: 45, blue: 25, peripheryColorsInput: 'R', pattern_length: 3, patternColorsInput: 'GGB' },
        periphery_nadj_const: { n: 10, m: 15, red: 40, green: 50, blue: 60, peripheryColorsInput: 'R' },
        adp_const: {dimension: 10, red: 36, green: 36, blue: 28, peripheryColorsInput: 'B', diagonalColorsInput: 'R', adjacent_tilesColorsInput: 'RG' }
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
  pattern_length: "Pattern Length",
  constraint_priorityColorsInput: "diagonal or periphery?",
  adjacent_tilesColorsInput: "Any two adjacent colors"
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

      delete payload.peripheryColorsInput;
      delete payload.diagonalColorsInput;
      delete payload.adjColorsInput;
      delete payload.patternColorsInput;
      delete payload.adjacent_tilesColorsInput;


      // Process color inputs only when they have content
      if (form.peripheryColorsInput?.trim()) {
        payload.periphery_colors = form.peripheryColorsInput.trim().split('');
      }
      if (form.diagonalColorsInput?.trim()) {
        payload.diagonal_colors = form.diagonalColorsInput.trim().split('');
      }
      if (form.adjColorsInput?.trim()) {
        payload.adjacency_cons = form.adjColorsInput.trim().split('');
      }
      if (form.patternColorsInput?.trim()) {
        payload.pattern = form.patternColorsInput.trim().split('');
      }
      if (form.adjacent_tilesColorsInput?.trim()) {
        payload.adjacent_tiles = form.adjacent_tilesColorsInput.trim().split('');
      }


      
      console.log("Sending Payload:", payload);
      axios.post(`${process.env.VUE_APP_API_URL}/generate-grid`, payload)
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
    async generatePrompt() {
      if (!this.inputText.trim()) return;
      this.response = "";
      this.displayText = "";
      this.loading = true;

      try {
        const res = await axios.post(`${process.env.VUE_APP_API_URL}/generate-gemini`, {
          text: this.inputText,
        });
        this.response = res.data.response;
        this.loading = false;
        this.revealText();
      } catch (error) {
        console.error("Error:", error);
        this.response = "Failed to generate response.";
        this.loading = false;
      }
    },
    revealText() {
      let index = 0;
      this.displayText = "";
      const interval = setInterval(() => {
        if (index < this.response.length) {
          this.displayText += this.response[index];
          index++;
        } else {
          clearInterval(interval);
        }
      }, 10); // Typing speed (30ms)
    }
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

.input-wrapper {
    position: relative;
    width: calc(100% - 20px);
    margin: 0 0 0 10px;

  }

  .input-box {
  width: calc(100% + 8px);
  height: 48px;
  padding: 12px;
  font-family: "Poppins", sans-serif;
  font-size: 16px;
  border: 2px solid #7a7a7a;
  border-radius: 12px;
  outline: none;
  background-color: #fafafa;
  box-shadow: 0px 0px 8px rgba(66, 161, 255, 0.4);
  margin-bottom: 5px;
  margin-left: -8px;
  transition: border-color 0.3s ease;
}

.input-box:focus {
  border-color: #4f4f4f;
  box-shadow: 0px 0px 12px rgba(255, 211, 203, 0.5);
}

.send-btn {
    position: absolute;
    right: -29px;
    bottom: 20px;
    width: 32px;
    height: 32px;
    background-color: #595959;
    color: #fff;
    border: none;
    border-radius: 50%;
    cursor: pointer;
    font-size: 18px;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0px 0px 10px rgba(30, 143, 255, 0.6);
    transition: background-color 0.2s ease;
    padding: 7px;
    
  }

  .send-btn svg {
  display: block;
  width: 100%;
  height: 100%;
}

  .send-btn:hover {
    background-color: #2d2d2d;
  }

.loader {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 12px;
  }

  .dot {
    width: 8px;
    height: 8px;
    margin: 0 4px;
    background-color: #575757;
    border-radius: 50%;
    animation: pulse 1.5s infinite ease-in-out;
  }

  .dot:nth-child(1) {
    animation-delay: 0s;
  }

  .dot:nth-child(2) {
    animation-delay: 0.2s;
  }

  .dot:nth-child(3) {
    animation-delay: 0.4s;
  }

  @keyframes pulse {
    0%, 80%, 100% {
      transform: scale(0);
      opacity: 0.3;
    }
    40% {
      transform: scale(1);
      opacity: 1;
    }
  }

    .response-box {
    width: 98%;
    transform: translateX(3px);
    padding: 10px;
    
    background-color: #f9f9f9;
    border: 1px solid #ddd;
    border-radius: 12px;
    margin-top: 0px;
    font-size: 16px;
    color: #333;
    white-space: pre-wrap;
    box-shadow: 0px 0px 6px rgba(0, 0, 0, 0.1);
    animation: fadeIn 0.3s ease;
    text-align: left;
  }

  @keyframes fadeIn {
    from {
      opacity: 0;
      transform: translateY(10px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

.gradient-text {
  grid-column: 1 / -1;
}

.right-column {
  grid-column: 2;
  text-align: left;
  padding: 0 30px;
}

.left-column {
  grid-column: 1;
  padding: 0 30px; /* This adds 30px padding to left/right sides */
  display: flex;
  flex-direction: column;
  gap: 20px;
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
  justify-content: center;
  margin-top: 0px;
  display: flex;
  width: fit-content;
  margin-left: auto;
  margin-right: auto;
  margin-top: auto;
  margin-bottom: auto;
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
  margin-left: auto;
  margin-right: auto;
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

table {
  border-collapse: collapse;
  width: 100%;
  
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