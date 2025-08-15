package com.example.Ecommerce.Model;

import java.util.List;

public class RecommendationResponse {

    private List<Integer> recommended_product_ids;

    // Getters and setters
    public List<Integer> getRecommended_product_ids() {
        return recommended_product_ids;
    }

    public void setRecommended_product_ids(List<Integer> recommended_product_ids) {
        this.recommended_product_ids = recommended_product_ids;
    }
}