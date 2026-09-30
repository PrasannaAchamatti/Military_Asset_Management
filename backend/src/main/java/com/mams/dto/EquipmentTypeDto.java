package com.mams.dto;
import jakarta.validation.constraints.NotBlank;
import lombok.Data;
@Data
public class EquipmentTypeDto {
    private Long id;
    @NotBlank private String equipmentCode;
    @NotBlank private String equipmentName;
    @NotBlank private String category;
    private String description;
    @NotBlank private String unit;
    private boolean active;
}