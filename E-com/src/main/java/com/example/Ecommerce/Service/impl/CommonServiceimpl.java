package com.example.Ecommerce.Service.impl;

import com.example.Ecommerce.Service.CommonService;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpSession;
import org.springframework.stereotype.Service;
import org.springframework.web.context.request.RequestContextHolder;
import org.springframework.web.context.request.ServletRequestAttributes;

@Service("commonServiceImpl")
public class CommonServiceimpl implements CommonService {
//changed i = i in impl
    @Override
    public void removeSessionMessage() {
      HttpServletRequest request = ((ServletRequestAttributes) ( RequestContextHolder.getRequestAttributes())).getRequest();
       HttpSession session= request.getSession();

session.removeAttribute("succMsg");
session.removeAttribute("errorMsg");
    }
}
