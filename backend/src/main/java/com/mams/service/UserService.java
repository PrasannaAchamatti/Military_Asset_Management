package com.mams.service;

import com.mams.audit.AuditAction;
import com.mams.audit.AuditService;
import com.mams.dto.UserInfoDto;
import com.mams.entity.User;
import com.mams.exception.ResourceNotFoundException;
import com.mams.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.stream.Collectors;

@Service
public class UserService {
    @Autowired private UserRepository userRepository;
    @Autowired private PasswordEncoder passwordEncoder;
    @Autowired private AuditService auditService;

    public List<UserInfoDto> getAllUsers() {
        return userRepository.findAll().stream()
                .map(u -> new UserInfoDto(u.getId(), u.getUsername(), u.getFullName(), u.getRole(), u.getBase() != null ? u.getBase().getId() : null))
                .collect(Collectors.toList());
    }

    // In a real scenario you would have CreateUserDto and UpdateUserDto. 
    // This is just a scaffold for the API logic.
}
