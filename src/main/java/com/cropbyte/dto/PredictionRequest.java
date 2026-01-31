package com.cropbyte.dto;

public class PredictionRequest {
    private String imageBase64;
    private String notes;

    public PredictionRequest() {
    }

    public PredictionRequest(String imageBase64, String notes) {
        this.imageBase64 = imageBase64;
        this.notes = notes;
    }

    public String getImageBase64() {
        return imageBase64;
    }

    public void setImageBase64(String imageBase64) {
        this.imageBase64 = imageBase64;
    }

    public String getNotes() {
        return notes;
    }

    public void setNotes(String notes) {
        this.notes = notes;
    }
}




