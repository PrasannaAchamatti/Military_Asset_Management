package com.mams.controller;

import com.mams.entity.User;
import com.mams.entity.Role;
import com.mams.entity.Base;
import com.mams.repository.UserRepository;
import com.mams.repository.BaseRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.web.bind.annotation.*;
import org.springframework.http.ResponseEntity;
import org.springframework.http.HttpStatus;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/users")
@PreAuthorize("hasRole('ADMIN')")
public class UserController {
    
    @Autowired
    private UserRepository userRepository;
    
    @Autowired
    private BaseRepository baseRepository;
    
    @Autowired
    private PasswordEncoder passwordEncoder;

    @GetMapping
    public List<User> getAllUsers() {
        return userRepository.findAll();
    }

    @PostMapping
    public ResponseEntity<?> createUser(@RequestBody Map<String, String> payload) {
        try {
            User user = new User();
            user.setFullName(payload.get("fullName"));
            user.setUsername(payload.get("username"));
            user.setEmail(payload.get("email"));
            user.setPasswordHash(passwordEncoder.encode(payload.get("password")));
            user.setRole(Role.valueOf(payload.get("role")));
            
            if (payload.get("baseId") != null && !payload.get("baseId").isEmpty()) {
                Base base = baseRepository.findById(Long.parseLong(payload.get("baseId"))).orElse(null);
                user.setBase(base);
            }
            
            user.setActive(true);
            User saved = userRepository.save(user);
            return ResponseEntity.ok(saved);
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(e.getMessage());
        }
    }
}
