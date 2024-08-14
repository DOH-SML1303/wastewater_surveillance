# snakemake

rule all:
  input:
    "results/latest_sc2_variants_ww.pdf"

rule plot_variant_proportions:
  input:
    data = "results/WW_data.csv"
  output:
    props = "results/proportions.csv",
    table = "results/proportions_table.csv",
    plot =  "results/proportions_plot.jpg"
  shell:
    """
    python3 ./scripts/plot_variant_props.py {input.data} {output.props} {output.table} {output.plot}
    """

rule get_latest_proportions:
  input:
    table = "results/proportions_table.csv"
  output:
    latest_props = "results/latest_proportions.csv"
  shell:
    """
    python3 ./scripts/get_latest_proportions.py {input.table} {output.latest_props}
    """

rule create_report:
  input:
    plot =  "results/proportions_plot.jpg",
    latest_props = "results/latest_proportions.csv"
  output:
    pdf = "results/latest_sc2_variants_ww.pdf"
  shell:
    """
    python3 ./scripts/create_report.py {input.plot} {input.latest_props} {output.pdf}
    """
