from __future__ import absolute_import, unicode_literals

import gc
import logging
import os
import random
import subprocess
import time
import traceback
from datetime import datetime
from multiprocessing.dummy import Pool as ThreadPool
from typing import List

import requests
import toml
from celery.app import shared_task
from django.core.cache import cache
from django.db.models import Q
from lxml import etree

from auxiliary.base import DownloaderCategory
from auxiliary.celery import BaseTask
from download.models import Downloader
from my_site.models import MySite, TorrentInfo
from spider.views import PtSpider, toolbox
from toolbox import aliyundrive
from toolbox.schema import CommonResponse
from website.models import WebSite

# 引入日志
logger = logging.getLogger('ptools')
# 引入线程池
if os.getenv('MYSQL_CONNECTION'):
    cpu_count = os.cpu_count() if os.cpu_count() <= 16 else 16
else:
    cpu_count = os.cpu_count() if os.cpu_count() <= 8 else 8
pool = ThreadPool(cpu_count)
pt_spider = PtSpider()
notice = toolbox.parse_toml("notice")
notice_category_enable = notice.get("notice_category_enable", {})


@shared_task
def auto_reload_supervisor():
    """
    重启所有进程
    :return:
    """
    subprocess.run(["supervisorctl", "reload"])


@shared_task(bind=True, base=BaseTask)
def auto_sign_in(self):
    """执行签到"""
    start = time.time()

    logger.info('开始执行签到任务')

    aliyundrive_params = toolbox.parse_toml('aliyundrive')
    if len(aliyundrive_params) > 0:
        try:
            logger.info('检测到阿里云参数，开始签到阿里云盘')
            aliyundrive_sign_in_list = cache.get(f"aliyundrive_sign_in_list", [])
            refresh_token_list = aliyundrive_params.get('refresh_token')
            if len(refresh_token_list) == len(aliyundrive_sign_in_list):
                logger.info('阿里云盘签到任务已完成')
            else:
                welfare = aliyundrive_params.get('reward', True)
                result = aliyundrive.aliyundrive_sign_in(refresh_token_list=refresh_token_list, welfare=welfare)
                if notice_category_enable.get("aliyundrive_notice", True):
                    toolbox.send_text(title='阿里云签到', message=result)
        except Exception as e:
            msg = f'阿里云签到失败！{e}'
            logger.error(msg)
            logger.error(traceback.format_exc(5))
            toolbox.send_text(title='阿里云签到', message=msg)
    t98 = toolbox.parse_toml('t98')
    if len(t98) > 0:
        try:
            logger.info('检测到98参数，开始签到')
            t98_sign_in_state = cache.get(f"t98_sign_in_state", False)
            if not t98_sign_in_state:
                res = toolbox.sht_sign(
                    host=t98.get('host'),
                    username=t98.get('username'),
                    password=t98.get('password'),
                    cookie=t98.get('cookie'),
                    user_agent=t98.get('user_agent'),
                )
                toolbox.send_text(title='98签到', message=res.msg)
        except Exception as e:
            msg = f'98签到失败！{e}'
            logger.error(msg)
            logger.error(traceback.format_exc(5))
            toolbox.send_text(title='98签到', message=msg)
    cnlang = toolbox.parse_toml('cnlang')
    if len(cnlang) > 0:
        try:
            logger.info('检测到cnlang参数，开始签到')
            cnlang_sign_state = cache.get(f"cnlang_sign_state", False)
            if not cnlang_sign_state:
                res = toolbox.cnlang_sign(
                    username=cnlang.get('username'),
                    cookie=cnlang.get('cookie'),
                    host=cnlang.get('host', 'cnlang.org'),
                    user_agent=cnlang.get('user_agent',
                                          'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.62'),
                )
                toolbox.send_text(title='cnlang签到', message=res.msg)
        except Exception as e:
            msg = f'cnlang签到失败！{e}'
            logger.error(msg)
            logger.error(traceback.format_exc(5))
            toolbox.send_text(title='cnlang签到', message=msg)
    ssdforum = toolbox.parse_toml('ssdforum')
    if ssdforum is not None:
        try:
            logger.info('检测到SSDForum签到参数，开始签到')
            sign_ssd_forum_state = cache.get(f"sign_ssd_forum_state", False)
            if not sign_ssd_forum_state:
                res = toolbox.sign_ssd_forum(
                    cookie=ssdforum.get('cookie'),
                    user_agent=ssdforum.get('user_agent'),
                    todaysay=random.choice(ssdforum.get('todaysay', [
                        '今天好天气！',
                        '明天真期待',
                        '后天星期天？',
                        '周一bukaixin',
                        '周二ε＝ε＝ε＝(#>д<)ﾉ',
                        '周三交水电费啦',
                        'Hello World!',
                    ]))
                )
                toolbox.send_text(title='SSDForum签到', message=res.msg)
        except Exception as e:
            msg = f'SSDForum签到失败！{e}'
            logger.error(msg)
            logger.error(traceback.format_exc(5))
            toolbox.send_text(title='SSDForum签到', message=msg)
    logger.info('筛选需要签到的站点')
    message_list = []
    queryset = [
        my_site for my_site in MySite.objects.filter(sign_in=True) if
        WebSite.objects.get(id=my_site.site).sign_in and
        my_site.signin_set.filter(created_at__date__gte=datetime.today(), sign_in_today=True).count() == 0 and
        (datetime.now().hour >= 9 or WebSite.objects.get(id=my_site.site).url not in ['https://u2.dmhy.org/'])
    ]
    message = '站点：`U2` 早上九点之前不执行签到任务哦！ \n\n'
    logger.debug(message)
    message_list.append(message)
    if len(queryset) <= 0:
        message_list = ['已全部签到或无需签到！ \n\n']
        logger.info(message_list)
        # toolbox.send_text(title='通知：自动签到', message='\n'.join(message_list))
        return message_list
    # toolbox.send_text(title='通知：正在签到',
    #                   message=f'开始执行签到任务，共有{len(queryset)}站点需要签到，当前时间：{datetime.fromtimestamp(start)}')
    results = pool.map(pt_spider.sign_in, queryset)
    logger.info('执行签到任务')
    success_message = []
    failed_message = []
    for my_site, result in zip(queryset, results):
        logger.debug(f'自动签到：{my_site}, {result}')
        if result.code == 0:
            msg = f'✅ {my_site.nickname} 签到成功！{result.msg} \n'
            logger.debug(msg)
            success_message.append(msg)
        else:
            message = f'🆘 {my_site.nickname}签到失败：{result.msg} \n'
            failed_message.append(message)
            logger.error(message)
        # message_list.append(f'{my_site.nickname}: {result.msg}')
    end = time.time()
    message = f'当前时间：{datetime.fromtimestamp(end)},' \
              f'本次签到任务执行完毕，共有{len(queryset)}站点需要签到，成功签到{len(success_message)}个站点，' \
              f'失败{len(failed_message)}个站点，耗费时间：{round(end - start, 2)} \n'
    success_message.insert(0, message)
    message_list.append(message)
    if notice_category_enable.get('sign_in_error', True):
        message_list.extend(failed_message)
    message_list.append('*' * 20)
    if notice_category_enable.get('sign_in_success', True):
        message_list.extend(success_message)
    logger.info(f'签到记录{message}')
    logger.debug(f'失败记录{len(failed_message)}')
    logger.debug(f'成功记录{len(success_message)}')

    if notice_category_enable.get('sign_in_info', True):
        toolbox.send_text(title='通知：自动签到', message='\n'.join(message_list))
    # toolbox.send_text(title='通知：签到成功', message='\n'.join(success_message))
    # 释放内存
    gc.collect()
    return message_list


@shared_task(bind=True, base=BaseTask, time_limit=1200)
def auto_get_status(self):
    """
    更新个人数据
    """
    start = time.time()
    message_list = ['# 更新个人数据  \n\n']
    failed_message = []
    success_message = []
    websites = WebSite.objects.all()
    # queryset = MySite.objects.filter(
    #     get_info=True
    # ) if len(site_list) == 0 else MySite.objects.filter(get_info=True, id__in=site_list)
    queryset = [my_site for my_site in MySite.objects.filter(get_info=True) if
                websites.get(id=my_site.site).get_info]
    results = pool.map(pt_spider.send_status_request, queryset)
    for my_site, result in zip(queryset, results):
        if result.code == 0:
            # res = pt_spider.parse_status_html(my_site, result.data)
            logger.info('自动更新个人数据: {}, {}'.format(my_site.nickname, result))
            # if res.code == 0:
            status = result.data
            message = toolbox.generate_notify_content(notice, status)
            logger.info(f'{my_site.nickname} {message}')
            # toolbox.send_text(title='通知：个人数据更新', message=my_site.nickname + ' 信息更新成功！' + message)
            success_message.append(f'✅ {my_site.nickname} 信息更新成功！{message}  \n')
        else:
            print(result)
            message = f'🆘 {my_site.nickname} 信息更新失败！原因：{result.msg}'
            logger.warning(message)
            failed_message.append(f'{message}  \n')
            # toolbox.send_text(title='通知：个人数据更新', message=f'{my_site.nickname} 信息更新失败！原因：{message}')
    # 发送今日数据

    if notice_category_enable.get('today_data', True):
        total_upload, total_download, increase_info_list = toolbox.today_data()
        increase_list = []
        for increase_info in increase_info_list:
            info = f'\n\n- ♻️ 站点：{increase_info.get("name")}'
            if increase_info.get("uploaded") > 0:
                info += f'\n\t\t⬆ {toolbox.FileSizeConvert.parse_2_file_size(increase_info.get("uploaded"))}'
            if increase_info.get("downloaded") > 0:
                info += f'\n\t\t⬇ {toolbox.FileSizeConvert.parse_2_file_size(increase_info.get("downloaded"))}'
            increase_list.append(info)
        incremental = f'⬆ 总上传：{toolbox.FileSizeConvert.parse_2_file_size(total_upload)}\n' \
                      f'⬇ 总下载：{toolbox.FileSizeConvert.parse_2_file_size(total_download)}\n' \
                      f'✔ 说明: 数据均相较于本站今日之前最近的一条数据，可能并非昨日\n' \
                      f'⚛ 数据列表：{"".join(increase_list)}'
        logger.info(incremental)
        toolbox.send_text(title='通知：今日数据', message=incremental)
    end = time.time()
    consuming = f'自动更新个人数据 任务运行成功！共有{len(queryset)}个站点需要执行，' \
                f'共计成功 {len(success_message)} 个站点，失败 {len(failed_message)} 个站点，' \
                f'耗时：{round(end - start, 2)} 完成时间：{time.strftime("%Y-%m-%d %H:%M:%S")}  \n'
    message_list.append(consuming)
    logger.info(message_list)
    message_list.extend(failed_message)
    message_list.append('*' * 20)
    message_list.extend(success_message)
    logger.info(f'更新记录{consuming}')
    logger.debug(f'失败记录{len(message_list)}')
    logger.debug(f'成功记录{len(success_message)}')
    time.sleep(2)
    if notice_category_enable.get('site_data', True):
        toolbox.send_text(title='通知：更新个人数据', message='\n'.join(message_list))
    # toolbox.send_text(title='通知：更新个人数据-成功', message='\n'.join(success_message))
    # 释放内存
    gc.collect()
    # 发送任务确认信号
    # auto_get_status.acknowledge()
    return message_list


@shared_task(bind=True, base=BaseTask, autoretry_for=(Exception,), time_limit=200)
def auto_get_torrents(self, *site_list: List[int]):
    """
    拉取最新种子
    """
    start = time.time()
    message_list = []
    message_success = ['### 这些成功了  \n']
    message_failed = ['### 这些出错了  \n']
    message_push = ['### 这是推到下载器的  \n']
    websites = WebSite.objects.all()
    queryset = [my_site for my_site in MySite.objects.filter(id__in=site_list) if
                websites.get(id=my_site.site).brush_free]
    results = pool.map(pt_spider.send_torrent_info_request, queryset)
    for my_site, result in zip(queryset, results):
        logger.debug('获取种子：{}{}'.format(my_site.nickname, result))
        # print(result is tuple[int])
        if result.code == 0:
            res = pt_spider.get_torrent_info_list(my_site, result.data)
            # 通知推送
            if res.code == 0:
                message = f'> ✅ {my_site.nickname}种子抓取成功！ {res.msg}  \n\n'
                logger.debug(message)
                message_success.append(message)
                site = websites.get(id=my_site.site)
                logging.info(f'站点Free刷流：{my_site.brush_free}，绑定下载器：{my_site.downloader}')
                if my_site.downloader:
                    torrents = res.data
                    if len(res.data) <= 0:
                        continue
                    # 解析刷流推送规则,筛选符合条件的种子并推送到下载器
                    torrents = toolbox.filter_torrent_by_rules(my_site, torrents)
                    msg = f'> ✅ {my_site.nickname} 站点共有{len(res.data)}条种子未推送,有符合条件的种子：{len(torrents)} 个！  \n\n'
                    logger.debug(msg)
                    downloader = my_site.downloader
                    client, downloader_category = toolbox.get_downloader_instance(my_site.downloader_id)
                    if not client:
                        logger.warning(f'{my_site.downloader.name} 链接出错了')
                        continue
                    for torrent in torrents:
                        # 限速到站点限速的92%。以防超速
                        category = f'{site.nickname}-{torrent.tid}' if not torrent.hash_string else site.nickname
                        toolbox.push_torrents_to_downloader(
                            client, downloader_category,
                            urls=torrent.magnet_url,
                            cookie=my_site.cookie,
                            category=category,
                            is_paused=my_site.package_file and downloader.package_files,
                            upload_limit=int(site.limit_speed * 1024 * 0.92)
                        )
                        torrent.downloader = downloader
                        torrent.state = 1
                        torrent.save()
                    logging.info(f'ℹ️ 站点拆包状态：{my_site.package_file}，下载器拆包状态：{downloader.package_files}')
                    if my_site.package_file and downloader.package_files:
                        package_start = time.time()
                        # 30秒等待种子下载到下载器
                        time.sleep(30)
                        hash_list = []
                        for hash_string in [torrent.hash for torrent in torrents]:
                            try:
                                toolbox.package_files(
                                    client=client, hash_string=hash_string,
                                    package_size=downloader.package_size,
                                    package_percent=downloader.package_percent,
                                    delete_one_file=downloader.delete_one_file,
                                )
                            except Exception as e:
                                logger.error(traceback.format_exc(3))
                                # 拆包失败的写入hash_list
                                hash_list.append(hash_string)
                            finally:
                                client.torrents_resume(torrent_hashes=hash_string)
                        message = f'♻️ 拆包任务执行结束！耗时：{time.time() - package_start} \n ' \
                                  f'当前时间：{time.strftime("%Y-%m-%d %H:%M:%S")} \n' \
                                  f'成功拆包{len(torrents) - len(hash_list)}个，失败{len(hash_list)}个！'
                        if notice_category_enable.get("package_torrent", True):
                            toolbox.send_text(title='拆包', message=message)
                    message_push.append(msg)
            else:
                message = f'> 🆘 {my_site.nickname} 抓取种子信息失败！原因：{res.msg}  \n'
                message_failed.append(message)
                logger.error(message)
        else:
            # toolbox.send_text(my_site.nickname + ' 抓取种子信息失败！原因：' + result[0])
            message = f'> 🆘 {my_site.nickname} 抓取种子信息失败！原因：{result.msg}  \n'
            logger.error(message)
            message_failed.append(message)
    end = time.time()
    consuming = f'> ♻️ 拉取最新种子 任务运行成功！共有{len(site_list)}个站点需要执行，执行成功{len(message_success) - 1}个，' \
                f'失败{len(message_failed) - 1}个。本次任务耗时：{end - start} 当前时间：{time.strftime("%Y-%m-%d %H:%M:%S")}  \n\n'
    message_list.append(consuming)
    if len(message_failed) > 1:
        message_list.extend(message_failed)
    message_list.extend(message_success)
    if len(message_push) > 1:
        message_list.extend(message_push)
    logger.info(consuming)
    # toolbox.send_text(title='通知：拉取最新种子', message='\n'.join(message_list))
    # if len(message_success) > 0:
    #     toolbox.send_text(title='通知：拉取最新种子-成功', message=''.join(message_success))
    # 释放内存
    gc.collect()
    return consuming


# @shared_task(bind=True, base=BaseTask)
# def auto_get_hash_by_category(self, ):
#     start = time.time()
#     my_site_list = MySite.objects.filter(brush_free=True, downloader__isnull=False).all()
#     results = pool.map(toolbox.get_hash_by_category, my_site_list)
#     failed_msg = []
#     succeeded_msg = []
#     for result in results:
#         succeeded_msg.append(result.msg) if result.code == 0 else failed_msg.append(result.msg)
#     end = time.time()
#     consuming = f'> ♻️ 完善种子信息 任务运行成功！执行成功{len(succeeded_msg)}个，失败{len(failed_msg)}个。' \
#                 f'本次任务耗时：{end - start} 当前时间：{time.strftime("%Y-%m-%d %H:%M:%S")}  \n'
#     logger.info(consuming)
#     message_list = [consuming]
#     message_list.extend(failed_msg)
#     message_list.extend(succeeded_msg)
#     toolbox.send_text(title='通知：完善种子信息', message='\n'.join(message_list))
#     # if len(succeeded_msg) > 0:
#     #     toolbox.send_text(title='通知：完善种子信息-成功', message='\n'.join(succeeded_msg))
#     # 释放内存
#     gc.collect()
#     return '\n'.join(message_list)


# @shared_task(bind=True, base=BaseTask)
# def auto_calc_torrent_pieces_hash(self, ):
#     """
#     计算种子块HASH(根据种子信息进行补全)
#     """
#     start = time.time()
#     torrent_info_list = TorrentInfo.objects.filter(
#         downloader__isnull=False, state=1, pieces_qb__isnull=True
#     ).all()
#     website_list = WebSite.objects.all()
#     count = 0
#     for torrent_info in torrent_info_list:
#         logger.info('种子名称：{}'.format(torrent_info.title))
#         try:
#             client, _ = toolbox.get_downloader_instance(torrent_info.downloader_id)
#             if not torrent_info.hash_string:
#                 # 种子信息未填写hash的，组装分类信息，到下载器查询种子信息
#                 site = website_list.get(id=torrent_info.site.site)
#                 category = f'{site.nickname}-{torrent_info.tid}'
#                 torrents = client.torrents_info(category=category)
#             else:
#                 # 以后hash的直接查询
#                 torrents = client.torrents_info(torrent_hashes=torrent_info.hash_string)
#             if len(torrents) == 1:
#                 # 保存种子hash
#                 hash_string = torrents[0].hash_string
#                 torrent_info.hash_string = hash_string
#                 # 获取种子块HASH列表，并生成种子块HASH列表字符串的sha1值，保存
#                 pieces_hash_list = client.torrents_piece_hashes(torrent_hash=hash_string)
#                 pieces_hash_string = str(pieces_hash_list).replace(' ', '')
#                 torrent_info.pieces_hash = hashlib.sha1(pieces_hash_string.encode()).hexdigest()
#                 # 获取文件列表，并生成文件列表字符串的sha1值，保存
#                 file_list = client.torrents_files(torrent_hash=hash_string)
#                 file_list_hash_string = str(file_list).replace(' ', '')
#                 torrent_info.filelist = hashlib.sha1(file_list_hash_string.encode()).hexdigest()
#                 torrent_info.files_count = len(file_list)
#             torrent_info.state = 1
#             torrent_info.save()
#             count += 1
#         except Exception as e:
#             logging.error(traceback.format_exc(3))
#             continue
#     end = time.time()
#     message = f'> 计算种子Pieces的HASH值 任务运行成功！共成功处理种子{count}个，耗时：{end - start}  \n{time.strftime("%Y-%m-%d %H:%M:%S")}'
#     toolbox.send_text(title='通知：计算种子HASH', message=message)
#     # 释放内存
#     gc.collect()


@shared_task(bind=True, base=BaseTask, time_limit=200)
def auto_get_rss(self, *site_list: List[int]):
    start = time.time()
    # site_list = site_list.split('|')
    logger.info(site_list)
    my_site_list = MySite.objects.filter(id__in=site_list, rss__startswith='https://').all()
    websites = WebSite.objects.filter(brush_rss=True).all()
    message_list = []
    message_failed = []
    message_success = []
    results = pool.map(toolbox.parse_rss, [my_site.rss for my_site in my_site_list])
    for my_site, result in zip(my_site_list, results):
        try:
            website = websites.get(id=my_site.site)
            updated = 0
            created = 0
            torrent_list = []
            # urls = []
            for t in result:
                tid = t.get('tid')
                # 组装种子详情页URL 解析详情页信息
                # res_detail = pt_spider.get_torrent_detail(my_site, f'{website.url}{website.page_detail.format(tid)}')
                # 如果无报错，将信息合并到torrent
                # if res_detail.code == 0:
                #     torrent.update(res_detail.data)
                logger.debug(t)
                res = TorrentInfo.objects.update_or_create(site=my_site, tid=tid, defaults=t, )
                if res[1]:
                    res[0].downloader = my_site.downloader
                    res[0].save()
                    torrent_list.append(res[0])
                    created += 1
                else:
                    updated += 1
                # logger.debug(res)
            msg = f'✅ {my_site.nickname} 新增种子：{created} 个，更新种子：{updated}个！'
            logger.info(msg)
            message_success.append(msg)
            logging.info(f'✅ 站点RSS刷流：{my_site.brush_rss}，绑定下载器：{my_site.downloader}')
            if my_site.brush_rss and my_site.downloader:
                downloader = my_site.downloader
                client, downloader_category = toolbox.get_downloader_instance(downloader.id)
                if not client:
                    logger.warning(f'{my_site.downloader.name} 链接出错了')
                    continue
                push_message = []
                for torrent in torrent_list:
                    torrent.magnet_url = f'{website.url}{website.page_download.format(torrent.tid)}'
                    res = toolbox.push_torrents_to_downloader(
                        client, downloader_category,
                        urls=torrent.magnet_url,
                        cookie=my_site.cookie,
                        is_paused=my_site.package_file and downloader.package_files,
                        category=f'{website.nickname}-{torrent.tid}'
                    )
                    if res.code == 0:
                        torrent.downloader = downloader
                        torrent.state = 1
                        torrent.save()
                    msg = f'{torrent.title} 推送状态：{res.msg}'
                    logging.info(msg)
                    push_message.append(msg)
                message = f'> ♻️ RSS 任务运行成功！耗时：{time.time() - start}  \n' \
                          f'当前时间：{time.strftime("%Y-%m-%d %H:%M:%S")} \n 种子推送记录' + '\n'.join(push_message)
                logging.info(f'ℹ️ 站点拆包状态：{my_site.package_file}，下载器拆包状态：{downloader.package_files}')
                # 拆包
                if my_site.package_file and downloader.package_files:
                    package_start = time.time()
                    # 30秒等待种子下载到下载器
                    time.sleep(30)
                    hash_list = []
                    for hash_string in [torrent.hash for torrent in torrent_list]:
                        try:
                            toolbox.package_files(
                                client=client, hash_string=hash_string,
                                package_size=downloader.package_size,
                                package_percent=downloader.package_percent,
                                delete_one_file=downloader.delete_one_file,
                            )
                        except Exception as e:
                            logger.error(traceback.format_exc(3))
                            # 拆包失败的写入hash_list
                            hash_list.append(hash_string)
                            continue
                    message = f'♻️ 拆包任务执行结束！耗时：{time.time() - package_start} \n ' \
                              f'当前时间：{time.strftime("%Y-%m-%d %H:%M:%S")} \n' \
                              f'成功拆包{len(torrent_list) - len(hash_list)}个，失败{len(hash_list)}个！'
                    if notice_category_enable.get("package_torrent", True):
                        toolbox.send_text(title='拆包', message=message)
                    package_files = {
                        'site': my_site.nickname,
                        'time': time.strftime("%Y-%m-%d %H:%M:%S"),
                        'downloader_id': downloader.id,
                        'hash_list': hash_list
                    }
                    # 从缓存获取需要拆包的任务参数列表
                    cache_package_files_list = cache.get(f'cache_package_files_list')
                    if not cache_package_files_list or len(cache_package_files_list) <= 0:
                        cache_package_files_list = [package_files]
                    else:
                        # 如果列表存在就讲本次生成的参数添加到列表末尾
                        cache_package_files_list.append(package_files)
                    # 更新参数列表
                    cache.set(f'cache_package_files_list', cache_package_files_list, 60 * 60 * 24)
        except Exception as e:
            logger.error(traceback.format_exc(3))
            msg = f'{my_site.nickname} RSS获取或解析失败'
            logger.error(msg)
            message_failed.append(msg)
            continue
    end = time.time()
    message = f'> ♻️ RSS 任务运行成功！耗时：{end - start}  \n{time.strftime("%Y-%m-%d %H:%M:%S")} \n'
    message_list.append(message)
    message_list.extend(message_failed)
    message_list.extend(message_success)
    msg = '\n - '.join(message_list)
    # toolbox.send_text(title='通知：RSS 任务运行成功！', message=msg)
    return msg


@shared_task(bind=True, base=BaseTask, time_limit=200)
def auto_torrents_package_files(self):
    """
    拆包并下载
    :param self:
    :return:
    """
    cache_package_files_list = cache.get(f'cache_package_files_list')
    if not cache_package_files_list or len(cache_package_files_list) <= 0:
        logger.info('❎ 没有任务，我去玩耍了，一会儿再来！')
        pass
    else:
        message_list = []
        for index, package in enumerate(cache_package_files_list):
            try:
                downloader_id = package.get("downloader_id")
                downloader = Downloader.objects.get(id=downloader_id)
                client, _ = toolbox.get_downloader_instance(downloader_id)
                if not client:
                    logger.warning(f'{downloader.name} 链接出错了')
                    continue
                # 拆包
                hash_list = package.get("hash_list")
                packaged_hashes = []
                succeed = 0
                for hash_string in hash_list:
                    try:
                        toolbox.package_files(
                            client=client, hash_string=hash_string,
                            package_size=downloader.package_size,
                            package_percent=downloader.package_percent,
                            delete_one_file=downloader.delete_one_file,
                        )
                        packaged_hashes.append(hash_string)
                        succeed += 1
                    except Exception as e:
                        logger.error(traceback.format_exc(3))
                # 开始下载
                if len(packaged_hashes) == len(hash_list):
                    # 拆包完成的任务从列表中移除
                    del cache_package_files_list[index]
                    msg = f"✅ {package.get('site')} {package.get('time')}写入的拆包任务执行结束，开始下载"
                    logger.info(msg)
                else:
                    msg = f"🆘 {package.get('site')} {package.get('time')}拆包结束，部分种子操作失败，下次重试，现在开始下载已拆包种子"
                    logger.info(msg)
                # torrents = client.torrents_info(status_filter='paused')
                # if len(torrents) > 0:
                #     for torrent in torrents:
                #         try:
                #             toolbox.package_files(client=client, hash_string=torrent.get('hash'))
                #         except Exception as e:
                #             logger.error(e)
                #             continue
                client.torrents_resume(torrent_hashes=packaged_hashes)
                msg = f"\n ✅ {package.get('site')} {package.get('time')}推送的种子拆包完成，" \
                      f"成功拆包{succeed}个，失败{len(hash_list) - succeed}个，开始下载"
                logger.info(msg)
                message_list.append(msg)
            except Exception as e:
                logger.error(traceback.format_exc(3))
                continue
        message = f'♻️ 拆包任务执行结束！{time.strftime("%Y-%m-%d %H:%M:%S")} \n {"".join(message_list)}'
        if notice_category_enable.get("package_torrent", True):
            toolbox.send_text(title='拆包', message=message)


@shared_task(bind=True, base=BaseTask, time_limit=200)
def auto_cleanup_not_registered(self):
    downloaders = Downloader.objects.filter(category=DownloaderCategory.qBittorrent, brush=True)
    not_registered_msg = [
        'torrent not registered with this tracker',
        'err torrent deleted due to other',
    ]
    for downloader in downloaders:
        hashes = []
        client, _ = toolbox.get_downloader_instance(downloader.id)
        if not client:
            logger.warning(f'{downloader.name} 链接出错了')
            continue
        torrents = client.torrents_info(status_filter='stalled_downloading|stalledUP')
        for torrent in torrents:
            hash_string = torrent.get('hash')
            trackers = client.torrents_trackers(torrent_hash=hash_string)
            tracker_checked = False
            tracker_msg_list = [tracker.get('msg').lower() for tracker in trackers]
            for tracker_msg in tracker_msg_list:
                delete_msg = [msg for msg in not_registered_msg if tracker_msg.startswith(msg)]
                msg = f'{torrent.get("name")} - {hash_string} - msg：{tracker_msg} -{len(delete_msg)}'
                logger.debug(msg)
                if len(delete_msg) > 0:
                    hashes.append(hash_string)
                    # hashes.append(f'{torrent.get("name")} - {hash_string}')
                    tracker_checked = True
                    break
            if tracker_checked:
                continue
        logger.info(f'✅ {downloader.name} 本次任务共检查出 {len(hashes)} 个已删除种子！')
        if len(hashes) > 0:
            toolbox.send_text(title='已失效种子', message='♻️ {}\n{}'.format(downloader.name, '\n'.join(hashes)))
            # todo 未来在这里会将已被删除的种子HASH发送至服务器
            client.torrents_delete(torrent_hashes=hashes, delete_files=True)


@shared_task(bind=True, base=BaseTask, time_limit=200)
def auto_remove_brush_task(self, *site_list: List[int]):
    start = time.time()
    my_site_list = MySite.objects.filter(
        Q(brush_rss=True) | Q(brush_free=True), downloader__isnull=False, id__in=site_list,
        remove_torrent_rules__startswith='{', ).all()
    message_list = []
    failed_message = []
    succeed_message = []
    websites = WebSite.objects.filter(brush_rss=True, id__in=[my_site.site for my_site in my_site_list]).all()
    results = pool.map(toolbox.remove_torrent_by_site_rules, my_site_list)
    count = 0
    for res in results:
        if res.code == 0:
            count += res.data
            succeed_message.append(res.msg)
        else:
            failed_message.append(res.msg)
    msg = f"\n ✅ 删种任务完成，成功删除种子{count}个，{len(failed_message)}个站点删种出错,耗时：{int(time.time() - start)}秒！\n\n> "
    message_list.append(msg)
    if len(failed_message) > 0:
        message_list.extend(failed_message)
    if len(succeed_message) > 0:
        message_list.extend(succeed_message)
    message = '\n\n> '.join(message_list)
    logger.debug(message)
    if len(failed_message) > 0 or count > 0:
        if notice_category_enable.get("delete_torrent", True):
            toolbox.send_text(title=f'删种-成功删除{count}条', message=message)
    return message


@shared_task(bind=True, base=BaseTask, time_limit=200)
def auto_get_rss_torrent_detail(self, my_site_id: int = None):
    if not my_site_id:
        my_site_list = MySite.objects.filter(brush_free=True, rss__contains='http').all()
    else:
        my_site_list = MySite.objects.filter(id=my_site_id, brush_free=True, rss__contains='http').all()
    if len(my_site_list) <= 0:
        return '❎ 没有站点需要RSS，请检查RSS链接与抓种开关！'
    website_list = WebSite.objects.all()
    results = pool.map(toolbox.parse_rss, [my_site.rss for my_site in my_site_list])
    for my_site, result in zip(my_site_list, results):
        try:
            website = website_list.get(id=my_site.site)
            hash_list = []
            urls = []
            updated = 0
            created = 0
            for torrent in result:
                tid = torrent.get('tid')
                urls.append(f'{website.url}{website.page_download.format(tid)}')
                # 组装种子详情页URL 解析详情页信息
                # res_detail = pt_spider.get_torrent_detail(my_site, f'{website.url}{website.page_detail.format(tid)}')
                # 如果无报错，将信息合并到torrent
                # if res_detail.code == 0:
                #     torrent.update(res_detail.data)
                res = TorrentInfo.objects.update_or_create(
                    site=my_site,
                    tid=tid,
                    defaults=torrent,
                )
                if res[1]:
                    created += 1
                else:
                    updated += 1
                logger.info(res)
                hash_list.append(res[0].hash_string)
            if website.brush_rss and my_site.brush_rss and my_site.downloader:
                downloader = my_site.downloader
                client, downloader_category = toolbox.get_downloader_instance(downloader.id)
                if not client:
                    logger.warning(f'{downloader.name} 链接出错了')
                    continue
                res = toolbox.push_torrents_to_downloader(
                    client, downloader_category,
                    urls=urls,
                    cookie=my_site.cookie,
                )
                if downloader.package_files:
                    client, _ = toolbox.get_downloader_instance(downloader.id)
                    if not client:
                        logger.warning(f'{downloader.name} 链接出错了')
                        continue
                    for hash_string in hash_list:
                        toolbox.package_files(
                            client=client,
                            hash_string=hash_string
                        )
                logging.info(res.msg)
            msg = f'✅ {my_site.nickname} 新增种子{created} 个，更新{updated}个'
            logger.info(msg)
            if notice_category_enable.get("rss_torrent", True):
                toolbox.send_text(title='RSS', message=msg)
            if len(my_site_list) == 1:
                return {'hash_list': hash_list, 'msg': msg}
        except Exception as e:
            msg = f'❌ {my_site.nickname} RSS获取或解析失败'
            logger.error(msg)
            logger.error(traceback.format_exc(3))
            if len(my_site_list) == 1:
                return msg
            continue


@shared_task(bind=True, base=BaseTask, time_limit=200)
def auto_get_update_torrent(self, torrent_id):
    if isinstance(torrent_id, str):
        torrent_ids = torrent_id.split('|')
        torrent_list = TorrentInfo.objects.filter(id__in=torrent_ids).all()
    else:
        torrent_list = TorrentInfo.objects.filter(state=False).all()
    count = 0
    for torrent in torrent_list:
        try:
            res = pt_spider.get_update_torrent(torrent)
            if res.code == 0:
                count += 1
        except Exception as e:
            logger.error(traceback.format_exc(3))
            continue
    msg = f'♻️ 共有{len(torrent_list)}种子需要更新，本次更新成功{count}个，失败{len(torrent_list) - count}个'
    logger.info(msg)


@shared_task(bind=True, base=BaseTask)
def auto_push_to_downloader(self, *site_list: List[int]):
    """推送到下载器"""
    start = time.time()
    logging.info('ℹ️ 推送种子到下载器任务开始')
    my_site_list = MySite.objects.filter(brush_free=True, id__in=site_list).all()
    website_list = WebSite.objects.all()
    message_list = []
    for my_site in my_site_list:
        site = website_list.get(id=my_site.site)
        logging.info(f'ℹ️ 站点Free刷流：{my_site.brush_free}，绑定下载器：{my_site.downloader}')
        torrents = TorrentInfo.objects.filter(site=my_site, state=0, sale_status__contains='Free')
        logger.info(f'ℹ️ 站点有{len(torrents)}条种子未推送')
        if my_site.downloader:
            # 解析刷流推送规则,筛选符合条件的种子并推送到下载器
            torrents = toolbox.filter_torrent_by_rules(my_site, torrents)
            logger.info(f'ℹ️ 共有符合条件的种子：{len(torrents)} 个')
            client, downloader_category = toolbox.get_downloader_instance(my_site.downloader_id)
            if not client:
                logger.warning(f'{my_site.downloader.name} 链接出错了')
                continue
            for torrent in torrents:
                # 限速到站点限速的92%。以防超速
                toolbox.push_torrents_to_downloader(
                    client, downloader_category,
                    urls=torrent.magnet_url,
                    cookie=my_site.cookie,
                    category=f'{site.nickname}-{torrent.tid}',
                    upload_limit=int(site.limit_speed * 1024 * 0.92)
                )
                torrent.downloader = my_site.downloader
                torrent.state = 1
                torrent.save()
            msg = f'✅ {my_site.nickname} 站点共有{len(torrents)}条种子未推送,有符合条件的种子：{len(torrents)} 个'
            message_list.append('\n')
            message_list.append(msg)
    end = time.time()
    message = f'> ♻️ 签到 任务运行成功！耗时：{end - start}  \n{time.strftime("%Y-%m-%d %H:%M:%S")} \n{"".join(message_list)}'
    if notice_category_enable.get("push_torrent", True):
        toolbox.send_text(title='通知：推送种子任务', message=message)
    # 释放内存
    gc.collect()


@shared_task(bind=True, base=BaseTask)
def auto_update_torrent_info(self, ):
    """自动获取种子"""
    start = time.time()
    print('自动获取种子HASH')
    time.sleep(5)
    end = time.time()
    message = f'> ♻️获取种子HASH 任务运行成功！耗时：{end - start}  \n{time.strftime("%Y-%m-%d %H:%M:%S")}'
    if notice_category_enable.get("get_torrent_hash", True):
        toolbox.send_text(title='通知：自动获取种子HASH', message=message)
    # 释放内存
    gc.collect()


@shared_task(bind=True, base=BaseTask)
def exec_command(self, commands):
    """执行命令行命令"""
    result = []
    for key, command in commands.items():
        p = subprocess.run(command, shell=True)
        logger.info('{} 命令执行结果：\n{}'.format(key, p))
        result.append({
            'command': key,
            'res': p.returncode
        })
    # 释放内存
    gc.collect()
    return result


@shared_task(bind=True, base=BaseTask)
def auto_program_upgrade(self, ):
    """程序更新"""
    try:
        logger.info('开始自动更新')
        update_commands = {
            # 'cp db/db.sqlite3 db/db.sqlite3-$(date "+%Y%m%d%H%M%S")',
            '更新依赖环境': 'wget -O requirements.txt https://gitee.com/ngfchl/ptools/raw/master/requirements.txt &&'
                            ' pip install -r requirements.txt -U',
            '强制覆盖本地': 'git clean -df && git reset --hard',
            '获取更新信息': 'git fetch --all',
            '拉取代码更新': f'git pull origin {os.getenv("DEV")}',
        }
        logger.info('拉取最新代码')
        result = exec_command(update_commands)
        logger.info('更新完毕')
        message = f'> 更新完成！！请在接到通知后同步数据库！{datetime.now()}'
        if notice_category_enable.get("program_upgrade", True):
            toolbox.send_text(title='通知：程序更新', message=message)
        return CommonResponse.success(
            msg='更新成功！稍后请在接到通知后同步数据库！！',
            data={
                'result': result
            }
        )
    except Exception as e:
        # raise
        msg = '更新失败!{}，请尝试同步数据库！'.format(str(e))
        logger.error(msg)
        message = f'> <font color="red">{msg}</font>'
        toolbox.send_text(title=msg, message=message)
        return CommonResponse.error(
            msg=msg
        )
    finally:
        # 释放内存
        gc.collect()


@shared_task(bind=True, base=BaseTask)
def auto_remove_expire_torrent(self):
    """
    清理免费到期的种子
    :param self:
    :return:
    """
    # 筛选标记为刷流的下载器
    downloaders = Downloader.objects.filter(brush=True).all()
    # 筛选已推送到下载器的种子
    torrent_info_list = TorrentInfo.objects.filter(state=1, downloader__in=downloaders).all()
    for downloader in downloaders:
        client, _ = toolbox.get_downloader_instance(downloader.id)
        if not client:
            logger.warning(f'{downloader.name} 链接出错了')
            continue
        # 筛选已过期和剩余免费时间小于三分钟的种子
        torrents = [torrent for torrent in torrent_info_list if
                    torrent.downloader.id == downloader.id and time.strptime(
                        torrent.sale_expire).timestamp() < time.time() - 60 * 3]
        hashes = [torrent.hash for torrent in torrents]
        # 如果开启了保留已下载完毕种子选项，则选下载中的种子
        if downloader.keep_completed:
            downloading_torrents = client.torrents_info(
                status_filter=['downloading', 'stalled_downloading'], torrent_hashes=hashes)
            print(downloading_torrents)
            hashes = [torrent.get('hash') for torrent in downloading_torrents]
        client.torrents_delete(torrent_hashes=hashes, delete_files=True)


@shared_task(bind=True, base=BaseTask)
def auto_update_license(self, ):
    """auto_update_license"""
    res = toolbox.generate_config_file()
    if res.code != 0:
        return CommonResponse.error(
            msg=res.msg
        )
    data = toml.load('db/ptools.toml')
    print(data)
    pt_helper = data.get('pt_helper')
    if len(pt_helper) <= 0:
        return CommonResponse.error(
            msg='请先配置小助手相关信息再进行操作！'
        )
    host = pt_helper.get('host')
    username = pt_helper.get('username')
    password = pt_helper.get('password')
    url = 'http://get_pt_helper_license.guyubao.com/getTrial'
    license_xpath = '//h2/text()'
    session = requests.Session()
    res = session.get(url=url)
    token = ''.join(etree.HTML(res.content).xpath(license_xpath))
    login_url = host + '/login/submit'
    login_res = session.post(
        url=login_url,
        data={
            'username': username,
            'password': password,
        }
    )
    token_url = host + '/sys/config/update'
    logger.info(login_res.cookies.get_dict())
    cookies = session.cookies.get_dict()
    logger.info(cookies)
    res = session.post(
        url=token_url,
        cookies=cookies,
        data={
            'Id': 4,
            'ParamKey': 'license',
            'ParamValue': token.split('：')[-1],
            'Status': 1,
        }
    )
    logger.info(f'结果：{res.text}')
    result = res.json()
    if result.get('code') == 0:
        result['data'] = token
        toolbox.send_text(title='小助手License更新成功！', message=f'> {token}')
        return CommonResponse.success(
            data=result
        )
    # 释放内存
    gc.collect()
    return CommonResponse.error(
        msg=f'License更新失败！'
    )


@shared_task(bind=True, base=BaseTask)
def import_from_ptpp(self, data_list: List):
    results = pool.map(pt_spider.get_uid_and_passkey, data_list)

    message_list = [result.msg for result in results]
    logger.info(message_list)
    # send_text(title='PTPP站点导入通知', message='Cookies解析失败，请确认导入了正确的cookies备份文件！')
    if notice_category_enable.get("ptpp_import", True):
        toolbox.send_text(title='PTPP站点导入通知', message='\n\n'.join(message_list))
    return message_list


# @shared_task
@shared_task(bind=True, base=BaseTask)
def auto_repeat_torrent(self):
    # 加载辅种配置项
    repeat = toolbox.parse_toml('repeat')
    logger.debug(f'加载辅种配置项: {repeat}')
    push_timeout = repeat.get('push_timeout', 150)
    logger.info('筛选开启辅种的下载器')
    downloaders = Downloader.objects.filter(repeat=True).all()
    downloader_ids = [downloader.id for downloader in downloaders]
    logger.info(downloaders)
    logger.info('开始辅种')
    results1 = pool.map(pt_spider.repeat_torrents, downloader_ids)
    time.sleep(push_timeout)
    results2 = pool.map(pt_spider.start_torrent, downloader_ids)
    logger.info('辅种结束')
    message_list = []
    for downloader, result1, result2 in zip(downloaders, results1, results2):
        logger.info(f'result1: {result1}')
        logger.info(f'result2: {result2}')

        if result1.code == 0 and result2.code == 0:
            repeat_count, cached_count, push_count = result1.data

            paused_count, recheck_count, resume_count = result2.data

            message = f'- ✅ 下载器 {downloader.name} 在本次辅种任务中：  \n' \
                      f'> 获取{repeat_count}条可辅种数据  \n' \
                      f'> 缓存{cached_count}条辅种数据  \n' \
                      f'> 推送{push_count}条辅种数据  \n' \
                      f'> 获取到{paused_count}个暂停的种子  \n' \
                      f'> 校验了{recheck_count}个种子  \n' \
                      f'> 开始了{resume_count}个种子  \n'
        else:
            message = f'- 🚫 下载器 {downloader.name} 在本次辅种出错了：{result1.msg} {result2.msg}'
        message_list.append(message)
    messages = '\n'.join(message_list)
    logger.info(messages)
    if notice_category_enable.get("repeat_torrent", True):
        toolbox.send_text(title=f'辅种任务', message=messages)
    return messages


@shared_task(bind=True, base=BaseTask)
def test_task(self, *args):
    logger.info(args)
    toolbox.send_text(title='测试', message=str(args))
    return args
