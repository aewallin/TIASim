# TIASim
TIASim - Transimpedance Amplifier Simulation.

For some example designs and comparisons to TIASim see [One Inch Phototdetector](https://github.com/aewallin/One-Inch-Photodetector).

## References

* Hobbs, [Photodiode front ends](https://electrooptical.net/static/oldsite/www/frontends/frontends.pdf)
* Transimpedance Amplifiers (TIA): Choosing the Best Amplifier for the Job, http://www.ti.com.cn/cn/lit/an/snoa942a/snoa942a.pdf
* Transimpedance Considerations for High-Speed Amplifiers http://www.ti.com/lit/an/sboa122/sboa122.pdf
  - RF lower than 2 kOhm -> use BJT opamp
  - RF higher than 2 kOhm -> use FET opamp

## op-amps

Open-loop gain, input-referred voltage and current noise, and input-capacitance are modeled for the following op-amps:

| Op-amp        | Input           | Bandwidth |
| ------------- | -------------   | --------- |
| OPA657        | FET             |  1.6 GHz  |
| OPA859        | FET             |  1.8 GHz  |
| OPA847        | BJT             |  3.9 GHz  |
| OPA858        | FET             |  5.5 GHz  |
| OPA855        | BJT             |  8 GHz    |

### OPA657
http://www.ti.com/lit/ds/symlink/opa657.pdf

![opa657-image](doc/opa657.png)

### OPA847
http://www.ti.com/lit/ds/symlink/opa847.pdf
![opa847-image](doc/opa847.png)

### OPA855
http://www.ti.com/lit/ds/symlink/opa855.pdf

