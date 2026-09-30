package com.mams.service;

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
