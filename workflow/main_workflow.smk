# snakemake

rule all:
  input:
    "results/WW_data.csv"

rule add_parent_variant:
  input:
    master_data = "data/WW_master.csv",
    variants = "data/WW_variants.csv"
  output:
    data_parents = "data/WW_data_variants.csv"
  shell:
    """
    python3 ./scripts/ww_add_parent_variant.py {input.master_data} {input.variants} {output.data_parents}
    """

rule add_hex_codes:
    input:
        data_parents = "data/WW_data_variants.csv",
        hexcodes = "data/WW_hexcodes.csv"
    output:
        data_hexcodes = "data/WW_data_hexcodes.csv"
    shell:
        """
        python3 ./scripts/add_hex_codes.py {input.data_parents} {input.hexcodes} {output.data_hexcodes}
        """

rule add_lat_long:
    input:
        data_hexcodes = "data/WW_data_hexcodes.csv",
        lat_long = "data/sample_site-counties.csv"
    output:
        data_lat_long = "data/WW_data_lat_long.csv"
    shell:
        """
        python3 ./scripts/add_lat_long.py {input.data_hexcodes} {input.lat_long} {output.data_lat_long}
        """

rule convert_to_week_dates:
    input:
        data_lat_long = "data/WW_data_lat_long.csv"
    output:
        data_week_dates = "data/WW_data_week_dates.csv"
    shell:
        """
        python3 ./scripts/convert_to_week_dates.py {input.data_lat_long} {output.data_week_dates}
        """

rule normalize_proportions:
    input:
        data_week_dates = "data/WW_data_week_dates.csv"
    output:
        data = "results/WW_data.csv"
    shell:
        """
        python3 ./scripts/normalize_proportions.py {input.data_week_dates} {output.data}
        """
