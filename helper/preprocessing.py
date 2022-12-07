def set_sex(female, male):
    """Set the sex according to the highest probability.
    If the difference is less than 10 %, it is set to " Undetermined ".
    """
    if abs(female - male) < 0.1:
        return 'Undetermined'
    elif female > male:
        return 'Female'
    else:
        return 'Male'
