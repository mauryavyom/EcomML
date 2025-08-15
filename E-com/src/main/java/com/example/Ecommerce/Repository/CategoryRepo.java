package com.example.Ecommerce.Repository;

import com.example.Ecommerce.Model.Category;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface CategoryRepo extends JpaRepository<Category,Integer> {

    public Boolean existsByName(String name);

    public List<Category> findByIsActiveTrue();
}
