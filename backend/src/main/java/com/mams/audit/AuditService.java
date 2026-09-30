package com.mams.audit;

import com.mams.entity.AuditLog;
import com.mams.repository.AuditLogRepository;
import com.mams.security.UserPrincipal;
import jakarta.servlet.http.HttpServletRequest;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Service;
import org.springframework.web.context.request.RequestContextHolder;
import org.springframework.web.context.request.ServletRequestAttributes;

@Service
public class AuditService {

    @Autowired
    private AuditLogRepository auditLogRepository;

    public void logAction(AuditAction action, String entityType, String entityId, String description) {
        AuditLog log = new AuditLog();
        log.setAction(action.name());
        log.setEntityType(entityType);
        log.setEntityId(entityId);
        log.setDescription(description);

        Authentication auth = SecurityContextHolder.getContext().getAuthentication();
        if (auth != null && auth.getPrincipal() instanceof UserPrincipal) {
            UserPrincipal user = (UserPrincipal) auth.getPrincipal();
            log.setUserId(user.getId());
            log.setUsername(user.getUsername());
            log.setRole(user.getAuthorities().iterator().next().getAuthority());
        }

        try {
            HttpServletRequest request = ((ServletRequestAttributes) RequestContextHolder.currentRequestAttributes()).getRequest();
            log.setIpAddress(request.getRemoteAddr());
        } catch (Exception e) {
            log.setIpAddress("Unknown");
        }

        auditLogRepository.save(log);
    }
}
