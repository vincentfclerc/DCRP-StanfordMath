import csv
import random
#######################################################
# 1) LENGTH_CONVERSIONS
#    Handling nm, m, km, mi, ft, etc.
#######################################################
LENGTH_CONVERSIONS = {
    # SI <-> SI
    ("nm", "m"): 1.0e-9,          # 1 nm = 1e-9 m
    ("m", "nm"): 1.0e9,
    ("m", "cm"): 100.0,
    ("cm", "m"): 0.01,
    ("m", "mm"): 1000.0,
    ("mm", "m"): 0.001,
    ("m", "km"): 0.001,
    ("km", "m"): 1000.0,

    # SI -> Non-SI
    ("m", "in"): 39.3700787,    # 1 m ~ 39.37 in
    ("in", "m"): 1.0/39.3700787,
    ("m", "ft"): 3.2808399,     # 1 m ~ 3.2808 ft
    ("ft", "m"): 1.0/3.2808399,
    ("m", "yd"): 1.0936133,
    ("yd", "m"): 1.0/1.0936133,
    ("m", "mi"): 0.0006213712,  # 1 m ~ 6.21e-4 mi
    ("mi", "m"): 1.0/0.0006213712,

    # Non-SI <-> Non-SI
    ("in", "ft"): 1.0/12.0,
    ("ft", "in"): 12.0,
    ("ft", "yd"): 1.0/3.0,
    ("yd", "ft"): 3.0,
    ("mi", "ft"): 5280.0,
    ("ft", "mi"): 1.0/5280.0,

    # More exotic or 'nonsensical'
    ("mm", "ly"): 1.057000834e-19,  # 1 mm ~ 1.057e-19 ly
    ("ly", "mm"): 1.0/1.057000834e-19,
    ("km", "AU"): 6.68458712e-9,    # 1 km ~ 6.6846e-9 AU
    ("AU", "km"): 1.0/6.68458712e-9,
    ("parsec", "ly"): 3.26156,
    ("ly", "parsec"): 1.0/3.26156,
}

#######################################################
# 2) TIME_CONVERSIONS
#    Handling s, ms, min, hr, day, etc.
#######################################################
TIME_CONVERSIONS = {
    # SI <-> SI
    ("s", "ms"): 1000.0,
    ("ms", "s"): 0.001,
    ("s", "μs"): 1.0e6,
    ("μs", "s"): 1.0e-6,
    ("s", "ns"): 1.0e9,
    ("ns", "s"): 1.0e-9,

    # Larger units
    ("s", "min"): 1.0/60.0,
    ("min", "s"): 60.0,
    ("min", "hr"): 1.0/60.0,
    ("hr", "min"): 60.0,
    ("hr", "day"): 1.0/24.0,
    ("day", "hr"): 24.0,
    ("s", "hr"): 1.0/3600.0,
    ("hr", "s"): 3600.0,
    ("s", "day"): 1.0/86400.0,
    ("day", "s"): 86400.0,

    # More unusual
    ("day", "yr"): 1.0/365.25,
    ("yr", "day"): 365.25,

    # Possibly nonsensical / fun
    ("min", "Myr"): 1.0/(60*24*365.25*1.0e6),   # million years
    ("Myr", "min"): 1.0 / (1.0/(60*24*365.25*1.0e6)),
}

#######################################################
# 3) MASS_CONVERSIONS
#    Handling kg, mg, lb, etc.
#######################################################
MASS_CONVERSIONS = {
    # SI <-> SI
    ("kg", "g"): 1000.0,
    ("g", "kg"): 0.001,
    ("kg", "mg"): 1.0e6,
    ("mg", "kg"): 1.0e-6,

    # Non-SI
    ("kg", "lb"): 2.2046226218,
    ("lb", "kg"): 1.0/2.2046226218,
    ("kg", "oz"): 35.27396195,
    ("oz", "kg"): 1.0/35.27396195,

    # Earth / solar masses
    ("kg", "earth_mass"): 1.0/5.97219e24,
    ("earth_mass", "kg"): 5.97219e24,
    ("kg", "solar_mass"): 1.0/1.98847e30,
    ("solar_mass", "kg"): 1.98847e30,
}

#######################################################
# 4) SPEED_CONVERSIONS
#    Handling m/s, mph, km/h, etc.
#######################################################
SPEED_CONVERSIONS = {
    # SI <-> SI
    ("m/s", "km/h"): 3.6,
    ("km/h", "m/s"): 1.0/3.6,

    # SI <-> Non-SI
    ("m/s", "mph"): 2.236936292,
    ("mph", "m/s"): 1.0/2.236936292,

    ("km/h", "mph"): 0.621371,
    ("mph", "km/h"): 1.0/0.621371,

    # Possibly exotic
    ("m/s", "c"): 1.0/299792458.0,   # fraction of speed of light
    ("c", "m/s"): 299792458.0,

    # e.g. knots
    ("m/s", "kn"): 1.94384449,  # 1 m/s = 1.94384449 knots approx
    ("kn", "m/s"): 1.0/1.94384449,
}

#######################################################
# 5) ENERGY_CONVERSIONS
#    Handling J, eV, TeV, etc.
#######################################################
ENERGY_CONVERSIONS = {
    # SI
    ("J", "kJ"): 0.001,
    ("kJ", "J"): 1000.0,

    # eV <-> J
    ("J", "eV"): 1.0/1.602176634e-19,  # 1 eV = 1.602176634e-19 J
    ("eV", "J"): 1.602176634e-19,

    # TeV <-> eV
    ("TeV", "eV"): 1.0e12,
    ("eV", "TeV"): 1.0e-12,

    # J <-> TeV
    ("J", "TeV"): (1.0/1.602176634e-19) * 1.0e-12,  # first J->eV, then eV->TeV
    ("TeV", "J"): 1.602176634e-19 * 1.0e12,
}

#######################################################
# 6) PRESSURE_CONVERSIONS
#    kPa, bar, atm, Pa, etc.
#######################################################
PRESSURE_CONVERSIONS = {
    ("Pa", "kPa"): 1.0/1000.0,
    ("kPa", "Pa"): 1000.0,

    ("Pa", "bar"): 1.0e-5,
    ("bar", "Pa"): 1.0e5,

    ("Pa", "atm"): 1.0/101325.0,
    ("atm", "Pa"): 101325.0,

    ("kPa", "bar"): 0.01,
    ("bar", "kPa"): 100.0,
    ("kPa", "atm"): 1.0/101.325,
    ("atm", "kPa"): 101.325,

    ("bar", "atm"): 1.0/1.01325,
    ("atm", "bar"): 1.01325,
}

#######################################################
# 7) DATA_CONVERSIONS
#    Handling GB, MB, etc.
#######################################################
DATA_CONVERSIONS = {
    ("GB", "MB"): 1024.0,
    ("MB", "GB"): 1.0/1024.0,

    # If you want decimal-based:
    ("GB_dec", "MB_dec"): 1000.0,   # e.g. 1 GB (decimal) = 1000 MB
    ("MB_dec", "GB_dec"): 0.001,
}

#######################################################
# 8) DIMENSIONAL_EQUIVALENCES (Optional)
#    Symbolic dimension relationships
#######################################################
DIMENSIONAL_EQUIVALENCES = {
    "F": "kg^-1 * m^-2 * s^4 * A^2",     # Farad dimension
    "N": "kg * m * s^-2",               # Newton
    "Pa": "kg * m^-1 * s^-2",           # Pascal
    "J": "kg * m^2 * s^-2",             # Joule
    "W": "kg * m^2 * s^-3",             # Watt
    "C": "s * A",                       # Coulomb
    "V": "kg * m^2 * s^-3 * A^-1",      # Volt
    "Ω": "kg * m^2 * s^-3 * A^-2",      # Ohm
}


ALL_CONVERSIONS = [
    LENGTH_CONVERSIONS,
    TIME_CONVERSIONS,
    MASS_CONVERSIONS,
    SPEED_CONVERSIONS,
    ...
]
# Example possible randomization ranges for known variables
# key: variable name, value: (min, max)
RANDOM_RANGES = {
    # velocity or speed
    "v0": (0.1, 100.0),      # from 0.1 to 100 (m/s or etc.)

    # acceleration
    "a": (0.1, 50.0),        # e.g. 0.1 to 50 m/s^2

    # time
    "t": (0.01, 3600.0),     # from 0.01 s up to 3600 s (1 hour)
    "dt": (0.001, 100.0),

    # distance or displacement
    "x": (0.001, 1e6),       # 1 mm up to 1e6 m = 1000 km
    "r": (0.001, 1e7),       # radius range, etc.

    # angles
    "theta": (0.0, 360.0),   # degrees if needed

    # mass
    "m": (0.001, 1e5),       # from 1 g to 1e5 kg
    "M": (1.0, 1e30),        # e.g. for star mass, 1 kg to 1e30 kg

    # energy
    "E": (1e-3, 1e9),        # e.g. from 1 mJ to 1 GJ

    # force
    "F": (0.1, 1e7),         # 0.1 N to 1e7 N, etc.

    # power
    "P": (0.1, 1e9),

    # temperature (Kelvin)
    "T": (1.0, 1e5),         # 1 K up to 1e5 K

    # current
    "I": (1e-3, 1e3),        # 1 mA to 1 kA

    # etc...
}

def randomize_variable(var_name, original_value):
    """
    Given a variable name and its original numeric value,
    pick a new value within a certain range.
    If no known range, return original.
    """
    if var_name in RANDOM_RANGES:
        vmin, vmax = RANDOM_RANGES[var_name]
        return random.uniform(vmin, vmax)
    # If we don't have a known range, just perturb it a little
    return original_value * (1.0 + random.uniform(-0.2, 0.2))

def try_unit_conversion(old_unit, new_unit, value):
    """
    If we have a known conversion factor from old_unit to new_unit,
    return the new_value and new_unit.
    Otherwise, return (value, old_unit).
    """
    # e.g. if (old_unit, new_unit) = ('m', 'cm'), factor = 100
    # new_value = value * factor
    pair = (old_unit, new_unit)
    if pair in LENGTH_CONVERSIONS:
        factor = LENGTH_CONVERSIONS[pair]
        return value * factor, new_unit
    if pair in TIME_CONVERSIONS:
        factor = TIME_CONVERSIONS[pair]
        return value * factor, new_unit
    # No known conversion
    return value, old_unit


def pick_random_unit(old_unit):
    if random.random() < 0.5:
        return old_unit
    candidates = []
    for conv_dict in ALL_CONVERSIONS:
        for (u1, u2) in conv_dict.keys():
            if u1 == old_unit:
                candidates.append(u2)
    if not candidates:
        return old_unit
    return random.choice(candidates)

def generate_random_variation(row):
    """
    row is a dictionary with fields like:
      {
        "Level US": ...,
        "Level FR": ...,
        "Question": ...,
        "Variables": "v0=10 m/s, a=2 m/s^2, t=5 s",
        "Variables (no units)": "v0:10, a:2, t:5",
        "Formula": "v0 * t + 0.5 * a * (t**2)",
        ...
      }
    We'll parse the "Variables (no units)" to get numeric values, randomize them,
    also parse the original units from "Variables", do possible unit conversions,
    then build a new row.
    """
    # 1) Parse "Variables (no units)" into a dict
    # e.g. "v0:10, a:2, t:5" => {"v0":10.0, "a":2.0, "t":5.0}
    var_no_units_str = row.get("Variables (no units)", "")
    var_pairs = [p.strip() for p in var_no_units_str.split(",") if p.strip()]
    numeric_dict = {}
    for pair in var_pairs:
        if ":" not in pair:
            continue
        key, val_str = pair.split(":", 1)
        key = key.strip()
        try:
            val_float = float(val_str.strip())
        except ValueError:
            val_float = None
        if val_float is not None:
            numeric_dict[key] = val_float

    # 2) Also parse "Variables" to get original units
    # e.g. "v0=10 m/s, a=2 m/s^2, t=5 s"
    # We'll assume each chunk is "v0=10 m/s" or "a=2 m/s^2" etc.
    # We'll create a structure: {"v0":(10.0, "m/s"), "a":(2.0, "m/s^2"), "t":(5.0, "s")}
    var_str = row.get("Variables", "")
    unit_dict = {}
    # split by commas
    chunks = [c.strip() for c in var_str.split(",") if c.strip()]
    for chunk in chunks:
        # chunk ~ "v0=10 m/s"
        # we'll do a regex or just naive parsing
        # naive approach: split by '=' => "v0", "10 m/s"
        eq_split = chunk.split("=")
        if len(eq_split) < 2:
            continue
        varname = eq_split[0].strip()
        val_unit_str = eq_split[1].strip()  # e.g. "10 m/s"
        # separate numeric from unit
        # we'll split by space => "10", "m/s"
        parts = val_unit_str.split(None, 1)
        if len(parts) == 2:
            val_str, unit_str = parts
            try:
                val_float = float(val_str)
            except ValueError:
                val_float = None
            if val_float is not None:
                unit_dict[varname] = (val_float, unit_str)
        else:
            # maybe just "10" or something
            pass

    # 3) Randomize numeric_dict
    for k in numeric_dict:
        old_val = numeric_dict[k]
        new_val = randomize_variable(k, old_val)
        numeric_dict[k] = new_val

    # 4) Possibly pick a new unit and do a conversion
    # For each var in unit_dict, we see old_unit => new_unit => adjust numeric_dict
    for k in unit_dict:
        if k not in numeric_dict:
            continue
        old_val, old_unit = unit_dict[k]
        new_unit = pick_random_unit(old_unit)
        if new_unit != old_unit:
            # apply conversion
            new_val, final_unit = try_unit_conversion(old_unit, new_unit, numeric_dict[k])
            numeric_dict[k] = new_val
            # Update unit_dict as well
            unit_dict[k] = (new_val, final_unit)
        else:
            # keep unit but update the new random numeric value
            unit_dict[k] = (numeric_dict[k], old_unit)

    # 5) Build the new row
    new_row = dict(row)  # copy original
    # update the "Variables" with new numeric and unit
    # e.g. "v0=15.2 m/s, a=3.9 m/s^2, t=9 s"
    new_vars = []
    for varname, (val, unit) in unit_dict.items():
        new_vars.append(f"{varname}={val:.3g} {unit}")
    new_row["Variables"] = ", ".join(new_vars)
    # update the "Variables (no units)"
    # e.g. "v0:15.2, a:3.9, t:9"
    new_vars_no_units = []
    for varname in numeric_dict:
        new_vars_no_units.append(f"{varname}:{numeric_dict[varname]:.3g}")
    new_row["Variables (no units)"] = ", ".join(new_vars_no_units)

    # Optionally, you might want to re-compute the "Numeric answer" using a formula engine,
    # or leave it blank. For now, let's just blank it out or keep it.
    new_row["Numeric answer"] = ""

    return new_row

def main(input_csv_path, output_csv_path):
    # read all rows
    rows = []
    with open(input_csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=';')
        for r in reader:
            rows.append(r)

    # generate random variations
    variations = []
    for r in rows:
        # e.g. generate N variations per row
        for _ in range(3):
            new_r = generate_random_variation(r)
            variations.append(new_r)

    # Now combine original + variations or just variations
    # Here we write just variations to a new CSV
    fieldnames = rows[0].keys()
    with open(output_csv_path, "w", newline="", encoding="utf-8") as f_out:
        writer = csv.DictWriter(f_out, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()
        for var_r in variations:
            writer.writerow(var_r)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python random_variations.py <input_csv> <output_csv>")
        sys.exit(1)
    
    input_csv = sys.argv[1]
    output_csv = sys.argv[2]
    main(input_csv, output_csv)
