package com.mams.controller;

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
