package com.example.Ecommerce.config;

import com.example.Ecommerce.Model.UserDtls;
import com.example.Ecommerce.Repository.UserRepository;
import com.example.Ecommerce.Service.UserService;
import com.example.Ecommerce.util.AppConstant;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Lazy;
import org.springframework.security.authentication.LockedException;
import org.springframework.security.core.AuthenticationException;
import org.springframework.security.web.authentication.SimpleUrlAuthenticationFailureHandler;
import org.springframework.stereotype.Component;

import java.io.IOException;

@Component
public class AuthFailureHandlerImpl extends SimpleUrlAuthenticationFailureHandler {

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private UserService userService;

    @Override
    public void onAuthenticationFailure(HttpServletRequest request, HttpServletResponse response, AuthenticationException exception) throws IOException, ServletException {

        String email =request.getParameter("username");

        UserDtls userDtls =userRepository.findByEmail(email);

        if(userDtls!=null) {
            if (userDtls.getIsEnable()) {
                if (userDtls.getAccountNonLocked()) {

                    if (userDtls.getFailedAttempt() < AppConstant.ATTEMPT_TIME) {
                        userService.increaseFailedAttempt(userDtls);
                    } else {
                        userService.userAccountLock(userDtls);
                        exception = new LockedException("Your Account is Locked !! failed attempt 3");
                    }

                } else {
                    if (userService.unlockAccountTimeExpired(userDtls)) {
                        exception = new LockedException("Your Account is unlocked !! Please Try to Login");
                    } else {
                        exception = new LockedException("Your Account is Locked !! Please try after some time");
                    }
                }

            } else {
                exception = new LockedException("Your Account is inactive");
            }
        }else{
            exception = new LockedException("Email or Password is invalid");
        }

        super.setDefaultFailureUrl("/signin?error");
        super.onAuthenticationFailure(request, response, exception);
    }
}
