from pathlib import Path

def load_keybind_section(config: Path = Path("~/.config/zellij/config.kdl").expanduser()):
    '''
    Load the keybinds from the config file
    '''


    # Flag for whether or we are in the keybind potion of the file
    in_binds = False

    # This will be a list of the stripped lines
    bind_section = []

    with open(config, "r") as f:

        # Iterate over the lines
        for line in f.readlines():

            # If were not current in the keybinds, see if this 
            # is the first line of the keybinds definition
            if not in_binds:
                if "keybinds" in line:
                    in_binds = True
                else:
                    continue

            # If we get here we are in the keybind section
            bind_section.append(line.strip())

    return bind_section

def parse_keybinds(rawlines: list[str]):
    '''
    Parse the keybinds from load_keybind_section
    '''


    clean_lines = []
    cur_section_name = "None"

    for line in rawlines:
        if "bind" not in line and "{" in line:
            cur_section_name = line.split()[0]
        # Start by getting every line that has bind in it
        if "bind" in line:
            formated_line = line.replace("{", "is")
            formated_line = formated_line.replace("}", "")
            formated_line = formated_line.replace(";", "")

            clean_lines.append((cur_section_name,formated_line))

    return clean_lines

def pretty_print_keys(keys: list[str]):
    for key in keys:
        print(f"{key[0]:<4} | {key[1]}")
    return

def keyword_search(lines: list[str], words: list[str]):
    '''
    Search for word matches and print the lines 
    that contain the keyword
    '''

    print("Seach for", words)
    for line in lines:
        if any(word.lower() in line[1].lower() for word in words):
            print(f"{line[0]:<4} | {line[1]}")
    
    print("Search done")
    return


if __name__ == "__main__":
    cleaned_keys = parse_keybinds(load_keybind_section())

    pretty_print_keys(cleaned_keys)

    keyword_search(cleaned_keys, ['move'])
