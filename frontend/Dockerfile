# Use Node.js stable version (same as yours)
FROM node:18

# Set working directory inside the container
WORKDIR /app

# Copy package.json and package-lock.json to ensure exact dependency versions
COPY package.json package-lock.json ./

# Install dependencies using npm
RUN npm install

# Copy the rest of the project files
COPY . .

# Expose the default Vue port (adjust if needed)
EXPOSE 5173

# Start the Vue development server
CMD ["npm", "run", "dev"]
