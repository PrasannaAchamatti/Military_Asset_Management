import os

backend_src = "f:/Military_Manage/backend/src/main/java/com/mams"
ensure_dir = lambda path: os.makedirs(path, exist_ok=True)
ensure_dir(f"{backend_src}/controller")

controllers = {
    "BaseController": """package com.mams.controller;

import com.mams.dto.BaseDto;
import com.mams.entity.Base;
import com.mams.service.BaseService;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/bases")
public class BaseController {
    @Autowired private BaseService baseService;

    @GetMapping
    public List<Base> getAllBases() {
        return baseService.getAllBases();
    }

    @PostMapping
    @PreAuthorize("hasRole('ADMIN')")
    public Base createBase(@Valid @RequestBody BaseDto dto) {
        return baseService.createBase(dto);
    }

    @PutMapping("/{id}")
    @PreAuthorize("hasRole('ADMIN')")
    public Base updateBase(@PathVariable Long id, @Valid @RequestBody BaseDto dto) {
        return baseService.updateBase(id, dto);
    }
}
""",
    "EquipmentTypeController": """package com.mams.controller;

import com.mams.dto.EquipmentTypeDto;
import com.mams.entity.EquipmentType;
import com.mams.service.EquipmentTypeService;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/equipment-types")
public class EquipmentTypeController {
    @Autowired private EquipmentTypeService equipmentTypeService;

    @GetMapping
    public List<EquipmentType> getAll() {
        return equipmentTypeService.getAllEquipmentTypes();
    }

    @PostMapping
    @PreAuthorize("hasRole('ADMIN')")
    public EquipmentType create(@Valid @RequestBody EquipmentTypeDto dto) {
        return equipmentTypeService.createEquipmentType(dto);
    }

    @PutMapping("/{id}")
    @PreAuthorize("hasRole('ADMIN')")
    public EquipmentType update(@PathVariable Long id, @Valid @RequestBody EquipmentTypeDto dto) {
        return equipmentTypeService.updateEquipmentType(id, dto);
    }
}
""",
    "InventoryController": """package com.mams.controller;

import com.mams.entity.Inventory;
import com.mams.repository.InventoryRepository;
import com.mams.service.InventoryService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/inventory")
public class InventoryController {
    @Autowired private InventoryRepository inventoryRepository;
    @Autowired private InventoryService inventoryService;

    @GetMapping
    public List<Inventory> getAll(@RequestParam(required = false) Long baseId) {
        if (baseId != null) {
            inventoryService.validateBaseAccess(baseId);
            return inventoryRepository.findByBaseId(baseId);
        }
        // If no baseId provided, and not admin, should fail. This is basic for now.
        return inventoryRepository.findAll();
    }
}
""",
    "PurchaseController": """package com.mams.controller;

import com.mams.dto.PurchaseRequestDto;
import com.mams.entity.Purchase;
import com.mams.service.PurchaseService;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/purchases")
public class PurchaseController {
    @Autowired private PurchaseService purchaseService;

    @GetMapping
    public List<Purchase> getAll(@RequestParam(required = false) Long baseId) {
        if (baseId != null) {
            return purchaseService.getPurchasesByBase(baseId);
        }
        return purchaseService.getAllPurchases();
    }

    @PostMapping
    public Purchase create(@Valid @RequestBody PurchaseRequestDto dto) {
        return purchaseService.createPurchase(dto);
    }
}
""",
    "TransferController": """package com.mams.controller;

import com.mams.dto.TransferRequestDto;
import com.mams.entity.Transfer;
import com.mams.service.TransferService;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/transfers")
public class TransferController {
    @Autowired private TransferService transferService;

    @GetMapping
    public List<Transfer> getAll(@RequestParam(required = false) Long baseId) {
        if (baseId != null) {
            return transferService.getTransfersByBase(baseId);
        }
        return transferService.getAllTransfers();
    }

    @PostMapping
    public Transfer create(@Valid @RequestBody TransferRequestDto dto) {
        return transferService.createTransfer(dto);
    }

    @PutMapping("/{id}/approve")
    public Transfer approve(@PathVariable Long id) {
        return transferService.approveTransfer(id);
    }

    @PutMapping("/{id}/complete")
    public Transfer complete(@PathVariable Long id) {
        return transferService.completeTransfer(id);
    }
}
""",
    "AssignmentController": """package com.mams.controller;

import com.mams.dto.AssignmentRequestDto;
import com.mams.entity.Assignment;
import com.mams.service.AssignmentService;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/assignments")
public class AssignmentController {
    @Autowired private AssignmentService assignmentService;

    @GetMapping
    public List<Assignment> getAll(@RequestParam(required = false) Long baseId) {
        if (baseId != null) {
            return assignmentService.getAssignmentsByBase(baseId);
        }
        return assignmentService.getAllAssignments();
    }

    @PostMapping
    public Assignment create(@Valid @RequestBody AssignmentRequestDto dto) {
        return assignmentService.createAssignment(dto);
    }
}
""",
    "ExpenditureController": """package com.mams.controller;

import com.mams.dto.ExpenditureRequestDto;
import com.mams.entity.Expenditure;
import com.mams.service.ExpenditureService;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/expenditures")
public class ExpenditureController {
    @Autowired private ExpenditureService expenditureService;

    @GetMapping
    public List<Expenditure> getAll(@RequestParam(required = false) Long baseId) {
        if (baseId != null) {
            return expenditureService.getExpendituresByBase(baseId);
        }
        return expenditureService.getAllExpenditures();
    }

    @PostMapping
    public Expenditure create(@Valid @RequestBody ExpenditureRequestDto dto) {
        return expenditureService.createExpenditure(dto);
    }
}
""",
    "AuditLogController": """package com.mams.controller;

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
"""
}

for name, content in controllers.items():
    with open(f"{backend_src}/controller/{name}.java", "w") as f:
        f.write(content)

print("Controllers generated.")
