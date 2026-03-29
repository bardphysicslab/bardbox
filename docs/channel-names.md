# Channel Names

Bard Box uses standardized short channel names to identify sensor measurements. Channel names are used in serial output, driver code, API responses, and dashboards.

---

## Naming Convention

* Channel names are lowercase
* Use underscores to separate components
* No spaces
* Names should reflect the physical quantity and unit where appropriate

Examples:

* `temp_c`
* `rh_pct`
* `press_pa`
* `c03`

---

## Registered Channels

### Particle Count Channels (GT-521S and compatible)

| Channel | Particle size | Unit      | Notes |
| ------- | ------------- | --------- | ----- |
| `c03`   | ≥ 0.3 µm      | count/ft³ |       |
| `c05`   | ≥ 0.5 µm      | count/ft³ |       |
| `c10`   | ≥ 1.0 µm      | count/ft³ |       |
| `c25`   | ≥ 2.5 µm      | count/ft³ |       |
| `c50`   | ≥ 5.0 µm      | count/ft³ |       |
| `c100`  | ≥ 10.0 µm     | count/ft³ |       |

---

### Environmental Channels (BME280 and compatible)

| Channel    | Description         | Unit | Source |
| ---------- | ------------------- | ---- | ------ |
| `temp_c`   | Air temperature     | °C   | BME280 |
| `rh_pct`   | Relative humidity   | %    | BME280 |
| `press_pa` | Barometric pressure | Pa   | BME280 |

---

## Adding a New Channel

1. Choose a short, descriptive name that does not conflict with existing channels
2. Use lowercase with underscores, no spaces
3. Ensure the unit is clearly defined and consistent with the naming
4. Add the channel to the appropriate table above
5. Update:

   * the relevant driver `README.md`
   * the device `README.md`
   * any affected dashboards or APIs

---

## Notes

* Channel names are part of the Bard Box protocol and should remain stable once introduced
* Do not rename existing channels without a migration plan
* Do not invent alternate names if a standard channel already exists (e.g. use `c03`, not `pm03_cf`)
