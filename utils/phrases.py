def get_number_from_text(text:str) -> int:
    """
        Gets the number of context.
    """

    for char in text:
        try:
            int(char)
            return int(char)
        except:
            continue
    
    return -1