# Components by category

| Category | Description |
|---|---|
| `mcu`, `soc` | Microcontrollers and systems-on-chip |
| `fpga`, `cpld` | Programmable logic |
| `gnss`, `ins`, `imu` | Navigation |
| `rf`, `datalink`, `transceiver`, `antenna` | Radio links |
| `memory` | Flash, DRAM, EEPROM |
| `power`, `regulator` | Power conversion |
| `optics`, `camera`, `ir_sensor` | EO/IR |
| `propulsion`, `engine`, `motor`, `esc` | Propulsion |
| `mechanical`, `connector`, `passive` | Long tail |

Drill down via `data/components.csv`:

```python
import pandas as pd
df = pd.read_csv('data/components.csv')
df[df['category']=='mcu']['manufacturer'].value_counts().head(20)
```
