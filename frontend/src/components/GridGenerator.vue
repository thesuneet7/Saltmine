<template>
    <div id="particles-js"></div>
    <div class="container">
      <h1 class="gradient-text fixed-width">Grid Generator</h1>
      <h2 class="subheading">Simplify your Grid creation</h2>
      <p class="description">An easy-to-use tool for generating customizable grids with constraints.</p>
      <button class="navigate-btn" @click="navigateToHelloWorld">Start</button>
    </div>
  </template>
  
  <script>
  export default {
    methods: {
      navigateToHelloWorld() {
        this.$router.push("/hello");
      },
    },
  };
  </script>
  
  <style scoped>
  @import url("https://fonts.googleapis.com/css2?family=Poppins:wght@600&display=swap");
  
  #particles-js {
    position: fixed;
    width: 100%;
    height: 100%;
    z-index: -1;
    top: 0;
    left: 0;
    background: #ffffff; /* Optional: You can change this */
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
  