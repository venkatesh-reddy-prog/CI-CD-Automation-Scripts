import os
import yaml  # type: ignore

def parse_env_variable_string(env_variable_str):
    env_dict = {}
    if env_variable_str:
        pairs = env_variable_str.split(',')
        for pair in pairs:
            key, value = pair.split('=')
            env_dict[key.strip()] = value.strip("'").strip()
    return env_dict

def replace_modify_values(yaml_data, env_dict):
    modified = False
    if isinstance(yaml_data, dict):
        for key, value in yaml_data.items():
            if isinstance(value, dict) or isinstance(value, list):
                if replace_modify_values(value, env_dict):
                    modified = True
            elif isinstance(value, str) and "Modify" in value:
                env_value = env_dict.get(key)
                if env_value:
                    yaml_data[key] = value.replace("Modify", env_value)
                    modified = True    
    elif isinstance(yaml_data, list):
        for item in yaml_data:
            if replace_modify_values(item, env_dict):
                modified = True
    return modified

def modify_yaml_file(src_file_path, dest_file_path, env_dict):
    try:
        with open(src_file_path, 'r') as file:
            yaml_documents = list(yaml.safe_load_all(file))
        
        for yaml_data in yaml_documents:
            if replace_modify_values(yaml_data, env_dict):
                print(f"Modified file: {dest_file_path}")

        os.makedirs(os.path.dirname(dest_file_path), exist_ok=True)
        with open(dest_file_path, 'w') as file:
            yaml.dump_all(yaml_documents, file)
        return 0
    except Exception as e:
        print(f"Error processing file {src_file_path}: {e}")
        return 1

def process_yaml_files_in_directory(src_directory, dest_directory, env_dict):
    for root, dirs, files in os.walk(src_directory):
        for file in files:
            if file.endswith(('.yaml', '.yml')):
                src_file_path = os.path.join(root, file)
                dest_file_path = os.path.join(dest_directory, os.path.relpath(src_file_path, src_directory))
                modify_yaml_file(src_file_path, dest_file_path, env_dict)

if __name__ == "__main__":
    updates_str = os.getenv('UPDATES')
    env_dict = parse_env_variable_string(updates_str)
    
    # Use user-specific paths
    source_clone_dir = os.path.expanduser("./Clone_Repo/Template_Repo")
    dest_clone_dir = os.path.expanduser("./Clone_Repo/Demo1-Folder")
    
    process_yaml_files_in_directory(source_clone_dir, dest_clone_dir, env_dict)

    print("YAML files have been processed and written to the destination repository.")
