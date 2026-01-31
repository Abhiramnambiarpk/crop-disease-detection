# Cropbyte - Technical Specifications for Research Paper

## Project Overview
**Cropbyte** is a full-stack crop disease detection system that uses deep learning to identify plant diseases from images. The system provides real-time disease prediction with actionable recommendations for farmers.

---

## 1. Programming Languages

### Backend
- **Java 17** (JDK 17)
  - Primary language for backend development
  - Used for RESTful API implementation
  - Object-oriented programming paradigm

### Machine Learning
- **Python 3.8+**
  - Used for machine learning model training and inference
  - Script-based execution for predictions
  - Integration with TensorFlow/Keras

### Frontend
- **HTML5**
- **JavaScript** (Vanilla JS)
- **CSS3**

---

## 2. Frameworks and Libraries

### Backend Framework
- **Spring Boot 3.2.0**
  - Main framework for building RESTful web services
  - Provides dependency injection, auto-configuration
  - Embedded Tomcat server

### Spring Boot Modules Used
- **spring-boot-starter-web** (v3.2.0)
  - RESTful API development
  - HTTP request/response handling
  - Multipart file upload support

- **spring-boot-starter-validation** (v3.2.0)
  - Input validation and data binding

- **spring-boot-devtools** (v3.2.0)
  - Development tools for hot reloading

- **spring-boot-starter-test** (v3.2.0)
  - Testing framework integration

### Machine Learning Libraries
- **TensorFlow 2.x**
  - Deep learning framework
  - Model training and inference
  - Keras API integration

- **Keras** (via TensorFlow)
  - High-level neural network API
  - Model architecture definition
  - Transfer learning implementation

- **NumPy**
  - Numerical computations
  - Array operations for image processing

- **Pillow (PIL)**
  - Image loading and preprocessing

- **Matplotlib**
  - Visualization of training results
  - Accuracy and loss plotting

### Utility Libraries
- **Apache Commons IO 2.15.1**
  - File handling utilities
  - I/O operations

- **Jackson Databind**
  - JSON serialization/deserialization
  - REST API JSON processing

### Build Tools
- **Apache Maven**
  - Dependency management
  - Project building and packaging
  - Lifecycle management

---

## 3. Technologies and Tools

### Architecture Pattern
- **RESTful API Architecture**
  - REST principles for API design
  - Stateless communication
  - JSON-based data exchange

- **Service-Oriented Architecture (SOA)**
  - Separation of concerns (Controller, Service, DTO layers)
  - Modular design

### Machine Learning Approach
- **Transfer Learning**
  - Pre-trained MobileNetV2 model (ImageNet weights)
  - Fine-tuning for crop disease classification

- **Deep Learning Model**
  - Convolutional Neural Network (CNN)
  - Base: MobileNetV2 (lightweight, mobile-optimized)
  - Custom classification head

- **Data Augmentation**
  - Random horizontal flips
  - Random rotations (0.2)
  - Random zoom (0.1)
  - Prevents overfitting

- **Regularization Techniques**
  - Dropout (0.3)
  - Data augmentation
  - Transfer learning

### Model Architecture Details
- **Input Size**: 224x224x3 (RGB images)
- **Base Model**: MobileNetV2 (pre-trained on ImageNet)
- **Output Layer**: Dense layer with softmax activation
- **Classes**: 2 (Tomato___healthy, Tomato___Late_blight)
- **Optimizer**: Adam (learning rate: 0.001)
- **Loss Function**: Sparse Categorical Crossentropy
- **Batch Size**: 32
- **Epochs**: 10

### Integration Approach
- **Java-Python Integration**
  - Process-based execution
  - Command-line interface
  - Inter-process communication via stdout/stderr
  - Temporary file handling for image transfer

### Web Technologies
- **HTTP/HTTPS Protocol**
- **Multipart Form Data** (for file uploads)
- **CORS (Cross-Origin Resource Sharing)**
  - Enabled for frontend-backend communication

### Development Tools
- **Maven Compiler Plugin**
  - Java 17 compilation
  - UTF-8 encoding

- **Spring Boot Maven Plugin**
  - JAR packaging
  - Executable JAR creation

---

## 4. Project Structure

```
approooo/
├── src/main/java/com/cropbyte/
│   ├── CropbyteApplication.java          # Spring Boot main class
│   ├── controller/
│   │   └── CropDiseaseController.java    # REST API endpoints
│   ├── service/
│   │   └── CropDiseaseService.java       # Business logic
│   └── dto/
│       ├── PredictionRequest.java        # Request DTO
│       └── PredictionResponse.java       # Response DTO
├── src/main/resources/
│   ├── application.properties            # Configuration
│   └── predict.py                        # ML inference script
├── Trial model for SIH/
│   ├── crop_disease_model.keras          # Trained model
│   ├── train.py                          # Training script
│   └── mini_dataset/                     # Training dataset
├── pom.xml                               # Maven configuration
└── appproo.html                          # Frontend interface
```

---

## 5. Key Features and Functionalities

### Backend Features
1. **Image Upload API**
   - Multipart file upload support
   - Maximum file size: 10MB
   - Image validation

2. **Disease Prediction**
   - Real-time image analysis
   - Confidence score calculation
   - Disease classification

3. **Recommendation System**
   - Context-aware farmer tips
   - Disease-specific treatment advice
   - Prevention strategies

4. **Error Handling**
   - Comprehensive exception handling
   - User-friendly error messages
   - Process management

5. **Health Check Endpoint**
   - System status monitoring
   - Service availability check

### Machine Learning Features
1. **Transfer Learning**
   - Leverages pre-trained MobileNetV2
   - Efficient training with limited data
   - Mobile-optimized architecture

2. **Data Preprocessing**
   - Image resizing (224x224)
   - MobileNetV2 preprocessing
   - Batch normalization

3. **Model Inference**
   - Fast prediction execution
   - Confidence score generation
   - Class probability distribution

---

## 6. API Endpoints

### POST `/api/predict`
- **Purpose**: Disease prediction from uploaded image
- **Content-Type**: `multipart/form-data`
- **Parameters**:
  - `image` (file, required): Crop image file
  - `notes` (string, optional): Additional notes
- **Response**: JSON with prediction results and recommendations

### GET `/api/health`
- **Purpose**: Health check endpoint
- **Response**: Plain text status message

---

## 7. Configuration

### Server Configuration
- **Port**: 8080 (configurable)
- **File Upload Limits**: 10MB max file size

### ML Configuration
- **Model Path**: Configurable via `application.properties`
- **Python Executable**: Configurable (default: `python`)
- **Script Path**: Configurable

---

## 8. Data Flow

1. **Frontend** → Uploads image via HTTP POST
2. **Controller** → Receives multipart request
3. **Service** → Saves image to temporary file
4. **Service** → Executes Python script with image path
5. **Python Script** → Loads Keras model
6. **Python Script** → Preprocesses image
7. **Python Script** → Runs inference
8. **Python Script** → Returns prediction via stdout
9. **Service** → Parses output and generates response
10. **Controller** → Returns JSON response to frontend

---

## 9. Research Paper Keywords

- **Deep Learning**
- **Transfer Learning**
- **Convolutional Neural Networks (CNN)**
- **MobileNetV2**
- **Image Classification**
- **Crop Disease Detection**
- **Computer Vision**
- **RESTful API**
- **Microservices Architecture**
- **Java Spring Boot**
- **TensorFlow/Keras**
- **Agricultural Technology**
- **Precision Agriculture**
- **Machine Learning in Agriculture**

---

## 10. Technical Highlights for Research

1. **Hybrid Architecture**: Java backend with Python ML inference
2. **Transfer Learning**: Efficient use of pre-trained models
3. **Mobile-Optimized**: Lightweight MobileNetV2 for deployment
4. **Real-time Processing**: Fast inference for practical use
5. **Scalable Design**: RESTful API for easy integration
6. **Production-Ready**: Error handling, validation, and monitoring

---

## 11. Dependencies Summary

### Java Dependencies (Maven)
- Spring Boot 3.2.0
- Apache Commons IO 2.15.1
- Jackson Databind
- Spring Boot DevTools
- Spring Boot Test

### Python Dependencies
- TensorFlow 2.x
- NumPy
- Pillow
- Matplotlib

### System Requirements
- Java 17+
- Python 3.8+
- Maven 3.6+
- TensorFlow 2.x

---

## 12. Deployment Information

- **Build Tool**: Maven
- **Packaging**: JAR (Executable)
- **Server**: Embedded Tomcat (via Spring Boot)
- **Port**: 8080 (default)
- **Model Format**: Keras (.keras)
- **Image Format**: JPEG, PNG (via TensorFlow)

---

*This document provides comprehensive technical specifications for the Cropbyte project suitable for research paper documentation.*

