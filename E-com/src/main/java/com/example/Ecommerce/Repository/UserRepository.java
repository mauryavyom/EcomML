package com.example.Ecommerce.Repository;

import com.example.Ecommerce.Model.UserDtls;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface UserRepository extends JpaRepository<UserDtls,Integer> {

  public UserDtls findByEmail(String email);

  public List<UserDtls> findByRole(String role);

  public UserDtls findByResetToken(String token);

}
