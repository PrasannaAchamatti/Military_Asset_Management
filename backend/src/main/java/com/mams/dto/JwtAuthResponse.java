package com.mams.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import com.mams.entity.Role;

@Data
@AllArgsConstructor
public class JwtAuthResponse {
    private String accessToken;
    private String tokenType = "Bearer";
    private UserInfoDto user;

    public JwtAuthResponse(String accessToken, UserInfoDto user) {
        this.accessToken = accessToken;
        this.user = user;
    }
}
