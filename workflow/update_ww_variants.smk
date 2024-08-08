# snakemake

rule all:
    input:
        "results/proportions_plot.jpg"

rule add_parent_variant:
    input:
        data = "data/WW_master.csv",
        variants = "data/WW_variants.csv"
    output:
        data_parents = "data/WW_data_variants.csv"
    shell:
        """
        python3 ./scripts/ww_add_parent_variant.py {input.data} {input.variants} {output.data_parents}
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

rule plot_proportions:
    input:
        data_hexcodes = "data/WW_data_hexcodes.csv"
    output:
        proportions_results = "results/proportions.csv",
        proportions_plot = "results/proportions_plot.jpg"
    shell:
        """
        python3 ./scripts/plot_proportions.py {input.data_hexcodes} {output.proportions_results} {output.proportions_plot}
        """
