package com.mams.service;

import com.mams.dto.DashboardFilterDto;
import com.mams.dto.DashboardStatsDto;
import com.mams.entity.*;
import com.mams.repository.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.stream.Collectors;

@Service
public class DashboardService {
    @Autowired private PurchaseRepository purchaseRepository;
    @Autowired private TransferRepository transferRepository;
    @Autowired private AssignmentRepository assignmentRepository;
    @Autowired private ExpenditureRepository expenditureRepository;
    @Autowired private InventoryService inventoryService;

    public DashboardStatsDto getDashboardStats(DashboardFilterDto filter) {
        if (filter.getBaseId() != null) {
            inventoryService.validateBaseAccess(filter.getBaseId());
        }

        List<Purchase> purchases = purchaseRepository.findAll();
        List<Transfer> transfers = transferRepository.findAll();
        List<Assignment> assignments = assignmentRepository.findAll();
        List<Expenditure> expenditures = expenditureRepository.findAll();

        if (filter.getBaseId() != null) {
            purchases = purchases.stream().filter(p -> p.getBase().getId().equals(filter.getBaseId())).collect(Collectors.toList());
            assignments = assignments.stream().filter(a -> a.getBase().getId().equals(filter.getBaseId())).collect(Collectors.toList());
            expenditures = expenditures.stream().filter(e -> e.getBase().getId().equals(filter.getBaseId())).collect(Collectors.toList());
            
            // Transfer logic: in vs out
        }
        
        long totalPurchases = purchases.stream().mapToLong(Purchase::getQuantity).sum();
        long totalAssigned = assignments.stream().mapToLong(Assignment::getQuantity).sum();
        long totalExpended = expenditures.stream().mapToLong(Expenditure::getQuantity).sum();
        
        long transferIn = 0;
        long transferOut = 0;
        if (filter.getBaseId() != null) {
            transferIn = transfers.stream()
                .filter(t -> t.getToBase().getId().equals(filter.getBaseId()) && t.getStatus() == TransferStatus.COMPLETED)
                .mapToLong(Transfer::getQuantity).sum();
            transferOut = transfers.stream()
                .filter(t -> t.getFromBase().getId().equals(filter.getBaseId()) && t.getStatus() == TransferStatus.COMPLETED)
                .mapToLong(Transfer::getQuantity).sum();
        } else {
            transferIn = transfers.stream().filter(t -> t.getStatus() == TransferStatus.COMPLETED).mapToLong(Transfer::getQuantity).sum();
            transferOut = transferIn; // For global, they cancel out
        }

        long netMovement = totalPurchases + transferIn - transferOut;
        
        long openingBalance = 0; // Calculated dynamically in a real app based on date range
        long closingBalance = openingBalance + netMovement - totalAssigned - totalExpended;

        DashboardStatsDto stats = new DashboardStatsDto();
        stats.setOpeningBalance(openingBalance);
        stats.setPurchases(totalPurchases);
        stats.setTransferIn(transferIn);
        stats.setTransferOut(transferOut);
        stats.setAssigned(totalAssigned);
        stats.setExpended(totalExpended);
        stats.setNetMovement(netMovement);
        stats.setClosingBalance(closingBalance);

        return stats;
    }
}
