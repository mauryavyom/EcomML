package com.example.Ecommerce.Service;

import com.example.Ecommerce.Model.OrderRequest;
import com.example.Ecommerce.Model.Product;
import com.example.Ecommerce.Model.ProductOrder;
import jakarta.mail.MessagingException;
import org.springframework.stereotype.Service;

import java.io.UnsupportedEncodingException;
import java.util.List;

@Service
public interface OrderService {
    public void saveOrder(Integer userId, OrderRequest orderRequest) throws MessagingException, UnsupportedEncodingException;
    public List<ProductOrder> getOrderByUser(Integer userId);

    public ProductOrder updateOrderStatus(Integer id,String status);
    public List<ProductOrder> getAllOrders();

}
