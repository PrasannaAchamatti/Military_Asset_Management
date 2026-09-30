package com.mams.dto;
import jakarta.validation.constraints.NotBlank;
import lombok.Data;
@Data
public class BaseDto {
    private Long id;
    @NotBlank private String baseCode;
    @NotBlank private String baseName;
    private String location;
    private boolean active;
}