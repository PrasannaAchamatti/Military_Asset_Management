package com.mams.dto;

import lombok.Data;

@Data
public class DashboardFilterDto {
    private String fromDate;
    private String toDate;
    private Long baseId;
    private Long equipmentTypeId;
}
