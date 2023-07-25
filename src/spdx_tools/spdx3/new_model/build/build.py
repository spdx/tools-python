# SPDX-License-Identifier: Apache-2.0
#
# This file was auto-generated by dev/gen_python_model_from_spec.py
# Do not manually edit!

from ..core import CreationInfo, DictionaryEntry, Element, ExternalIdentifier, ExternalReference, Hash, IntegrityMethod
from beartype.typing import List, Optional
from dataclasses import field
from datetime import datetime
from spdx_tools.common.typing.type_checks import check_types_and_set_values

from spdx_tools.common.typing.dataclass_with_properties import dataclass_with_properties


@dataclass_with_properties
class Build(Element):
    """
    A build is a representation of the process in which a piece of software or artifact is built. It encapsulates
    information related to a build process and provides an element from which relationships can be created to describe
    the build's inputs, outputs, and related entities (e.g. builders, identities, etc.).

    Definitions of "BuildType", "ConfigSource", "Parameters" and "Environment" follow those defined in [SLSA
    provenance](https://slsa.dev/provenance/v0.2).

    ExternalIdentifier of type "urlScheme" may be used to identify build logs. In this case, the comment of the
    ExternalIdentifier should be "LogReference".

    Note that buildStart and buildEnd are optional, and may be omitted to simplify creating reproducible builds.
    """
    build_type: str
    """
    A buildType is a URI expressing the toolchain, platform, or infrastructure that the build was invoked on. For
    example, if the build was invoked on GitHub's CI platform using github actions, the buildType can be expressed as
    `https://github.com/actions`. In contrast, if the build was invoked on a local machine, the buildType can be
    expressed as `file://username@host/path/to/build`.
    """
    build_id: Optional[str] = None
    """
    A buildId is a locally unique identifier to identify a unique instance of a build. This identifier differs based on
    build toolchain, platform, or naming convention used by an organization or standard.
    """
    config_source_entrypoint: List[str] = field(default_factory=list)
    """
    A build entrypoint is the invoked executable of a build which always runs when the build is triggered. For example,
    when a build is triggered by running a shell script, the entrypoint is `script.sh`. In terms of a declared build,
    the entrypoint is the position in a configuration file or a build declaration which is always run when the build is
    triggered. For example, in the following configuration file, the entrypoint of the build is `publish`.

    ```
    name: Publish packages to PyPI

    on:
    create:
    tags: "*"

    jobs:
    publish:
    runs-on: ubuntu-latest
    if: startsWith(github.ref, 'refs/tags/')
    steps:

    ...
    ```
    """
    config_source_uri: List[str] = field(default_factory=list)
    """
    If a build configuration exists for the toolchain or platform performing the build, the configSourceUri of a build
    is the URI of that build configuration. For example, a build triggered by a GitHub action is defined by a build
    configuration YAML file. In this case, the configSourceUri is the URL of that YAML file. m
    """
    config_source_digest: List[Hash] = field(default_factory=list)
    """
    configSourceDigest is the checksum of the build configuration file used by a builder to execute a build. This
    Property uses the Core model's [Hash](../../Core/Classes/Hash.md) class.
    """
    parameters: List[DictionaryEntry] = field(default_factory=list)
    """
    parameters is a key-value map of all build parameters and their values that were provided to the builder for a build
    instance. This is different from the [environment](environment.md) property in that the keys and values are provided
    as command line arguments or a configuration file to the builder.
    """
    build_start_time: Optional[datetime] = None
    """
    buildStartTime is the time at which a build is triggered. The builder typically records this value.
    """
    build_end_time: Optional[datetime] = None
    """
    buildEndTime describes the time at which a build stops or finishes. This value is typically recorded by the builder.
    """
    environment: List[DictionaryEntry] = field(default_factory=list)
    """
    environment is a map of environment variables and values that are set during a build session. This is different from
    the [parameters](parameters.md) property in that it describes the environment variables set before a build is
    invoked rather than the variables provided to the builder.
    """

    def __init__(
        self,
        spdx_id: str,
        creation_info: CreationInfo,
        build_type: str,
        name: Optional[str] = None,
        summary: Optional[str] = None,
        description: Optional[str] = None,
        comment: Optional[str] = None,
        verified_using: List[IntegrityMethod] = None,
        external_reference: List[ExternalReference] = None,
        external_identifier: List[ExternalIdentifier] = None,
        extension: Optional[str] = None,
        build_id: Optional[str] = None,
        config_source_entrypoint: List[str] = None,
        config_source_uri: List[str] = None,
        config_source_digest: List[Hash] = None,
        parameters: List[DictionaryEntry] = None,
        build_start_time: Optional[datetime] = None,
        build_end_time: Optional[datetime] = None,
        environment: List[DictionaryEntry] = None,
    ):
        verified_using = [] if verified_using is None else verified_using
        external_reference = [] if external_reference is None else external_reference
        external_identifier = [] if external_identifier is None else external_identifier
        config_source_entrypoint = [] if config_source_entrypoint is None else config_source_entrypoint
        config_source_uri = [] if config_source_uri is None else config_source_uri
        config_source_digest = [] if config_source_digest is None else config_source_digest
        parameters = [] if parameters is None else parameters
        environment = [] if environment is None else environment
        check_types_and_set_values(self, locals())
