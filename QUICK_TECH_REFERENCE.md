# Cropbyte - Quick Technology Reference Guide

## 🎯 One-Page Tech Summary

### Frontend Stack
```
┌─────────────────────────────────────┐
│    HTML5 / CSS3 / JavaScript        │
│  ──────────────────────────────────  │
│  ✓ Single-page responsive UI        │
│  ✓ 7 Languages support              │
│  ✓ Mobile camera capture            │
│  ✓ Multipart form upload            │
│  ✓ Font Awesome icons (CDN)         │
└─────────────────────────────────────┘
```

**Key JavaScript APIs:**
- `Fetch API` → HTTP requests
- `FormData API` → Multipart encoding
- `File API` → Image upload
- `FileReader API` → Image preview
- `LocalStorage API` → Language persistence

---

### Backend Stack
```
┌─────────────────────────────────────┐
│       Java + Spring Boot            │
│  ──────────────────────────────────  │
│  ✓ RESTful API (Spring Web)         │
│  ✓ Dependency Injection (Spring IoC)│
│  ✓ Multipart file handling          │
│  ✓ MVC architecture                 │
│  ✓ CORS support                     │
│  ✓ Built-in Tomcat server           │
└─────────────────────────────────────┘
```

**Spring Boot Components:**
- `@SpringBootApplication` — Entry point
- `@RestController` — HTTP endpoints
- `@Service` — Business logic
- `@Autowired` — Dependency injection
- `@Value` — Config properties

---

### ML Stack
```
┌─────────────────────────────────────┐
│    Python + TensorFlow + Keras      │
│  ──────────────────────────────────  │
│  ✓ Deep learning inference          │
│  ✓ MobileNetV2 transfer learning    │
│  ✓ Image preprocessing (224×224)    │
│  ✓ Softmax classification           │
│  ✓ NumPy for numerical compute      │
└─────────────────────────────────────┘
```

**ML Libraries:**
- `TensorFlow 2.x` — Framework
- `Keras` — High-level API
- `NumPy` — Array operations
- `Pillow (PIL)` — Image loading

---

## 📊 Technology Comparison Table

| Aspect | Frontend | Backend | ML |
|--------|----------|---------|-----|
| **Language** | JavaScript (ES6+) | Java 11+ | Python 3.8+ |
| **Framework** | Vanilla (No framework) | Spring Boot 2.7/3.x | TensorFlow/Keras |
| **Paradigm** | Functional + Imperative | OOP + DI | Functional + Procedural |
| **Runtime** | Browser (Chrome, FF, Safari) | JVM (8GB RAM typical) | Python Interpreter (2GB typical) |
| **Build Tool** | None (HTML/JS direct) | Maven 3.8+ | Pip + Conda |
| **Main File** | appproo.html | pom.xml | predict.py |
| **Package Size** | ~50KB | ~88MB JAR | Model ~88MB |

---

## 🔄 Data Flow (Simplified)

```
USER
 ├─ Selects language (Hindi, Tamil, etc.)
 ├─ Uploads crop image
 ├─ Clicks "Analyze"
 │
 ▼
FRONTEND (JavaScript)
 ├─ Reads file from input
 ├─ Creates FormData (image + notes)
 ├─ fetch() POST to /api/predict
 │
 ▼
BACKEND (Java/Spring)
 ├─ @PostMapping /api/predict receives request
 ├─ Saves image to /tmp/crop_image_XXX.jpg
 ├─ Calls CropDiseaseService.predictDisease()
 │
 ▼
SERVICE (Java)
 ├─ Copies predict.py to /tmp/
 ├─ Loads config: model path, python executable
 ├─ Creates ProcessBuilder: python predict.py <image> <model>
 ├─ Reads stdout from Python process
 ├─ Parses "CLASS_NAME|CONFIDENCE"
 │
 ▼
PYTHON INFERENCE (predict.py)
 ├─ import tensorflow as tf
 ├─ Load model: tf.keras.models.load_model()
 ├─ Load image: tf.keras.utils.load_img()
 ├─ Preprocess: mobilenet_v2.preprocess_input()
 ├─ Predict: model.predict()
 ├─ Compute softmax
 ├─ Find argmax → predicted class
 ├─ Calculate confidence %
 ├─ print("Tomato___Late_blight|92.33")
 │
 ▼
SERVICE (Java)
 ├─ Maps class to farmer tips (dict lookup)
 ├─ Builds PredictionResponse JSON:
 │  {
 │    "status": "Success",
 │    "predictedClass": "Tomato___Late_blight",
 │    "confidence": 92.33,
 │    "recommendation": "Apply fungicide..."
 │  }
 ├─ Cleans up temp files
 ├─ Returns ResponseEntity.ok()
 │
 ▼
FRONTEND (JavaScript)
 ├─ Receives JSON response
 ├─ Displays results in browser
 ├─ Shows image, class, confidence, recommendation
 │
 ▼
USER
 └─ Sees prediction + farmer advice
```

---

## 📝 API Specification

### Endpoint 1: Predict Disease
```
POST /api/predict
Content-Type: multipart/form-data

Request:
  form-data:
    image: [binary JPG/PNG file]
    notes: [optional text]

Response (Success):
  HTTP 200 OK
  {
    "status": "Success",
    "predictedClass": "Tomato___healthy",
    "confidence": 94.56,
    "recommendation": "Your plant looks healthy!..."
  }

Response (Error):
  HTTP 500 Internal Server Error
  {
    "status": "Error",
    "predictedClass": "N/A",
    "confidence": 0.0,
    "recommendation": "Failed to process image..."
  }
```

### Endpoint 2: Health Check
```
GET /api/health

Response:
  HTTP 200 OK
  "Backend is running!"
```

---

## 🛠 Key Dependencies

### Backend (Maven pom.xml)
```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
    <!-- Includes: Spring Web, Embedded Tomcat, Jackson JSON -->
</dependency>
```

### Frontend (CDN)
```html
<!-- Font Awesome Icons -->
<link rel="stylesheet" href=
  "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css">
```

### ML (Python requirements)
```bash
pip install tensorflow>=2.10
pip install numpy
pip install pillow  # For image loading (optional, TF includes it)
```

---

## 🎨 UI/UX Features

### Multilingual Support
```
Languages: English, हिंदी, മലയാളം, தமிழ், తెలుగు, ಕನ್ನಡ, मराठी
Storage: Browser LocalStorage (persisted)
Fallback: English if not selected
```

### Responsive Design
```
Desktop: 350px card, centered layout
Mobile (≤500px): 98vw card, optimized touch targets
Breakpoint: @media (max-width: 500px)
```

### Color Scheme
```
Primary Green: #2ecc40     (Active, CTA buttons)
Secondary Green: #27ae60   (Hover states)
Light Green: #eafaf1       (Background)
Dark Green: #145a32        (Text)
Gray: #f9f9f9             (Alternate BG)
```

---

## 📦 Project Structure

```
approooo/
├── appproo.html                    [Frontend: HTML5/CSS3/JS]
├── pom.xml                         [Maven config + dependencies]
├── src/main/java/com/cropbyte/
│   ├── CropbyteApplication.java    [Entry point @SpringBootApplication]
│   ├── controller/
│   │   └── CropDiseaseController.java  [@RestController, @PostMapping]
│   ├── service/
│   │   └── CropDiseaseService.java     [@Service, subprocess management]
│   └── dto/
│       ├── PredictionRequest.java      [Request DTO]
│       └── PredictionResponse.java     [Response DTO]
├── src/main/resources/
│   ├── application.properties       [Config: port, model path, python exec]
│   └── predict.py                  [ML inference script]
├── target/
│   └── cropbyte-backend-1.0.0.jar  [Compiled JAR]
└── Trial model for SIH/
    ├── crop_disease_model.keras    [Trained Keras model]
    ├── train.py                    [Training script]
    └── mini_dataset/               [Training data]
```

---

## 🚀 Quick Start Commands

### 1. Build Backend
```bash
cd c:\Users\pkabh\OneDrive\Desktop\approooo
mvn clean package
```

### 2. Run Backend
```bash
mvn spring-boot:run
# Server runs on http://localhost:8080
```

### 3. Test Frontend
```bash
# Open in browser:
file:///c:/Users/pkabh/OneDrive/Desktop/approooo/appproo.html
# Or serve via HTTP server (recommended for CORS)
python -m http.server 3000
# Then visit: http://localhost:3000/appproo.html
```

### 4. Test API
```bash
# Health check
curl http://localhost:8080/api/health

# Predict (with image file)
curl -F "image=@crop.jpg" http://localhost:8080/api/predict
```

---

## 💡 Design Patterns Used

| Pattern | Used In | Purpose |
|---------|---------|---------|
| **MVC** | Controller + Service + DTO | Separation of concerns |
| **Dependency Injection** | Spring @Autowired | Loose coupling |
| **DTO** | PredictionRequest/Response | Decouple API from business logic |
| **Facade** | CropDiseaseService | Simplify subprocess complexity |
| **Configuration Externalization** | application.properties | Environment-specific configs |

---

## 📊 Technology Maturity & Industry Usage

| Technology | Maturity | Industry Usage | Production Ready |
|-----------|----------|----------------|------------------|
| HTML5 | ⭐⭐⭐⭐⭐ | Universal | ✅ Yes |
| CSS3 | ⭐⭐⭐⭐⭐ | Universal | ✅ Yes |
| JavaScript (ES6+) | ⭐⭐⭐⭐⭐ | Universal | ✅ Yes |
| Java 11 | ⭐⭐⭐⭐⭐ | Enterprise | ✅ Yes (LTS) |
| Spring Boot | ⭐⭐⭐⭐⭐ | Enterprise | ✅ Yes |
| TensorFlow 2.x | ⭐⭐⭐⭐⭐ | Research + Production | ✅ Yes |
| Keras | ⭐⭐⭐⭐⭐ | ML Industry Standard | ✅ Yes |
| Python 3.8+ | ⭐⭐⭐⭐⭐ | Data Science Standard | ✅ Yes |

---

## 🔒 Security & Best Practices

### Implemented
✅ CORS support for cross-origin requests  
✅ File upload size limits (10MB)  
✅ Error handling with try-catch blocks  
✅ Temporary file cleanup (no disk bloat)  
✅ Input validation (file existence checks)  

### Recommendations for Production
🔒 Add authentication (JWT/OAuth2)  
🔒 Implement rate limiting  
🔒 Add HTTPS/TLS  
🔒 Restrict CORS origins (not "*")  
🔒 Add request logging  
🔒 Add monitoring & alerting  
🔒 Database for result history  

---

## 📖 Learning Resources

### Frontend
- MDN Web Docs: https://developer.mozilla.org/
- JavaScript Tutorial: https://javascript.info/
- HTML5 Spec: https://html.spec.whatwg.org/

### Backend
- Spring Boot Guide: https://spring.io/guides/gs/spring-boot/
- Baeldung: https://www.baeldung.com/spring-boot
- Java SE Docs: https://docs.oracle.com/javase/

### Machine Learning
- TensorFlow Docs: https://www.tensorflow.org/
- Keras API: https://keras.io/
- MobileNetV2 Paper: https://arxiv.org/abs/1801.04381

---

**Created:** November 2024  
**For:** Research Paper Documentation  
**Status:** Complete & Ready to Reference
