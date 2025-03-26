# ✅ Base Image
FROM python:3.9

# ✅ Set the working directory
WORKDIR /app

# ✅ Copy all files to the container
COPY . /app

# ✅ Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# ✅ Expose the port Hugging Face expects
EXPOSE 7860

# ✅ Start the Flask App
CMD ["gunicorn", "-b", "0.0.0.0:7860", "app:app"]
