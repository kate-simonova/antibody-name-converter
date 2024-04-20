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

source_infixes = sorted(source_infixes.items(), key=lambda x: len(x[0]), reverse=True)
disease_infixes = sorted(disease_infixes.items(), key=lambda x: len(x[0]), reverse=True)
disease_infixes_outdated = sorted(disease_infixes_outdated.items(), key=lambda x: len(x[0]), reverse=True)

# Function to decode the antibody name
def decode_molecule(antibody):
    d, found = {}, False
    antibody = antibody.lower()

    if antibody.endswith("mab"):
        antibody = antibody[:-3]
        d["mab"] = "Monoclonal antibody (Old antibody nomenclature)"

        for key, value in source_infixes:
            if antibody.endswith(key):
                d[key] = value
                antibody = antibody[:-len(key)]
                break

        for key, value in disease_infixes_outdated:
            if antibody.endswith(key):
                d[key] = value
                antibody = antibody[:-len(key)]
                found = True
                break

        if not found:
            for key, value in disease_infixes:
                if antibody.endswith(key):
                    d[key] = value
                    antibody = antibody[:-len(key)]
                    break


        d[antibody] = "Prefix"
        d["Part of the Word"] = "Meaning"

         return dict(list(d.items())[::-1])

    elif antibody.endswith("ment"):
        antibody = antibody.rstrip("ment")
        d["ment"] = "Immunoglobulin fragment (derived from a variable domain) (New antibody nomenclature)"

    elif antibody.endswith("bart"):
        antibody = antibody.rstrip("bart")
        d["bart"] = "Artificial monoclonal antibody (New antibody nomenclature)"

    elif antibody.endswith("mig"):
        antibody = antibody.rstrip("mig")
        d["mig"] = "Multi-specific immunoglobulins (New antibody nomenclature)"

    elif antibody.endswith("tug"):
        antibody = antibody.rstrip("tug")
        d["tug"] = "Unmodified immunoglobulin (New antibody nomenclature)"

    else:
        print("ERROR: Invalid input")
        return None

    for key, value in disease_infixes:
        if antibody.endswith(key):
            d[key] = value
            antibody = antibody[:-len(key)]
            break

    d[antibody] = "Prefix"
    d["Part of the Word"] = "Meaning"

    return dict(list(d.items())[::-1])
