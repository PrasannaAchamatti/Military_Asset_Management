package com.mams.dto;
import lombok.Data;
@Data
public class DashboardStatsDto {
    private long openingBalance;
    private long purchases;
    private long transferIn;
    private long transferOut;
    private long assigned;
    private long expended;
    private long netMovement;
    private long closingBalance;
}