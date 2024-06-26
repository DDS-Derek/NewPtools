#!/usr/bin/env bash
PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:~/bin
export PATH
# --------------------------------------------------------------
#	项目: CloudflareSpeedTest 自动更新 Hosts
#	版本: 1.0.4
#	作者: XIU2
#	项目: https://github.com/XIU2/CloudflareSpeedTest
# --------------------------------------------------------------

Green="\033[32m"
Red="\033[31m"
Yellow='\033[33m'
Font="\033[0m"
INFO="[${Green}INFO${Font}]"
ERROR="[${Red}ERROR${Font}]"
WARN="[${Yellow}WARN${Font}]"
function INFO {
    echo -e "${INFO} ${1}"
}
function ERROR {
    echo -e "${ERROR} ${1}"
}
function WARN {
    echo -e "${WARN} ${1}"
}

_CHECK() {
  while true; do
    if [[ ! -e "/ptools/db/nowip_hosts.txt" ]]; then
      INFO "该脚本的作用为 CloudflareST 测速后获取最快 IP 并替换 Hosts 中的 Cloudflare CDN IP。"
      INFO "使用前请先阅读：https://github.com/XIU2/CloudflareSpeedTest/issues/42#issuecomment-768273848"
      INFO "第一次使用，请先将 Hosts 中所有 Cloudflare CDN IP 统一改为一个 IP。"
      read -e -p "输入该 Cloudflare CDN IP 并回车（后续不再需要该步骤）：" NOWIP
      if [[ ! -z "${NOWIP}" ]]; then
        echo ${NOWIP} >/ptools/db/nowip_hosts.txt
        break
      else
        WARN "该 IP 不能是空！"
      fi
    else
      break
    fi
  done
}

_UPDATE() {
  INFO "开始测速..."
  NOWIP=$(head -1 /ptools/db/nowip_hosts.txt)
  # 检测CPU
  ARCH=$(uname -m)
  echo $ARCH
  if [ "$ARCH" = "x86_64" ]; then
    cd /ptools/CloudflareST/CloudflareST_linux_amd64
  elif [ "$ARCH" = "aarch64" ]; then
    cd /ptools/CloudflareST/CloudflareST_linux_arm64
  else
    ERROR "Unsupported architecture: $ARCH"
  fi
  # 这里可以自己添加、修改 CloudflareST 的运行参数
  ./CloudflareST -o "/ptools/db/result_hosts.txt"

  # 如果需要 "找不到满足条件的 IP 就一直循环测速下去"，那么可以将下面的两个 exit 0 改为 _UPDATE 即可
  [[ ! -e "/ptools/db/result_hosts.txt" ]] && INFO "CloudflareST 测速结果 IP 数量为 0，跳过下面步骤..." && exit 0

  # 下面这行代码是 "找不到满足条件的 IP 就一直循环测速下去" 才需要的代码
  # 考虑到当指定了下载速度下限，但一个满足全部条件的 IP 都没找到时，CloudflareST 就会输出所有 IP 结果
  # 因此当你指定 -sl 参数时，需要移除下面这段代码开头的 # 井号注释符，来做文件行数判断（比如下载测速数量：10 个，那么下面的值就设在为 11）
  #[[ $(cat result_hosts.txt|wc -l) > 11 ]] && echo "CloudflareST 测速结果没有找到一个完全满足条件的 IP，重新测速..." && _UPDATE

  BESTIP=$(sed -n "2,1p" /ptools/db/result_hosts.txt | awk -F, '{print $1}')
  if [[ -z "${BESTIP}" ]]; then
    INFO "CloudflareST 测速结果 IP 数量为 0，跳过下面步骤..."
    exit 0
  fi
  echo ${BESTIP} >/ptools/db/nowip_hosts.txt
  echo -e "\n"
  INFO "旧 IP 为 ${NOWIP}\n"
  INFO "新 IP 为 ${BESTIP}\n"

  INFO "开始替换..."
  sed -i 's/'${NOWIP}'/'${BESTIP}'/g' /ptools/db/hosts
  cp -f /ptools/db/hosts /etc/hosts
  INFO "完成..."
}

_CHECK
_UPDATE
