package com.mams.controller;

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
