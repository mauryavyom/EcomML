package com.example.Ecommerce.util;

public enum OrderStatus {

    IN_PROGRESS(1,"In Progress"),
    ORDER_RECEIVED(2,"is Received "),
    PRODUCT_PACKED(3,"is Packed "),
    OUT_FOR_DELIVERY(4,"is Out for Delivery"),
    DELIVERED(5,"Delivered"),
    CANCEL(6,"Cancelled"),
    SUCCESS(7,"is Booked Successfully");

private Integer id;
private String name;

    OrderStatus(Integer id, String name) {
        this.id = id;
        this.name = name;
    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }
}
