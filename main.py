import argparse
import os
from Bio import SeqIO
from api import fetch_regulatory_features, fetch_region_sequence
from analyzer import process_features, generate_plots

def main():
    parser = argparse.ArgumentParser(description="Analyze regulatory elements in a genomic region.")
    parser.add_argument("--species", default="human", help="Species (e.g., human, mouse)")
    parser.add_argument("--chrom", required=True, help="Chromosome number")
    parser.add_argument("--start", type=int, required=True, help="Start coordinate")
    parser.add_argument("--end", type=int, required=True, help="End coordinate")
    parser.add_argument("--outdir", default="results", help="Output directory")
    
    args = parser.parse_args()
    os.makedirs(args.outdir, exist_ok=True)
    
    print(f"Querying Ensembl for {args.species} chr{args.chrom}:{args.start}-{args.end}...")
    
    # 1. Fetch Data
    features = fetch_regulatory_features(args.species, args.chrom, args.start, args.end)
    print(f"Found {len(features)} regulatory features. Fetching DNA sequence...")
    
    full_seq = fetch_region_sequence(args.species, args.chrom, args.start, args.end)
    
    # 2. Process Data
    print("Calculating GC% and CpG densities...")
    df, fasta_records = process_features(features, full_seq, args.start)
    
    # 3. Save Outputs
    csv_path = os.path.join(args.outdir, "features_summary.csv")
    df.to_csv(csv_path, index=False)
    print(f"Summary saved to {csv_path}")
    
    fasta_path = os.path.join(args.outdir, "sequence_data.fasta")
    SeqIO.write(fasta_records, fasta_path, "fasta")
    print(f"Sequences saved to {fasta_path}")
    
    # 4. Generate Visuals
    print("Generating plots...")
    generate_plots(df, args.outdir)
    print("Pipeline complete! 🧬")

if __name__ == "__main__":
    main()