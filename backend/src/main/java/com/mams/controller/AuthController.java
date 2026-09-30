package com.mams.controller;

import com.mams.dto.JwtAuthResponse;
import com.mams.dto.LoginRequest;
import com.mams.dto.UserInfoDto;
import com.mams.entity.User;
import com.mams.repository.UserRepository;
import com.mams.security.JwtTokenProvider;
import com.mams.security.UserPrincipal;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/auth")
public class AuthController {

    @Autowired
    private AuthenticationManager authenticationManager;

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private JwtTokenProvider tokenProvider;

    @PostMapping("/login")
    public ResponseEntity<?> authenticateUser(@Valid @RequestBody LoginRequest loginRequest) {

        Authentication authentication = authenticationManager.authenticate(
                new UsernamePasswordAuthenticationToken(
                        loginRequest.getUsername(),
                        loginRequest.getPassword()
                )
        );

        SecurityContextHolder.getContext().setAuthentication(authentication);

        String jwt = tokenProvider.generateToken(authentication);
        UserPrincipal userPrincipal = (UserPrincipal) authentication.getPrincipal();
        
        User user = userRepository.findById(userPrincipal.getId()).get();
        
        UserInfoDto userInfo = new UserInfoDto(
            user.getId(),
            user.getUsername(),
            user.getFullName(),
            user.getRole(),
            user.getBase() != null ? user.getBase().getId() : null
        );

        return ResponseEntity.ok(new JwtAuthResponse(jwt, userInfo));
    }
}
