from ete3 import TreeNode, TreeStyle, NodeStyle, TextFace, AttrFace, faces
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.colors as mcolors
import random
import glasbey

data = pd.read_csv("data/laccases_combined_analysis/1103_laccase_taxonomy_phylum_consolidated_SR.csv")
data['phylum_clean'] = data['phylum'].str.split('__').str[1]
data['phylum_clean'] = data['phylum_clean'].str.split('_').str[0]
#data.loc[data['phylum_clean'].isna(), 'phylum_clean'] = 'Unclassified'

#TODO: color the unclassified with grey or something dull
t = TreeNode(r"data/laccases_combined_analysis/1103_aligned_laccase_seqs_fasttree.nwk"
             ,format =1)

phyla = data['phylum_clean'].unique().tolist()
#selected_colors = glasbey.create_palette(palette_size=len(phyla), lightness_bounds=(20, 45), chroma_bounds=(40, 55))

selected_colors = []
with open("output/20260119_hex_colors.txt", "r") as f:
    for line in f:
        line = line.strip('\n')
        selected_colors.append(line)



sns.palplot(selected_colors)
plt.show()


phylum_color = {phyla[i]:selected_colors[i] for i in range(len(phyla))} #phylum is the key, the color code is value
# phylum_color['Unclassified'] = '#FFFFFF'

color_map = {label:phylum_color[phylum] for label,phylum in zip(data['label'].to_list(), data['phylum_clean'].to_list())}
#TODO: change 'nan' label to 'other' or not labeled
def create_legend(colours_dict, output_path):
    legend_elements = []
    for label in colours_dict.keys():
        legend_elements = legend_elements + [plt.Line2D([0], [0], color = colours_dict[label], lw=4, label=label)]
    # Create the figure
    fig, ax = plt.subplots(figsize = (3,3))
    ax.legend(handles=legend_elements, loc='center' )
    plt.gca().set_axis_off()
    plt.savefig(output_path, bbox_inches='tight',dpi=300)

node_styles = {}

def apply_colors(node):

    node_dict = {'YAOCHUN_JAGNTG010000097.1' : 'MCO1', 'HYV56308.1' : 'aMCO', 'HEY7867587.1' : 'mMCO'}
    if node.name in node_dict.keys():
        print(f"{node.name} found")
        node.img_style['bgcolor'] = 'black'
        # label_face = TextFace(node_dict[node.name], fsize=50, fgcolor="red", bold=True, tight_text=False)
        # label_face.margin_left = 200

        # faces.add_face_to_node(label_face, node, column=1, position="branch-right")

    elif node.is_leaf() and node.name in color_map:
       node.img_style["bgcolor"] = color_map[node.name]

# Apply the custom branch coloring function to the tree


# Create a TreeStyle object and apply the coloring function using on_iter
ts = TreeStyle()
ts.show_leaf_name = False
ts.layout_fn = apply_colors
ts.mode = "c" # Set the tree type to circular with "c" value for the mode
ts.arc_start = 0  # Set the starting angle
ts.arc_span = 360


ts.allow_face_overlap = True


t.render("output/20260120_laccase_seqs_fasttree_VP_no_txt_v8.svg", w=3000, dpi=600, tree_style=ts)
t.render("output/20260120_laccase_seqs_fasttree_VP_no_txt_v8.png", w=3000, dpi=600, tree_style=ts)
create_legend(phylum_color, "output/20260120_laccase_seqs_fasttree_legend_VP_v8.svg")
with open("output/20260120_selected_colors_hex_list_order_v8.txt", "w") as f:
    f.write('\n'.join(selected_colors))
print('done')