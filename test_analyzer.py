import pandas as pd
from analyzer import process_features

def test_process_features():
    """
    Tests the core biological math and sequence slicing logic
    without needing to make live API calls.
    """
    
    # 1. Setup Mock Inputs
    # Let's pretend we queried a 20-bp region starting at coordinate 1000
    region_start = 1000
    full_sequence = "ATGCGTGCGAGCGCATGCAT" 
    
    # Create fake Ensembl API response data for two features
    features_data = [
        {
            'id': 'enhancer_1',
            'description': 'putative enhancer',
            'start': 1000, 
            'end': 1004   # 5 bp sequence -> should extract "ATGCG"
        },
        {
            'id': 'promoter_1',
            'description': 'putative promoter',
            'start': 1010,
            'end': 1019   # 10 bp sequence -> should extract "GCGCATGCAT"
        }
    ]
    
    # 2. Run the function
    df, fasta_records = process_features(features_data, full_sequence, region_start)
    
    # 3. Verify DataFrame calculations
    assert len(df) == 2, "Should process exactly two features"
    
    # Check first feature (ATGCG)
    feat1 = df.iloc[0]
    assert feat1['ID'] == 'enhancer_1'
    assert feat1['Length'] == 5
    assert feat1['GC_Percent'] == 60.0  # 3 G/C bases out of 5 = 60%
    assert feat1['CpG_Count'] == 1      # One 'CG' dinucleotide
    
    # Check second feature (GCGCATGCAT)
    feat2 = df.iloc[1]
    assert feat2['ID'] == 'promoter_1'
    assert feat2['Length'] == 10
    assert feat2['GC_Percent'] == 60.0  # 6 G/C bases out of 10 = 60%
    assert feat2['CpG_Count'] == 1      # One 'CG' dinucleotide
    
    # 4. Verify FASTA sequence extraction
    assert len(fasta_records) == 2
    assert str(fasta_records[0].seq) == "ATGCG"
    assert fasta_records[0].id == "enhancer_1"
    assert str(fasta_records[1].seq) == "GCGCATGCAT"
    assert fasta_records[1].id == "promoter_1"