import sys
import pandas as pd

def read_files(input_file_1, input_file_2):
    line_list = pd.read_csv(input_file_1)
    variants_list = pd.read_csv(input_file_2)
    return line_list, variants_list

def create_lists(line_list, variants_list):
    line_list_variants = line_list['Variant_name'].tolist()
    add_variant = variants_list['variant_name'].tolist()
    new_variant = []
    return line_list_variants, add_variant, new_variant

def new_variant_list(line_list_variants, add_variant, new_variant):
    for variant in line_list_variants:
        if variant not in add_variant:
            new_variant.append(variant)
    return new_variant

def main(input_file_1, input_file_2, output_file):
    line_list, variants_list = read_files(input_file_1, input_file_2)
    line_list_variants, add_variant, new_variant = create_lists(line_list, variants_list)
    new_variant = new_variant_list(line_list_variants, add_variant, new_variant)
    new_variant = pd.DataFrame(new_variant)
    new_variant.to_csv(output_file, index=False)

if __name__ == "__main__":
    if len(sys.argv) !=4:
        print("Usage: python3 ./scripts/update_variant_list.py data/test_linelist.csv data/test_variants.csv results/new_variants.csv")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2], sys.argv[3])
