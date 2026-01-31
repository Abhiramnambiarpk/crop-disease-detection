# Setup Guide for Cropbyte Backend

## Quick Start

### 1. Prerequisites Check

Make sure you have installed:
- **Java 17+** (check with `java -version`)
- **Maven 3.6+** (check with `mvn -version`)
- **Python 3.8+** (check with `python --version` or `python3 --version`)

### 2. Install Python Dependencies

```bash
pip install tensorflow numpy pillow
```

Or if you need to use `python3`:
```bash
python3 -m pip install tensorflow numpy pillow
```

### 3. Verify ML Model Location

Ensure your ML model file exists at:
```
Trial model for SIH/crop_disease_model.keras
```

If your model is in a different location, update `src/main/resources/application.properties`:
```properties
ml.model.path=your/path/to/crop_disease_model.keras
```

### 4. Configure Python Executable (if needed)

If your Python command is `python3` instead of `python`, update `src/main/resources/application.properties`:
```properties
ml.python.executable=python3
```

### 5. Build the Project

```bash
mvn clean install
```

### 6. Run the Backend

```bash
mvn spring-boot:run
```

Or run the JAR file:
```bash
java -jar target/cropbyte-backend-1.0.0.jar
```

The backend will start on `http://localhost:8080`

### 7. Test the Backend

Open your browser and visit:
```
http://localhost:8080/api/health
```

You should see: "Backend is running!"

### 8. Open the Frontend

Open `appproo.html` in your web browser. The frontend is configured to connect to `http://localhost:8080/api/predict`

## Troubleshooting

### Python Not Found
**Error:** `python not found` or `python3 not found`

**Solution:** 
1. Make sure Python is installed and in your PATH
2. Update `application.properties` with the correct Python executable:
   - Windows: `python` or `py`
   - Linux/Mac: `python3`

### Model File Not Found
**Error:** `Model file not found`

**Solution:**
1. Check that `crop_disease_model.keras` exists in `Trial model for SIH/` directory
2. Update the path in `application.properties` if your model is in a different location
3. Use absolute path if relative path doesn't work

### Port Already in Use
**Error:** `Port 8080 is already in use`

**Solution:**
1. Change the port in `application.properties`:
   ```properties
   server.port=8081
   ```
2. Update the frontend `API_BASE_URL` in `appproo.html` to match the new port

### CORS Errors
**Error:** CORS policy errors in browser console

**Solution:**
The backend already includes CORS configuration. If you still see errors:
1. Make sure the backend is running
2. Check that the frontend is making requests to the correct URL
3. Verify the backend URL in `appproo.html` matches your backend port

### Python Script Errors
**Error:** Python script execution fails

**Solution:**
1. Test the Python script manually:
   ```bash
   python src/main/resources/predict.py <image_path> <model_path>
   ```
2. Make sure all Python dependencies are installed
3. Check that TensorFlow can load your model:
   ```python
   import tensorflow as tf
   model = tf.keras.models.load_model('Trial model for SIH/crop_disease_model.keras')
   ```

## Development Tips

- The backend uses Spring Boot DevTools for hot reloading during development
- Check logs in the console for detailed error messages
- Use Postman or curl to test the API endpoints:
  ```bash
  curl -X POST http://localhost:8080/api/predict \
    -F "image=@path/to/image.jpg" \
    -F "notes=Test notes"
  ```




