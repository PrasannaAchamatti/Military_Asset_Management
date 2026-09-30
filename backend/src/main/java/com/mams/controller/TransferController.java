package com.mams.controller;

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
