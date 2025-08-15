package com.example.Ecommerce.Service.impl;

import com.example.Ecommerce.Model.Category;
import com.example.Ecommerce.Repository.CategoryRepo;
import com.example.Ecommerce.Service.CategoryService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.util.ObjectUtils;

import java.util.List;

@Service
public class CategoryServiceimpl implements CategoryService {

    @Autowired
    private CategoryRepo categoryRepo;
    @Override
    public Category saveCategory(Category category) {
        return categoryRepo.save(category);
    }

    @Override
    public Boolean existCategory(String name) {
        return categoryRepo.existsByName(name);
    }


    @Override
    public List<Category> getAllCategory() {
        return categoryRepo.findAll();
    }

    @Override
    public Boolean deleteCategory(int id) {
       Category category=categoryRepo.findById(id).orElse(null);

    if(!ObjectUtils.isEmpty(category)){
        categoryRepo.delete(category);
        return true;
    }
        return false;
    }

    @Override
    public Category getCategoryById(int id) {
        Category category =categoryRepo.findById(id).orElse(null);
        return category;
    }

    @Override
    public List<Category> getAllActiveCategory() {
      List<Category> categories= categoryRepo.findByIsActiveTrue();
      return  categories;
    }


}
