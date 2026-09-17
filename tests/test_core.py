# -*- coding: utf-8 -*-
import hashlib

from vepforge.core.task import Task, TaskStatus
from vepforge.core.trajectory import Trajectory, StepRole
from vepforge.core.artifact import Artifact, ArtifactKind
from vepforge.core.evidence import Evidence, EvidenceKind
from vepforge.core.experience import Experience


def test_task_lifecycle():
    t = Task(goal="do something")
    t.mark(TaskStatus.RUNNING)
    t.mark(TaskStatus.SUCCEEDED)
    assert t.status == TaskStatus.SUCCEEDED
    assert t.started_at is not None and t.finished_at is not None


def test_trajectory_roundtrip():
    tr = Trajectory(task_id="t1")
    tr.add(StepRole.THOUGHT, {"x": 1})
    tr.add(StepRole.EVIDENCE, {"e": 2})
    d = tr.to_dict()
    tr2 = Trajectory.from_dict(d)
    assert len(tr2) == 2


def test_artifact_hash():
    a = Artifact(name="x", kind=ArtifactKind.CODE, content="hello")
    assert a.sha256 == hashlib.sha256(b"hello").hexdigest()


def test_experience_roundtrip():
    t = Task(goal="g")
    exp = Experience(task=t, trajectory=Trajectory(task_id=t.task_id))
    exp.add_artifact(Artifact(name="a", kind=ArtifactKind.TEXT, content="c"))
    exp.add_evidence(Evidence(kind=EvidenceKind.EXIT_CODE, value=0, tool="t"))
    d = exp.to_dict()
    exp2 = Experience.from_dict(d)
    assert len(exp2.artifacts) == 1 and len(exp2.evidences) == 1
