# Courtesy of https://www.reddit.com/user/lechaosx/
# https://topaz.github.io/paste/#XQAAAQDiCgAAAAAAAAA0m0pnuFI8c/fBNAqG6qhqad37PBl4YmgpuMHWvAT/cpW5xfV0EcJzmecQuKdd59U/Ma4Q8xHOWDQjLNYQTXYNv3BBr9zgRZK5wt4JaYZ58MnAZ1gSqzRWbBTUz7GTtultgRhJu3ZTX3L/bnpjcKTZYf/h3jHKZqzoFasWdGxMN0za97BE6O6eNoGQxqVcwu9xF82CW97c+BuCcGX/AitCAtTavMBZeF/PN8e/tkGlkJAj4V6NncH7r8PWWS51SdhBi8LydtMKISLzQilMSzXldkCBVV+c3jbrUxlrujgs8Zd29ohyxc7UdJpfTVRkmCfQ49tRz1NxP23WWBo0Mdtk6RkBltvG8UGDV5Kb0jcEKidC4EF0FDrJSFDgQnqlRR0Qatd0qmjm9gHGt8LpgBUeW2ecp2L/gT9u0Hw+Of76Jp26lf89x4NupnmgqopWKA2q7MZJVcwTMf/XRgRD8qDFesx2QCDO1L0XQBIyjQEpFkweT7+On0+XNezh/6AAeTfpWMBZI9i4rInZQ5o7J6qbdX7DUI3ui1Pu2meOA9AOFes3n64O2BkJbW2bAQkPqwQcorLlylSACBn2wMB9bvom73psS/7GnllTkD6wnPXda1+QIjW19YCXze/Wh2WH34HZs534/q/Y5j517K/L83u8Z2WInwabTtuI8W7RaZP/IHnfHyD9EbYcSNwljZgIOVlxX6nA/PkzKtlRNSKhp7w1laVrmF7uEsg2GgR8tLvg70NzH+huyg/SauDLYAkTa2S1dt0szgs0uoLwItb+H+/JXaIUS65fl+Thm1zDEOTxeRchmJmt1kQx4UdnQhe75abtVoSwBCBMvVBcIIj4c/iGj/ozkXSBjzYqNrFN40FTog2J5pDZ6UZiEdAnI2gXgYHrkPTWKN7MMbJDmey95qazRtJ58tv30AuRbiP9aVJ57yw18rdgGChJcurgZan6R/QcIrYWSgC5fa6W9wNa5vLyKsjlqmffthOT7+bUdP5Hht3soW7Qh/g99vbdazI68T3MsYdl8CCcWdm0guNj47CjFFD0UVwY6VUd808If75ZVY0yTG3tLgoPl3CArS3JGm7dxVvg//fFkzs=

import sys

def parse_map(input):
    conversion_map = []

    while line := input.readline().strip():
        if not line[0].isdigit():
            continue
        conversion_map.append(tuple(map(int, line.split())))

    return sorted(conversion_map, key=lambda item: item[1])

def intersect(a, b):
    a_start, a_length = a
    a_end = a_start + a_length

    b_start, b_length = b
    b_end = b_start + b_length

    intersection_start = max(a_start, b_start)
    intersection_end = min(a_end, b_end)
    intersection_length = intersection_end - intersection_start

    return (intersection_start, intersection_length)

def subtract(a, b):
    a_start, a_length = a
    a_end = a_start + a_length

    b_start, b_length = b
    b_end = b_start + b_length

    difference = []

    if a_start < b_start:
        difference.append((a_start, b_start - a_start))

    if a_end > b_end:
        difference.append((b_end, a_end - b_end))

    return difference

def map_ranges(map, unmapped_ranges):
    mapped_ranges = []
    
    for dst_range_start, src_range_start, range_len in map:
        rest_of_unmapped_ranges = []

        for unmapped_range in unmapped_ranges:
            intersection_start, intersection_length = intersect(unmapped_range, (src_range_start, range_len))

            if intersection_length > 0:
                mapped_ranges.append((intersection_start - src_range_start + dst_range_start, intersection_length))
                rest_of_unmapped_ranges += subtract(unmapped_range, (src_range_start, range_len))
            
            else:
                rest_of_unmapped_ranges.append(unmapped_range)

        unmapped_ranges = rest_of_unmapped_ranges

    return mapped_ranges + unmapped_ranges

def main():
    with open(sys.argv[1], "r") as file:
        seed_line = file.readline().split(":")[1].split()

        seed_ranges = [(int(seed_start), int(length)) for seed_start, length in zip(seed_line[::2], seed_line[1::2])]

        file.readline()

        seed_to_soil            = parse_map(file)
        soil_to_fertilizer      = parse_map(file)
        fertilizer_to_water     = parse_map(file)
        water_to_light          = parse_map(file)
        light_to_temperature    = parse_map(file)
        temperature_to_humidity = parse_map(file)
        humidity_to_location    = parse_map(file)

        def seeds_to_location_ranges(seed_ranges):
            soil_ranges             = map_ranges(seed_to_soil, seed_ranges)
            fertilizer_ranges       = map_ranges(soil_to_fertilizer, soil_ranges)
            water_ranges            = map_ranges(fertilizer_to_water, fertilizer_ranges)
            light_ranges            = map_ranges(water_to_light, water_ranges)
            temperature_ranges      = map_ranges(light_to_temperature, light_ranges)
            humidity_ranges         = map_ranges(temperature_to_humidity, temperature_ranges)
            location_ranges         = map_ranges(humidity_to_location, humidity_ranges)
            return location_ranges
        
        location_ranges = seeds_to_location_ranges(seed_ranges)

        print(min([range_begin for range_begin, _ in location_ranges]))
        
if __name__ == "__main__":
    print("Running main...")
    main()