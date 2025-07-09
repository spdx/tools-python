# Workflow

Official SPDX v3.0 serialization documentation and context file
are available at: <https://spdx.github.io/spdx-spec/v3.0/serializations/>

## Manually generate context file

Process to produce context file and a serialization example:

1. Run

    ```sh
    python spec-parser/main.py spdx-3-model/model parser_output
    ```

    - spdx-3-model (main; where v3.0.1 development happens)
    - spec-parser (main)

2. Convert the generated `parser_output/rdf/spdx-model.ttl` to a JSON-LD file
    using <https://frogcat.github.io/ttl2jsonld/demo/>.
3. Convert OWL to context using `owl_to_context.py`.
4. Place the generated `context.json` in `src/spdx_tools/spdx3/writer/json_ld/`.
5. To generate the JSON-LD from the test file, run:

    ```sh
    pyspdxtools3 -i  ./tests/spdx/data/SPDXJSONExample-v2.3.spdx.json -o example_with_context
    ```

## Known limitations

- Validation of enums does not work
- Additional keys seem to be ignored in validation
- Inherited properties aren't validated
