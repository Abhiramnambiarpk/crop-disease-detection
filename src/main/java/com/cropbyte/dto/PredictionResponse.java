package com.cropbyte.dto;

public class PredictionResponse {
    private String status;
    private String predictedClass;
    private double confidence;
    private String recommendation;

    public PredictionResponse() {
    }

    public PredictionResponse(String status, String predictedClass, double confidence, String recommendation) {
        this.status = status;
        this.predictedClass = predictedClass;
        this.confidence = confidence;
        this.recommendation = recommendation;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    public String getPredictedClass() {
        return predictedClass;
    }

    public void setPredictedClass(String predictedClass) {
        this.predictedClass = predictedClass;
    }

    public double getConfidence() {
        return confidence;
    }

    public void setConfidence(double confidence) {
        this.confidence = confidence;
    }

    public String getRecommendation() {
        return recommendation;
    }

    public void setRecommendation(String recommendation) {
        this.recommendation = recommendation;
    }
}




