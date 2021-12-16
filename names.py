def names_compare(abstract_name, td_name):
    abstract_name_split = abstract_name.split()
    abstract_first_name = abstract_name_split[0]
    abstract_last_name = abstract_name_split[-1]

    td_name_split = td_name.split()
    td_last_name = td_name_split[0]
    td_first_letter_first_name = td_name_split[-1]

    return (abstract_last_name == td_last_name) and (abstract_first_name[0] == td_first_letter_first_name[0])
