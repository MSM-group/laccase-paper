from ete3 import TreeNode, TreeStyle, NodeStyle, TextFace, AttrFace, faces
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.colors as mcolors
import random

data = pd.read_csv("data/laccases_combined_analysis/MCO1_homolog_table.csv")
data['phylum_clean'] = data['phylum'].str.split('__').str[1]
data['phylum_clean'] = data['phylum_clean'].str.split('_').str[0]
#data.loc[data['phylum_clean'].isna(), 'phylum_clean'] = 'Unclassified'

#TODO: color the unclassified with grey or something dull
t = TreeNode(r"data/laccases_combined_analysis/1103_aligned_laccase_seqs_fasttree.nwk"
             ,format =1)

phyla = data['phylum_clean'].unique().tolist()

# Choose a color-blind friendly palette
# For instance, 'glasbey' is a good option for distinct colors
colors = sns.color_palette("cubehelix", 5+len(phyla))
# Select the first 17 colors from the palette
hex_colors = [mcolors.to_hex(color) for color in colors]
selected_colors = hex_colors[4:-1]
random.shuffle(selected_colors)
# Plot the colors
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

# Function to apply custom branch colors
def apply_colors(node):
    if node.name == 'YAOCHUN_JAGNTG010000097.1':
        node.img_style['shape'] = 'circle'
        node.img_style['size'] = 50
        node.img_style["bgcolor"] = 'red'
        label_face = TextFace("MCO1", fsize=30, fgcolor="red")
        node.add_face(label_face, column=0, position="branch-right")
    else:
        if node.is_leaf() and node.name in color_map:
            node.img_style["bgcolor"] = color_map[node.name]


# Apply the custom branch coloring function to the tree
#t.img_style["size"] = 0  # Hide default node dots
# Apply the custom branch coloring function to the tree
t.traverse(apply_colors)

# Create a TreeStyle object and apply the coloring function using on_iter
ts = TreeStyle()
ts.show_leaf_name = True
ts.layout_fn = apply_colors
ts.mode = "c" # Set the tree type to circular with "c" value for the mode
ts.arc_start = 0  # Set the starting angle
ts.arc_span = 360

# query_leaf_name = 'YAOCHUN_JAGNTG010000097.1'
# node = t&query_leaf_name   # "&" is used to retrieve a node by name
# N = AttrFace("name", fsize=30)
# node.add_face(N, 0, position="aligned")


t.render("output/20240628_laccase_seqs_fasttree_VP_v4.png", w=600, dpi=300, tree_style=ts)
create_legend(phylum_color, "output/20240628_laccase_seqs_fasttree_legend_VP_v4.png")
with open("output/20240628_selected_colors_hex_list_order_v4.txt", "w") as f:
    f.write('\n'.join(selected_colors))
print('done')