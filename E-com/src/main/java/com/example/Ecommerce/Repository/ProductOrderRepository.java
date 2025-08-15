package com.example.Ecommerce.Repository;

import com.example.Ecommerce.Model.ProductOrder;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface ProductOrderRepository extends JpaRepository<ProductOrder,Integer> {
    List<ProductOrder> findByUserId(Integer userId);

}
