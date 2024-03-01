# Use a smaller base image
FROM node:18-alpine

# Set the working directory in the container
WORKDIR /app

COPY . .

# Install only production dependencies
RUN npm install


# Expose a port to communicate with the React app
EXPOSE 3000

# Start your React app
CMD ["npm", "run", "start", "--", "--host", "0.0.0.0"]
