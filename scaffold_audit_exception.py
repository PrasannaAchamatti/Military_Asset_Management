import os

backend_src = "f:/Military_Manage/backend/src/main/java/com/mams"

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

ensure_dir(f"{backend_src}/audit")
ensure_dir(f"{backend_src}/exception")

audit_action = """package com.mams.audit;

public enum AuditAction {
    PURCHASE_CREATED,
    TRANSFER_CREATED,
    TRANSFER_APPROVED,
    TRANSFER_COMPLETED,
    TRANSFER_CANCELLED,
    ASSIGNMENT_CREATED,
    EXPENDITURE_CREATED,
    USER_CREATED,
    USER_UPDATED,
    INVENTORY_UPDATED,
    BASE_CREATED,
    BASE_UPDATED,
    EQUIPMENT_CREATED,
    EQUIPMENT_UPDATED
}
"""

audit_service = """package com.mams.audit;

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
"""

global_exception = """package com.mams.exception;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.context.request.WebRequest;

import java.time.LocalDateTime;
import java.util.LinkedHashMap;
import java.util.Map;

@ControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(IllegalArgumentException.class)
    public ResponseEntity<Object> handleIllegalArgumentException(IllegalArgumentException ex, WebRequest request) {
        return buildErrorResponse(HttpStatus.BAD_REQUEST, "Validation Error", ex.getMessage());
    }

    @ExceptionHandler(ResourceNotFoundException.class)
    public ResponseEntity<Object> handleResourceNotFoundException(ResourceNotFoundException ex, WebRequest request) {
        return buildErrorResponse(HttpStatus.NOT_FOUND, "Not Found", ex.getMessage());
    }

    @ExceptionHandler(AccessDeniedException.class)
    public ResponseEntity<Object> handleAccessDeniedException(AccessDeniedException ex, WebRequest request) {
        return buildErrorResponse(HttpStatus.FORBIDDEN, "Forbidden", ex.getMessage());
    }

    @ExceptionHandler(Exception.class)
    public ResponseEntity<Object> handleGlobalException(Exception ex, WebRequest request) {
        return buildErrorResponse(HttpStatus.INTERNAL_SERVER_ERROR, "Internal Server Error", ex.getMessage());
    }

    private ResponseEntity<Object> buildErrorResponse(HttpStatus status, String error, String message) {
        Map<String, Object> body = new LinkedHashMap<>();
        body.put("timestamp", LocalDateTime.now());
        body.put("status", status.value());
        body.put("error", error);
        body.put("message", message);
        return new ResponseEntity<>(body, status);
    }
}
"""

resource_not_found = """package com.mams.exception;

public class ResourceNotFoundException extends RuntimeException {
    public ResourceNotFoundException(String message) {
        super(message);
    }
}
"""

access_denied = """package com.mams.exception;

public class AccessDeniedException extends RuntimeException {
    public AccessDeniedException(String message) {
        super(message);
    }
}
"""

with open(f"{backend_src}/audit/AuditAction.java", "w") as f: f.write(audit_action)
with open(f"{backend_src}/audit/AuditService.java", "w") as f: f.write(audit_service)
with open(f"{backend_src}/exception/GlobalExceptionHandler.java", "w") as f: f.write(global_exception)
with open(f"{backend_src}/exception/ResourceNotFoundException.java", "w") as f: f.write(resource_not_found)
with open(f"{backend_src}/exception/AccessDeniedException.java", "w") as f: f.write(access_denied)

print("Audit and Exception components generated.")
