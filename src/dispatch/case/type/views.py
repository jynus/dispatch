from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from dispatch.database.core import get_db
from dispatch.database.service import common_parameters, search_filter_sort_paginate
from dispatch.auth.permissions import SensitiveProjectActionPermission, PermissionsDependency
from dispatch.models import PrimaryKey

from .models import CaseTypeCreate, CaseTypePagination, CaseTypeRead, CaseTypeUpdate
from .service import create, get, update


router = APIRouter()


@router.get("", response_model=CaseTypePagination, tags=["case_types"])
def get_case_types(*, common: dict = Depends(common_parameters)):
    """Returns all case types."""
    return search_filter_sort_paginate(model="CaseType", **common)


@router.post(
    "",
    response_model=CaseTypeRead,
    dependencies=[Depends(PermissionsDependency([SensitiveProjectActionPermission]))],
)
def create_case_type(
    *,
    db_session: Session = Depends(get_db),
    case_type_in: CaseTypeCreate,
):
    """Creates a new case type."""
    case_type = create(db_session=db_session, case_type_in=case_type_in)
    return case_type


@router.put(
    "/{case_type_id}",
    response_model=CaseTypeRead,
    dependencies=[Depends(PermissionsDependency([SensitiveProjectActionPermission]))],
)
def update_case_type(
    *,
    db_session: Session = Depends(get_db),
    case_type_id: PrimaryKey,
    case_type_in: CaseTypeUpdate,
):
    """Updates an existing case type."""
    case_type = get(db_session=db_session, case_type_id=case_type_id)
    if not case_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "A case type with this id does not exist."}],
        )

    case_type = update(db_session=db_session, case_type=case_type, case_type_in=case_type_in)
    return case_type


@router.get("/{case_type_id}", response_model=CaseTypeRead)
def get_case_type(*, db_session: Session = Depends(get_db), case_type_id: PrimaryKey):
    """Gets a case type."""
    case_type = get(db_session=db_session, case_type_id=case_type_id)
    if not case_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "A case type with this id does not exist."}],
        )
    return case_type
