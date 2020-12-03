package com.bangmaple.repository;

import com.bangmaple.entities.ThermalData;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface ThermalDataRepository extends JpaRepository<ThermalData, String> {

}
