# -*- coding: utf-8 -*-
from vepforge.core.evidence import Evidence, EvidenceKind
from vepforge.verifier import ExitCodeVerifier, HashVerifier, HttpStatusVerifier


def test_exit_code():
    v = ExitCodeVerifier()
    ok = v.verify(Evidence(kind=EvidenceKind.EXIT_CODE, value=0, tool="t"))
    bad = v.verify(Evidence(kind=EvidenceKind.EXIT_CODE, value=1, tool="t"))
    assert ok.verified and not bad.verified


def test_hash():
    v = HashVerifier()
    e = Evidence(kind=EvidenceKind.HASH, value="a" * 64, tool="t")
    assert v.verify(e).verified


def test_http():
    v = HttpStatusVerifier()
    assert v.verify(Evidence(kind=EvidenceKind.HTTP_STATUS, value=200, tool="t")).verified
    assert not v.verify(Evidence(kind=EvidenceKind.HTTP_STATUS, value=404, tool="t")).verified
