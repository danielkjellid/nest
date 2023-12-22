from typing import Callable, TypedDict, TypeVar

import pytest
from django.db.models import Model

TSpec = TypeVar("TSpec", bound=TypedDict)
TModel = TypeVar("TModel", bound=Model)


def get_spec_for_instance(
    slug: str, default_spec: TSpec, request: pytest.FixtureRequest, marker: str
) -> TSpec:
    """
    Utility to modify the spec based on the default spec provided and the kwargs
    passed in the marker.
    """
    spec = default_spec.copy()

    if marker := request.node.get_closest_marker(marker):
        spec.update(marker.kwargs.get(slug, {}))

    return spec


def get_instance(
    slug: str,
    instances: dict[str, TModel],
    create_callback: Callable[[TSpec], TModel],
    get_spec_callback: Callable[[str], TSpec],
) -> TModel:
    """
    Utility to get an instance with provided spec.
    """
    if instance_ := instances.get(slug):
        return instance_

    spec = get_spec_callback(slug)
    instance_ = create_callback(spec)
    instances[slug] = instance_

    return instance_


def instance(
    create_callback: Callable[[TSpec], TModel],
    default_spec: TSpec,
    request: pytest.FixtureRequest,
    marker: str,
) -> TModel:
    """
    Utility to create a singleton instance.
    """
    spec = default_spec.copy()

    marker = request.node.get_closest_marker(marker)
    if marker:
        spec.update(marker.kwargs)

    return create_callback(spec)


def instances(
    request: pytest.FixtureRequest,
    markers: str,
    get_instance_callback: Callable[[str], TModel],
):
    """
    Utility to create a set of instances with their provided slug.
    """
    instances_: dict[str, TModel] = {}

    for marker in request.node.iter_markers(markers):
        assert not marker.args, "Only kwargs is accepted with this fixture"
        slugs = marker.kwargs

        for slug in slugs:
            instances_.update({slug: get_instance_callback(slug)})

    for name, spec in instances_.items():
        if name in request.node.fixturenames:
            request.node.funcargs.setdefault(name, spec)

    return instances_
