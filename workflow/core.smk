# snakemake
rule all:
    input:
    	"results/ww_report.pdf"

# add new run to master
rule add_new_run_to_master:
    input:
        master = "data/ww_master.csv",
        new_runs_dir = "new_data/"
    output:
        new_run_master = "results/ww_new_run_to_master.csv",
        new_variants_file = "results/new_variants.csv"
        # need another ww_master.csv in results to be copied over to data
        # folder when new runs come in
        # new ww_master.csv should just include only the data from new runs
    shell:
    	"""
   	 python3 ./scripts/add_new_run.py {input.master} {input.new_runs_dir} {output.new_run_master} {output.new_variants_file}
  	  """

# add parent lineage
rule add_parent_lineage_to_master:
    input:
    	new_run_master = "results/ww_new_run_to_master.csv",
    	lineage_class = "data/ww_lineage_classifications.csv"
    output:
    	new_lineages_master = "results/ww_new_lineages_to_master.csv"
    shell:
    	"""
   	 python3 ./scripts/add_parent_lineages.py {input.new_run_master} {input.lineage_class} {output.new_lineages_master}
   	"""

# add sample sites
rule add_sample_sites_to_master:
    input:
    	new_lineages_master = "results/ww_new_lineages_to_master.csv",
    	sample_sites = "data/sample_site-counties.csv"
    output:
    	new_added_sites = "results/ww_sites_added_master.csv"
    shell:
    	"""
    	python3 ./scripts/add_sample_sites.py {input.new_lineages_master} {input.sample_sites} {output.new_added_sites}
    	"""

# convert to week dates
rule convert_to_week_dates:
    input:
    	new_added_sites = "results/ww_sites_added_master.csv"
    output:
    	new_week_dates_added = "results/ww_week_dates_added.csv"
    shell:
   	 """
    	python3 ./scripts/convert_to_week_dates.py {input.new_added_sites} {output.new_week_dates_added}
    	"""

# normalize proportions
rule normalize_proportions:
    input:
    	new_week_dates_added = "results/ww_week_dates_added.csv"
    output:
    	new_proportions_normalized = "results/ww_added_norm_proportions.csv"
    shell:
    	"""
    	python3 ./scripts/normalize_proportions.py {input.new_week_dates_added} {output.new_proportions_normalized}
    	"""

# plot variant proportions
rule plot_variant_proportions:
    input:
    	new_proportions_normalized = "results/ww_added_norm_proportions.csv"
    output:
    	proportions = "results/proportions.csv",
    	proportions_table = "results/proportions_table.csv",
    	proportions_plot = "results/proportions_plot.jpg"
    shell:
    	"""
    	python3 ./scripts/plot_variant_proportions.py {input.new_proportions_normalized} {output.proportions} {output.proportions_table} {output.proportions_plot}
   	"""

# get latest proportions
rule get_latest_proportions:
    input:
    	proportions_table = "results/proportions_table.csv",
    	new_proportions_normalized = "results/ww_added_norm_proportions.csv"
    output:
    	heatmap = "results/heatmap_latest_proportions.jpg",
    	line_graph = "results/line_graph_latest_proportions.jpg"
    shell:
    	"""
    	python3 ./scripts/get_latest_proportions.py {input.proportions_table} {input.new_proportions_normalized} {output.heatmap} {output.line_graph}
    	"""

rule generate_timeline:
    input: 
    	new_proportions_normalized = "results/ww_added_norm_proportions.csv"
    output:
    	timeline = "results/timeline.jpg"
    shell:
    	"""
    	python3 ./scripts/timeline.py {input.new_proportions_normalized} {output.timeline}
    	"""

# generate gradient map
rule create_gradient_map:
    input:
    	new_proportions_normalized = "results/ww_added_norm_proportions.csv",
    	shape_file = "data/WA_County_Boundaries.shp"
    output:
    	gradient_map = "results/wa_geographic_map_gradient.jpg"
    shell:
    	"""
    	python3 ./scripts/create_gradient_map.py {input.new_proportions_normalized} {input.shape_file} {output.gradient_map}
    	"""
    
# generate geographic maps
rule create_geographic_maps:
    input:
    	new_proportions_normalized = "results/ww_added_norm_proportions.csv",
    	shape_file = "data/WA_County_Boundaries.shp"
    output:
    	geographic_maps = "results/wa_geographic_map_dominant_variants_last_3_months.jpg"
    shell:
    	"""
    	python3 ./scripts/create_geographic_maps.py {input.new_proportions_normalized} {input.shape_file} {output.geographic_maps}
    	"""

# create report
rule create_report:
    input:
    	proportions_plot = "results/proportions_plot.jpg",
    	proportions_text = "data/proportions.txt",
    	heatmap = "results/heatmap_latest_proportions.jpg",
    	heatmap_text = "data/heatmap.txt",
    	line_graph = "results/line_graph_latest_proportions.jpg",
    	line_graph_text = "data/line_graph.txt",
    	timeline = "results/timeline.jpg",
    	timeline_text = "data/timeline.txt",
    	gradient_map = "results/wa_geographic_map_gradient.jpg",
    	gradient_map_text = "data/gradient_map.txt",
    	geographic_maps = "results/wa_geographic_map_dominant_variants_last_3_months.jpg",
    	geographic_maps_text = "data/geographic_maps.txt"
    output:
    	report = "results/ww_report.pdf"
    shell:
    	"""
    	python3 ./scripts/create_report.py {output.report} {input.proportions_plot} {input.proportions_text} {input.heatmap} {input.heatmap_text} {input.line_graph} {input.line_graph_text} {input.timeline} {input.timeline_text} {input.gradient_map} {input.gradient_map_text} {input.geographic_maps} {input.geographic_maps_text}
    	"""

#rule upload:
 #   input:
  #  output:
   # shell:
    #"""
    #"""
