# -*- coding: utf-8 -*-
from vepforge.config import load_preset, PRESETS
from vepforge.templates import list_templates, get_template


def test_presets():
    for name in ("demo", "local-llm", "docker"):
        assert load_preset(name)["name"] == name


def test_templates():
    assert "data-aggregation" in list_templates()
    assert get_template("data-aggregation")["goal"]
