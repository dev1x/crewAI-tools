# MermaidDiagramGenerator
A Python utility that generates Mermaid diagrams from JSON configuration files. This tool automatically creates hierarchical flowcharts representing system architectures, with support for nested containers, properties, and relationships between components, dependencies, and more.

## Description
MermaidDiagramGenerator is designed to convert JSON-structured system configurations into visual Mermaid diagrams. It supports:

- Hierarchical visualization of system components
- Automatic node ID generation and sanitization
- Property mapping with nested structures
- Relationship definitions between components
- Custom styling for different hierarchy levels
- Multiple JSON file processing in a single diagram

## Installation
To start using the MermaidDiagramGenerator, you need to install the crewai_tools package. Execute the following command in your terminal:

```bash
pip install 'crewai[tools]'
```

## Example
### Example with your CrewAI agent
Remember to import the `MermaidDiagramGenerator` tool from `crewai_tools` and create an instance of it.

```python
from crewai_tools import MermaidDiagramGenerator

# Create the tool
mermaid_tool = MermaidDiagramGenerator()

# Create an agent with the tool
agent = Agent(
    ...
    tools=[mermaid_tool]
)
```

### Example with Arguments and Methods
Specify custom folder path and generate diagram for specific JSON files:

  ```python
  from crewai_tools import MermaidDiagramGenerator
  from pathlib import Path

  # Initialize with custom folder path
  generator = MermaidDiagramGenerator(folder_path="path/to/json/files")

  # Generate diagram for specific JSON files
  json_files = [
      Path("architecture.json"),
      Path("dependencies.json")
  ]
  diagram = generator.generate_diagram(json_files=json_files)

  # Save diagram with custom filename
  generator.save_diagram(output_filename="system_architecture.mmd")
  ```


## Arguments
### MermaidDiagramGenerator Class
#### Constructor Arguments
- `folder_path` (optional): Path to the folder containing JSON files. Defaults to the script's directory.

#### Methods

`save_diagram(output_filename=None)`
- `output_filename` (optional): Name of the output Mermaid diagram file. Defaults to `{folder_name}_diagram.mmd`

`generate_diagram(json_files=None)`
- `json_files` (optional): List of JSON files to process. Defaults to all JSON files in the specified folder.