# -*- coding: utf-8 -*-
"""
@Author  : yangkai
@Email   : 807440781@qq.com
@Project : Krun
@Module  : project_schema.py
@DateTime: 2025/2/2 13:38
"""
from typing import Optional

from pydantic import BaseModel, Field


class ProjectCreate(BaseModel):
    code: str = Field(example="KD001", description="项目代码")
    name: str = Field(example="机器人扭秧歌", description="项目名称")
    release: str = Field(example="0.0.1", description="项目版本")
    leader_id: Optional[int] = Field(example=1, description="项目所属负责人ID")
    description: Optional[str] = Field(example="这是一个项目的详细描述...")
    state: int = Field(example=2, description="项目状态(0:提测,1:删除)")

    def create_dict(self):
        return self.model_dump(exclude_unset=True)


class ProjectUpdate(BaseModel):
    id: int
    name: Optional[str] = None
    leader_id: Optional[int] = None
    release: Optional[str] = None
    description: Optional[str] = None
    state: Optional[int] = None
    updated_user: Optional[str] = None


class ProjectSelect(BaseModel):
    page_num: int = Field(default=1, ge=1, description="数据页码")
    page_size: int = Field(default=10, ge=10, description="数据数量")
    page_order: Optional[list] = Field(default=[], examples=["id"], description="数据排序")
    code: Optional[int] = None
    name: Optional[str] = None
    leader_id: Optional[int] = None
    release: Optional[str] = None
    state: Optional[int] = None
    created_user: Optional[str] = None
    updated_user: Optional[str] = None
    created_time: Optional[str] = None
    updated_time: Optional[str] = None
