<template>
    <div id="vanta-bg"></div>
    <div class="container">
      <h1 class="gradient-text fixed-width">Grid Generator</h1>
      <h2 class="subheading">Simplify your Grid creation</h2>
      <p class="description">An easy-to-use AI tool for generating customizable grids with constraints.</p>
      
      <!-- Input Box -->
      <textarea
      class="input-box"
      placeholder="Enter your grid constraints here"
      ></textarea>

      <button class="navigate-btn" @click="navigateToHelloWorld">Generate</button>
    </div>
  </template>
  
  
  <script>
  //import * as THREE from 'three';
  //import NET from "vanta/dist/vanta.net.min.js"; // Import Vanta.js effect

export default {
  data() {
    return {
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
  width: 100%;
  height: 48px;
  padding: 12px;
  font-family: "Poppins", sans-serif;
  font-size: 16px;
  border: 2px solid #595959;
  border-radius: 12px;
  outline: none;
  background-color: #fafafa;
  color: #333;
  box-shadow: 0px 0px 8px rgba(66, 161, 255, 0.4);
  margin-bottom: 20px;
  transition: border-color 0.3s ease;
}

.input-box:focus {
  border-color: #ff9a88;
  box-shadow: 0px 0px 12px rgba(255, 141, 120, 0.5);
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
  </style>
  