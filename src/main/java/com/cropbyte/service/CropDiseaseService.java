package com.cropbyte.service;

import com.cropbyte.dto.PredictionResponse;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.io.Resource;
import org.springframework.core.io.ResourceLoader;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.*;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.util.HashMap;
import java.util.Map;
import java.util.Scanner;

@Service
public class CropDiseaseService {

    @Value("${ml.model.path:Trial model for SIH/crop_disease_model.keras}")
    private String modelPath;

    @Value("${ml.python.script:predict.py}")
    private String pythonScriptPath;

    @Value("${ml.python.executable:python}")
    private String pythonExecutable;

    private final ResourceLoader resourceLoader;

    public CropDiseaseService(ResourceLoader resourceLoader) {
        this.resourceLoader = resourceLoader;
    }

    private static final Map<String, String> FARMER_TIPS = new HashMap<>();

    static {
        FARMER_TIPS.put("Tomato___healthy", 
            "Your plant looks healthy! Keep up the good work. Ensure consistent watering and monitor for any changes.");
        FARMER_TIPS.put("Tomato___Late_blight", 
            "Late Blight detected. Late blight is a fungal disease.\n" +
            "1. **Action**: Immediately remove and destroy infected leaves.\n" +
            "2. **Treatment**: Apply a copper-based fungicide.\n" +
            "3. **Prevention**: Ensure good air circulation around plants and avoid overhead watering.");
    }

    public PredictionResponse predictDisease(MultipartFile image, String notes) throws IOException {
        // Create temporary file for the uploaded image
        Path tempFile = Files.createTempFile("crop_image_", ".jpg");
        Path pythonScriptFile = null;
        
        try {
            // Save uploaded image to temp file
            image.transferTo(tempFile.toFile());
            
            // Get Python script from classpath and copy to temp file
            Resource scriptResource = resourceLoader.getResource("classpath:" + pythonScriptPath);
            if (!scriptResource.exists()) {
                // Try as file path if not in classpath
                pythonScriptFile = Paths.get(pythonScriptPath);
                if (!Files.exists(pythonScriptFile)) {
                    throw new FileNotFoundException("Python script not found: " + pythonScriptPath);
                }
            } else {
                // Copy script from classpath to temp file
                pythonScriptFile = Files.createTempFile("predict_", ".py");
                try (InputStream is = scriptResource.getInputStream()) {
                    Files.copy(is, pythonScriptFile, StandardCopyOption.REPLACE_EXISTING);
                }
            }
            
            // Resolve model path (try relative to current directory)
            Path modelPathResolved = Paths.get(modelPath);
            if (!Files.exists(modelPathResolved)) {
                // Try relative to project root
                Path projectRoot = Paths.get("").toAbsolutePath();
                modelPathResolved = projectRoot.resolve(modelPath);
                if (!Files.exists(modelPathResolved)) {
                    throw new FileNotFoundException("Model file not found: " + modelPath);
                }
            }
            
            // Call Python script for prediction
            String[] command = {
                pythonExecutable,
                pythonScriptFile.toString(),
                tempFile.toString(),
                modelPathResolved.toString()
            };
            
            ProcessBuilder processBuilder = new ProcessBuilder(command);
            // Redirect stderr to devnull to suppress TensorFlow messages
            processBuilder.redirectError(ProcessBuilder.Redirect.DISCARD);
            Process process = processBuilder.start();
            
            // Read output from Python script (only stdout, stderr is discarded)
            StringBuilder output = new StringBuilder();
            try (Scanner scanner = new Scanner(process.getInputStream())) {
                while (scanner.hasNextLine()) {
                    String line = scanner.nextLine();
                    // Only capture lines that match our expected format (CLASS_NAME|CONFIDENCE)
                    if (line.contains("|") && (line.startsWith("Tomato___") || line.startsWith("Error"))) {
                        output.append(line);
                        break; // We only expect one line of output
                    }
                }
            }
            
            int exitCode;
            try {
                exitCode = process.waitFor();
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                throw new RuntimeException("Process was interrupted", e);
            }
            
            if (exitCode != 0) {
                throw new RuntimeException("Python script failed with exit code: " + exitCode);
            }
            
            // Parse Python script output
            // Expected format: CLASS_NAME|CONFIDENCE
            String result = output.toString().trim();
            if (result.isEmpty()) {
                throw new RuntimeException("No output received from Python script");
            }
            
            String[] parts = result.split("\\|");
            
            if (parts.length != 2) {
                throw new RuntimeException("Unexpected output format from Python script: " + result);
            }
            
            String predictedClass = parts[0];
            double confidence = Double.parseDouble(parts[1]);
            String recommendation = FARMER_TIPS.getOrDefault(predictedClass, 
                "No specific recommendation available for this condition.");
            
            return new PredictionResponse("Success", predictedClass, confidence, recommendation);
            
        } finally {
            // Clean up temporary files
            Files.deleteIfExists(tempFile);
            if (pythonScriptFile != null && pythonScriptFile.toString().contains("predict_")) {
                Files.deleteIfExists(pythonScriptFile);
            }
        }
    }
}

