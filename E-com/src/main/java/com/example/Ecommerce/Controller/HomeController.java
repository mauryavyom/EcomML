package com.example.Ecommerce.Controller;

import com.example.Ecommerce.Model.Category;
import com.example.Ecommerce.Model.Product;
import com.example.Ecommerce.Model.UserDtls;
import com.example.Ecommerce.Repository.ProductRepository;
import com.example.Ecommerce.Service.CartService;
import com.example.Ecommerce.Service.CategoryService;
import com.example.Ecommerce.Service.ProductService;
import com.example.Ecommerce.Service.UserService;
import com.example.Ecommerce.util.CommonUtil;
import com.fasterxml.jackson.databind.DatabindContext;
import jakarta.mail.MessagingException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpSession;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.autoconfigure.security.SecurityProperties;
import org.springframework.core.io.ClassPathResource;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.util.ObjectUtils;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.File;
import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.security.Principal;
import java.util.List;
import java.util.UUID;

@Controller
public class HomeController {


    @Autowired
    private CategoryService categoryService;

   @Autowired
    private ProductService productService;

    @Autowired
    private UserService userService;

    @Autowired
    private CommonUtil commonUtil;

    @Autowired
    private BCryptPasswordEncoder passwordEncoder;

    @Autowired
    private CartService cartService;

    @ModelAttribute
    public void getUserDetails(Principal p, Model m )
    {
        if(p!=null){
            String email = p.getName();
            UserDtls userDtls = userService.getUserByEmail(email);
            m.addAttribute("user", userDtls);
            Integer countCart=cartService.getCountCart(userDtls.getId());
            m.addAttribute("countCart",countCart);
        }


        List<Category> allActiveCategory = categoryService.getAllActiveCategory();
        m.addAttribute("categorys",allActiveCategory);
    }
    @GetMapping("/")
    public String index() {

        return "index";
    }
    @GetMapping("/signin")
    public String login() {
        return "login";
    }

    @GetMapping("/register")
    public String register() {

        return "register";
    }


    @GetMapping("/product/{id}")
    public String view_product(@PathVariable int id, Model m){
        Product productById = productService.getProductById(id);
        m.addAttribute("product", productById);
        return "view_product";
    }

    @GetMapping("/products")
    public String products(Model m,@RequestParam(value = "category", defaultValue = "")String category){
        //System.out.println("category ="+category );
   List<Category> categories = categoryService.getAllActiveCategory();
 List<Product> products = productService.getAllActiveProducts(category);
  m.addAttribute("categories",categories);
        m.addAttribute("products",products);
        m.addAttribute("paramValue",category);
        return "product";
    }
    @PostMapping("/saveUser")
    public String saveUser(@ModelAttribute UserDtls user, @RequestParam("img") MultipartFile file, HttpSession session) throws IOException
    {
        String imageName=file.isEmpty() ? "default.jpg": file.getOriginalFilename();
        user.setProfileImage(imageName);
        UserDtls saveUser=userService.saveUser(user);
        if(!ObjectUtils.isEmpty(saveUser))
        {
             if(!file.isEmpty())
             {
                 File saveFile = new ClassPathResource("static/img").getFile();
                 Path path = Paths.get(saveFile.getAbsolutePath()+File.separator+"profile_img"+File.separator+file.getOriginalFilename());

                // System.out.println(path);
                 Files.copy(file.getInputStream(),path, StandardCopyOption.REPLACE_EXISTING);
             }
            session.setAttribute("succMsg","Saved Successfully");
        }
        else{
            session.setAttribute("errorMsg","Something wrong on server");
        }
        return "redirect:/register";

    }
    // Forget Password Code 19th video
    @GetMapping("/forgot-password")
    public String showForgotPassword(){
        return "forgot_password";
    }

    @PostMapping("/forgot-password")
    public String processForgotPassword(@RequestParam String email, HttpSession session, HttpServletRequest request)
    throws UnsupportedEncodingException, MessagingException {
        UserDtls userByEmail = userService.getUserByEmail(email);

        if(ObjectUtils.isEmpty(userByEmail)){
            session.setAttribute("errorMsg","Invalid email");
        }else{

            String resetToken = UUID.randomUUID().toString();
            userService.updateUserResetToken(email,resetToken);
            //Generate url :

            String url = CommonUtil.generateUrl(request)+"/reset-password?token="+resetToken;

            Boolean sendMail = commonUtil.sendMail(url, email);

            if(sendMail){
                session.setAttribute("succMsg","Please check your email...Password Reset");
            }else{
                session.setAttribute("errorMsg","Something wrong on server ! Email not send");
            }
        }
        return "redirect:/forgot-password";
    }

    @GetMapping("/reset-password")
    public String showResetPassword(@RequestParam String token, HttpSession session,Model m){

        UserDtls userByToken = userService.getUserByToken(token);

        if(userByToken == null){
            m.addAttribute("msg", "Your link is invalid or expired");
            return "message";
        }
        m.addAttribute("token",token);
        return  "reset_password";
    }

    @PostMapping("/reset-password")
    public String resetPassword(@RequestParam String token, @RequestParam String password,HttpSession session,Model m){

        UserDtls userByToken = userService.getUserByToken(token);

        if(userByToken == null){
            m.addAttribute("errorMsg", "Your link is invalid or expired");
            return "message";
        }else{
            userByToken.setPassword(passwordEncoder.encode(password));
            userByToken.setResetToken(null);
            userService.updateUser(userByToken);
            session.setAttribute("succMsg", "Password changed successfully !");
            m.addAttribute("msg","Password changed successfully !");
            return  "message";
        }
    }
}
