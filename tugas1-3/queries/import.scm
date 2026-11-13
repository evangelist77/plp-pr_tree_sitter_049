(import_statement
  name: [
    (dotted_name) @modul
    (aliased_import name: (dotted_name) @modul)
  ])

(import_from_statement
  module_name: [(dotted_name) (relative_import)] @modul)
