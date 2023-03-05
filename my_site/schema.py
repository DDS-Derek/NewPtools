from typing import Optional

from ninja import ModelSchema, Schema
from ninja.orm import create_schema

from my_site.models import *
from website.schema import WebSiteSchemaOut, UserLevelRuleSchemaOut


class MySiteSchemaOut(ModelSchema):
    """    站点基本信息及信息抓取规则    """

    # site: create_schema(WebSite, fields=['id', 'name'])
    updated: str

    class Config:
        model = MySite
        model_exclude = [
            'created_at',
            'passkey',
            'cookie',
            'user_agent'
        ]

    def resolve_updated(self, obj):
        return datetime.strftime(self.updated_at, '%Y年%m月%d日%H:%M:%S')


class MySiteDoSchemaIn(Schema):
    site_id: int


class MySiteSchemaEdit(ModelSchema):
    # site: create_schema(WebSite, fields=['id', 'name'])

    class Config:
        model = MySite
        model_exclude = ['created_at', 'updated_at']


class MySiteSortSchemaIn(ModelSchema):
    # site: create_schema(WebSite, fields=['id', 'name'])
    updated: str

    class Config:
        model = MySite
        model_exclude = ['id', 'sort_id']

    def resolve_updated(self, obj):
        return datetime.strftime(self.updated_at, '%Y年%m月%d日%H:%M:%S')


class SiteStatusSchemaOut(ModelSchema):
    """    站点基本信息及信息抓取规则    """
    site: create_schema(model=MySite, fields=['id'])
    updated: str

    class Config:
        model = SiteStatus
        model_exclude = ['created_at']

    def resolve_updated(self, obj):
        return datetime.strftime(self.updated_at, '%Y年%m月%d日%H:%M:%S')


class SiteStatusSchemaIn(ModelSchema):
    class Config:
        model = SiteStatus
        model_exclude = ['created_at', 'updated_at']


class SignInSchemaOut(ModelSchema):
    """    站点基本信息及信息抓取规则    """

    # site: create_schema(model=MySite, fields=['id'])
    updated: str

    class Config:
        model = SignIn
        model_exclude = ['created_at']

    def resolve_updated(self, obj):
        return datetime.strftime(self.updated_at, '%Y年%m月%d日%H:%M:%S')


class StatusSchema(Schema):
    """返回复杂数据"""
    my_site: MySiteSchemaOut
    site: WebSiteSchemaOut
    sign: Optional[SignInSchemaOut]
    status: Optional[SiteStatusSchemaOut]
    level: Optional[UserLevelRuleSchemaOut]
    next_level: Optional[UserLevelRuleSchemaOut]


class SignInSchemaIn(ModelSchema):
    class Config:
        model = SignIn
        model_exclude = ['created_at', 'updated_at']


class TorrentInfoSchemaOut(ModelSchema):
    class Config:
        model = SignIn
        model_exclude = ['created_at', 'updated_at']


class SignInQueryParamsSchemaIn(Schema):
    site_id: int
    page: int
    limit: int


class ImportSchema(Schema):
    info: str
    cookies: str
    # userdata: str
