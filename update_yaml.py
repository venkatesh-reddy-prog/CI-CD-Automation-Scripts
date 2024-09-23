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

def modify_yaml_file(file_path, env_dict):
    try:
        with open(file_path, 'r') as file:
            yaml_documents = list(yaml.safe_load_all(file))  
        
        modified = False
        for yaml_data in yaml_documents:
            if replace_modify_values(yaml_data, env_dict):
                modified = True

        if modified:
            with open(file_path, 'w') as file:
                yaml.dump_all(yaml_documents, file)  
        return 0
    except Exception as e:
        return 1

def process_yaml_files_in_directory(directory, env_dict):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(('.yaml', '.yml')):
                file_path = os.path.join(root, file)
                modify_yaml_file(file_path, env_dict)

if __name__ == "__main__":
    updates_str = os.getenv('updates')
    env_dict = parse_env_variable_string(updates_str)
    root_directory = r"C:\Users\I751676\Desktop\Clone_Repo\Template_Repo"
    process_yaml_files_in_directory(root_directory, env_dict)
