package com.example.Ecommerce.Model;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@AllArgsConstructor
@NoArgsConstructor
@Getter
@Setter
@Entity
public class Product {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private int id;

    @ManyToOne
    @JoinColumn(name = "subcategory_id")
    private subcategory subcategory; // FIX: Capitalized class name

    @Column(length = 500)
    private String title;

    @Column(length = 5000)
    private String description;

    private String category;

    private Double price;

    private int stock;

    private  String image;

    private int discount;

    // --- THIS IS THE CRITICAL FIX ---
    // This annotation tells your application the correct column name in the database.
    @Column(name = "discount_priced")
    private Double discountPrice;

    private Boolean isActive;

    private String brand;
}