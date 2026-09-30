import os

backend_src = "f:/Military_Manage/backend/src/main/java/com/mams"
ensure_dir = lambda path: os.makedirs(path, exist_ok=True)
ensure_dir(f"{backend_src}/service")

services = {
    "BaseService": """package com.mams.service;

import com.mams.audit.AuditAction;
import com.mams.audit.AuditService;
import com.mams.dto.BaseDto;
import com.mams.entity.Base;
import com.mams.exception.ResourceNotFoundException;
import com.mams.repository.BaseRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class BaseService {
    @Autowired private BaseRepository baseRepository;
    @Autowired private AuditService auditService;

    public List<Base> getAllBases() {
        return baseRepository.findAll();
    }

    public Base createBase(BaseDto dto) {
        Base base = new Base();
        base.setBaseCode(dto.getBaseCode());
        base.setBaseName(dto.getBaseName());
        base.setLocation(dto.getLocation());
        base.setActive(dto.isActive());
        
        Base saved = baseRepository.save(base);
        auditService.logAction(AuditAction.BASE_CREATED, "Base", saved.getId().toString(), "Created base: " + base.getBaseName());
        return saved;
    }

    public Base updateBase(Long id, BaseDto dto) {
        Base base = baseRepository.findById(id).orElseThrow(() -> new ResourceNotFoundException("Base not found"));
        base.setBaseCode(dto.getBaseCode());
        base.setBaseName(dto.getBaseName());
        base.setLocation(dto.getLocation());
        base.setActive(dto.isActive());
        
        Base saved = baseRepository.save(base);
        auditService.logAction(AuditAction.BASE_UPDATED, "Base", saved.getId().toString(), "Updated base: " + base.getBaseName());
        return saved;
    }
}
""",
    "EquipmentTypeService": """package com.mams.service;

import com.mams.audit.AuditAction;
import com.mams.audit.AuditService;
import com.mams.dto.EquipmentTypeDto;
import com.mams.entity.EquipmentType;
import com.mams.exception.ResourceNotFoundException;
import com.mams.repository.EquipmentTypeRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class EquipmentTypeService {
    @Autowired private EquipmentTypeRepository equipmentTypeRepository;
    @Autowired private AuditService auditService;

    public List<EquipmentType> getAllEquipmentTypes() {
        return equipmentTypeRepository.findAll();
    }

    public EquipmentType createEquipmentType(EquipmentTypeDto dto) {
        EquipmentType eq = new EquipmentType();
        eq.setEquipmentCode(dto.getEquipmentCode());
        eq.setEquipmentName(dto.getEquipmentName());
        eq.setCategory(dto.getCategory());
        eq.setDescription(dto.getDescription());
        eq.setUnit(dto.getUnit());
        eq.setActive(dto.isActive());
        
        EquipmentType saved = equipmentTypeRepository.save(eq);
        auditService.logAction(AuditAction.EQUIPMENT_CREATED, "EquipmentType", saved.getId().toString(), "Created equipment: " + eq.getEquipmentName());
        return saved;
    }

    public EquipmentType updateEquipmentType(Long id, EquipmentTypeDto dto) {
        EquipmentType eq = equipmentTypeRepository.findById(id).orElseThrow(() -> new ResourceNotFoundException("Equipment Type not found"));
        eq.setEquipmentCode(dto.getEquipmentCode());
        eq.setEquipmentName(dto.getEquipmentName());
        eq.setCategory(dto.getCategory());
        eq.setDescription(dto.getDescription());
        eq.setUnit(dto.getUnit());
        eq.setActive(dto.isActive());
        
        EquipmentType saved = equipmentTypeRepository.save(eq);
        auditService.logAction(AuditAction.EQUIPMENT_UPDATED, "EquipmentType", saved.getId().toString(), "Updated equipment: " + eq.getEquipmentName());
        return saved;
    }
}
""",
    "UserService": """package com.mams.service;

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
"""
}

for name, content in services.items():
    with open(f"{backend_src}/service/{name}.java", "w") as f:
        f.write(content)

print("CRUD services generated.")
