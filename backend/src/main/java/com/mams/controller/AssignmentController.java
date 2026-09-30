package com.mams.controller;

import com.mams.dto.AssignmentRequestDto;
import com.mams.entity.Assignment;
import com.mams.service.AssignmentService;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/assignments")
public class AssignmentController {
    @Autowired private AssignmentService assignmentService;

    @GetMapping
    public List<Assignment> getAll(@RequestParam(required = false) Long baseId) {
        if (baseId != null) {
            return assignmentService.getAssignmentsByBase(baseId);
        }
        return assignmentService.getAllAssignments();
    }

    @PostMapping
    public Assignment create(@Valid @RequestBody AssignmentRequestDto dto) {
        return assignmentService.createAssignment(dto);
    }
}
