#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File              : SERSMIGHTONEDRIVEPROGRAMSYEXPLORERMAIN.PY
# Author            : yang <mightyang@hotmail.com>
# Date              : 05.12.2018
# Last Modified Date: 05.12.2018
# Last Modified By  : yang <mightyang@hotmail.com>

from src.modules import yExplorer
import logging


# ####################配置日志###########################
logger = logging.getLogger(__name__)
formatter = logging.Formatter(
    '%(asctime)s %(name)s %(lineno)d %(levelname)s: %(message)s')
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
logger.addHandler(handler)
# #######################################################

# 初始化 api
ye = yExplorer.yExplorer()

logging.info('启动 yExplorer')

# 加载 container, node, parameter 模块
# 添加路径到 PYTHONPATH 里


if __name__ == '__main__':
    # ye.createContainer('')
    pass
