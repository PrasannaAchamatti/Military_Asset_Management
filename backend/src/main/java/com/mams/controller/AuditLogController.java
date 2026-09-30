package com.mams.controller;

import com.mams.entity.AuditLog;
import com.mams.repository.AuditLogRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/audit-logs")
public class AuditLogController {
    @Autowired private AuditLogRepository auditLogRepository;

    @GetMapping
    @PreAuthorize("hasRole('ADMIN')")
    public List<AuditLog> getAll() {
        return auditLogRepository.findAll();
    }
}
