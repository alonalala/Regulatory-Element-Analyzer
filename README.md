# Regulatory Element Analyzer 🧬

## What does this project do?
In molecular biology and epigenetics, studying how genes are regulated often involves manually looking up a genomic region, finding putative enhancers/promoters, downloading their DNA sequences, and analyzing them for specific transcription factor binding motifs or CpG density. This process involves switching between multiple web browsers, databases, and excel sheets. 

This project completely automates that workflow. The **Regulatory Element Analyzer** is a Python-based CLI (Command Line Interface) pipeline that:
1. Queries the Ensembl REST API for a specific genomic coordinate.
2. Extracts all regulatory features (enhancers, promoters).
3. Fetches the underlying DNA sequence (FASTA) for those features.
4. Analyzes the sequences for rolling GC% content, CpG density, and custom mammalian binding motifs.
5. Outputs a summary report and publication-ready density plots.


## Input and Output
**Input:**
* A genomic region (Species, Chromosome, Start, End) provided via command-line arguments.
* (Optional) A `.txt` file containing specific DNA motifs to search for (e.g., `TCAGCACC` for REST).

**Output:**
* `features_summary.csv`: A clean table of all regulatory features found in the region, their exact coordinates, length, and motif hit counts.
* `sequence_data.fasta`: The actual DNA sequences of the identified elements.
* `plots/`: A folder containing `.png` graphs plotting the GC% and CpG density across the length of the top 5 longest regulatory elements.

## Acknowledgments
This project was developed as the final capstone project for the [Weizmann Institute of Science Python Course](https://github.com/Code-Maven/wis-python-course-2026-03). Special thanks to the course instructor, Gabor Szabo and for the kind TAs Liron and Hadar.

## Technicalities

### Prerequisites
* Python 3.9+
* A stable internet connection (for API calls)

### How to install dependencies
Clone this repository and install the required 3rd-party libraries using `pip`:
```bash
git clone [https://github.com/](https://github.com/)[Your-Username]/Regulatory-Element-Analyzer.git
cd Regulatory-Element-Analyzer
pip install -r requirements.txt
