package com.mams.controller;

import com.mams.dto.DashboardFilterDto;
import com.mams.dto.DashboardStatsDto;
import com.mams.service.DashboardService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/dashboard")
public class DashboardController {

    @Autowired private DashboardService dashboardService;

    @GetMapping
    public DashboardStatsDto getDashboardStats(
            @RequestParam(required = false) String fromDate,
            @RequestParam(required = false) String toDate,
            @RequestParam(required = false) Long baseId,
            @RequestParam(required = false) Long equipmentTypeId) {
        
        DashboardFilterDto filter = new DashboardFilterDto();
        filter.setFromDate(fromDate);
        filter.setToDate(toDate);
        filter.setBaseId(baseId);
        filter.setEquipmentTypeId(equipmentTypeId);
        
        return dashboardService.getDashboardStats(filter);
    }
}
