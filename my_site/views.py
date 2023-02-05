import logging
import traceback
from typing import List

from django.shortcuts import get_object_or_404
from ninja import Router

from autopt import views as autopt
from my_site.schema import *
from spider.views import PtSpider
from toolbox import views as toolbox
from toolbox.schema import CommonResponse
from toolbox.views import FileSizeConvert

# Create your views here.
logger = logging.getLogger('ptools')
pt_spider = PtSpider()
router = Router(tags=['mysite'])


class MessageTemplate:
    """消息模板"""
    status_message_template = "{} 等级：{} 魔力：{} 时魔：{} 积分：{} 分享率：{} " \
                              "做种量：{} 上传量：{} 下载量：{} 上传数：{} 下载数：{} " \
                              "邀请：{} H&R：{}\n"


@router.get('/mysite', response=List[MySiteSchemaOut], description='我的站点-列表')
def get_mysite_list(request):
    return MySite.objects.order_by('id')


@router.get('/mysite/{int:mysite_id}', response=MySiteSchemaOut, description='我的站点-单个')
def get_mysite(request, mysite_id):
    return get_object_or_404(MySite, id=mysite_id)


@router.post('/mysite', description='我的站点-添加')
def add_mysite(request, my_site_params: MySiteSchemaIn):
    my_site_params.schema().pop('id')
    logger.info(my_site_params)
    my_site = MySite.objects.create(**my_site_params.dict())
    return my_site


@router.put('/mysite/{int:my_site_id}', description='我的站点-更新')
def edit_mysite(request, my_site_id: int, my_site_params: MySiteSchemaIn):
    try:
        my_site_res = MySite.objects.filter(id=my_site_id).aupdate(**my_site_params.dict())
        logger.info(my_site_res)
        return CommonResponse.success(
            msg=f'{my_site_res} 信息更新成功！'
        )
    except:
        return CommonResponse.error(
            msg=f'{my_site_params.nickname} 参数有误，请确认后重试！'
        )


@router.delete('/mysite/{int:mysite_id}', description='我的站点-删除')
def remove_mysite(request, mysite_id):
    count = SiteStatus.objects.filter(id=mysite_id).delete()
    return f'remove/{count}'


@router.get('/status', response=List[SiteStatusSchemaOut], description='每日状态-列表')
def get_status_list(request):
    return SiteStatus.objects.order_by('id').select_related('site')


@router.get('/status/{int:status_id}', response=SiteStatusSchemaOut, description='每日状态-单个')
def get_status(request, status_id):
    return get_object_or_404(SiteStatus, id=status_id)


@router.get('/signin', response=List[SignInSchemaOut], description='每日签到-列表')
def get_signin_list(request):
    return SignIn.objects.order_by('id').select_related('site')


@router.get('/signin/{int:signin_id}', response=SignInSchemaOut, description='每日状态-单个')
def get_signin(request, signin_id):
    return get_object_or_404(SignIn, id=signin_id)


def today_data():
    """获取当日相较于前一日上传下载数据增长量"""
    today_site_status_list = SiteStatus.objects.filter(created_at__date=datetime.today())
    # yesterday_site_status_list = SiteStatus.objects.filter(
    #     created_at__day=datetime.today() - timedelta(days=1))
    increase_list = []
    total_upload = 0
    total_download = 0
    for site_state in today_site_status_list:
        my_site = site_state.site
        yesterday_site_status_list = SiteStatus.objects.filter(site=my_site)
        if len(yesterday_site_status_list) >= 2:
            yesterday_site_status = SiteStatus.objects.filter(site=my_site).order_by('-created_at')[1]
            uploaded_increase = site_state.uploaded - yesterday_site_status.uploaded
            downloaded_increase = site_state.downloaded - yesterday_site_status.downloaded
        else:
            uploaded_increase = site_state.uploaded
            downloaded_increase = site_state.downloaded
        if uploaded_increase + downloaded_increase <= 0:
            continue
        total_upload += uploaded_increase
        total_download += downloaded_increase
        increase_list.append(f'\n\n- 站点：{my_site.site.name}'
                             f'\n\t\t上传：{FileSizeConvert.parse_2_file_size(uploaded_increase)}'
                             f'\n\t\t下载：{FileSizeConvert.parse_2_file_size(downloaded_increase)}')
    # incremental = {
    #     '总上传': FileSizeConvert.parse_2_file_size(total_upload),
    #     '总下载': FileSizeConvert.parse_2_file_size(total_download),
    #     '说明': '数据均相较于本站今日之前最近的一条数据，可能并非昨日',
    #     '数据列表': increase_list,
    # }
    incremental = f'#### 总上传：{FileSizeConvert.parse_2_file_size(total_upload)}\n' \
                  f'#### 总下载：{FileSizeConvert.parse_2_file_size(total_download)}\n' \
                  f'> 说明: 数据均相较于本站今日之前最近的一条数据，可能并非昨日\n' \
                  f'#### 数据列表：{"".join(increase_list)}'
    logger.info(incremental)
    # todo
    # self.send_text(title='通知：今日数据', message=incremental)


@router.post('/import', response=SignInSchemaOut, description='PTPP备份导入')
def import_from_ptpp(request, data: ImportSchema):
    res = toolbox.parse_ptpp_cookies(data)
    if res.code == 0:
        cookies = res.data
        # logger.info(cookies)
    else:
        return res.to_dict()
    message_list = []
    for data in cookies:
        try:
            # logger.info(data)
            res = toolbox.get_uid_and_passkey(data)
            msg = res.msg
            logger.info(msg)
            if res.code == 0:
                message_list.append({
                    'msg': msg,
                    'tag': 'success'
                })
            else:
                message_list.append({
                    'msg': msg,
                    'tag': 'error'
                })
        except Exception as e:
            message = '{} 站点导入失败！{}  \n'.format(data.get('domain'), str(e))
            message_list.append({
                'msg': message,
                'tag': 'warning'
            })
            # raise
        logger.info(message_list)
    return message_list


@router.get('/status/{site_id}', response=CommonResponse, description='站点数据展示')
def site_data_api(request, site_id: int):
    """站点数据(柱状图)"""
    # my_site_id = request.GET.get('id')
    logger.info(f'ID值：{type(site_id)}')
    if int(site_id) == 0:
        my_site_list = MySite.objects.all()
        diff_list = []
        # 提取日期
        date_list = set([
            status.created_at.date().strftime('%Y-%m-%d') for status in SiteStatus.objects.all()
        ])
        date_list = list(date_list)
        date_list.sort()
        # print(f'日期列表：{date_list}')
        print(f'日期数量：{len(date_list)}')

        for my_site in my_site_list:
            # 每个站点获取自己站点的所有信息
            site_status_list = my_site.sitestatus_set.order_by('created_at').all()
            # print(f'站点数据条数：{len(site_status_list)}')
            info_list = [
                {
                    'uploaded': site_info.uploaded,
                    'date': site_info.created_at.date().strftime('%Y-%m-%d')
                } for site_info in site_status_list
            ]
            # print(f'提取完后站点数据条数：{len(info_list)}')

            # 生成本站点的增量列表，并标注时间
            '''
            site_info_list = [{
                'name': my_site.site.name,
                'type': 'bar',
                'stack': info_list[index + 1]['date'],
                'value': info_list[index + 1]['uploaded'] - info['uploaded'] if index < len(
                    info_list) - 1 else 0,
                'date': info['date']
            } for (index, info) in enumerate(info_list) if index < len(info_list) - 1]
            '''
            diff_info_list = {
                info['date']: info['uploaded'] - info_list[index - 1]['uploaded'] if
                info['uploaded'] - info_list[index - 1]['uploaded'] > 0 else 0 for
                (index, info) in enumerate(info_list) if 0 < index < len(info_list)

            }
            # print(f'处理完后站点数据条数：{len(info_list)}')
            for date in date_list:
                if not diff_info_list.get(date):
                    diff_info_list[date] = 0
            # print(diff_info_list)
            # print(len(diff_info_list))
            diff_info_list = sorted(diff_info_list.items(), key=lambda x: x[0])
            diff_list.append({
                'name': my_site.site.name,
                'type': 'bar',
                'large': 'true',
                'stack': 'increment',
                'data': [value[1] if value[1] > 0 else 0 for value in diff_info_list]
            })
        return CommonResponse.success(
            data={'date_list': date_list, 'diff': diff_list}
        )

    logger.info(f'前端传来的站点ID：{site_id}')
    my_site = MySite.objects.filter(id=site_id).first()
    if not my_site:
        return CommonResponse.error(
            msg='访问出错咯！'
        )
    site_info_list = my_site.sitestatus_set.order_by('created_at').all()
    # logger.info(site_info_list)
    site_status_list = []
    site = {
        'id': my_site.id,
        'name': my_site.site.name,
        'icon': my_site.site.logo,
        'url': my_site.site.url,
        'class': my_site.my_level,
        'last_active': datetime.strftime(my_site.updated_at, '%Y/%m/%d %H:%M:%S'),
    }
    for site_info in site_info_list:
        my_site_status = {
            'uploaded': site_info.uploaded,
            'downloaded': site_info.downloaded,
            'ratio': 0 if site_info.ratio == float('inf') else site_info.ratio,
            'seedingSize': site_info.seed_vol,
            'sp': site_info.my_sp,
            'sp_hour': site_info.sp_hour,
            'bonus': site_info.my_bonus,
            'seeding': site_info.seed,
            'leeching': site_info.leech,
            'invitation': site_info.invitation,
            'info_date': site_info.created_at.date()
        }
        site_status_list.append(my_site_status)
    logger.info(site)
    # logger.info(site_status_list)
    return CommonResponse.success(
        data={'site': site, 'site_status_list': site_status_list}
    )


@router.get('/sign/do/{site_id}', response=CommonResponse, description='站点签到')
def sign_in_api(request, site_id: int):
    try:
        if int(site_id) == 0:
            autopt.auto_sign_in()
            return CommonResponse.success(
                msg='签到指令已发送，请注意查收推送消息！'
            )
        my_site = MySite.objects.filter(id=site_id).first()
        sign_state = pt_spider.sign_in(my_site)
        logger.info(sign_state.to_dict())
        # if sign_state.code == StatusCodeEnum.OK.code:
        #     return JsonResponse(data=CommonResponse.success(
        #         msg=sign_state.msg
        #     ).to_dict(), safe=False)
        return sign_state.to_dict()
    except Exception as e:
        logger.error(f'签到失败：{e}')
        logger.error(traceback.format_exc(limit=3))
        return CommonResponse.error(msg=f'签到失败：{e}')


@router.get('/status/do/{site_id}', response=CommonResponse, description='刷新站点数据')
def update_site_api(request, site_id: int):
    try:
        if int(site_id) == 0:
            autopt.auto_get_status()
            return CommonResponse.success(
                msg='更新指令已发送，请注意查收推送消息！'
            )
        my_site = MySite.objects.filter(id=site_id).first()
        res_status = pt_spider.send_status_request(my_site)
        message_template = MessageTemplate.status_message_template
        if res_status.code == 0:
            res = pt_spider.parse_status_html(my_site, res_status.data)
            logger.info(f'{my_site.site.name}数据获取结果：{res.to_dict()}')
            if res.code != 0:
                return res.to_dict()
            status = res.data[0]
            if isinstance(status, SiteStatus):
                message = message_template.format(
                    my_site.site.name,
                    my_site.my_level,
                    status.my_bonus,
                    status.bonus_hour,
                    status.my_score,
                    status.ratio,
                    FileSizeConvert.parse_2_file_size(status.seed_volume),
                    FileSizeConvert.parse_2_file_size(status.uploaded),
                    FileSizeConvert.parse_2_file_size(status.downloaded),
                    status.seed,
                    status.leech,
                    status.invitation,
                    my_site.my_hr
                )
                return CommonResponse.success(msg=message)
            return CommonResponse.error(msg=res.msg)
        else:
            return res_status.to_dict()
    except Exception as e:
        logger.error(f'数据更新失败：{e}')
        logger.error(traceback.format_exc(limit=3))
        return CommonResponse.error(msg=f'数据更新失败：{e}')


@router.get('/sign/show/{site_id}', response=CommonResponse, description='站点签到信息')
def show_sign_api(request, site_id: int):
    try:
        my_site = MySite.objects.filter(id=site_id).first()
        site = get_object_or_404(WebSite, my_site.site)
        sign_in_list = my_site.signin_set.order_by('-pk')[:15]
        sign_in_list = [
            {'created_at': sign_in.created_at.strftime('%Y-%m-%d %H:%M:%S'), 'sign_in_info': sign_in.sign_in_info}
            for sign_in in sign_in_list]
        site_info = {
            'id': site.id,
            'name': site.name,
            'icon': site.logo,
            'url': site.url,
            'last_active': datetime.strftime(my_site.updated_at, '%Y年%m月%d日%H:%M:%S'),
        }
        return CommonResponse.success(data={'site': site_info, 'sign_in_list': sign_in_list})
    except Exception as e:
        logger.error(f'签到历史数据获取失败：{e}')
        logger.error(traceback.format_exc(limit=3))
        return CommonResponse.error(
            msg=f'签到历史数据获取失败：{e}'
        )


@router.get('/sign/show/{site_id}/{sort}', response=CommonResponse, description='站点排序')
def site_sort_api(request, site_id: int, sort: int):
    try:
        my_site = MySite.objects.filter(id=site_id).first()
        my_site.sort_id += int(sort)

        if int(my_site.sort_id) <= 0:
            my_site.sort_id = 0
            my_site.save()
            return CommonResponse.success(msg='排序已经最靠前啦，不要再点了！')
        my_site.save()
        return CommonResponse.success(msg='排序成功！')
    except Exception as e:
        logger.error(f'数据更新失败：{e}')
        logger.error(traceback.format_exc(limit=3))
        return CommonResponse.error(msg=f'数据更新失败：{e}')
