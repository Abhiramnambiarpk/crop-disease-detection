package com.cropbyte.controller;

import com.cropbyte.dto.PredictionResponse;
import com.cropbyte.service.CropDiseaseService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;

@RestController
@RequestMapping("/api")
@CrossOrigin(origins = "*")
public class CropDiseaseController {

    @Autowired
    private CropDiseaseService cropDiseaseService;

    @PostMapping(value = "/predict", consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    public ResponseEntity<PredictionResponse> predictDisease(
            @RequestParam("image") MultipartFile image,
            @RequestParam(value = "notes", required = false) String notes) {
        
        try {
            if (image.isEmpty()) {
                return ResponseEntity.badRequest()
                    .body(new PredictionResponse("Error", "No image provided", 0.0, "Please upload an image."));
            }

            PredictionResponse response = cropDiseaseService.predictDisease(image, notes);
            return ResponseEntity.ok(response);
            
        } catch (IOException e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body(new PredictionResponse("Error", "File processing error", 0.0, 
                    "Failed to process image: " + e.getMessage()));
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body(new PredictionResponse("Error", "Prediction error", 0.0, 
                    "Failed to predict disease: " + e.getMessage()));
        }
    }

    @GetMapping("/health")
    public ResponseEntity<String> health() {
        return ResponseEntity.ok("Backend is running!");
    }
}

