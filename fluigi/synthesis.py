from typing import List


def synthesize(
    input_files: List[str],
    outpath: str,
    technology: str,
    library_path: str,
    pre_load: List[str],
) -> None:
    raise NotImplementedError(
        "Need to implement end-to-end synthesis method that catches all the LFR synthesized devices"
    )
