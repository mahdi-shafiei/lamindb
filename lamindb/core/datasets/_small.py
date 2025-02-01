from __future__ import annotations

from typing import Any, Literal

import anndata as ad
import numpy as np
import pandas as pd


def small_dataset1(
    format: Literal["df", "anndata"],
    with_typo: bool = False,
) -> tuple[pd.DataFrame, dict[str, Any]] | ad.AnnData:
    # define the data in the dataset
    # it's a mix of numerical measurements and observation-level metadata
    ifng = "IFNJ" if with_typo else "IFNG"
    dataset_dict = {
        "CD8A": [1, 2, 3],
        "CD4": [3, 4, 5],
        "CD14": [5, 6, 7],
        "cell_medium": ["DMSO", ifng, "DMSO"],
        "sample_note": ["was ok", "looks naah", "pretty! 🤩"],
        "cell_type_by_expert": ["B cell", "T cell", "T cell"],
        "cell_type_by_model": ["B cell", "T cell", "T cell"],
    }
    # define the dataset-level metadata
    metadata = {
        "temperature": 21.6,
        "study": "Candidate marker study 1",
        "date_of_study": "2024-12-01",
        "study_note": "We had a great time performing this study and the results look compelling.",
    }
    # the dataset as DataFrame
    dataset_df = pd.DataFrame(dataset_dict, index=["sample1", "sample2", "sample3"])
    if format == "df":
        return dataset_df, metadata
    else:
        dataset_ad = ad.AnnData(
            dataset_df.iloc[:, :3], obs=dataset_df.iloc[:, 3:], uns=metadata
        )
        return dataset_ad


def small_dataset2(
    format: Literal["df", "anndata"],
) -> tuple[pd.DataFrame, dict[str, Any]] | ad.AnnData:
    dataset_dict = {
        "CD8A": [2, 3, 3],
        "CD4": [3, 4, 5],
        "CD38": [4, 2, 3],
        "cell_medium": ["DMSO", "IFNG", "IFNG"],
        "cell_type_by_model": ["B cell", "T cell", "T cell"],
    }
    metadata = {
        "temperature": 22.6,
        "study": "Candidate marker study 2",
        "date_of_study": "2025-02-13",
    }
    dataset_df = pd.DataFrame(
        dataset_dict,
        index=["sample4", "sample5", "sample6"],
    )
    ad.AnnData(
        dataset_df[["CD8A", "CD4", "CD38"]],
        obs=dataset_df[["cell_medium", "cell_type_by_model"]],
    )
    if format == "df":
        return dataset_df, metadata
    else:
        dataset_ad = ad.AnnData(
            dataset_df.iloc[:, :3], obs=dataset_df.iloc[:, 3:], uns=metadata
        )
        return dataset_ad


def small_dataset3_cellxgene(
    otype: Literal["DataFrame", "AnnData"] = "AnnData",
) -> tuple[pd.DataFrame, dict[str, Any]] | ad.AnnData:
    # TODO: consider other ids for other organisms
    # "ENSMUSG00002076988"
    var_ids = ["invalid_ensembl_id", "ENSG00000000419", "ENSG00000139618"]
    dataset_dict = {
        var_ids[0]: [2, 3, 3],
        var_ids[1]: [3, 4, 5],
        var_ids[2]: [4, 2, 3],
        "disease_ontology_term_id": ["MONDO:0004975", "MONDO:0004980", "MONDO:0004980"],
        "organism": ["human", "human", "human"],
        "sex": ["female", "male", "unknown"],
        "tissue": ["lungg", "lungg", "heart"],
        "donor": ["-1", "1", "2"],
    }
    dataset_df = pd.DataFrame(
        dataset_dict,
        index=["barcode1", "barcode2", "barcode3"],
    )
    dataset_df["tissue"] = dataset_df["tissue"].astype("category")
    ad.AnnData(
        dataset_df[var_ids],
        obs=dataset_df[[key for key in dataset_dict if key not in var_ids]],
    )
    if otype == "DataFrame":
        return dataset_df
    else:
        dataset_ad = ad.AnnData(dataset_df.iloc[:, :3], obs=dataset_df.iloc[:, 3:])
        return dataset_ad


def anndata_with_obs() -> ad.AnnData:
    """Create a mini anndata with cell_type, disease and tissue."""
    import anndata as ad
    import bionty.base as bionty_base

    celltypes = ["T cell", "hematopoietic stem cell", "hepatocyte", "my new cell type"]
    celltype_ids = ["CL:0000084", "CL:0000037", "CL:0000182", ""]
    diseases = [
        "chronic kidney disease",
        "liver lymphoma",
        "cardiac ventricle disorder",
        "Alzheimer disease",
    ]
    tissues = ["kidney", "liver", "heart", "brain"]
    df = pd.DataFrame()
    df["cell_type"] = celltypes * 10
    df["cell_type_id"] = celltype_ids * 10
    df["tissue"] = tissues * 10
    df["disease"] = diseases * 10
    df.index = "obs" + df.index.astype(str)

    adata = ad.AnnData(X=np.zeros(shape=(40, 100), dtype=np.float32), obs=df)
    adata.var.index = bionty_base.Gene().df().head(100)["ensembl_gene_id"].values

    return adata
