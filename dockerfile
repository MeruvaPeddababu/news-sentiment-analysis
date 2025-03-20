# Use Python 3.9
FROM python:3.9

# Set working directory
WORKDIR /app

# Copy all files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port for Flask & Streamlit
EXPOSE 7860

# Start Flask & Streamlit
CMD ["sh", "-c", "python backend.py & streamlit run app.py --server.port 7860 --server.address 0.0.0.0"]
