package com.bangmaple.entities;

import lombok.*;

import javax.persistence.*;
import java.io.Serializable;

@Entity
@Table(name = "ThermalData")
@Data
@NoArgsConstructor
@AllArgsConstructor
@RequiredArgsConstructor
public class ThermalData implements Serializable {

    private static final long serialVersionUID = 1L;

    @Id
    @Basic(optional = false)
    @NonNull
    @Column(name = "Temperature")
    private double temp;

    @Column(name = "CurrentTime")
    private Integer time;

    @Column(name = "Image")
    private byte time;

}
