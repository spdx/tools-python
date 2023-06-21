### Workflow

Process to produce context file and a serialization example:

1. Run 
```
spec-parser --gen-md --gen-refs --gen-rdf ../spdx-3-model/model
```
- spdx-3-model (commit: 6cb4316, last commit where spec-parser is able to run) <br>
- spec-parser (main with commits from PR 44, 45)

2. Convert the generated `spec-parser/md_generated/model.ttl` to a json-ld file using https://frogcat.github.io/ttl2jsonld/demo/.
3. Convert owl to context using `convert_spdx_owl_to_jsonld_context("SPDX_OWL.json")`.
4. Place the generated `context.json` in `spdx_tools/spdx3/writer/jsonld/`.
5. To generate the jsonld from the testfile run
```
pyspdxtools3 -i  ./tests/spdx/data/SPDXJSONExample-v2.3.spdx.json -o example_with_context
```


### Manually


### Known limitations
- Validation of enums does not work
- Additional keys seem to be ignored in validation
- inherited properties aren't validated
