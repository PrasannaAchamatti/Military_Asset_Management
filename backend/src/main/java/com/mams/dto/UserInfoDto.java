package com.mams.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import com.mams.entity.Role;

@Data
@AllArgsConstructor
public class UserInfoDto {
    private Long id;
    private String username;
    private String fullName;
    private Role role;
    private Long baseId;
}
