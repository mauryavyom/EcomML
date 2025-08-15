package com.example.Ecommerce.Service.impl;

import com.example.Ecommerce.Model.Cart;
import com.example.Ecommerce.Model.OrderAddress;
import com.example.Ecommerce.Model.OrderRequest;
import com.example.Ecommerce.Model.ProductOrder;
import com.example.Ecommerce.Repository.CartRepository;
import com.example.Ecommerce.Repository.ProductOrderRepository;
import com.example.Ecommerce.Service.OrderService;
import com.example.Ecommerce.util.CommonUtil;
import com.example.Ecommerce.util.OrderStatus;
import jakarta.mail.MessagingException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.io.UnsupportedEncodingException;
import java.time.LocalDate;
import java.util.Date;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

@Service
public class OrderServiceImpl implements OrderService {

    @Override
    public ProductOrder updateOrderStatus(Integer id, String status) {
        Optional<ProductOrder> findById=orderRepository.findById(id);
        if(findById.isPresent()){

            ProductOrder productOrder=findById.get();
            productOrder.setStatus(status);
            ProductOrder updateOrder = orderRepository.save(productOrder);
            return updateOrder;
        }
        return null;
    }

    @Autowired
    private ProductOrderRepository orderRepository;

    @Autowired
    private CartRepository cartRepository;

    @Autowired
    private CommonUtil commonUtil;

    @Override
    public List<ProductOrder> getOrderByUser(Integer userId) {
      List<ProductOrder> orders=  orderRepository.findByUserId(userId);
        return orders;
    }

    @Override
    public void  saveOrder(Integer userId, OrderRequest orderRequest) throws MessagingException, UnsupportedEncodingException {
       List<Cart> carts= cartRepository.findByUserId(userId);

       for(Cart cart:carts){
ProductOrder order=new ProductOrder();
order.setOrderId(UUID.randomUUID().toString());
order.setOrderDate(LocalDate.now());
order.setProduct(cart.getProduct());
order.setPrice(cart.getProduct().getDiscountPrice());
order.setQuantity(cart.getQuantity());

order.setUser(cart.getUser());

order.setStatus(OrderStatus.IN_PROGRESS.getName());
order.setPaymentType(orderRequest.getPaymentType());

           OrderAddress address = new OrderAddress();
           address.setFirstName(orderRequest.getFirstName());
           address.setLastName(orderRequest.getLastName());
           address.setEmail(orderRequest.getEmail());
           address.setMobileNo(orderRequest.getMobileNo());
   address.setAddress(orderRequest.getAddress());
   address.setCity(orderRequest.getCity());
   address.setState(orderRequest.getState());
   address.setPincode(orderRequest.getPincode());

   order.setOrderAddress(address);

   ProductOrder  saveOrder = orderRepository.save(order);

commonUtil.sendMailForProductOrder(saveOrder,"is Booked Successfully");

       }
    }

    @Override
    public List<ProductOrder> getAllOrders() {
        return orderRepository.findAll();

    }
}
