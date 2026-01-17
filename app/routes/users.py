from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..auth import get_current_user, require_admin
from .. import models
from .. import crud, schemas
from ..db import get_db
from typing import List

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me")
def read_current_user(user: models.User = Depends(get_current_user)):
    return {
        "email": user.email,
        "role": user.role
    }


@router.get("/admin-only")
def admin_only(user: models.User = Depends(require_admin)):
    return {"message": "Welcome Admin"}

@router.put("/{user_id}/role")
def update_role(
    user_id: int,
    data: schemas.RoleUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    user = crud.update_user_role(db, user_id, data.role)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "Role updated", "role": user.role}
@router.get("/", response_model=List[dict])
def list_users(
    db: Session = Depends(get_db),
    user=Depends(require_admin)
):
    users = db.query(models.User).all()
    return [
        {
            "id": u.id,
            "email": u.email,
            "role": u.role
        }
        for u in users
    ]

@router.put("/{user_id}/role")
def update_user_role(
    user_id: int,
    data: schemas.RoleUpdate,
    db: Session = Depends(get_db),
    user=Depends(require_admin)
):
    updated_user = crud.update_user_role(db, user_id, data.role)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "id": updated_user.id,
        "email": updated_user.email,
        "role": updated_user.role
    }

@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin)
):
    # Optional safety check: prevent admin from deleting themselves
    if current_user.id == user_id:
        raise HTTPException(
            status_code=400,
            detail="Admin cannot delete their own account"
        )

    deleted_user = crud.delete_user(db, user_id)
    if not deleted_user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "message": "User deleted successfully",
        "deleted_user": {
            "id": deleted_user.id,
            "email": deleted_user.email,
            "role": deleted_user.role
        }
    }
