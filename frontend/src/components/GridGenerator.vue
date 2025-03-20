<template>
    <div id="vanta-bg"></div>
    <div class="container">
      <h1 class="gradient-text fixed-width">Grid Generator</h1>
      <h2 class="subheading">Simplify your Grid creation</h2>
      <p class="description">An easy-to-use AI tool for generating customizable grids with constraints.</p>
      
      <!-- Input Box -->
      <div class="input-wrapper">
      <textarea
        class="input-box"
        placeholder="Enter your grid constraints here"
        v-model="inputText"
        @keydown.enter.prevent="generateGrid"
      ></textarea>
      <button class="send-btn" @click="generateGrid">
        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M5 12l7-7 7 7"></path>
        <path d="M12 19V5"></path>
        </svg>
      </button>
      </div>
      <!-- Loading Indicator -->
      <div v-if="loading" class="loader">
        <span class="dot"></span>
        <span class="dot"></span>
        <span class="dot"></span>
      </div>

      <!-- Revealing Response -->
      <div v-if="displayText" class="response-box">
        {{ displayText }}
      </div>

      <button class="navigate-btn" @click="navigateToHelloWorld">Start making your grid</button>
    </div>
  </template>
  
  
  <script>
  //import * as THREE from 'three';
  //import NET from "vanta/dist/vanta.net.min.js"; // Import Vanta.js effect
  import axios from "axios";

export default {
  data() {
    return {
      inputText: "",
      response: "",
      displayText: "",
      loading: false,
      vantaEffect: null, // Store Vanta instance
    };
  },
  methods: {
    navigateToHelloWorld() {
      this.$router.push("/hello");
    },
    initVantaEffect() {  // Moved inside methods
      this.vantaEffect = window.VANTA.NET({
        el: "#vanta-bg",
        THREE: window.THREE,
        mouseControls: true,
        touchControls: true,
        gyroControls: false,
        minHeight: 200.0,
        minWidth: 200.0,
        scale: 1.0,
        scaleMobile: 1.0,
        color: 0xff5531,
        lineColor: 0xff0000,  // Line color
        backgroundColor: 0xfff8f6,
        points: 8.00,
        maxDistance: 18.00,
        spacing: 18.0
      });
    },
    async generateGrid() {
      if (!this.inputText.trim()) return;
      this.response = "";
      this.displayText = "";
      this.loading = true;

      try {
        const res = await axios.post("http://localhost:8000/generate-gemini", {
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
      }, 30); // Typing speed (30ms)
    }
  },
  mounted() {
    // Script loading logic
    const threeScript = document.createElement('script');
    threeScript.src = 'https://cdn.jsdelivr.net/npm/three@0.134.0/build/three.min.js';
    
    const vantaScript = document.createElement('script');
    vantaScript.src = 'https://cdn.jsdelivr.net/npm/vanta@latest/dist/vanta.net.min.js';

    threeScript.onload = () => {
      vantaScript.onload = () => {
        this.initVantaEffect();  // Now properly references the method
      };
      document.head.appendChild(vantaScript);
    };
    
    document.head.appendChild(threeScript);
  },
  beforeUnmount() {
    if (this.vantaEffect) {
      this.vantaEffect.destroy();
      this.vantaEffect = null;
    }
  },
};
  </script>
  
  <style scoped>
  @import url("https://fonts.googleapis.com/css2?family=Poppins:wght@600&display=swap");
  
  #vanta-bg {
  position: fixed;
  width: 100%;
  height: 100%;
  z-index: -1;
  top: 0;
  left: 0;
}
  
  .container {
  max-width: 700px;
  margin: auto;
  font-family: "Poppins", sans-serif;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 60vh; /* Ensures full viewport height */
  padding-top: 0; /* Remove unnecessary top padding */
  position: relative;
}

  .input-wrapper {
    position: relative;
    width: 100%;
  }

  .send-btn {
    display: none;
    position: absolute;

    right: -21px;
    bottom: 34px;
    width: 32px;
    height: 32px;
    background-color: #595959;
    color: #fff;
    border: none;
    border-radius: 50%;
    cursor: pointer;
    font-size: 18px;
    align-items: center;
    justify-content: center;
    box-shadow: 0px 0px 10px rgba(30, 143, 255, 0.6);
    transition: background-color 0.2s ease;
  }

  .send-btn:hover {
    background-color: #2d2d2d;
  }
  
  .gradient-text {
    font-size: 5rem;
    font-weight: 700;
    text-align: center;
    width: 100%;
    background: linear-gradient(90deg, #1e90ff, #ff6347);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 10px;
  }

  .subheading {
  font-size: 3rem;
  font-weight: 600;
  color: #1e1e1e;
  margin-top: 5px;
  margin-bottom: 5px;
  }

  .description {
  font-size: 1.2rem;
  font-weight: 200;
  color: #6e6e6e;
  max-width: 600px;
  margin-top: 3px;
  margin-bottom: 20px;
  }

  .fixed-width {
    max-width: 100%;
    white-space: nowrap;
  }

  .input-box {
  display: none;
  width: 100%;
  height: 48px;
  padding: 12px;
  font-family: "Poppins", sans-serif;
  font-size: 16px;
  border: 2px solid #7a7a7a;
  border-radius: 12px;
  outline: none;
  background-color: #fafafa;
  box-shadow: 0px 0px 8px rgba(66, 161, 255, 0.4);
  margin-bottom: 20px;
  transition: border-color 0.3s ease;
}

.input-box:focus {
  border-color: #4f4f4f;
  box-shadow: 0px 0px 12px rgba(255, 211, 203, 0.5);
}
  .navigate-btn {
    background-color: #ffffff;
    color: rgb(192, 120, 120);
    font-weight: bold;
    border: none;
    padding: 12px 24px;
    font-size: 18px;
    border-radius: 12px;
    position: relative;
    overflow: hidden;
    cursor: pointer;
    transition: all 0.3s ease-in-out;
    box-shadow: 0px 0px 10px rgba(30, 143, 255, 0.6);
    margin-top: 16px;
  }
  
  .navigate-btn::before {
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
  .navigate-btn:hover {
    box-shadow: 0px 0px 20px rgba(30, 144, 255, 0.4);
    transform: scale(1.05);
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
    width: 100%;
    transform: translateX(3px);
    padding: 10px;
    margin: auto;
    background-color: #f9f9f9;
    border: 1px solid #ddd;
    border-radius: 12px;
    margin-top: 2px;
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
  </style>
  