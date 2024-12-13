import json
from pathlib import Path

class MermaidDiagramGenerator:
    def __init__(self, folder_path=None):
        """Initialize the diagram generator with an optional folder path"""
        self.folder_path = Path(folder_path) if folder_path else Path(__file__).parent
        self.folder_name = self.folder_path.name

    def create_node_id(self, prefix, name):
        """Create a sanitized node ID"""
        sanitized = name.lower().replace(' ', '_').replace('-', '_').replace(':', '_').replace('/', '_').replace('.', '_')
        return f"{prefix}_{sanitized}" if prefix else sanitized

    def format_value(self, key, value):
        """Format the node text with key-value pair"""
        return f"{key}: {value}"

    def process_container(self, container_data, container_name, file_name, diagram):
        """Process individual container"""
        container_id = self.create_node_id(file_name, container_name)
        display_name = f"{container_name} ({container_data.get('type', 'resource')})"
        diagram.append(f"            subgraph {container_id}[\"{display_name}\"]")
        
        for key in ["name", "type", "technology", "description"]:
            if key in container_data:
                node_id = self.create_node_id(f"{file_name}_{container_name}", key)
                diagram.append(f"                {node_id}[\"{self.format_value(key, container_data[key])}\"]")
        
        if "properties" in container_data:
            props_id = self.create_node_id(f"{file_name}_{container_name}", "properties")
            diagram.append(f"                subgraph {props_id}[Properties]")
            for key, value in container_data["properties"].items():
                if isinstance(value, dict):
                    for env_key, env_value in value.items():
                        node_id = self.create_node_id(f"{file_name}_{container_name}", f"{key}_{env_key}")
                        diagram.append(f"                    {node_id}[\"{key}: {env_key}={env_value}\"]")
                elif isinstance(value, list):
                    node_id = self.create_node_id(f"{file_name}_{container_name}", key)
                    diagram.append(f"                    {node_id}[\"{key}: {', '.join(map(str, value))}\"]")
                else:
                    node_id = self.create_node_id(f"{file_name}_{container_name}", key)
                    diagram.append(f"                    {node_id}[\"{self.format_value(key, value)}\"]")
            diagram.append("                end")
        
        diagram.append("            end")
        return container_id

    def process_containers(self, json_data, file_name, diagram):
        """Process containers and return container IDs"""
        container_ids = {}
        
        containers_dict = {}
        if isinstance(json_data, list):
            for container in json_data:
                if "name" in container:
                    containers_dict[container["name"]] = container
        else:
            containers_dict = json_data
        
        for key, value in containers_dict.items():
            if isinstance(value, dict):
                if "type" in value:
                    container_ids[key] = self.process_container(value, key, file_name, diagram)
        
        return container_ids

    def add_relationships(self, json_data, container_ids, diagram):
        """Add relationships between containers"""
        if isinstance(json_data, dict):
            containers_dict = json_data
        else:
            containers_dict = {container["name"]: container for container in json_data if "name" in container}
        
        diagram.append("            %% Relationships")
        for container_name, container_data in containers_dict.items():
            if "relationships" in container_data:
                for rel in container_data["relationships"]:
                    if isinstance(rel, dict) and "target" in rel and "type" in rel:
                        source_id = container_ids[container_name]
                        target_id = container_ids[rel["target"]]
                        rel_type = rel["type"].replace("_", " ")
                        diagram.append(f"            {source_id} ---|{rel_type}| {target_id}")

    def generate_diagram(self, json_files=None):
        """Generate Mermaid diagram from JSON files"""
        if json_files is None:
            json_files = list(self.folder_path.glob('*.json'))

        if not json_files:
            raise ValueError("No JSON files found")

        diagram = []
        diagram.append("flowchart TD")
        diagram.append("    %% Styling")
        diagram.append("    classDef topLevel fill:#e6f3ff,stroke:#2980b9,stroke-width:2px")
        diagram.append("    classDef secondLevel fill:#f5f5f5,stroke:#34495e,stroke-width:1px")
        diagram.append("    classDef default fill:#ffffff,stroke:#7f8c8d,stroke-width:1px")
        
        sanitized_diagram_name = self.create_node_id("", self.folder_name)
        diagram.append(f"    subgraph {sanitized_diagram_name}")
        diagram.append(f"    class {sanitized_diagram_name} topLevel")
        
        for json_file in json_files:
            with open(json_file, 'r') as f:
                json_data = json.load(f)
                
            file_name = json_file.stem.replace('-', ' ').title()
            sanitized_file_name = self.create_node_id("", file_name)
            diagram.append(f"        subgraph {sanitized_file_name}")
            diagram.append(f"        class {sanitized_file_name} secondLevel")
            
            container_ids = self.process_containers(json_data, sanitized_file_name, diagram)
            self.add_relationships(json_data, container_ids, diagram)
            
            diagram.append("        end")
        
        diagram.append("    end")
        
        return "\n".join(diagram)

    def save_diagram(self, output_filename=None):
        """Generate and save the Mermaid diagram to a file"""
        try:
            diagram = self.generate_diagram()
            
            if output_filename is None:
                output_filename = f"{self.folder_name}_diagram.mmd"
            
            output_path = self.folder_path / output_filename
            
            with open(output_path, 'w') as f:
                f.write(diagram)
            
            print(f"Successfully created diagram: {output_path.name}")
            return diagram, output_path  # Return both the diagram content and the path
            
        except Exception as e:
            print(f"Error creating diagram: {e}")
            raise