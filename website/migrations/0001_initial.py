# Generated by Django 4.2.1 on 2023-05-29 00:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='WebSite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('url',
                 models.URLField(default='', help_text='请保留网址结尾的"/"', unique=True, verbose_name='站点网址')),
                ('name', models.CharField(max_length=32, verbose_name='站点名称')),
                ('nickname',
                 models.CharField(default='', help_text='英文，用于刷流', max_length=16, verbose_name='站点简称')),
                ('logo', models.URLField(default='favico.ico', help_text='站点logo图标', verbose_name='站点logo')),
                ('tracker',
                 models.CharField(default='', help_text='tracker网址关键字', max_length=256, verbose_name='tracker')),
                ('sp_full', models.FloatField(default=107, help_text='站点满时魔', verbose_name='满魔')),
                ('limit_speed',
                 models.IntegerField(default=100, help_text='单种限速，单位：MB/S', verbose_name='上传速度限制')),
                ('tags', models.CharField(default='电影,电视剧', help_text='站点资源类型，以`,`分割', max_length=128,
                                          verbose_name='站点标签')),
                ('iyuu', models.IntegerField(default=0, verbose_name='iyuu')),
                ('sign_in', models.BooleanField(default=True, verbose_name='签到支持')),
                ('get_info', models.BooleanField(default=True, verbose_name='站点数据')),
                ('repeat_torrents', models.BooleanField(default=False, verbose_name='辅种支持')),
                ('brush_free', models.BooleanField(default=True, verbose_name='Free刷流')),
                ('brush_rss', models.BooleanField(default=False, verbose_name='RSS刷流')),
                ('hr_discern', models.BooleanField(default=False, verbose_name='HR识别')),
                ('search_torrents', models.BooleanField(default=False, verbose_name='搜索支持')),
                ('page_index', models.CharField(default='index.php', max_length=64, verbose_name='首页')),
                ('page_torrents',
                 models.CharField(default='torrents.php?incldead=1', max_length=64, verbose_name='默认搜索页面')),
                (
                'page_sign_in', models.CharField(default='attendance.php', max_length=64, verbose_name='默认签到链接')),
                ('page_control_panel', models.CharField(default='usercp.php', max_length=64, verbose_name='控制面板')),
                ('page_detail',
                 models.CharField(default='details.php?id={}', max_length=64, verbose_name='详情页面链接')),
                ('page_download',
                 models.CharField(default='download.php?id={}', max_length=64, verbose_name='默认下载链接')),
                ('page_user',
                 models.CharField(default='userdetails.php?id={}', max_length=64, verbose_name='用户信息链接')),
                ('page_search',
                 models.CharField(default='torrents.php?incldead=1&search={}', max_length=64, verbose_name='搜索链接')),
                ('page_message', models.CharField(default='messages.php', max_length=64, verbose_name='消息页面')),
                ('page_hr',
                 models.CharField(default='myhr.php?hrtype=1&userid={}', max_length=64, verbose_name='HR考核页面')),
                ('page_leeching',
                 models.CharField(default='getusertorrentlistajax.php?userid={}&type=leeching', max_length=64,
                                  verbose_name='当前下载信息')),
                ('page_uploaded',
                 models.CharField(default='getusertorrentlistajax.php?userid={}&type=uploaded', max_length=64,
                                  verbose_name='发布种子信息')),
                ('page_seeding',
                 models.CharField(default='getusertorrentlistajax.php?userid={}&type=seeding', max_length=64,
                                  verbose_name='当前做种信息')),
                ('page_completed',
                 models.CharField(default='getusertorrentlistajax.php?userid={}&type=completed', max_length=64,
                                  verbose_name='完成种子信息')),
                ('page_mybonus', models.CharField(default='mybonus.php', max_length=64, verbose_name='魔力值页面')),
                ('page_viewfilelist',
                 models.CharField(default='viewfilelist.php?id={}', max_length=64, verbose_name='文件列表链接')),
                ('sign_info_title', models.CharField(default='//td[@id="outer"]//td[@class="embedded"]/h2/text()',
                                                     help_text='签到页面消息标题', max_length=128,
                                                     verbose_name='签到消息标题')),
                ('sign_info_content',
                 models.CharField(default='//td[@id="outer"]//td[@class="embedded"]/table//td//text()',
                                  help_text='签到页面消息内容', max_length=128, verbose_name='签到消息内容')),
                ('hr', models.BooleanField(default=False, help_text='站点是否开启HR', verbose_name='H&R')),
                ('hr_rate',
                 models.IntegerField(default=2, help_text='站点要求HR种子的分享率，最小：1', verbose_name='HR分享率')),
                ('hr_time', models.IntegerField(default=10, help_text='站点要求HR种子最短做种时间，单位：小时',
                                                verbose_name='HR时间')),
                ('search_params',
                 models.CharField(default='', help_text='字典格式：{"accept":"application/json","c":"d"}',
                                  max_length=256, verbose_name='促销参数')),
                ('my_invitation_rule',
                 models.CharField(default='//span/a[contains(@href,"invite.php?id=")]/following-sibling::text()[1]',
                                  max_length=128, verbose_name='邀请资格')),
                ('my_time_join_rule',
                 models.CharField(default='//td[contains(text(),"加入")]/following-sibling::td/span/@title',
                                  max_length=128, verbose_name='注册时间')),
                ('my_latest_active_rule',
                 models.CharField(default='//td[contains(text(),"最近动向")]/following-sibling::td/span/@title',
                                  max_length=128, verbose_name='最后活动时间')),
                ('my_uploaded_rule',
                 models.CharField(default='//font[@class="color_uploaded"]/following-sibling::text()[1]',
                                  max_length=128, verbose_name='上传量')),
                ('my_downloaded_rule',
                 models.CharField(default='//font[@class="color_downloaded"]/following-sibling::text()[1]',
                                  max_length=128, verbose_name='下载量')),
                ('my_ratio_rule',
                 models.CharField(default='//font[@class="color_ratio"][1]/following-sibling::text()[1]',
                                  max_length=128, verbose_name='分享率')),
                ('my_bonus_rule',
                 models.CharField(default='//a[@href="mybonus.php"]/following-sibling::text()[1]', max_length=128,
                                  verbose_name='魔力值')),
                ('my_per_hour_bonus_rule',
                 models.CharField(default='//div[contains(text(),"每小时能获取")]/text()[1]', max_length=128,
                                  verbose_name='时魔')),
                ('my_score_rule', models.CharField(
                    default='//font[@class="color_bonus" and contains(text(),"积分")]/following-sibling::text()[1]',
                    max_length=128, verbose_name='保种积分')),
                ('my_level_rule', models.CharField(
                    default='//table[@id="info_block"]//span/a[contains(@class,"_Name") and contains(@href,"userdetails.php?id=")]/@class',
                    max_length=128, verbose_name='用户等级')),
                ('my_passkey_rule',
                 models.CharField(default='//td[contains(text(),"密钥")]/following-sibling::td[1]/text()',
                                  max_length=128, verbose_name='Passkey')),
                ('my_uid_rule', models.CharField(
                    default='//table[@id="info_block"]//span/a[contains(@class,"_Name") and contains(@href,"userdetails.php?id=")]/@href',
                    max_length=128, verbose_name='用户ID')),
                ('my_hr_rule',
                 models.CharField(default='//a[@href="myhr.php"]//text()', max_length=128, verbose_name='H&R')),
                ('my_leech_rule',
                 models.CharField(default='//img[@class="arrowdown"]/following-sibling::text()[1]', max_length=128,
                                  verbose_name='下载数量')),
                ('my_publish_rule', models.CharField(default='//p/preceding-sibling::b/text()[1]', max_length=128,
                                                     verbose_name='发种数量')),
                ('my_seed_rule',
                 models.CharField(default='//img[@class="arrowup"]/following-sibling::text()[1]', max_length=128,
                                  verbose_name='做种数量')),
                ('my_seed_vol_rule', models.CharField(default='//tr/td[3]', help_text='需对数据做处理', max_length=128,
                                                      verbose_name='做种大小')),
                ('my_mailbox_rule',
                 models.CharField(default='//a[@href="messages.php"]/font[contains(text(),"条")]/text()[1]',
                                  help_text='获取新邮件', max_length=128, verbose_name='邮件规则')),
                ('my_message_title',
                 models.CharField(default='//img[@alt="Unread"]/parent::td/following-sibling::td/a[1]//text()',
                                  help_text='获取邮件标题', max_length=128, verbose_name='邮件标题')),
                ('my_notice_rule',
                 models.CharField(default='//a[@href="index.php"]/font[contains(text(),"条")]/text()[1]',
                                  help_text='获取新公告', max_length=128, verbose_name='公告规则')),
                ('my_notice_title',
                 models.CharField(default='//td[@class="text"]/div/a//text()', help_text='获取公告标题', max_length=128,
                                  verbose_name='公告标题')),
                ('my_notice_content',
                 models.CharField(default='//td[@class="text"]/div/a/following-sibling::div', help_text='获取公告内容',
                                  max_length=128, verbose_name='公告内容')),
                ('torrents_rule',
                 models.CharField(default='//table[@class="torrents"]/tr', max_length=128, verbose_name='种子行信息')),
                ('torrent_title_rule', models.CharField(default='.//td[@class="embedded"]/a/b/text()', max_length=128,
                                                        verbose_name='种子名称')),
                ('torrent_subtitle_rule',
                 models.CharField(default='.//a[contains(@href,"detail")]/parent::td/text()[last()]', max_length=128,
                                  verbose_name='种子标题')),
                ('torrent_detail_url_rule',
                 models.CharField(default='.//td[@class="embedded"]/a[contains(@href,"detail")]/@href', max_length=128,
                                  verbose_name='种子详情')),
                ('torrent_category_rule',
                 models.CharField(default='.//td[@class="rowfollow nowrap"][1]/a[1]/img/@title', max_length=128,
                                  verbose_name='分类')),
                ('torrent_poster_rule',
                 models.CharField(default='.//table/tr/td[1]/img/@src', max_length=128, verbose_name='海报')),
                ('torrent_magnet_url_rule',
                 models.CharField(default='.//td/a[contains(@href,"download.php?id=")]/@href', max_length=128,
                                  verbose_name='主页下载链接')),
                ('torrent_size_rule',
                 models.CharField(default='.//td[5]/text()', max_length=128, verbose_name='文件大小')),
                ('torrent_hr_rule',
                 models.CharField(default='.//table/tr/td/img[@class="hitandrun"]/@title', max_length=128,
                                  verbose_name='H&R')),
                ('torrent_sale_rule', models.CharField(default='.//img[contains(@class,"free")]/@alt', max_length=128,
                                                       verbose_name='促销信息')),
                ('torrent_sale_expire_rule',
                 models.CharField(default='.//img[contains(@class,"free")]/following-sibling::font/span/@title',
                                  max_length=128, verbose_name='促销时间')),
                ('torrent_release_rule',
                 models.CharField(default='.//td[4]/span/@title', max_length=128, verbose_name='发布时间')),
                ('torrent_seeders_rule',
                 models.CharField(default='.//a[contains(@href,"#seeders")]/text()', max_length=128,
                                  verbose_name='做种人数')),
                ('torrent_leechers_rule',
                 models.CharField(default='.//a[contains(@href,"#leechers")]/text()', max_length=128,
                                  verbose_name='下载人数')),
                ('torrent_completers_rule',
                 models.CharField(default='.//a[contains(@href,"viewsnatches")]//text()', max_length=128,
                                  verbose_name='完成人数')),
                ('detail_title_rule',
                 models.CharField(default='//h1/text()[1]', max_length=128, verbose_name='详情页种子标题')),
                ('detail_subtitle_rule',
                 models.CharField(default='//td[contains(text(),"副标题")]/following-sibling::td/text()[1]',
                                  max_length=128, verbose_name='详情页种子副标题')),
                ('detail_download_url_rule',
                 models.CharField(default='//a[@class="index" and contains(@href,"download.php")]/@href',
                                  max_length=128, verbose_name='详情页种子链接')),
                ('detail_size_rule',
                 models.CharField(default='//td//b[contains(text(),"大小")]/following::text()[1]', max_length=128,
                                  verbose_name='详情页种子大小')),
                ('detail_category_rule',
                 models.CharField(default='//td/b[contains(text(),"类型")]/following-sibling::text()[1]',
                                  max_length=128, verbose_name='详情页种子类型')),
                ('detail_area_rule',
                 models.CharField(default='//h1/following::td/b[contains(text(),"地区")]/text()', max_length=128,
                                  verbose_name='详情页种子地区')),
                ('detail_count_files_rule',
                 models.CharField(default='//td/b[contains(text(),"文件数")]/following-sibling::text()[1]',
                                  max_length=128, verbose_name='详情页文件数')),
                ('detail_hash_rule',
                 models.CharField(default='//td/b[contains(text(),"Hash")]/following-sibling::text()[1]',
                                  max_length=128, verbose_name='详情页种子HASH')),
                ('detail_free_rule',
                 models.CharField(default='//td//b[contains(text(),"大小")]/following::text()[1]', max_length=128,
                                  verbose_name='详情页促销标记')),
                ('detail_free_expire_rule', models.CharField(
                    default='//h1/b/font[contains(@class,"free")]/parent::b/following-sibling::b/span/@title',
                    max_length=128, verbose_name='详情页促销时间')),
                ('detail_douban_rule',
                 models.CharField(default='//td/a[starts-with(@href,"https://movie.douban.com/subject/")][1]',
                                  help_text='提取做种列表中文件大小计算总量', max_length=128,
                                  verbose_name='详情页豆瓣信息')),
                ('detail_year_publish_rule',
                 models.CharField(default='//td/b[contains(text(),"发行版年份")]/text()', max_length=128,
                                  verbose_name='发行年份')),
            ],
            options={
                'verbose_name': '站点信息',
                'verbose_name_plural': '站点信息',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='UserLevelRule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('level_id', models.IntegerField(default=1, verbose_name='等级id')),
                (
                'level', models.CharField(default='User', help_text='请去除空格', max_length=24, verbose_name='等 级')),
                ('days', models.IntegerField(default=0, help_text='原样输入，单位：周', verbose_name='时 间')),
                ('uploaded',
                 models.CharField(default=0, help_text='原样输入，例：50GB，1.5TB', max_length=12, verbose_name='上 传')),
                ('downloaded',
                 models.CharField(default=0, help_text='原样输入，例：50GB，1.5TB', max_length=12, verbose_name='下 载')),
                ('bonus', models.FloatField(default=0, verbose_name='魔 力')),
                ('score', models.IntegerField(default=0, verbose_name='积 分')),
                ('ratio', models.FloatField(default=0, verbose_name='分享率')),
                ('torrents', models.IntegerField(default=0, help_text='发布种子数', verbose_name='发 种')),
                ('leeches', models.IntegerField(default=0, help_text='完成种子数', verbose_name='吸血数')),
                ('seeding_delta', models.FloatField(default=0, help_text='累计做种时间', verbose_name='做种时间')),
                ('keep_account', models.BooleanField(default=False, verbose_name='保 号')),
                ('graduation', models.BooleanField(default=False, verbose_name='毕 业')),
                (
                'rights', models.TextField(default='无', help_text='当前等级所享有的权利与义务', verbose_name='权 利')),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.website',
                                           verbose_name='站 点')),
            ],
            options={
                'verbose_name': '升级进度',
                'verbose_name_plural': '升级进度',
                'unique_together': {('site', 'level_id', 'level')},
            },
        ),
    ]
