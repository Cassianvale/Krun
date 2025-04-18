# -*- coding: utf-8 -*-
"""
@Author  : yangkai
@Email   : 807440781@qq.com
@Project : Krun
@Module  : api_testcase_schema.py
@DateTime: 2025/3/28 15:42
"""
from typing import Optional, List, Dict, Set, Any

from pydantic import BaseModel, Field

from backend.enums.http_enum import HTTPMethod
from backend.enums.testcase_priority_enum import TestCasePriorityEnum


class ApiTestCaseCreate(BaseModel):
    url: str
    method: HTTPMethod
    headers: Optional[Dict[str, Any]] = None

    params: Optional[Dict[str, Any]] = None
    json_body: Optional[Dict[str, Any]] = None
    form_data: Optional[Dict[str, Any]] = None
    x_www_form_urlencoded: Optional[Dict[str, Any]] = None

    project_id: int
    module_id: Optional[int] = None
    env_id: int
    priority: TestCasePriorityEnum
    testcase_name: str
    testcase_tags: Optional[str] = None
    description: Optional[str] = None

    variables: Optional[Dict[str, Any]] = None
    created_user: str
    updated_user: Optional[str] = None

    def create_dict(
            self,
            *,
            exclude: Optional[Set[str]] = None,
            include: Optional[Set[str]] = None,
            exclude_unset: bool = False,
            exclude_none: bool = False,
    ):
        """
        model_dump 方法支持多个参数，可以灵活控制输出字典的内容：
        •  exclude：排除指定字段。
        •  include：只包含指定字段。
        •  exclude_unset：排除未设置的字段（即没有显式赋值的字段）。
        •  exclude_defaults：排除字段的默认值。
        •  exclude_none：排除值为 None 的字段。
        :return:
        """
        return self.model_dump(
            exclude=exclude,
            include=include,
            exclude_unset=exclude_unset,
            exclude_none=exclude_none
        )


class ApiTestCaseUpdate(BaseModel):
    url: Optional[str] = None
    method: Optional[HTTPMethod] = None
    headers: Optional[Dict[str, Any]] = None

    params: Optional[Dict[str, Any]] = None
    json_body: Optional[Dict[str, Any]] = None
    form_data: Optional[Dict[str, Any]] = None
    x_www_form_urlencoded: Optional[Dict[str, Any]] = None

    project_id: Optional[int] = None
    module_id: Optional[int] = None
    env_id: Optional[int] = None
    priority: Optional[TestCasePriorityEnum] = None
    testcase_name: Optional[str] = None
    testcase_tags: Optional[str] = None
    description: Optional[str] = None

    variables: Optional[Dict] = None
    updated_user: Optional[str] = None
