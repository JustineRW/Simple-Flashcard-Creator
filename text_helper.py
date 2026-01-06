
def clean_text(input_string: str):
    cleaned_input : str = str.replace(input_string,"‘","'")
    return cleaned_input

def get_species_full_name_or_plural(genus : str, species : str):
    species_name_or_plural = species if isinstance(species, str) else 'spp.' #empty species cell indicates we just want to use the genus name
    full_name = clean_text(genus + ' ' + species_name_or_plural)
    return full_name