# ThoughtSpot TML Examples

## Basic examples 
If writing your own scripts using thoughtspot_tml, look to these two examples along with the README to understand basic functionality and workflows:

- *basic_input_output.py*: small sample functions showing the .load and .loads methods and the .dump and .dumps methods for going from TML files to library objects and back
- *common_attribute_changes.py*: small sample functions on the most common TML objects showing the properties that are typically changed when doing TML manipulation, and the syntax for how to access any other properties

## Complete workflow examples
- [Worksheet Namespace Remapping][eg-worksheet-remap-ns]
- 🚧 TODO 🚧 Worksheet GUID Remapping
- 🚧 TODO 🚧 Repoint a Table to a new Connection
- 🚧 TODO 🚧 Programmatically add a New Column to a Table
- 🚧 TODO 🚧 Programmatically add a New Column to a Worksheet
- 🚧 TODO 🚧 Programmatically add a New Visualization to a Liveboard

## Key Terms

| Abbrev. | Term                                            | Definition                                                                                     |
|  :---:  | :---                                            | :---                                                                                           |
| `GUID`  | __globally unique id__                          | *a unique identifier found on all* __ThoughtSpot__ *objects*                                   |
| `SDLC`  | __software development lifecycle__              | *the process of moving content between environments (DEV --> TEST --> PROD)*                   |
| `CDC`   | __change data capture__                         | *the process of identifying, capturing, and delivering changes in real-time to an environment* |
| `CI/CD` | __continuous integration, continuous delivery__ | *enabling a process of making multiple changes to a codebase simultaneously*                   |
| `fqn`   | __fully qualified name__                        | *the guid of an object in* __ThoughtSpot__                                                     |
|         | __namespacing__                                 | *a mechanism for isolating content within a single shared environment*                         |

[eg-worksheet-remap-ns]: worksheet-namespace-remapping/README.md
[eg-worksheet-remap-guid]: worksheet-guid-remapping/README.md
