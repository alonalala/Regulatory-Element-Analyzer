import os
import pandas as pd
import matplotlib.pyplot as plt
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio import SeqIO

def process_features(features_data, full_sequence, region_start):
    """Calculates metrics for each feature and extracts its DNA sequence."""
    records = []
    fasta_entries = []
    
    for item in features_data:
        feat_start = item['start']
        feat_end = item['end']
        
        # Slicing the full sequence to get just the feature's DNA
        # Convert 1-based Ensembl coordinates to 0-based Python indices
        seq_slice = full_sequence[feat_start - region_start : feat_end - region_start + 1].upper()
        
        length = len(seq_slice)
        if length == 0:
            continue
            
        gc_content = (seq_slice.count('G') + seq_slice.count('C')) / length * 100
        cpg_count = seq_slice.count('CG')
        
        records.append({
            'ID': item.get('id'),
            'Type': item.get('description'),
            'Start': feat_start,
            'End': feat_end,
            'Length': length,
            'GC_Percent': round(gc_content, 2),
            'CpG_Count': cpg_count
        })
        
        # Prepare for FASTA export
        fasta_entries.append(
            SeqRecord(Seq(seq_slice), id=item.get('id'), description=item.get('description'))
        )
        
    return pd.DataFrame(records), fasta_entries

def generate_plots(df, outdir):
    """Creates a scatter plot of Length vs GC Content for the features."""
    if df.empty:
        return
        
    plots_dir = os.path.join(outdir, "plots")
    os.makedirs(plots_dir, exist_ok=True)
    
    plt.figure(figsize=(10, 6))
    
    # Color by feature type
    types = df['Type'].unique()
    colors = plt.cm.get_cmap('tab10', len(types))
    
    for i, f_type in enumerate(types):
        subset = df[df['Type'] == f_type]
        plt.scatter(subset['Length'], subset['GC_Percent'], label=f_type, color=colors(i), alpha=0.7)
        
    plt.xlabel("Feature Length (bp)")
    plt.ylabel("GC Content (%)")
    plt.title("Regulatory Features: Length vs. GC Content")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    
    plot_path = os.path.join(plots_dir, "gc_vs_length.png")
    plt.savefig(plot_path, dpi=300)
    plt.close()
    print(f"Plot saved to {plot_path}")