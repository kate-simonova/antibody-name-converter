#!/bin/python3

from collections import OrderedDict

disease_infixes = {
    'ba': 'Bacterial infections',
    'ta': 'Tumor and cancers',
    'ki': 'Cytokine and cytokine receptors',
    'li': 'Immune system targets',
    'ne': 'Neuronal targets',
    'vi': 'Viral infections',
    'ci': 'Cardiovascular',
    'ami': 'Serum amyloid protein (SAP)/amyloidosis',
    'de': 'Metabolic or endocrine pathways',
    'eni': 'Enzyme inhibition',
    'fung': 'Fungal',
    'gro': 'Growth factor and growth factor receptor',
    'ler': 'Allergen',
    'sto': 'Immunostimulatory',
    'pru': 'Immunosuppressive',
    'os': 'Bone',
    'vet': 'Veterinary use',
    'toxa': 'Toxin'
}

disease_infixes_outdated = {
    'tu': 'Tumor and cancers',
    'anibi': 'Angiogenesis',
    'les': 'Inflammatory leisons',
    'li': 'Immunomodulating',
    'lim': 'Immunomodulating',
    'l': 'Immunomodulating',
    'mul': 'Musculoskeletal system',
    'co': 'Colon tumor',
    'col': 'Colon tumor',
    'go': 'Testicular/ovarian tumor',
    'gov': 'Ovarian tumor',
    'got': 'Testicular tumor',
    'ma': 'Mammary glands tumor',
    'mar': 'Mammary glands tumor',
    'me': 'Melanoma',
    'mel': 'Melanoma',
    'pr': 'Prostate tumor',
    'pro': 'Prostate tumor',
    'tum': 'Tumor and cancers',
    }


source_infixes = {
    'zu': 'Humanized',
    'o': 'Mouse',
   # 'e': 'Hamster',
    'u': 'Human',
   # 'a': 'Rat',
    'xi': 'Chimeric',
   # 'i' : 'Primate',
    'axo' : 'Rat-Murine hybrid',
    'xizu': 'Chimeric-humanized',
}

mab_new_names = {
    'unmodified immunoglobulins (New antibody nomenclature)' : 'tug',
    'artificial immunoglobulins (New antibody nomenclature)' : 'bart',
    'immunoglobulin fragments (New antibody nomenclature)' : 'ment',
    'multi-specific immunoglobulins (New antibody nomenclature)' : 'mig',
    'monoclonal antibody (Old antibody nomenclature)' : 'mab'
}


disease_infixes = OrderedDict(sorted(disease_infixes.items(), key=lambda x: len(x[0]), reverse=True))
disease_infixes_outdated = OrderedDict(sorted(disease_infixes_outdated.items(), key=lambda x: len(x[0]), reverse=True))
source_infixes = OrderedDict(sorted(source_infixes.items(), key=lambda x: len(x[0]), reverse=True))
encode_disease_infixes = {value:key for key, value in disease_infixes.items()}

# Function to decode the antibody name
def decode_molecule(antibody):
    d, found = {}, False
    antibody = antibody.lower()

    for description, suffix in mab_new_names.items():
        if antibody.endswith(suffix):
            antibody = antibody[:-len(suffix)] 
            d[suffix] = description
            break
    else:
        print('ERROR: Invalid input')
        return None

    for infix, description in source_infixes.items():
            if antibody.endswith(infix):
                d[infix] = description
                antibody = antibody[:-len(infix)]
                break

    for infix, description in disease_infixes.items():
        if antibody.endswith(infix):
            d[infix] = description
            antibody = antibody[:-len(infix)]
            found = True
            break

    if not found:
        for infix, description in disease_infixes_outdated.items():
            if antibody.endswith(infix):
                d[infix] = description
                antibody = antibody[:-len(infix)]
                break

    d[antibody] = 'Prefix'
    d['Part of the Word'] = 'Meaning'

    return dict(list(d.items())[::-1])
