from __future__ import annotations

from lamindb.models import ParamManager, Run, Transform


def __init__(run: Run, *args, **kwargs):
    run.params = ParamManager(run)  # type: ignore
    if len(args) == len(run._meta.concrete_fields):
        super(Run, run).__init__(*args, **kwargs)
        return None
    # now we proceed with the user-facing constructor
    if len(args) > 1:
        raise ValueError("Only one non-keyword arg allowed: transform")
    transform: Transform = None
    if "transform" in kwargs or len(args) == 1:
        transform = kwargs.pop("transform") if len(args) == 0 else args[0]
    reference: str | None = kwargs.pop("reference") if "reference" in kwargs else None
    reference_type: str | None = (
        kwargs.pop("reference_type") if "reference_type" in kwargs else None
    )
    initiated_by_run: Run | None = kwargs.pop("initiated_by_run", None)
    if transform is None:
        raise TypeError("Pass transform parameter")
    if transform._state.adding:
        raise ValueError("Please save transform record before creating a run")

    super(Run, run).__init__(  # type: ignore
        transform=transform,
        reference=reference,
        initiated_by_run=initiated_by_run,
        reference_type=reference_type,
    )


def delete_run_artifacts(run: Run) -> None:
    environment = None
    if run.environment is not None:
        environment = run.environment
        run.environment = None
    report = None
    if run.report is not None:
        report = run.report
        run.report = None
    if environment is not None or report is not None:
        run.save()
    if environment is not None:
        # only delete if there are no other runs attached to this environment
        if environment._environment_of.count() == 0:
            environment.delete(permanent=True)
    if report is not None:
        report.delete(permanent=True)


def delete(self) -> None:
    delete_run_artifacts(self)
    super(Run, self).delete()


Run.__init__ = __init__  # type: ignore
Run.delete = delete  # type: ignore
